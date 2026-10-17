"""User-authorized three-hour research window; one central submission queue."""
import json,math,pathlib,subprocess,sys,time,statistics,os
from datetime import datetime,timezone
from research.unnormalized_muon.queue import ROOT,REPO,load
from research.unnormalized_muon.gap_wd_campaign import record,stage
from research.unnormalized_muon.continue_campaign import config,register,tuning
from research.unnormalized_muon.fresh_math import matched_static_wd
D=REPO/'research/unnormalized_muon';LAM=.1837498798375862


def deadline():return json.loads((ROOT/'work-window.json').read_text())['deadline_epoch']
def left():return deadline()-time.time()


def base(lr,wd,**kw):
    c=config('control',lr);c.update(protocol_version=5,fixed_wd=wd,runtime_limit=1200,window_family='fixed');c.update(kw);return c


def paired_report(prefix,seeds,filename="WINDOW_PAIRED.md"):
    rows=['# Three-hour WD/schedule comparison','',
        f'Focused seed0 tuning first, then settings frozen for NEW paired seeds{seeds}; matched heldout block recorded in each config. Fixed standard WD and a changing-radius reciprocal-mixing WD hypothesis are separately labelled. Same native direction and auxiliary rules; one B300/run. Three seeds are limited evidence.','',
        '| Arm | Seed | Heldout CE | Delta vs reference | Updates | Active sec | Process sec |','|---|---:|---:|---:|---:|---:|---:|']
    selection_path=D/'WINDOW_SELECTION.json'
    if selection_path.exists():
        sel=json.loads(selection_path.read_text());rows[4:4]=[f'Frozen comparison: **{sel.get("comparison_kind","WD/schedule comparison")}**. Reference `{sel["reference_run"]}`, candidate `{sel["candidate_run"]}`. See [full settings](WINDOW_SELECTION.json). Static retuning is not evidence of adaptive-gap superiority.','']
    ds=[]
    for seed in seeds:
        a=json.loads((ROOT/f'um-{prefix}-reference-s{seed}/summary.json').read_text());b=json.loads((ROOT/f'um-{prefix}-candidate-s{seed}/summary.json').read_text())
        assert a['heldout']['validation_hash']==b['heldout']['validation_hash']
        def manifest(arm):return json.loads((ROOT/f'um-{prefix}-{arm}-s{seed}'/'metrics.jsonl').read_text().splitlines()[0])
        assert manifest('reference')['initial_parameter_hash']==manifest('candidate')['initial_parameter_hash']
        for arm,s in [('reference',a),('candidate',b)]:
            d=s['heldout']['loss']-a['heldout']['loss'];rows.append(f'| {arm} | {seed} | {s["heldout"]["loss"]:.6f} | {d:+.6f} | {s["updates"]} | {s["training_active_seconds"]:.3f} | {s["process_seconds"]:.2f} |')
        ds.append(b['heldout']['loss']-a['heldout']['loss'])
    rows+=['',f'Candidate paired heldout deltas mean {statistics.mean(ds):+.6f}; sample SD {statistics.stdev(ds):.6f}; n=3.']
    p=D/filename;p.write_text('\n'.join(rows)+'\n');subprocess.run(['git','add',str(p.relative_to(REPO))],cwd=REPO,check=True)
    subprocess.run(['git','commit','-m','Report new paired WD/schedule confirmation'],cwd=REPO,check=True)
    from research.unnormalized_muon.gap_wd_campaign import push
    push();return ds


def publish_status(note):
    (ROOT/'work-window-heartbeat.json').write_text(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(),seconds_left=left(),note=note),indent=2))


