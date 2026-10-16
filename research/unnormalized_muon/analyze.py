"""Aggregate saved metrics only: no model execution or extra training queries."""
import json,pathlib
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
DEST=pathlib.Path(__file__).resolve().parent

def generate():
 runs=[]
 for p in ROOT.glob('um-*/summary.json'):
  s=json.loads(p.read_text());c=s.get('config',json.loads((p.parent/'resolved_config.json').read_text()))
  if not c.get('clean'):continue
  points=[json.loads(l) for l in (p.parent/'metrics.jsonl').read_text().splitlines() if l.strip()]
  vals=[x for x in points if x['event']=='validation' and x['label']=='tuning']
  runs.append((p.parent.name,c,s,points,vals))
 rows=['# Detailed clean Muon evaluation','',
 'All results use the B300 fork model/data/tokenizer and a fixed tuning-validation prefix. CE is natural-log token cross-entropy; lower is better. Single-seed LR/WD screening is not a confirmation. Final heldout data is reserved for frozen settings. Compare endpoints only at matching token budgets. Wall-time curves include all training work, including FW forward probes; curves with token-based LR schedules are descriptive, not a separately matched equal-time experiment.','',
 '## Longer runs','', '| Method | LR | Updates | Val CE | Training sec | Total process sec |', '|---|---:|---:|---:|---:|---:|']
 for n,c,s,pts,vals in sorted(runs):
  if s['updates']<20000:continue
  method='normalized' if not c['variant'] else 'unnormalized '+c.get('matrix_schedule','cooldown')
  mode=c.get('decay_mode','none');method+=f' WD {mode} '+str(c.get('weight_decay',0))
  rows.append(f'| {method} | {c["matrix_lr"]:g} | {s["updates"]} | {s["validation"]["loss"]:.6f} | {s["training_seconds"]:.2f} | {s.get("process_seconds",0):.2f} |')
 rows+=['','## Weight decay search','',
 'Clean geometry keeps row equilibration and NorMuon disabled. Standard decay applies W <- (1-eta*lambda)W - eta*a*Q; cautious decay masks its shrinkage by sign((aQ)*W)>=0. The unnormalization factor scales only the directional term. Native batch/model-horizon coefficient scaling and cosine WD schedule remain intact; explicit update count does not change the native compute-optimal model horizon used to scale lambda. Auxiliary AdamW is unchanged.','',
 'CLI lambda = 0.28*(0.04/CLI_eta)*strength matches nominal eta*lambda exposure across LRs/methods for the same cooldown horizon and shape. Cautious masks make its logged nominal exposure an upper bound. Strength is tuned independently for each method and rule. Zero-WD controls are reported separately.','',
 '| Method | Decay | Strength | CLI LR | CLI WD | Updates | Val CE | Nominal Muon exposure range |','|---|---|---:|---:|---:|---:|---:|---|']
 for n,c,s,pts,vals in sorted(runs):
  if 'wd_strength' not in c:continue
  manifest=next(x for x in pts if x['event']=='manifest')
  ex=[s['decay_exposure'][str(i)] for i,g in enumerate(manifest['optimizer_groups']) if g['kind']=='muon']
  rows.append(f'| {"unnormalized" if c["variant"] else "normalized"} | {c["decay_mode"]} | {c["wd_strength"]:g} | {c["matrix_lr"]:g} | {c["weight_decay"]:.7g} | {s["updates"]} | {s["validation"]["loss"]:.6f} | {min(ex):.5g}–{max(ex):.5g} |')
 rows+=['','## FW gap-based step and line search','',
 'Fixed radii R_i=max(1,radius_factor*initial spectral norm(W_i)). A certified spectral-safe approximate polar direction Q_i defines D_i=-R_i Q_i-W_i. One shared gamma=clip(b/(L*v),0,gamma_cap); original runs use gamma_cap=1, while scheduled-cap variants multiply a tuned cap by the common warmup/cooldown LR multiplier. This is an explicit additional safeguard, not automatic shrinking from the gap alone. The gap uses b=-sum<G_i,D_i>, v=sum||D_i||F^2. Current-gradient and momentum oracles are separately labelled. With an approximate or momentum oracle, b is a directional gap, not an exact FW optimality certificate. Nonpositive b skips all candidate forwards. No additional matrix decay is applied.','',
 'Strict smoothness backtracking compares a same-path functional reference at gamma=0 with candidates on the entire current effective batch, using the same token weighting and preserved RNG. Auxiliary weights are frozen during checks and updated afterward. The separately labelled Armijo variant accepts f(candidate)<=f0-c*gamma*b with c=.01 and forbids measured increases; it does NOT certify the original quadratic smoothness bound. Same-batch decrease does not guarantee heldout improvement.','',
 '| Run | Updates | Val CE | Accepted | Negative b | Extra batch forwards | FW sec | Max spectral ratio |','|---|---:|---:|---:|---:|---:|---:|---:|']
 for n,c,s,pts,vals in sorted(runs):
  if not c.get('fw'):continue
  f=s.get('fw_diagnostics',{});acc=f.get('accepted_steps','—');neg=f.get('negative_alignment_steps','—')
  rows.append(f'| {n} | {s["updates"]} | {s["validation"]["loss"]:.6f} | {acc} | {neg} | {s.get("extra_forward_evals",0)} | {s.get("fw_seconds",0):.2f} | {max(s["fw_feasibility"].values()):.6f} |')
 for n,c,s,pts,vals in sorted(runs):
  f=s.get('fw_diagnostics')
  if not f:continue
  audit=[x for x in pts if x['event']=='fw_search_audit']
  fw=[x for x in pts if x['event']=='fw_update']
  rows+=['',f'### {n}','',f'Oracle: {f["oracle"]}; acceptance: {f.get("acceptance","smoothness")}; compiled candidates: {f.get("compiled_candidates",False)}; radius factor: {f["radius_factor"]:g}; gamma cap: {f.get("gamma_cap",1):g}; scheduled: {f.get("schedule_gamma",False)}. Search state/RNG audit: {bool(audit)}. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: {s["extra_microbatch_forward_evals"]}. Extra diagnostic gradient queries: {f.get("diagnostic_gradient_evals",0)}, diagnostic seconds: {f.get("diagnostic_seconds",0):.3f}.', '',
    '| Quantity | Min | P25 | Median | P75 | Max |','|---|---:|---:|---:|---:|---:|']
  for key,q in f['statistics'].items():rows.append('| '+key+' | '+' | '.join(f'{q[k]:.6g}' for k in ['min','p25','median','p75','max'])+' |')
  rows+=['', 'FW timing components (seconds): '+', '.join(f'{k}={v:.3f}' for k,v in f['component_seconds'].items())+'.',
   f'Accepted steps with measured minibatch increase: {sum(x["accepted"] and x["actual_decrease"]<0 for x in fw)}; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.']
 (DEST/'DETAILED_EVAL.md').write_text('\n'.join(rows)+'\n')
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axs=plt.subplots(1,2,figsize=(11,4))
 for n,c,s,pts,vals in sorted(runs):
  if s['updates']<20000:continue
  label=('U '+c.get('matrix_schedule','cooldown') if c['variant'] else 'N')+f' lr{c["matrix_lr"]:g} WD{c.get("decay_mode","none")}'
  vals=[v for v in vals if v['step']>0]
  axs[0].plot([v['step']*32768/1e6 for v in vals],[v['loss'] for v in vals],'.-',label=label)
  axs[1].plot([v['training_seconds'] for v in vals],[v['loss'] for v in vals],'.-',label=label)
 for ax in axs:ax.set_ylabel('Validation CE');ax.grid(alpha=.2)
 axs[0].set_xlabel('Fresh tokens (millions)');axs[1].set_xlabel('Measured training seconds')
 if axs[0].lines:axs[0].legend(fontsize=7)
 fig.tight_layout();fig.savefig(DEST/'long_comparison.png',dpi=140);plt.close(fig)
 fw_runs=[x for x in runs if x[2].get('fw_diagnostics')]
 if fw_runs:
  fig,axs=plt.subplots(2,2,figsize=(11,7))
  for n,c,s,pts,vals in fw_runs:
   xs=[x for x in pts if x['event']=='fw_update'];label=n.removeprefix('um-')
   for ax,key in zip(axs.flat,['gamma','L','b','actual_decrease']):
    ax.plot([x['step'] for x in xs],[x[key] for x in xs],label=label,alpha=.8);ax.set_xlabel('Update');ax.set_ylabel(key);ax.grid(alpha=.2)
  for ax in axs.flat:ax.set_yscale('symlog',linthresh=1e-6)
  axs[0,0].legend(fontsize=6)
  fig.tight_layout();fig.savefig(DEST/'fw_diagnostics.png',dpi=140);plt.close(fig)
 return ['research/unnormalized_muon/'+name for name in ['DETAILED_EVAL.md','long_comparison.png','fw_diagnostics.png'] if (DEST/name).exists()]
if __name__=='__main__':generate()
