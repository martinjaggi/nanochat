"""Creative FW-lens search with screening, refinement, paired seeds and equal time."""
import copy,json,math,pathlib,statistics,subprocess,sys
from research.unnormalized_muon.queue import ROOT,REPO
from research.unnormalized_muon.gap_wd_campaign import record,stage,push
D=REPO/'research/unnormalized_muon';LAM=.1837498798375862

def rows():
 out=[]
 for p in ROOT.glob('um-lens-*/summary.json'):
  s=json.loads(p.read_text());c=s.get('config')
  if c and c.get('protocol_version')==2:out.append(dict(name=p.parent.name,c=c,s=s))
 return out

def score(r):return r['s']['validation']['loss']
def speed(r):return r['s']['training_active_seconds']/r['s']['updates']
def family(c):
 if c.get('lens_family'):return c['lens_family']
 return c.get('gap_scope',c.get('matrix_schedule','cooldown'))+'-'+c.get('gap_cap_schedule','none')
def base():return dict(protocol_version=2,clean=True,variant=False,decay_mode='standard',fixed_wd=LAM,gap_geometry='q_scaled',matrix_lr=.04,matrix_schedule='cooldown',updates=2000,seed=0,depth=8,runtime_limit=1800,warmup_updates=3)

def main_configs():
 out={}
 for schedule,label in [('cooldown','control'),('fw_reciprocal','reciprocal')]:
  for lr in [.02,.04,.08]:out[f'lens-main-{label}-lr{lr:g}']=dict(base(),matrix_schedule=schedule,matrix_lr=lr,lens_family=label,runtime_limit=900)
 for scope,accept in [('joint','quadratic'),('layer','armijo')]:
  for policy in ['stable','cooldown']:
   for cap in [.005,.02,.08]:out[f'lens-main-{scope}-{policy}-cap{cap:g}']=dict(base(),gap_scope=scope,gap_acceptance=accept,gap_eta_cap=cap,gap_cap_schedule=policy,lens_family=scope+'-'+policy)
 return out

def validate_checks():
 rr={r['name']:r for r in rows()}
 for suffix in ['0-control','1-joint','2-layer','3-time-control','4-time-layer','5-creative','6-periodic']:
  r=rr['um-lens-check-'+suffix];c=r['c'];s=r['s']
  assert c['gap_geometry']=='q_scaled' and c['fixed_wd']==LAM
  points=[json.loads(x) for x in (ROOT/r['name']/'metrics.jsonl').read_text().splitlines() if x.strip()]
  if c.get('time_budget'):
   assert s['training_active_seconds']>=c['time_budget'] and s['training_compile_seconds']>0
   assert s['time_overshoot']<=s['last_step_active_seconds']+1e-4
  else:assert s['updates']==64
  if c.get('gap_scope'):
   g=s['gap_diagnostics'];assert g['applied_steps']>=.75*s['updates']
   assert any(p['event']=='gap_wd_audit' for p in points)
   records=[p for p in points if p['event']=='gap_wd_update'];last=0
   for p in records:
    assert max(p['gammas'])<=1+1e-7
    if not p['checked']:assert p['extra_forward_evals']==last,'unchecked step ran hidden forward'
    last=p['extra_forward_evals']
   if c.get('gap_probe_every')==4:assert g['unchecked_steps']==48
   if c.get('gap_proposal_beta'):assert all(p['proposal_beta']==.9 for p in records)
  assert s['extra_microbatch_forward_evals']==2*s['extra_forward_evals'] if c.get('gap_scope') else True
 for suffix in ['7-warm-time-control','8-warm-time-layer']:
  r=rr['um-lens-check-'+suffix];s=r['s'];assert s['warmup_gradient_evals']==3
  assert s['updates']>=2 and s['training_active_seconds']>=5 and s['time_overshoot']<=s['last_step_active_seconds']+1e-4
  points=[json.loads(x) for x in (ROOT/r['name']/'metrics.jsonl').read_text().splitlines() if x.strip()]
  assert any(x['event']=='disposable_warmup' and x['model_optimizer_data_rng_reset'] for x in points)

def screen():return [r for r in rows() if r['s']['updates']==2000 and not r['c'].get('time_budget')]

