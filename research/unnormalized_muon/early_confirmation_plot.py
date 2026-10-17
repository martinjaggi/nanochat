"""Reproduce four-arm early-allocation confirmation curves and paired deltas."""
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from research.unnormalized_muon.early_allocation import ROOT,D
from research.unnormalized_muon.events import read_events


def main(kind='confirm'):
    fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained');summaries={}
    for arm,col in [('baseline','#2468a0'),('early','#d96925'),('matched','#708238'),('neutral','#6b3e91')]:
        curves=[];positions=[]
        for seed in [70,71,72]:
            p=ROOT/f'um-earlyalloc-{kind}-{arm}-s{seed}'
            if not (p/'summary.json').exists():continue
            s=json.loads((p/'summary.json').read_text());summaries[arm,seed]=s
            ev=[e for e in read_events(p/'metrics.jsonl',{'validation'}) if e.get('label')=='tuning' and e['step']>0]
            if ev:
                axs[1].plot([e['training_active_seconds'] for e in ev],[e['loss'] for e in ev],'.-',color=col,alpha=.45,label=arm if seed==70 else None)
            if len(ev)==4:curves.append([e['loss'] for e in ev]);positions.append([e['step'] for e in ev])
        if curves and all(p==positions[0] for p in positions):
            a=np.asarray(curves);x=np.asarray(positions[0])*32768/1e6;axs[0].plot(x,a.mean(0),'.-',color=col,label=f'{arm} (n={len(a)})')
            if len(a)>1:axs[0].fill_between(x,a.mean(0)-a.std(0,ddof=1),a.mean(0)+a.std(0,ddof=1),color=col,alpha=.1)
        if arm!='baseline':
            seeds=[s for s in [70,71,72] if (arm,s) in summaries and ('baseline',s) in summaries]
            ds=[summaries[arm,s]['heldout']['loss']-summaries['baseline',s]['heldout']['loss'] for s in seeds]
            if ds:axs[2].plot(seeds,ds,'o-',color=col,label=f'{arm}: mean {statistics.mean(ds):+.5f}')
    for ax in axs:ax.grid(alpha=.2);ax.legend()
    axs[0].set(xlabel='Fresh update-data tokens (million)',ylabel='Development CE',title='Token-matched: mean ± sample SD')
    axs[1].set(xlabel='Training-active seconds',ylabel='Development CE',title='Measured trajectories; individual seeds')
    axs[2].axhline(0,color='gray',lw=1);axs[2].set(xlabel='Fresh paired seed',ylabel='Heldout CE minus baseline',xticks=[70,71,72],title='Frozen heldout block6 endpoints')
    fig.suptitle('WD-independent early reciprocal allocation: '+kind+'\nToken-clock trajectories are not independent equal-time endpoints',fontsize=11)
    fig.savefig(D/f'EARLY_ALLOCATION_{kind.upper()}.png',dpi=160);plt.close(fig)

if __name__=='__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else 'confirm')
