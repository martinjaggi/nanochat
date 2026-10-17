"""Read-only independent schedule/decay audit; no model evaluation."""
import pathlib,json,sys,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'/mloscratch/homes/mljaggi/nanochat-unnormalized-muon')
from research.unnormalized_muon.events import read_events
R=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
O=pathlib.Path('/tmp/muon-window-audit');O.mkdir(exist_ok=True)
names={'um-window-joint-terminal-lr0p01-f0p01':'Cooldown final .01, CLI .01', 'um-follow-first-tune-control-lr0p01':'Cooldown final .05, CLI .01', 'um-follow-mid-reciprocal-high':'Reciprocal, CLI .0283', 'um-window-schedule-lr0p02-f0p05':'Reciprocal + cooldown, CLI .02', 'um-window-first-wd-mixing':'Changing WD, LR .005', 'um-window-first-wd-static-product':'Static matched WD, LR .005'}
fig,axs=plt.subplots(2,2,figsize=(12,8));records=[]
for n,label in names.items():
 p=R/n
 if not (p/'summary.json').exists():continue
 s=json.loads((p/'summary.json').read_text());es=read_events(p/'metrics.jsonl',{'manifest','update','validation'})
 m=next(e for e in es if e['event']=='manifest');u=[e for e in es if e['event']=='update'];v=[e for e in es if e['event']=='validation' and e.get('label')=='tuning']
 idx=[i for i,g in enumerate(m['optimizer_groups']) if g['kind']=='muon'];assert idx
 a=idx[0];assert all(all(e['group_lrs'][i]==e['group_lrs'][a] and e['group_weight_decays'][i]==e['group_weight_decays'][a] for i in idx) for e in u)
 logp=sum(math.log1p(-e['group_lrs'][a]*e['group_weight_decays'][a]) for e in u)
 assert math.isclose(logp,s['muon_contraction'][str(a)]['log_abs'],rel_tol=1e-12,abs_tol=1e-9)
 sample=u[::100]+[u[-1]]
 axs[0,0].plot([x['step']*32768/1e6 for x in v],[x['loss'] for x in v],marker='.',label=label)
 axs[0,1].plot([x['training_active_seconds'] for x in v],[x['loss'] for x in v],marker='.',label=label)
 axs[1,0].plot([x['step'] for x in sample],[x['group_lrs'][a] for x in sample],label=label)
 axs[1,1].plot([x['step'] for x in sample],[x['group_lrs'][a]*x['group_weight_decays'][a] for x in sample],label=label)
 records.append(dict(run=n,label=label,ce=s['validation']['loss'],final_eta=u[-1]['group_lrs'][a],final_wd=u[-1]['group_weight_decays'][a],log_contraction=logp,active_seconds=s['training_active_seconds'],tokens=s['fresh_tokens']))
for ax,x,y in zip(axs.flat,['Update-data tokens (millions)','Training-active seconds','Optimizer update index','Optimizer update index'],['Validation CE (nats/token)','Validation CE (nats/token)','Actual matrix LR','Per-step contraction gamma']):
 ax.set_xlabel(x);ax.set_ylabel(y);ax.grid(alpha=.2)
axs[0,0].set_ylim(3.07,3.6);axs[0,1].set_ylim(3.07,3.6);axs[1,0].set_yscale('log');axs[1,1].set_yscale('log');axs[0,0].legend(fontsize=8)
fig.suptitle('Seed-0 development diagnostics; different WD/LR settings are labelled')
fig.tight_layout();fig.savefig(O/'schedule_diagnostics.png',dpi=160);plt.close(fig)
(O/'audit.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
