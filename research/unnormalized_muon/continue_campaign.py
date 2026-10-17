"""Finish reciprocal compute comparison and fairly tune the long-horizon control."""
import copy,json,math,statistics,subprocess,sys
from research.unnormalized_muon.queue import ROOT,REPO,load
from research.unnormalized_muon.gap_wd_campaign import record,stage
LAM=.1837498798375862;D=REPO/'research/unnormalized_muon'


def read(name):return json.loads((ROOT/name/'summary.json').read_text())


def config(arm,lr,updates=20000,seed=0,**kwargs):
    return dict(protocol_version=4,clean=True,variant=False,decay_mode='standard',fixed_wd=LAM,
        gap_geometry='q_scaled',matrix_lr=lr,matrix_schedule='cooldown' if arm=='control' else 'fw_reciprocal',
        updates=updates,seed=seed,depth=8,runtime_limit=2400 if updates==20000 else 3600,warmup_updates=3,
        follow_arm=arm,heldout=False,**kwargs)


def tuning(arm,horizon):
    rows=[]
    for p in ROOT.glob('um-*/summary.json'):
        s=json.loads(p.read_text());c=s.get('config',{})
        if c.get('cap_sign'):continue
        if s.get('status')!='completed' or c.get('seed')!=0 or s['updates']!=horizon or c.get('time_budget') or c.get('fresh_diagnosis'):continue
        if not c.get('clean') or c.get('variant') or c.get('gap_scope') or c.get('gap_geometry')!='q_scaled' or c.get('fixed_wd')!=LAM:continue
        if c.get('wd_schedule','fixed')!='fixed':continue
        if c.get('matrix_schedule')!=('cooldown' if arm=='control' else 'fw_reciprocal'):continue
        rows.append(dict(name=p.parent.name,c=c,s=s))
    return rows


def register(configs,note):
    # Resume every stage from immutable on-disk configs, never recompute a
    # submitted trial from subsequently observed outcomes.
    fixed={}
    for name,c in configs.items():
        p=D/'configs'/(name+'.json');fixed[name]=json.loads(p.read_text()) if p.exists() else c
    record(fixed,note)


def paired(prefix,seeds):
    groups={}
    for arm in ['control','reciprocal']:
        groups[arm]={seed:read(f'um-{prefix}-{arm}-s{seed}') for seed in seeds}
    for seed in seeds:
        a,b=groups['control'][seed],groups['reciprocal'][seed]
        assert a['heldout']['validation_hash']==b['heldout']['validation_hash']
        def manifest(arm):return json.loads((ROOT/f'um-{prefix}-{arm}-s{seed}'/'metrics.jsonl').read_text().splitlines()[0])
        assert manifest('control')['initial_parameter_hash']==manifest('reciprocal')['initial_parameter_hash']
    return groups


def frozen_settings(horizon):
    path=D/f'FOLLOWUP_SELECTION_{horizon}.json'
    if path.exists():return json.loads(path.read_text())
    selected={arm:min(tuning(arm,horizon),key=lambda r:r['s']['validation']['loss']) for arm in ['control','reciprocal']}
    payload={arm:dict(tuning_run=r['name'],matrix_lr=r['c']['matrix_lr'],validation_loss=r['s']['validation']['loss']) for arm,r in selected.items()}
    path.write_text(json.dumps(payload,indent=2)+'\n')
    subprocess.run(['git','add',str(path.relative_to(REPO))],cwd=REPO,check=True)
    subprocess.run(['git','commit','-m',f'Freeze seed0-only {horizon}-update reciprocal and control settings'],cwd=REPO,check=True)
    from research.unnormalized_muon.gap_wd_campaign import push
    push();return payload


def confirm_and_time(horizon,seeds,block):
    settings=frozen_settings(horizon);cfg={};tag=f'follow-confirm{horizon}'
    for arm in settings:
        for seed in seeds:
            c=config(arm,settings[arm]['matrix_lr'],horizon,seed);c.update(heldout=True,heldout_block=block)
            cfg[f'{tag}-{arm}-s{seed}']=c
    register(cfg,f'Fresh paired seeds{seeds}, {horizon} updates; freeze both LRs using seed0 development scores only. NEW disjoint heldout block{block}; prior blocks are not used to select settings. One B300/run, maximum6,50GPUh total.')
    stage(tag+'-');groups=paired(tag,seeds)
    H=statistics.median(s['training_active_seconds'] for s in groups['control'].values());cfg={};tag=f'follow-time{horizon}'
    for arm in settings:
        for seed in seeds:
            c=config(arm,settings[arm]['matrix_lr'],horizon,seed);c.update(heldout=True,heldout_block=block,time_budget=H,reference_updates=horizon,max_updates=200000,runtime_limit=math.ceil(H+900))
            cfg[f'{tag}-{arm}-s{seed}']=c
    register(cfg,f'Independent equal-time reruns H={H:.9f}s, median NEW control confirmations. All matrix/auxiliary/momentum schedules use active-time fraction, including reciprocal. Seeds{seeds}, final heldout block{block}; report one-update overshoot and all job overhead.')
    stage(tag+'-');paired(tag,seeds)
    from research.unnormalized_muon.publish import publish
    publish();return groups


