"""Compact v2 search, cost and contraction report from saved run artifacts."""
import json,pathlib,statistics
from research.unnormalized_muon.events import read_events
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');DEST=pathlib.Path(__file__).resolve().parent

def generate():
 runs=[]
 for p in ROOT.glob('um-lens-*/summary.json'):
  s=json.loads(p.read_text());c=s.get('config')
  if c and c.get('protocol_version')==2:runs.append((p.parent.name,c,s,p.parent))
 lines=['# FW-lens v2 live evaluation','',
 'Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l; fixed ordinary unmasked lambda=.1837498798375862. Unlike v1 native-shaped rays, shape does not multiply decay. Approximate finite NS/Nesterov/minibatch directions do not reproduce deterministic exact-LMO theorems. Row equilibration and NorMuon are off. Auxiliary AdamW stays frozen during loss checks and updates afterward.','',
 'Joint uses positive part after summing directional gaps and a checked global quadratic model. Layer Armijo freezes its per-layer proposal and backtracks one shared multiplier. Smoothed/relative-cap proposals retain that check. Periodic-curvature variants explicitly skip loss checks on intervening updates and have no observed-descent guarantee for those steps.','',
 'Token-based schedule curves are descriptive. Independently scheduled equal-time endpoints are reported in FW_LENS_EQUAL_TIME.md after completion. Active time excludes recorded overlapping compiler events and separate validation/checkpoint/setup; new measured runs discard3 warmup updates and reset complete model/optimizer/data/RNG first. Warmup gradient/forward counts and seconds remain in total job cost.','',
 '| Run | Family | Budget | Seed | Val CE | Heldout CE | Active sec | Extra batch forwards | Warmup sec | Process sec |','|---|---|---|---:|---:|---:|---:|---:|---:|']
 for n,c,s,p in sorted(runs):
  fam=c.get('lens_family',c.get('gap_scope',c.get('matrix_schedule','control')))
  budget=f'{c["time_budget"]:.3f}s' if c.get('time_budget') else f'{s["updates"]} updates'
  held=f'{s["heldout"]["loss"]:.6f}' if s.get('heldout') else '—'
  lines.append(f'| {n} | {fam} | {budget} | {c["seed"]} | {s["validation"]["loss"]:.6f} | {held} | {s.get("training_active_seconds",0):.3f} | {s.get("extra_forward_evals",0)} | {s.get("warmup_seconds",0):.3f} | {s.get("process_seconds",0):.2f} |')
 lines+=['','## Adaptive diagnostics and contraction','',
 'Contraction is the actual coefficient product_t(1-lambda*eta_l,t), represented in signed log space when necessary. It is not the parameter-norm ratio because the directional term also changes weights. Different schedules retain the same lambda/domain geometry but can have very different cumulative contraction.','',
 '| Run | Checked accepted / updates | Unchecked | Median eta | Median gamma | Median curvature | Median backtracks | Contraction log range | Final spectral ratio max |','|---|---|---:|---:|---:|---:|---:|---|---:|']
 for n,c,s,p in sorted(runs):
  g=s.get('gap_diagnostics')
  if not g:continue
  contracts=[x['log_abs'] for x in s.get('muon_contraction',{}).values() if x and x.get('log_abs') is not None]
  cr=f'{min(contracts):.4g} to {max(contracts):.4g}' if contracts else '—'
  lines.append(f'| {n} | {g["accepted_steps"]}/{g["steps"]} | {g.get("unchecked_steps",0)} | {g["actual_eta_quantiles"]["median"]:.5g} | {g["gamma_quantiles"]["median"]:.5g} | {g["L_quantiles"]["median"]:.5g} | {g["trial_quantiles"]["median"]:.3g} | {cr} | {max(s["gap_feasibility"].values()):.6g} |')
 lines+=['', 'Curvature values in Armijo variants parameterize proposals; their acceptance is NOT a certificate of the quadratic upper model. Final spectral ratios are lambda*||W_l||op/c_l; native approximate NS output is not certified to have unit spectral norm. Initial/final iterate feasibility alone does not certify oracle accuracy. Cold two-second clock checks intentionally permit one-update overshoot; do not use them as quality endpoints.','']
 (DEST/'FW_LENS_RESULTS.md').write_text('\n'.join(lines))
 paths=['research/unnormalized_muon/FW_LENS_RESULTS.md']
 if not runs:return paths
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(11,4.5))
 for scope,ax in zip(['joint','layer'],axes):
  for policy,color in [('stable','tab:orange'),('cooldown','tab:blue')]:
   rr=sorted([(n,c,s,p) for n,c,s,p in runs if c.get('lens_family')==scope+'-'+policy and s['updates']==2000 and not c.get('time_budget')],key=lambda x:x[1]['gap_eta_cap'])
   if rr:ax.scatter([x[1]['gap_eta_cap'] for x in rr],[x[2]['validation']['loss'] for x in rr],label=policy,color=color)
  ax.set_xscale('log',base=2);ax.set_xlabel('Actual LR cap');ax.set_ylabel('Validation CE');ax.set_title(scope+' gap,65.5M tokens');ax.grid(alpha=.2)
  if ax.collections:ax.legend()
 fig.tight_layout();fig.savefig(DEST/'fw_lens_caps.png',dpi=140);plt.close(fig);paths.append('research/unnormalized_muon/fw_lens_caps.png')
 fig,axes=plt.subplots(1,2,figsize=(11,4.5));selected={}
 for r in runs:
  n,c,s,p=r
  if s['updates']<512 or c.get('time_budget') or c['seed']!=0:continue
  fam=c.get('lens_family',c.get('gap_scope','control'))
  key=(fam,s['updates'])
  if key not in selected or s['validation']['loss']<selected[key][2]['validation']['loss']:selected[key]=r
 for n,c,s,p in selected.values():
  pts=read_events(p/'metrics.jsonl',{'validation'})
  pts=[x for x in pts if x['event']=='validation' and x['label']=='tuning' and x['step']>0]
  label=c.get('lens_family','method')+f' T{s["updates"]}'
  axes[0].plot([x['step']*32768/1e6 for x in pts],[x['loss'] for x in pts],'.-',label=label)
  axes[1].plot([x.get('training_active_seconds',x['training_seconds']) for x in pts],[x['loss'] for x in pts],'.-',label=label)
 for ax in axes:ax.set_ylabel('Validation CE');ax.grid(alpha=.2)
 axes[0].set_xlabel('Fresh tokens (millions)');axes[1].set_xlabel('Measured training-active seconds')
 if axes[1].lines:axes[1].legend(fontsize=6,loc='upper left',bbox_to_anchor=(1.02,1))
 fig.tight_layout();fig.savefig(DEST/'fw_lens_progress.png',dpi=140,bbox_inches='tight');plt.close(fig);paths.append('research/unnormalized_muon/fw_lens_progress.png')
 return paths