def main():
    publish_status('take over existing continuation and fill free slots with narrowly defined WD probes')
    # These probes are defined BEFORE observing the pending .005 baseline.
    # They share its LR, so do not confound this first WD comparison with LR.
    cfg={f'window-first-wd-x{x:g}':base(.005,LAM*x) for x in [0.,.25,.5,2.]}
    cfg['window-first-wd-mixing']=base(.005,LAM,wd_schedule='fw_mixing_reciprocal',window_family='mixing')
    cfg['window-first-wd-static-product']=base(.005,matched_static_wd(.00125,LAM,20000))
    register(cfg,'Three-hour work window until2026-10-17 10:48:18UTC: fill free slots beside pending baseline LR.005 with6 WD probes at SAME LR,20k updates. Fixed lambda multiples{0,.25,.5,2}, shifted reciprocal mixing lambda_t=gamma_t/eta_t, and matched-final-product static WD. Reuse pending reference lambda1. One central queue/one B300/job/max6/50GPUh total. WD0 is unconstrained, no finite-radius FW claim.')
    stage('follow-edge0-,window-first-')
    cfg={}
    for lr in [.02,.04]:
        for final in [.05,.25]:
            c=base(lr,LAM);c.update(matrix_schedule='fw_reciprocal_cooldown',reciprocal_final_factor=final,window_family='reciprocal-cooled')
            cfg[f'window-schedule-lr{lr:g}-f{final:g}']=c
    cap=base(.01,LAM);cap.update(updates=64,cap_sign=True,gpu_checks=True,window_family='cap-sign-check')
    cfg['window-cap-check-002']=cap
    register(cfg,'NEW targeted schedule hypothesis from terminal-step audit: plain reciprocal ends near.00049, tuned cooldown control near.000125. Test reciprocal PLUS common65% terminal cooldown with final factors{.05,.25}, peak LRs{.02,.04}, fixed ordinary lambda. Native momentum/auxiliary schedule matched, no extra gradient queries. Quarter factor approximately matches the stronger baseline terminal LR. Not an online controller or exact-theorem claim.')
    publish_status('finish fair long-horizon schedule/LR comparison')
    subprocess.run([sys.executable,'-u','-m','research.unnormalized_muon.continue_campaign'],cwd=REPO,check=True)
    if left()<1500:return
    # Frozen diagnosis had EXACT cap/sign==Armijo on12/12 probes with zeta1.
    # Only promote the cheap no-query rule after compiled GPU/state checks.
    check=json.loads((ROOT/'um-window-cap-check-002/summary.json').read_text())
    assert check['status']=='completed' and check['updates']==64
    from research.unnormalized_muon.events import read_events
    check_rows=read_events(ROOT/'um-window-cap-check-002/metrics.jsonl',{'manifest','update'});manifest=next(x for x in check_rows if x['event']=='manifest')
    matrices=[n for g in manifest['optimizer_groups'] if g['kind']=='muon' for n in g['names']]
    assert check['cap_sign_statistics']['total']==64*len(matrices)
    expected={n:0. for n in matrices}
    for row in [x for x in check_rows if x['event']=='update']:
        j=0
        for i,g in enumerate(manifest['optimizer_groups']):
            if g['kind']!='muon':continue
            for n,gate,eta in zip(g['names'],row['cap_sign_gates'][j],row['cap_sign_effective_lrs'][j]):
                assert eta==row['group_lrs'][i]*int(gate)
                expected[n]+=eta*row['group_weight_decays'][i]
            j+=1
    assert all(math.isclose(check['decay_exposure']['actual_muon:'+n],x,rel_tol=1e-10,abs_tol=1e-12) for n,x in expected.items()),'gated contraction accounting failed'
    selection=json.loads((D/'FOLLOWUP_SELECTION_20000.json').read_text());peak=selection['control']['matrix_lr'];cfg={}
    for factor in [.5,1.,2.]:
        c=base(peak*factor,LAM);c.update(cap_sign=True,window_family='cap-sign')
        cfg[f'window-cap-tune-x{factor:g}']=c
    register(cfg,'Compiled cap/sign checks passed. Frozen diagnosis supported exact12/12 cap/sign==Armijo,zeta1. Now test cheap per-matrix eta=eta_base*I(<G,Q+lambda W> >0), using current raw G and skipping BOTH direction/decay while native momentum advances once. No extra gradients/forwards, same auxiliary recipe. Fair peak-LR factors{half,best,double} around tuned long reference; actual gated contraction logged per matrix.')
    # Equal boundary rule for both terminal factors, full20k budgets.
    for round_index in range(2):
        cfg={}
        for final in [.05,.25]:
            rr=[]
            for p in ROOT.glob('um-window-*/summary.json'):
                ss=json.loads(p.read_text());cc=ss.get('config',{})
                if cc.get('matrix_schedule')=='fw_reciprocal_cooldown' and cc.get('reciprocal_final_factor')==final and cc.get('seed')==0:rr.append((ss['validation']['loss'],cc))
            best=min(rr,key=lambda x:x[0])[1];vals=[c['matrix_lr'] for _,c in rr];lr=best['matrix_lr']
            new=lr/2 if lr==min(vals) else lr*2 if lr==max(vals) else None
            if new is not None:
                c=dict(best,matrix_lr=new);cfg[f'window-schedule-edge{round_index}-f{final:g}']=c
        if not cfg:
            if round_index==0:stage('window-cap-tune-')
            break
        register(cfg,f'Fair factor-two peak-LR boundary expansion round{round_index} for BOTH reciprocal terminal-cooldown factors; seed0, full20k schedule. No heldout selection.')
        stage(f'window-schedule-edge{round_index}-'+(',window-cap-tune-' if round_index==0 else ''))
        if left()<1500:return
    cfg={}
    for lr,final in [(.02,.01),(.0025,.25)]:
        c=base(lr,LAM);c.update(matrix_schedule='cooldown_refined',matrix_final_factor=final,window_family='terminal-control')
        cfg[f'window-terminal-edge-lr{lr:g}-f{final:g}']=c
    register(cfg,'Equal factor-two edge expansion for BOTH ordinary terminal controls before claiming schedule superiority: final.01 preferred upper peak.01, expand to.02; final.25 preferred lower peak.005, expand to.0025. Full20k,seed0; auxiliary/momentum unchanged.')
    stage('window-terminal-edge-')
    if left()<1500:return
    # Joint LR/WD screen around the improved baseline, including zero-WD's
    # previously competitive larger LR. This is not an online-controller grid.
    selected=json.loads((D/'FOLLOWUP_SELECTION_20000.json').read_text());peak=selected['control']['matrix_lr']
    cfg={};levels=[0.,.25,.5]
    first_static=[]
    for p in ROOT.glob('um-window-first-*/summary.json'):
        ss=json.loads(p.read_text());cc=ss.get('config',{})
        if ss.get('status')=='completed' and ss.get('updates')==20000 and cc.get('wd_schedule','fixed')=='fixed':first_static.append((ss['validation']['loss'],cc['fixed_wd']/LAM))
    if first_static:
        best_level=min(first_static,key=lambda z:z[0])[1]
        if not any(math.isclose(best_level,x,rel_tol=1e-12,abs_tol=1e-12) for x in levels+[1.]):levels.append(best_level)
    for x in levels:
        for factor in [.5,1.,2.]:
            lr=peak*factor;cfg[f'window-joint-wd{x:g}-x{factor:g}']=base(lr,LAM*x)
    cfg['window-joint-zero-lr0.04']=base(.04,0.)
    for factor in [.5,1.,2.]:cfg[f'window-joint-mixing-x{factor:g}']=base(peak*factor,LAM,wd_schedule='fw_mixing_reciprocal',window_family='mixing')
    for lr in [peak/2,peak]:
        for final in [.01,.25]:
            c=base(lr,LAM);c.update(matrix_schedule='cooldown_refined',matrix_final_factor=final,window_family='terminal-control')
            cfg[f'window-joint-terminal-lr{lr:g}-f{final:g}']=c
    reused={}
    completed=[]
    for result_path in ROOT.glob('um-*/summary.json'):
        prior=json.loads(result_path.read_text())
        if prior.get('status')=='completed':completed.append((result_path,prior))
    for name,c in list(cfg.items()):
        if (D/'configs'/(name+'.json')).exists():continue
        matches=[(p,ss) for p,ss in completed if ss.get('config')==c]
        if matches:
            p,ss=matches[0];reused[name]=dict(source_run=p.parent.name,source_commit=ss['git_commit'],config=c)
            del cfg[name]
    if reused:
        reuse_path=D/'WINDOW_REUSE.json';reuse_path.write_text(json.dumps(reused,indent=2)+'\n')
        subprocess.run(['git','add',str(reuse_path.relative_to(REPO))],cwd=REPO,check=True)
        subprocess.run(['git','commit','-m','Reuse only exact full-configuration completed WD screens'],cwd=REPO,check=True)
        record({},'Exact full-configuration equality avoids duplicate GPU work: '+json.dumps({k:v['source_run'] for k,v in reused.items()})+'. Native default path passed compiled GPU parity after opt-in additions; preserve original implementation commit/cost. Existing source results stay in candidate pool; no synthetic trials or duplicated charges.')
    register(cfg,'Remaining work-window stage: joint LR/WD interaction around newly tuned baseline. Static lambda{0,.25,.5} times reference PLUS the first screen best static coefficient if distinct, across peak LR{half,best,double}; include zero-WD LR.04 because earlier long zero-WD runs preferred larger LR. Give changing-radius mixing WD the SAME3 LR candidates. Full20k schedules; seed0 development only, no final-heldout selection.')
    stage('window-joint-')
    if left()<1500:return
    candidates=[]
    for p in ROOT.glob('um-window-*/summary.json'):
        s=json.loads(p.read_text());c=s.get('config',{})
        if s.get('status')=='completed' and s.get('updates')==20000 and not c.get('time_budget') and c.get('seed')==0:candidates.append((s['validation']['loss'],c,p.parent.name))
    def static_control(c):
        return (c.get('clean') and not c.get('variant') and not c.get('cap_sign') and not c.get('gap_scope')
                and c.get('wd_schedule','fixed')=='fixed' and c.get('matrix_schedule') in {'cooldown','cooldown_refined'})
    controls=tuning('control',20000)+[dict(name=n,c=c,s=json.loads((ROOT/n/'summary.json').read_text())) for loss,c,n in candidates if static_control(c)]
    # The best changed static WD gets the SAME terminal-factor test as
    # original WD before a new method can claim practical superiority.
    preliminary=min(controls,key=lambda r:r['s']['validation']['loss']);terminal_cfg={}
    for final in [.01,.25]:
        exists=any(x['c']['fixed_wd']==preliminary['c']['fixed_wd'] and x['c']['matrix_lr']==preliminary['c']['matrix_lr'] and x['c'].get('matrix_final_factor',.05)==final for x in controls)
        if not exists:
            cc=dict(preliminary['c'],matrix_schedule='cooldown_refined',matrix_final_factor=final,window_family='static-terminal-refinement')
            terminal_cfg[f'window-static-terminal-f{final:g}']=cc
    if terminal_cfg:
        register(terminal_cfg,'Before adaptive confirmation, best static WD/LR gets SAME matrix-only terminal-factor tests{.01,.25}, unchanged auxiliary/momentum; seed0 development only. This prevents a cooldown advantage versus a control whose WD and terminal factor were tuned separately.')
        stage('window-static-terminal-')
        for p in ROOT.glob('um-window-static-terminal-*/summary.json'):
            ss=json.loads(p.read_text());cc=ss.get('config',{})
            if ss.get('status')=='completed' and ss.get('updates')==20000:controls.append(dict(name=p.parent.name,c=cc,s=ss))
    original=min((x for x in controls if x['c']['fixed_wd']==LAM),key=lambda r:r['s']['validation']['loss'])
    tuned_static=min(controls,key=lambda r:r['s']['validation']['loss'])
    variants=[x for x in candidates if not static_control(x[1])]
    adaptive=min(variants,key=lambda x:x[0])
    if adaptive[0]<tuned_static['s']['validation']['loss']-.001:
        best=adaptive;reference=tuned_static;comparison_kind='adaptive versus best tested static-WD control'
    elif tuned_static['s']['validation']['loss']<original['s']['validation']['loss']-.001:
        best=(tuned_static['s']['validation']['loss'],tuned_static['c'],tuned_static['name'])
        reference=original;comparison_kind='static WD/LR retuning; no adaptive method screen win'
    else:
        record({},'Work-window screen found neither an adaptive advantage>.001CE over fully tuned static WD nor static retuning gain>.001CE over original-lambda control. Stop promotions, retain negative result and audit until deadline.');return
    reference_config=dict(reference['c'])
    chosen=dict(best[1]);frozen=D/'WINDOW_SELECTION.json';frozen.write_text(json.dumps(dict(comparison_kind=comparison_kind,candidate=chosen,candidate_run=best[2],reference_run=reference['name'],reference_lr=reference['c']['matrix_lr'],reference_config=reference_config),indent=2)+'\n')
    subprocess.run(['git','add',str(frozen.relative_to(REPO))],cwd=REPO,check=True);subprocess.run(['git','commit','-m','Freeze seed0-only WD candidate before new paired seeds'],cwd=REPO,check=True)
    from research.unnormalized_muon.gap_wd_campaign import push
    push();cfg={}
    for seed in [40,41,42]:
        for arm,c in [('reference',dict(reference_config)),('candidate',chosen)]:
            c=dict(c,seed=seed,heldout=True,heldout_block=4);cfg[f'window-confirm-{arm}-s{seed}']=c
    register(cfg,'Freeze '+comparison_kind+' before NEW paired seeds40/41/42 and NEW heldout block4. Same20k tokens/update/auxiliary streams; all selection used seed0 development. OneB300/run, six slots, runtime1200s.')
    stage('window-confirm-');ds=paired_report('window-confirm',[40,41,42])
    # Independent equal-time endpoints precede any larger-horizon promotion.
    if left()>1100:
        H=statistics.median(json.loads((ROOT/f'um-window-confirm-reference-s{seed}/summary.json').read_text())['training_active_seconds'] for seed in [40,41,42]);cfg={}
        for seed in [40,41,42]:
            for arm,c in [('reference',dict(reference_config)),('candidate',chosen)]:
                cc=dict(c,seed=seed,heldout=True,heldout_block=4,time_budget=H,reference_updates=20000,max_updates=200000,runtime_limit=math.ceil(H+240))
                cfg[f'window-time-{arm}-s{seed}']=cc
        register(cfg,f'Independent WD equal-time confirmation H={H:.9f}s, median matched reference active times. LR, WD, momentum and auxiliary schedules all use shared active-time progress; seeds40/41/42, fixed heldout block4. Finish last update and report overshoot. No token-clock prefix comparison.')
        stage('window-time-');paired_report('window-time',[40,41,42],filename='WINDOW_EQUAL_TIME.md')
    if left()>1800 and all(x<0 for x in ds) and statistics.mean(ds)<-.003:
        cfg={}
        for arm,c in [('reference',dict(reference_config)),('candidate',chosen)]:
            for factor in [.5,1.,2.]:
                cc=dict(c,matrix_lr=c['matrix_lr']*factor,updates=40000,runtime_limit=2200)
                cfg[f'window-long-{arm}-x{factor:g}']=cc
        register(cfg,'New WD paired win survives all3 seeds with mean<-.003CE: tune both reference/candidate at fresh40k-update/1.31B-token horizon, three peak LRs EACH. Only launch if time remains; seed0 development, no final-heldout tuning.')
        stage('window-long-')
        if left()>1800:
            winners={}
            for arm in ['reference','candidate']:
                rows=[]
                for p in ROOT.glob(f'um-window-long-{arm}-*/summary.json'):
                    ss=json.loads(p.read_text());rows.append((ss['validation']['loss'],ss['config']))
                winners[arm]=min(rows,key=lambda z:z[0])[1]
            cfg={}
            for seed in [60,61,62]:
                for arm,c in winners.items():cfg[f'window-longconfirm-{arm}-s{seed}']=dict(c,seed=seed,heldout=True,heldout_block=5)
            register(cfg,'Freeze40k WD/reference peak settings from seed0 before NEW paired seeds60/61/62 and previously unused final heldout block5. Full1.31B-token schedules; only start if enough of the three-hour window remains.')
            stage('window-longconfirm-');paired_report('window-longconfirm',[60,61,62],filename='WINDOW_LONG_PAIRED.md')
    publish_status('paired confirmation complete; audit and report until work-window deadline')

if __name__=='__main__':
    try:
        main()
    except Exception as error:
        publish_status('stage stopped: '+str(error))
        # Reap only this campaign's registered jobs; never cancel other work.
        subprocess.run([sys.executable,'-m','research.unnormalized_muon.queue','watch'],cwd=REPO)
        raise
    finally:
        # Stay active for the full requested window, monitoring persistent
        # artifacts. No blind GPU spending when the scientific gate fails.
        while left()>0:
            publish_status('monitoring completed stages; ready for new input, no unjustified GPU sweep')
            time.sleep(min(30,max(0,left())))
        subprocess.run([sys.executable,'-m','research.unnormalized_muon.queue','watch'],cwd=REPO)
        record({},'Requested three-hour work window ended. New submissions stopped at10:48:18UTC; last-started jobs finished/reaped. See FOLLOWUP_RESULTS.md, WINDOW_RESULTS.md and paired report if completed. Hard50B300 GPUh total remains; completed research gates do not justify spending unused allowance.')
