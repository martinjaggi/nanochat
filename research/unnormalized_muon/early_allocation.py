"""Controlled early LR allocation: screen, contraction match, fresh seeds, time.

Each stage uses the existing single six-slot/50-hour queue. No candidate is
selected with heldout results. Configuration files are immutable once written.
"""
import json,math,statistics,subprocess,sys,datetime
from pathlib import Path
from research.unnormalized_muon.queue import ROOT,REPO,load
from research.unnormalized_muon.gap_wd_campaign import record,stage,push
from research.unnormalized_muon.cooldown_schedule import early_reciprocal
from research.unnormalized_muon.events import read_events
D=REPO/'research/unnormalized_muon'


def read(name):
    s=json.loads((ROOT/('um-'+name)/'summary.json').read_text())
    assert s['status']=='completed'
    return s


def rates(k):return [early_reciprocal(.005,t,peak_multiplier=k) for t in range(20000)]


def log_contraction(etas,wd):return math.fsum(math.log1p(-wd*x) for x in etas)


def matching_wd(target,etas):
    lo,hi=0.,.999/max(etas)
    for _ in range(100):
        mid=(lo+hi)/2
        if log_contraction(etas,mid)>target:lo=mid
        else:hi=mid
    return (lo+hi)/2


def config(k,seed=0,**kw):
    c=json.loads((D/'configs/earlyalloc-screen-k1.json').read_text())
    c.update(seed=seed,early_peak_multiplier=k,early_tau_updates=None if k==1 else 6960/(k-1))
    c.update(kw);return c


def commit(message):
    subprocess.run(['git','add','research/unnormalized_muon','tests/test_cooldown_schedule.py'],cwd=REPO,check=True)
    if subprocess.run(['git','diff','--cached','--quiet'],cwd=REPO).returncode:
        subprocess.run(['git','commit','-m',message],cwd=REPO,check=True)
    push()


def audit(name):
    s=read(name);k=s['config']['early_peak_multiplier'];es=read_events(ROOT/('um-'+name)/'metrics.jsonl',{'manifest','update','validation'})
    m=next(e for e in es if e['event']=='manifest');updates=[e for e in es if e['event']=='update']
    assert len(updates)==s['updates']==20000
    for e in updates:
        expected=early_reciprocal(.005,e['step'],peak_multiplier=k)
        assert all(math.isclose(v,expected,rel_tol=1e-12,abs_tol=1e-16) for v in e['group_lrs'][6:]),(name,e['step'])
        assert all(v==s['config']['fixed_wd'] for v in e['group_weight_decays'][6:])
    target=log_contraction(rates(k),s['config']['fixed_wd'])
    assert all(abs(v['log_abs']-target)<1e-8 and v['sign']==1 for v in s['muon_contraction'].values())
    assert s['fresh_microbatch_gradient_passes']==20000
    assert 'B300' in (ROOT/('um-'+name)/'run.log').read_text()[:100]
    return dict(initial_hash=m['initial_parameter_hash'],validation_hash=s['validation']['validation_hash'],log_contraction=target,updates=len(updates))


