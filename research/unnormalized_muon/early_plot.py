"""Reproduce early-allocation rates, contraction, and measured validation curves."""
import json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from research.unnormalized_muon.early_allocation import D,ROOT,rates
from research.unnormalized_muon.events import read_events


def main():
    fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained')
    for k,color in [(1.,'#2468a0'),(1.5,'#d96925'),(2.,'#6b3e91')]:
        eta=np.asarray(rates(k));label=f'{k:g}x early peak'
        axs[0].plot(np.arange(len(eta)),eta,label=label,color=color)
        logc=np.cumsum(np.log1p(-.04593746995939655*eta))
        axs[1].plot(np.arange(len(eta)),np.exp(logc),label=label,color=color)
        name=f'um-earlyalloc-screen-k{k:g}'.replace('.','p')
        path=ROOT/name/'metrics.jsonl'
        if path.exists():
            ev=read_events(path,{'validation'});ev=[e for e in ev if e.get('label')=='tuning' and e['step']>0]
            axs[2].plot([e['step']*32768/1e6 for e in ev],[e['loss'] for e in ev],'.-',label=label,color=color)
    for ax in axs:ax.grid(alpha=.2);ax.legend()
    axs[0].axvline(7000,color='gray',linestyle=':');axs[0].set(xlabel='Update',ylabel='Actual matrix LR',title='Identical late cooldown')
    axs[1].set(xlabel='Update',ylabel='Cumulative contraction product',title='Fixed WD changes total contraction',yscale='log')
    axs[2].set(xlabel='Fresh training tokens (million)',ylabel='Development CE (nats/token)',title='Seed0 measured validation')
    fig.savefig(D/'EARLY_ALLOCATION_SCREEN.png',dpi=160);plt.close(fig)

if __name__=='__main__':main()
