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


def paired_report(prefix,seeds):
    rows=['# Three-hour WD/schedule comparison','',
        'Focused seed0 tuning first, then settings frozen for NEW paired seeds40/41/42 and previously unused heldout block4. Fixed standard WD and a changing-radius reciprocal-mixing WD hypothesis are separately labelled. Same native direction and auxiliary rules; one B300/run. Three seeds are limited evidence.','',
        '| Arm | Seed | Heldout CE | Delta vs reference | Updates | Active sec | Process sec |','|---|---:|---:|---:|---:|---:|---:|']
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
    p=D/'WINDOW_PAIRED.md';p.write_text('\n'.join(rows)+'\n');subprocess.run(['git','add',str(p.relative_to(REPO))],cwd=REPO,check=True)
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
    publish_status('finish fair long-horizon schedule/LR comparison')
    subprocess.run([sys.executable,'-u','-m','research.unnormalized_muon.continue_campaign'],cwd=REPO,check=True)
    if left()<1500:return
    # Joint LR/WD screen around the improved baseline, including zero-WD's
    # previously competitive larger LR. This is not an online-controller grid.
    selected=json.loads((D/'FOLLOWUP_SELECTION_20000.json').read_text());peak=selected['control']['matrix_lr']
    cfg={}
    for x in [0.,.25,.5]:
        for factor in [.5,1.,2.]:
            lr=peak*factor;cfg[f'window-joint-wd{x:g}-x{factor:g}']=base(lr,LAM*x)
    cfg['window-joint-zero-lr0.04']=base(.04,0.)
    for factor in [.5,1.,2.]:cfg[f'window-joint-mixing-x{factor:g}']=base(peak*factor,LAM,wd_schedule='fw_mixing_reciprocal',window_family='mixing')
    register(cfg,'Remaining work-window stage: joint LR/WD interaction around newly tuned baseline. Static lambda{0,.25,.5} times reference across peak LR{half,best,double}; include zero-WD LR.04 because earlier long zero-WD runs preferred larger LR. Give changing-radius mixing WD the SAME3 LR candidates. Full20k schedules; seed0 development only, no final-heldout selection.')
    stage('window-joint-')
    if left()<1500:return
    candidates=[]
    for p in ROOT.glob('um-window-*/summary.json'):
        s=json.loads(p.read_text());c=s.get('config',{})
        if s.get('status')=='completed' and c.get('seed')==0:candidates.append((s['validation']['loss'],c,p.parent.name))
    best=min(candidates,key=lambda x:x[0]);reference=min(tuning('control',20000),key=lambda r:r['s']['validation']['loss'])
    if best[0]>=reference['s']['validation']['loss']-.001:
        record({},'Work-window WD screen found no >.001 CE gain over tuned reference; no large confirmation sweep justified. Keep exact losses and costs, continue audit/report work until requested deadline.');return
    chosen=dict(best[1]);frozen=D/'WINDOW_SELECTION.json';frozen.write_text(json.dumps(dict(candidate=chosen,candidate_run=best[2],reference_run=reference['name'],reference_lr=reference['c']['matrix_lr']),indent=2)+'\n')
    subprocess.run(['git','add',str(frozen.relative_to(REPO))],cwd=REPO,check=True);subprocess.run(['git','commit','-m','Freeze seed0-only WD candidate before new paired seeds'],cwd=REPO,check=True)
    from research.unnormalized_muon.gap_wd_campaign import push
    push();cfg={}
    for seed in [40,41,42]:
        for arm,c in [('reference',base(reference['c']['matrix_lr'],LAM)),('candidate',chosen)]:
            c=dict(c,seed=seed,heldout=True,heldout_block=4);cfg[f'window-confirm-{arm}-s{seed}']=c
    register(cfg,'Freeze best WD hypothesis and tuned original-lambda reference before NEW paired seeds40/41/42 and NEW heldout block4. Same20k tokens/update/auxiliary streams; all selection used seed0 development. OneB300/run, six slots, runtime1200s.')
    stage('window-confirm-');ds=paired_report('window-confirm',[40,41,42])
    if left()>1800 and all(x<0 for x in ds) and statistics.mean(ds)<-.003:
        cfg={}
        for arm,c in [('reference',base(reference['c']['matrix_lr'],LAM)),('candidate',chosen)]:
            for factor in [.5,1.,2.]:
                cc=dict(c,matrix_lr=c['matrix_lr']*factor,updates=40000,runtime_limit=2200)
                cfg[f'window-long-{arm}-x{factor:g}']=cc
        register(cfg,'New WD paired win survives all3 seeds with mean<-.003CE: tune both reference/candidate at fresh40k-update/1.31B-token horizon, three peak LRs EACH. Only launch if time remains; seed0 development, no final-heldout tuning.')
        stage('window-long-')
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