def report():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();q=load();selpath=D/'EARLY_ALLOCATION_SELECTION.json'
    lines=['# Early reciprocal allocation results','',f'Updated {now}. Two-hour research window11:53–13:53UTC,17October2026. Exactly one verified B300/run, six-slot central queue,50B300-hour project-total cap.','',
    'This is a new WD-independent schedule, distinct from the earlier WD-coupled reciprocal curve multiplied by cooldown. Baseline actual eta .005, fixed ordinary WD .04593746995939655; 40-update warmup, join at7000, original late65% cooldown unchanged to nominal .00005. Full20k updates/655.36M tokens per token-matched run. [Protocol](EARLY_ALLOCATION_PROTOCOL.md).','',
    '| Seed0 arm | Development CE | Active seconds | Contraction product |','|---|---:|---:|---:|']
    for k in [1.,1.5,2.]:
        p=ROOT/f'um-earlyalloc-screen-k{str(k).removesuffix(".0").replace(".","p")}'/'summary.json'
        if p.exists():
            s=json.loads(p.read_text());c=next(iter(s['muon_contraction'].values()))['value']
            lines.append(f'| Early peak {k:g}x | {s["validation"]["loss"]:.9f} | {s["training_active_seconds"]:.3f} | {c:.9f} |')
    p=ROOT/'um-earlyalloc-match-seed0'/'summary.json'
    if p.exists():
        s=json.loads(p.read_text());c=next(iter(s['muon_contraction'].values()))['value']
        lines.append(f'| Baseline LR, matched WD {s["config"]["fixed_wd"]:.9f} | {s["validation"]["loss"]:.9f} | {s["training_active_seconds"]:.3f} | {c:.9f} |')
    if selpath.exists():
        selection=json.loads(selpath.read_text());lines+=['','Frozen seed0-only selection:', '```json',json.dumps(selection,indent=2),'```']
    for kind,title in [('confirm','Token-matched fresh seeds'),('time','Independent equal-training-time reruns')]:
        rows=[]
        for seed in [70,71,72]:
            ss={}
            for arm in ['baseline','early','matched','neutral']:
                p=ROOT/f'um-earlyalloc-{kind}-{arm}-s{seed}'/'summary.json'
                if p.exists():ss[arm]=json.loads(p.read_text())
            if ss:rows.append((seed,ss))
        if rows:
            lines+=['',f'## {title}','','| Seed | Arm | Heldout CE | Delta vs baseline | Active seconds | Updates |','|---|---|---:|---:|---:|---:|']
            for seed,ss in rows:
                for arm,s in ss.items():
                    delta=s['heldout']['loss']-ss['baseline']['heldout']['loss'] if 'baseline' in ss else float('nan')
                    lines.append(f'| {seed} | {arm} | {s["heldout"]["loss"]:.9f} | {delta:+.9f} | {s["training_active_seconds"]:.3f} | {s["updates"]} |')
            for arm in ['early','matched','neutral']:
                ds=[ss[arm]['heldout']['loss']-ss['baseline']['heldout']['loss'] for seed,ss in rows if arm in ss and 'baseline' in ss]
                if len(ds)==3:lines+=['',f'{arm} minus baseline: mean **{statistics.mean(ds):+.6f} CE**, sample SD **{statistics.stdev(ds):.6f}**, n=3.']
    lines+=['','## Limits and accounting','',
    'Matching final contraction does not match decay history. Both fixed-WD early-allocation and matched-contraction comparisons are required to separate explanations. Auxiliary LRs/WD and momentum are matched. Per-run schedules/logs/checkpoints and hardware assertions are preserved outside Git. Three paired seeds provide limited evidence. Development and heldout blocks are distinct; block6 is used only after settings freeze. Token-clock time curves are descriptive and are not equal-time endpoints.', '',
    f'Conservative recorded request-hours {sum(v.get("gpu_seconds",0) for v in q.values())/3600:.6f}; outstanding reserved hours {sum(v["seconds"]+30 for v in q.values() if not v["recorded"])/3600:.6f}. Includes prior and failed work; queued/startup/cleanup request time upper-bounds GPU occupancy.']
    (D/'EARLY_ALLOCATION_RESULTS.md').write_text('\n'.join(lines)+'\n')


