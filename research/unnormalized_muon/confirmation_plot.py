"""Plot completed token-matched confirmations; time curves are not time reruns."""
import argparse,json,pathlib,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research.unnormalized_muon.events import read_events
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--prefix',default='window-confirm');parser.add_argument('--output',default='/tmp/muon-window-audit/confirmation_curves.png');args=parser.parse_args()
 fig,axs=plt.subplots(1,3,figsize=(15,4.5),layout='constrained');summaries={};manifests={};ys=[]
 for arm,color in [('reference','#2468a0'),('candidate','#d96925')]:
  losses=[];steps=[]
  for seed in [40,41,42]:
   p=ROOT/f'um-{args.prefix}-{arm}-s{seed}';s=json.loads((p/'summary.json').read_text());assert s['status']=='completed' and s['updates']==20000
   summaries[arm,seed]=s;events=read_events(p/'metrics.jsonl',{'manifest','validation'});manifests[arm,seed]=next(e for e in events if e['event']=='manifest')
   values=[e for e in events if e['event']=='validation' and e.get('label')=='tuning' and e['step']>0];assert [e['step'] for e in values]==[5000,10000,15000,20000]
   losses.append([e['loss'] for e in values]);steps=[e['step'] for e in values];ys.extend(losses[-1])
   label=arm if seed==40 else None
   axs[1].plot([e['training_active_seconds'] for e in values],losses[-1],'.-',color=color,alpha=.55,label=label)
  a=np.asarray(losses);x=np.asarray(steps)*32768/1e6;mean=a.mean(0);sd=a.std(0,ddof=1)
  axs[0].plot(x,mean,'.-',color=color,label=arm);axs[0].fill_between(x,mean-sd,mean+sd,color=color,alpha=.15)
 deltas=[]
 for seed in [40,41,42]:
  a,b=summaries['reference',seed],summaries['candidate',seed]
  assert a['heldout']['validation_hash']==b['heldout']['validation_hash']
  assert manifests['reference',seed]['initial_parameter_hash']==manifests['candidate',seed]['initial_parameter_hash']
  deltas.append(b['heldout']['loss']-a['heldout']['loss'])
 axs[2].axhline(0,color='grey',linewidth=1);axs[2].plot([40,41,42],deltas,'o',color='#6b3e91');axs[2].axhline(statistics.mean(deltas),color='#6b3e91',linestyle='--',label=f'mean {statistics.mean(deltas):+.5f}\nSD {statistics.stdev(deltas):.5f}, n=3')
 for ax in axs:ax.grid(alpha=.2)
 for ax in axs[:2]:ax.set_ylim(min(ys)-.02,max(ys)+.02);ax.set_ylabel('Development CE (nats/token)');ax.legend()
 axs[0].set_xlabel('Update-data tokens (millions)');axs[0].set_title('Token-matched: mean ± sample SD')
 axs[1].set_xlabel('Measured training-active seconds');axs[1].set_title('Token-clock curves: individual seeds')
 axs[2].set_xlabel('New paired seed');axs[2].set_xticks([40,41,42]);axs[2].set_ylabel('Heldout CE: candidate minus reference');axs[2].set_title('20k-update heldout endpoints');axs[2].legend()
 fig.suptitle('Frozen static-Muon setting comparison; 25–100% evaluations shown\nTime curves do not constitute independent equal-time reruns',fontsize=12)
 out=pathlib.Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out,dpi=160);plt.close(fig)
 print('Saved',out)

if __name__=='__main__':main()
