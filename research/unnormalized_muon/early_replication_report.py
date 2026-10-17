"""Summarize all frozen fixed-WD shapes on both paired seed cohorts."""
import json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research.unnormalized_muon.early_allocation import ROOT,D
from research.unnormalized_muon.events import read_events


def main():
    seeds=[70,71,72,80,81,82];ss={};curves={}
    for arm in ['baseline','mid','early']:
        for seed in seeds:
            p=ROOT/f'um-earlyalloc-confirm-{arm}-s{seed}'
            if not (p/'summary.json').exists():continue
            s=json.loads((p/'summary.json').read_text());assert s['updates']==20000 and s['status']=='completed'
            ev=read_events(p/'metrics.jsonl',{'manifest','validation'});m=ev[0]
            assert m['GPU_count']==1 and 'B300' in m['GPU_model']
            ss[arm,seed]=(s,m)
            curves[arm,seed]=[e for e in ev if e['event']=='validation' and e['label']=='tuning' and e['step']>0]
    lines=['# Frozen early-allocation family: paired replication','',
    'All arms use ordinary fixed WD .04593746995939655, actual join LR .005 and identical late65% cooldown. Peak multipliers1/1.5/2 were frozen using seed0 development only. Initial cohort70/71/72; extension80/81/82. The extension was fixed after the ambiguous initial2x result, before any1.5x heldout endpoint: this is descriptive pilot evidence, not an originally fixed-sample significance test. Same heldoutblock6 and262144 targets. [Extension protocol](EARLY_ALLOCATION_REPLICATION_PROTOCOL.md).','',
    '| Seed | Arm | Heldout CE | CE minus paired baseline | Active seconds | Fresh Mtoken/s |','|---|---|---:|---:|---:|---:|']
    deltas={a:[] for a in ['mid','early']}
    for seed in seeds:
        for arm in ['baseline','mid','early']:
            if (arm,seed) not in ss or ('baseline',seed) not in ss:continue
            s,m=ss[arm,seed];b,bm=ss['baseline',seed]
            assert s['heldout']['validation_hash']==b['heldout']['validation_hash'] and m['initial_parameter_hash']==bm['initial_parameter_hash']
            delta=s['heldout']['loss']-b['heldout']['loss']
            if arm!='baseline':deltas[arm].append(dict(seed=seed,delta=delta))
            lines.append(f'| {seed} | {arm} | {s["heldout"]["loss"]:.9f} | {delta:+.9f} | {s["training_active_seconds"]:.3f} | {s["fresh_tokens"]/s["training_active_seconds"]/1e6:.4f} |')
    summary={}
    for arm in ['mid','early']:
        for cohort,label in [([70,71,72],'initial3'),([80,81,82],'new3'),(seeds,'pooled6')]:
            ds=[r['delta'] for r in deltas[arm] if r['seed'] in cohort]
            if len(ds)>=2:
                x=dict(n=len(ds),mean=statistics.mean(ds),sample_sd=statistics.stdev(ds));summary[arm+'_'+label]=x
                lines+=['',f'{arm}/{label}: n={len(ds)}, mean **{x["mean"]:+.6f}CE**, sampleSD **{x["sample_sd"]:.6f}**.']
    lines+=['','Negative deltas favor the early reciprocal arm. No setting is retuned from these heldout results. Static/history contraction controls have3seeds only and are reported separately. Token-matched endpoints contain the same gradient count and native optimizer pipeline. Different wall times across jobs are descriptive; no independent equal-time result is implied.125829354 trainable parameters,655360000 update-data tokens/run,5.2083tokens/parameter. Finite NS/BF16/Nesterov and these stochastic outcomes establish no deterministic FW theorem.','', '![Frozen-family replication](EARLY_ALLOCATION_REPLICATION.png)']
    (D/'EARLY_ALLOCATION_REPLICATION.md').write_text('\n'.join(lines)+'\n')
    (D/'EARLY_ALLOCATION_REPLICATION.json').write_text(json.dumps(dict(deltas=deltas,summary=summary),indent=2)+'\n')
    fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for arm,col in [('baseline','#2468a0'),('mid','#6b3e91'),('early','#d96925')]:
        available=[seed for seed in seeds if (arm,seed) in ss and len(curves[arm,seed])==4]
        if available:
            ys=np.asarray([[e['loss'] for e in curves[arm,s]] for s in available]);x=np.asarray([5000,10000,15000,20000])*32768/1e6
            axs[0,0].plot(x,ys.mean(0),'.-',label=f'{dict(baseline="Baseline",mid="1.5×",early="2×")[arm]} (n={len(ys)})',color=col)
            if len(ys)>1:axs[0,0].fill_between(x,ys.mean(0)-ys.std(0,ddof=1),ys.mean(0)+ys.std(0,ddof=1),color=col,alpha=.1)
        if arm!='baseline':
            common=[s for s in available if ('baseline',s) in ss and len(curves['baseline',s])==4]
            if common:
                ds=np.asarray([[a['loss']-b['loss'] for a,b in zip(curves[arm,s],curves['baseline',s])] for s in common]);axs[0,1].plot(x,ds.mean(0),'.-',color=col,label=dict(baseline="Baseline",mid="1.5×",early="2×")[arm])
                if len(ds)>1:axs[0,1].fill_between(x,ds.mean(0)-ds.std(0,ddof=1),ds.mean(0)+ds.std(0,ddof=1),color=col,alpha=.1)
            if deltas[arm]:axs[1,0].plot([r['seed'] for r in deltas[arm]],[r['delta'] for r in deltas[arm]],'o',color=col,label=dict(baseline="Baseline",mid="1.5×",early="2×")[arm])
        if available:axs[1,1].scatter([seed for seed in available],[ss[arm,s][0]['fresh_tokens']/ss[arm,s][0]['training_active_seconds']/1e6 for s in available],color=col,label=dict(baseline="Baseline",mid="1.5×",early="2×")[arm])
    for ax in axs.flat:ax.grid(alpha=.2);ax.legend()
    axs[0,0].set(xlabel='Fresh tokens (million)',ylabel='Development CE',title='Mean ± sample SD')
    axs[0,1].set(xlabel='Fresh tokens (million)',ylabel='Paired development CE delta',title='Early arm minus baseline');axs[0,1].axhline(0,color='gray',lw=1)
    axs[1,0].set(xlabel='Paired seed',ylabel='Heldout CE delta',title='Frozen heldout endpoints');axs[1,0].axhline(0,color='gray',lw=1)
    axs[1,1].set(xlabel='Paired seed',ylabel='Fresh million tokens / active second',title='Timing varies across scheduled jobs')
    fig.suptitle('WD-independent early reciprocal allocation; fixed late cooldown',fontsize=12)
    fig.savefig(D/'EARLY_ALLOCATION_REPLICATION.png',dpi=150);plt.close(fig)

if __name__=='__main__':main()