def main():
    stage('earlyalloc-screen-')
    audits={k:audit(f'earlyalloc-screen-k{k:g}') for k in [1.,1.5,2.]}
    assert len({x['initial_hash'] for x in audits.values()})==1
    assert len({x['validation_hash'] for x in audits.values()})==1
    (D/'EARLY_ALLOCATION_AUDIT.json').write_text(json.dumps(audits,indent=2)+'\n')
    baseline=read('earlyalloc-screen-k1');old=json.loads((ROOT/'um-window-static-terminal-f0p01'/'summary.json').read_text())
    regression=dict(new_ce=baseline['validation']['loss'],old_ce=old['validation']['loss'],delta=baseline['validation']['loss']-old['validation']['loss'])
    # BF16 compiled reductions are not bitwise reproducible across jobs:
    # even before the first changed schedule input, loss can differ ~1e-6.
    # Validate exact inputs/state/cursor, and report endpoint drift separately.
    prev=read_events(ROOT/'um-window-static-terminal-f0p01'/'metrics.jsonl',{'manifest','update'})
    curr=read_events(ROOT/'um-earlyalloc-screen-k1'/'metrics.jsonl',{'manifest','update'})
    assert prev[0]['initial_parameter_hash']==curr[0]['initial_parameter_hash']
    old_updates=[e for e in prev if e['event']=='update'];new_updates=[e for e in curr if e['event']=='update']
    assert len(old_updates)==len(new_updates)==20000
    first_difference=None
    for a,b in zip(old_updates,new_updates):
        assert a['group_lrs']==b['group_lrs'] and a['group_weight_decays']==b['group_weight_decays']
        assert a['data_state']==b['data_state']
        if first_difference is None and a['loss']!=b['loss']:
            first_difference=dict(step=a['step'],old_loss=a['loss'],new_loss=b['loss'])
    regression['first_training_loss_difference']=first_difference
    regression['exact_schedule_initial_parameters_and_data_cursors']=True
    regression['bitwise_trajectory']=first_difference is None
    assert abs(regression['delta'])<.01,'large baseline drift requires investigation before selection' 
    candidates=[(read(f'earlyalloc-screen-k{k:g}')['validation']['loss'],k) for k in [1.5,2.]]
    score,k=min(candidates)
    if score>=baseline['validation']['loss']:
        report();record({},f'Early allocation seed0 screen: no elevated peak beats exact baseline. k1 regression {regression}; retain negative result, inspect curves before any additional hypothesis.');commit('Report early-allocation development screen without a win');return
    wd=matching_wd(log_contraction(rates(k),baseline['config']['fixed_wd']),rates(1.))
    neutral_wd=matching_wd(log_contraction(rates(1.),baseline['config']['fixed_wd']),rates(k))
    selection=dict(neutral_early_wd=neutral_wd,peak_multiplier=k,tau_updates=6960/(k-1),fixed_wd=baseline['config']['fixed_wd'],matched_baseline_wd=wd,seed0_ce=score,baseline_seed0_ce=baseline['validation']['loss'],regression=regression,frozen_before_heldout=True,confirmation_seeds=[70,71,72],heldout_block=6)
    p=D/'EARLY_ALLOCATION_SELECTION.json'
    if p.exists():assert json.loads(p.read_text())==selection
    else:p.write_text(json.dumps(selection,indent=2)+'\n')
    report();commit('Freeze early allocation peak using development only; validate executed LR curves')
    cfg={'earlyalloc-match-seed0':config(1.,fixed_wd=wd,contraction_control=True),
         'earlyalloc-neutral-seed0':config(k,fixed_wd=neutral_wd,contraction_control=True)}
    for seed in [70,71,72]:
        for arm,peak,lam in [('baseline',1.,selection['fixed_wd']),('early',k,selection['fixed_wd']),('matched',1.,wd),('neutral',k,neutral_wd)]:
            cfg[f'earlyalloc-confirm-{arm}-s{seed}']=config(peak,seed,fixed_wd=lam,heldout=True,heldout_block=6,early_arm=arm)
    record(cfg,f'Early allocation {k:g}x improves seed0 CE {score:.6f} vs {baseline["validation"]["loss"]:.6f}. Freeze before NEW paired seeds70/71/72/block6. Add baseline schedule with static WD {wd:.12f} matching final contraction exactly. Fourteen trials including two seed0 contraction controls, one B300 each, timeout1200s, at most six via central queue; estimated3.1GPUh. Both directions of final-contraction matching are predeclared before fresh heldout scores.')
    stage('earlyalloc-match-,earlyalloc-neutral-,earlyalloc-confirm-')
    for seed in [70,71,72]:
        ss=[read(f'earlyalloc-confirm-{arm}-s{seed}') for arm in ['baseline','early','matched','neutral']]
        assert len({s['heldout']['validation_hash'] for s in ss})==1
        ms=[read_events(ROOT/f'um-earlyalloc-confirm-{arm}-s{seed}'/'metrics.jsonl',{'manifest'})[0] for arm in ['baseline','early','matched','neutral']]
        assert len({m['initial_parameter_hash'] for m in ms})==1
    report();commit('Report fresh paired early allocation and contraction-control confirmation')
    ds=[read(f'earlyalloc-confirm-early-s{s}')['heldout']['loss']-read(f'earlyalloc-confirm-baseline-s{s}')['heldout']['loss'] for s in [70,71,72]]
    neutral_ds=[read(f'earlyalloc-confirm-neutral-s{s}')['heldout']['loss']-read(f'earlyalloc-confirm-baseline-s{s}')['heldout']['loss'] for s in [70,71,72]]
    if not (all(d<0 for d in ds) or all(d<0 for d in neutral_ds)):
        record({},f'Early allocation fresh-seed confirmation not consistently better: {ds}. Stop before extra equal-time jobs; inspect complete matched-control evidence.');report();commit('Record early allocation confirmation gate');return
    H=statistics.median(read(f'earlyalloc-confirm-baseline-s{s}')['training_active_seconds'] for s in [70,71,72])
    window=json.loads((ROOT/'work-window.json').read_text())
    import time
    # Twelve fresh runs require two waves. Reserve compilation, evaluation, and cleanup.
    if time.time()+2*(H+180)>window['deadline_epoch']:
        record({},f'Consistent paired token win, but insufficient two-hour window for twelve independent equal-time reruns at H={H:.3f}s. Do not interpret token-clock curves as equal-time endpoints.');return
    cfg={}
    for seed in [70,71,72]:
        for arm,peak,lam in [('baseline',1.,selection['fixed_wd']),('early',k,selection['fixed_wd']),('matched',1.,wd),('neutral',k,neutral_wd)]:
            cfg[f'earlyalloc-time-{arm}-s{seed}']=config(peak,seed,fixed_wd=lam,heldout=True,heldout_block=6,early_arm=arm,time_budget=H,reference_updates=20000,max_updates=200000,runtime_limit=math.ceil(H+300))
    record(cfg,f'Independent equal-time reruns, all four frozen arms and pairedseeds70/71/72, H={H:.9f}s median baseline confirmations. Matrix, auxiliary and momentum schedules use common active-time clock; actual contraction remeasured. Twelve trials, oneB300each, maxsix, limitsH+300s, cost~{12*(H+60)/3600:.2f}GPUh. Outputs um-earlyalloc-time-* .')
    stage('earlyalloc-time-');report();commit('Report independent equal-time early allocation comparison')

if __name__=='__main__':main()