def confirmation_report(prefix,filename,title):
 groups={}
 for r in rows():
  if r['name'].startswith(prefix):groups.setdefault(r['c']['lens_arm'],{})[r['c']['seed']]=r
 baseline=groups['control'];lines=['# '+title,'',
 'Geometry: Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l, fixed ordinary unmasked lambda=.1837498798375862. Native Nesterov/five NS/Frobenius and AdamW groups retained. Seed0 tuning only; settings frozen before paired seeds10/11/12 and reserved heldout. Three seeds are limited evidence. Approximate NS and minibatch acceptance do not validate deterministic FW convergence theorems.','',
 '| Method | Seed | Updates | Active sec | Heldout CE | Paired delta vs control | Extra batch forwards | Process sec | Overshoot sec |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
 for arm,rr in sorted(groups.items()):
  ds=[]
  for seed,r in sorted(rr.items()):
   s=r['s'];b=baseline[seed]['s'];assert s.get('heldout') and b.get('heldout')
   def manifest(row):return json.loads((ROOT/row['name']/'metrics.jsonl').read_text().splitlines()[0])
   assert manifest(r)['initial_parameter_hash']==manifest(baseline[seed])['initial_parameter_hash']
   assert s['heldout']['validation_hash']==b['heldout']['validation_hash']
   d=s['heldout']['loss']-b['heldout']['loss'];ds.append(d)
   lines.append(f'| {arm} | {seed} | {s["updates"]} | {s["training_active_seconds"]:.3f} | {s["heldout"]["loss"]:.6f} | {d:+.6f} | {s.get("extra_forward_evals",0)} | {s["process_seconds"]:.2f} | {s.get("time_overshoot",0):.4f} |')
  assert len(ds)==3
  lines+=['',f'{arm}: paired heldout deltas mean {statistics.mean(ds):+.6f}, sample SD {statistics.stdev(ds):.6f}, n=3.','']
 p=D/filename;p.write_text('\n'.join(lines)+'\n');subprocess.run(['git','add',str(p.relative_to(REPO))],cwd=REPO,check=True)
 subprocess.run(['git','commit','-m',title],cwd=REPO,check=True);push()
 return groups

def main():
 stage('lens-check-');validate_checks()
 record(main_configs(),'FW-lens v2 hardware prerequisites passed. Screen18 configurations at65.5M tokens: tuned ordinary-WD control and shifted reciprocal; joint quadratic and layer Armijo share caps{.005,.02,.08}, stable versus cooldown. All trials recorded; no heldout selection.')
 stage('lens-main-,wd-grid-')
 # Refine each family's best peak/cap fairly and check startup curvature.
 if not list((D/'configs').glob('lens-refine-*.json')):
  configs={}
  for fam in ['control','reciprocal','joint-stable','joint-cooldown','layer-stable','layer-cooldown']:
   best=min([r for r in screen() if family(r['c'])==fam],key=score);c=best['c']
   key='matrix_lr' if fam in ['control','reciprocal'] else 'gap_eta_cap'
   values=[r['c'][key] for r in screen() if family(r['c'])==fam]
   for index,factor in enumerate(([.5,2.] if key=='gap_eta_cap' or c[key] in [min(values),max(values)] else [2**-.5,2**.5])):
    cc=copy.deepcopy(c);cc[key]*=factor
    if cc[key] not in values:configs[f'lens-refine-{fam}-{index}']=cc
   if c.get('gap_scope'):
    for index,L in enumerate([.001,.1]):configs[f'lens-startL-{fam}-{index}']=dict(c,gap_initial_L=L)
  record(configs,'Refine best LR/cap for ALL six families; factor-two boundary checks or geometric midpoints, plus matched initial-curvature sensitivity for all four adaptive families. Same2000-update budget.')
 stage('lens-refine-,lens-startL-')
 configs={};joint=min([r for r in screen() if r['c'].get('gap_scope')=='joint'],key=score);layer=min([r for r in screen() if r['c'].get('gap_scope')=='layer'],key=score)
 for beta in [.5,.9]:configs[f'lens-creative-ema{beta:g}']=dict(layer['c'],gap_proposal_beta=beta,lens_family='layer-ema')
 for relative in [.01,.03]:configs[f'lens-creative-relative{relative:g}']=dict(layer['c'],gap_relative_cap=relative,lens_family='layer-relative')
 for cadence in [2,4]:configs[f'lens-creative-periodic{cadence}']=dict(joint['c'],gap_probe_every=cadence,lens_family='joint-periodic')
 record(configs,'Creative controlled screening: layer LR proposal EMA beta{.5,.9}; relative update norm cap{.01,.03}; joint cached-curvature checks every{2,4}. Six candidates restart at identical seed0; unchecked steps have NO loss probes or acceptance claim.')
 stage('lens-creative-')
 configs={}
 # Keep the two cap policies represented at the longer horizon.
 for fam in ['control','reciprocal']:
  group=sorted([r for r in screen() if family(r['c'])==fam],key=score)
  for rank,r in enumerate(group[:2]):configs[f'lens-long-{fam}-{rank}']=dict(r['c'],updates=20000,runtime_limit=2400,heldout=False)
 for scope in ['joint','layer']:
  for policy in ['stable','cooldown']:
   r=min([r for r in screen() if family(r['c'])==scope+'-'+policy],key=score)
   configs[f'lens-long-{scope}-{policy}']=dict(r['c'],updates=20000,runtime_limit=5400,heldout=False)
 creative=[r for r in screen() if r['name'].startswith('um-lens-creative-')]
 competitive=[r for r in creative if score(r)<=min(score(joint),score(layer))+.03 or (r['c'].get('gap_probe_every',1)>1 and score(r)<=score(joint)+.15 and speed(r)<.8*speed(joint))]
 if competitive:
  fam=family(min(competitive,key=score)['c']);g=sorted([r for r in creative if family(r['c'])==fam],key=score)
  for rank,r in enumerate(g[:2]):configs[f'lens-long-creative-{rank}']=dict(r['c'],updates=20000,runtime_limit=5400,heldout=False)
 record(configs,'Promote at most10 fresh655M-token settings: control/reciprocal best2, best stable/cooled joint and layer, plus best2 from ONE competitive creative family. All full-horizon schedules restarted; no test-set tuning. Keep costs within50GPUh total.')
 stage('lens-long-')
 long=[r for r in rows() if r['name'].startswith('um-lens-long-')];selected={}
 for fam in ['control','reciprocal']:
  selected[fam]=min([r for r in long if family(r['c'])==fam],key=score)
 for scope in ['joint','layer']:
  selected[scope]=min([r for r in long if r['c'].get('gap_scope')==scope],key=score)
 # Confirmation focuses on the strongest comparison; retain both gap scopes
 # if within.05CE of the tuned control, otherwise confirm the better gap only.
 gap_best=min([selected['joint'],selected['layer']],key=score)
 selected={k:r for k,r in selected.items() if k=='control' or (k=='reciprocal' and score(r)<=score(selected['control'])+.03) or (k in ['joint','layer'] and (score(r)<=score(selected['control'])+.05 or r is gap_best))}
 configs={}
 for arm,r in selected.items():
  for seed in [10,11,12]:configs[f'lens-confirm-{arm}-s{seed}']=dict(r['c'],seed=seed,heldout=True,lens_arm=arm)
 record(configs,'Freeze best v2 settings using seed0 tuning. Three NEW paired seeds10/11/12 for tuned control and strongest gap comparison(s); reciprocal only if competitive. Reserved heldout used only now. All attempts and actual cost retained.')
 stage('lens-confirm-');groups=confirmation_report('um-lens-confirm-','FW_LENS_CONFIRMATION.md','FW-lens paired token-matched confirmation')
 H=statistics.median(r['s']['training_active_seconds'] for r in groups['control'].values())
 configs={}
 gap_arm='joint' if 'joint' in selected and selected['joint'] is gap_best else 'layer'
 for arm in ['control',gap_arm]:
  for seed in [10,11,12]:
   c=dict(selected[arm]['c'],seed=seed,heldout=True,lens_arm=arm,time_budget=H,reference_updates=20000,max_updates=200000,runtime_limit=math.ceil(H+900))
   configs[f'lens-time-{arm}-s{seed}']=c
 record(configs,f'Explicit equal-training-time reruns: H={H:.6f}s, median three control confirmation active times. Rerun control and strongest gap on same3 seeds; time-clock LR/caps/auxiliary schedules, finish one started update and report overshoot. Include compile/eval/checkpoint/job costs separately.')
 stage('lens-time-');confirmation_report('um-lens-time-','FW_LENS_EQUAL_TIME.md','FW-lens independently scheduled equal-time confirmation')
 record({},'FW-lens v2 stages completed. See FW_LENS_CONFIRMATION.md, FW_LENS_EQUAL_TIME.md, and detailed results. Report negative outcomes and full tuning/compute cost; no deterministic theorem validation claim.')

if __name__=='__main__':
 try:main()
 except Exception:
  subprocess.run([sys.executable,'-m','research.unnormalized_muon.queue','watch'],cwd=REPO)
  record({},'FW-lens v2 controller stopped at a failed prerequisite or50GPUh budget guard; no further stages submitted. Remaining jobs preserved/reaped. Inspect private lens-campaign.log before resuming; incomplete comparisons are not final rankings.')
  raise