def main():
    assert not any(not v['recorded'] for v in load().values()),'another campaign has live jobs'
    # The missing equal-time endpoint uses previously frozen settings and same
    # old paired seeds, alongside only seed0 long-horizon tuning candidates.
    H=statistics.median(read(f'um-lens-confirm-control-s{s}')['training_active_seconds'] for s in [10,11,12])
    cfg={f'follow-first-tune-control-lr{lr:g}':config('control',lr) for lr in [.01,.02]}
    cfg['follow-first-tune-reciprocal-lr0.01']=config('reciprocal',.01)
    for seed in [10,11,12]:
        c=config('reciprocal',.02,seed=seed);c.update(heldout=True,heldout_block=1,time_budget=H,reference_updates=20000,max_updates=200000,runtime_limit=math.ceil(H+900))
        cfg[f'follow-first-time-reciprocal-s{seed}']=c
    register(cfg,'Continue after completed gap/fresh-data campaign,21.22GPUh charged. Respect failed fresh gate: NO further online-controller sweep. First six jobs: missing reciprocal equal-time seeds10/11/12 at frozen LR.02 and H=678.993s, plus seed0 655M-token control LRs{.01,.02} and reciprocal.01. Long control optimum was at its tested lower edge. Six-slot queue,1verified B300/job,50GPUh PROJECT TOTAL.')
    stage('follow-first-')
    for round_index in range(2):
        cfg={}
        for arm in ['control','reciprocal']:
            existing=list((D/'configs').glob(f'follow-edge{round_index}-{arm}-*.json'))
            if existing:
                cfg.update({p.stem:json.loads(p.read_text()) for p in existing});continue
            rs=tuning(arm,20000);best=min(rs,key=lambda r:r['s']['validation']['loss']);lrs=[r['c']['matrix_lr'] for r in rs];lr=best['c']['matrix_lr']
            new=lr/2 if lr==min(lrs) else lr*2 if lr==max(lrs) else None
            if new is not None:cfg[f'follow-edge{round_index}-{arm}-lr{new:g}']=config(arm,new)
        if cfg:
            register(cfg,f'Matched factor-two long-horizon boundary rule round{round_index}, both prescribed schedules. Seed0 only,20000 updates; no heldout selection.')
            stage(f'follow-edge{round_index}-')
    cfg={}
    for arm in ['control','reciprocal']:
        existing=list((D/'configs').glob(f'follow-mid-{arm}-*.json'))
        if existing:cfg.update({p.stem:json.loads(p.read_text()) for p in existing});continue
        rs=tuning(arm,20000);best=min(rs,key=lambda r:r['s']['validation']['loss']);values=sorted(set(r['c']['matrix_lr'] for r in rs));i=values.index(best['c']['matrix_lr'])
        for side,j in [('low',i-1),('high',i+1)]:
            if 0<=j<len(values):cfg[f'follow-mid-{arm}-{side}']=config(arm,math.sqrt(values[i]*values[j]))
    register(cfg,'Refine both long-horizon schedule families with geometric midpoints adjacent to their seed0 best rates. Restart every candidate for the full655M-token horizon.')
    stage('follow-mid-,window-schedule-,window-cap-check-');groups=confirm_and_time(20000,[20,21,22],2)
    deltas=[groups['reciprocal'][s]['heldout']['loss']-groups['control'][s]['heldout']['loss'] for s in [20,21,22]]
    if not(all(x<0 for x in deltas) and statistics.mean(deltas)<-.003):
        record({},'Follow-up completed: reciprocal failed preregistered scale-up gate (all3 paired improvements and mean<-.003 CE) after fair long-horizon LR tuning. Stop scale-up; preserve negative/ambiguous results. Remaining budget is not a spending target. See FOLLOWUP_RESULTS.md.');return
    # A larger horizon only follows a new paired win, not the earlier short
    # pilot or a post-hoc choice of budget endpoint.
    settings=frozen_settings(20000);cfg={}
    for arm in settings:
        for factor in [.5,1.,2.]:cfg[f'follow-scale-tune-{arm}-x{factor:g}']=config(arm,settings[arm]['matrix_lr']*factor,40000)
    register(cfg,'New paired win survives fair20k LR tuning: screen BOTH schedules at fresh40000-update/1.31B-token horizon, three peak rates each {half,best,double}; no reuse of shorter schedule prefixes. No new online controllers.')
    stage('follow-scale-tune-')
    cfg={}
    for arm in settings:
        rs=tuning(arm,40000);best=min(rs,key=lambda r:r['s']['validation']['loss']);vals=[r['c']['matrix_lr'] for r in rs];lr=best['c']['matrix_lr']
        new=lr/2 if lr==min(vals) else lr*2 if lr==max(vals) else None
        if new is not None:cfg[f'follow-scale-edge-{arm}']=config(arm,new,40000)
    if cfg:register(cfg,'Same LR edge expansion for both schedules at40k before freezing; seed0 development only.');stage('follow-scale-edge-')
    confirm_and_time(40000,[30,31,32],3)
    record({},'Follow-up completed through paired1.31B-token and independent equal-time comparison. See FOLLOWUP_RESULTS.md. No remaining preauthorized scientific stage; stop submission and report evidence rather than exhaust50GPUh.')

if __name__=='__main__':main()
