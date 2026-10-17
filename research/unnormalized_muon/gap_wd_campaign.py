"""Run fixed-WD subtopic stages through the ONE capped submission queue."""
import copy,json,pathlib,statistics,subprocess,sys,os
from research.unnormalized_muon.queue import ROOT,REPO
D=REPO/'research/unnormalized_muon';CONFIG=D/'configs';LAM=.1837498798375862

def rows():
 out=[]
 for p in ROOT.glob('um-*/summary.json'):
  s=json.loads(p.read_text());c=s.get('config')
  if c and c.get('fixed_wd')==LAM:out.append(dict(name=p.parent.name,c=c,s=s))
 return out

def score(r):return r['s']['validation']['loss']

def stage(prefix):
 print('STAGE',prefix,'one B300/job; maximum6; aggregate50GPUh incl prior runs',flush=True)
 subprocess.run([sys.executable,'-m','research.unnormalized_muon.queue','sweep','--prefix',prefix],cwd=REPO,check=True)

def record(configs,note):
 paths=[]
 for name,c in configs.items():
  p=CONFIG/(name+'.json');body=json.dumps(c,indent=2)+'\n'
  if p.exists():assert p.read_text()==body,'never rewrite submitted configs'
  else:p.write_text(body)
  paths.append(str(p.relative_to(REPO)))
 with (D/'STATUS.md').open('a') as f:f.write('\n'+note+'\n')
 paths.append('research/unnormalized_muon/STATUS.md')
 subprocess.run(['git','add',*paths],cwd=REPO,check=True)
 if subprocess.run(['git','diff','--cached','--quiet'],cwd=REPO).returncode:subprocess.run(['git','commit','-m',note[:72]],cwd=REPO,check=True)
 push()

def push():
 subprocess.run(['git','push','origin','HEAD:unnormalized-muon'],cwd=REPO,check=True,env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes -o UserKnownHostsFile=/mloscratch/homes/mljaggi/rcp-tools/github-known-hosts'))

def check(name):
 matches=[r for r in rows() if r['name']==name];assert len(matches)==1,name+' not completed'
 r=matches[0];s=r['s'];c=r['c'];g=s.get('gap_diagnostics')
 assert s['updates']==64 and g and g['accepted_steps']>=48,'gap integration failed or excessive skips'
 assert s['extra_microbatch_forward_evals']==2*s['extra_forward_evals'],'accumulation accounting'
 points=[json.loads(x) for x in (ROOT/name/'metrics.jsonl').read_text().splitlines() if x.strip()]
 assert any(x['event']=='gap_wd_audit' for x in points),'state/RNG audit missing'
 assert all(abs(x['accumulated_fresh_loss']-y['loss'])<1e-5 for x,y in zip([x for x in points if x['event']=='gap_wd_update'],[x for x in points if x['event']=='update'])),'averaged baseline mismatch'
 return r

def pilot_configs():
 configs={}
 for schedule,label in [('cooldown','cosine'),('fw_reciprocal','reciprocal')]:
  for lr in [.02,.04,.08]:
   configs[f'gapwd-pilot-{label}-lr{lr:g}']=dict(clean=True,variant=False,decay_mode='standard',fixed_wd=LAM,matrix_lr=lr,matrix_schedule=schedule,updates=2000,seed=0,depth=8,runtime_limit=900)
 for scope,shape,label in [('layer','uniform','layer'),('joint','uniform','joint'),('joint','native','joint-native')]:
  configs[f'gapwd-pilot-{label}']=dict(clean=True,variant=False,decay_mode='standard',fixed_wd=LAM,matrix_lr=.04,updates=2000,seed=0,depth=8,runtime_limit=1800,gap_scope=scope,gap_shape=shape,gap_initial_L=.01,gap_safe_oracle=False)
 return configs

def confirmation():
 groups={}
 for r in rows():
  arm=r['c'].get('gap_confirmation_arm')
  if arm:groups.setdefault(arm,{})[r['c']['seed']]=r
 base=groups['cosine'];text=['# Fixed-WD paired confirmation','',
  'Fixed actual lambda=.1837498798375862; ordinary unmasked decay. Seed0 tuning selected settings. Seeds10/11/12 are new paired runs; final heldout tokens were reserved. Three seeds are limited evidence. Gap-step raw loss checks freeze AdamW groups; native finite NS/Nesterov make this a practical adaptation, not a theorem reproduction. All probes and compilation count toward total job cost. Curves do not constitute independently scheduled equal-time endpoints.','',
  '| Method | Seed | Tuning CE | Heldout CE | Heldout delta vs cosine | Process sec |','|---|---:|---:|---:|---:|---:|']
 for arm,rr in sorted(groups.items()):
  deltas=[]
  for seed,r in sorted(rr.items()):
   s=r['s'];b=base[seed]['s'];assert s.get('heldout') and b.get('heldout')
   def manifest(row):return json.loads((ROOT/row['name']/'metrics.jsonl').read_text().splitlines()[0])
   assert manifest(r)['initial_parameter_hash']==manifest(base[seed])['initial_parameter_hash'],'paired model mismatch'
   assert s['heldout']['validation_hash']==b['heldout']['validation_hash'],'heldout token mismatch'
   delta=s['heldout']['loss']-b['heldout']['loss'];deltas.append(delta)
   text.append(f'| {arm} | {seed} | {s["validation"]["loss"]:.6f} | {s["heldout"]["loss"]:.6f} | {delta:+.6f} | {s["process_seconds"]:.2f} |')
  assert len(deltas)==3,'incomplete confirmation'
  text+=['',f'{arm}: paired mean heldout delta {statistics.mean(deltas):+.6f}; sample standard deviation {statistics.stdev(deltas):.6f}; n=3.','']
 p=D/'FW_GAP_WD_CONFIRMATION.md';p.write_text('\n'.join(text)+'\n');subprocess.run(['git','add',str(p.relative_to(REPO))],cwd=REPO,check=True)
 subprocess.run(['git','commit','-m','Report fixed-WD gap LR paired heldout confirmation'],cwd=REPO,check=True);push()

def main():
 stage('gapwd-first-')
 check('um-gapwd-first-layer-001')
 first=[r for r in rows() if r['name']=='um-gapwd-first-layer-001'][0]['c']
 cfg={}
 for shape in ['uniform','native']:
  c=copy.deepcopy(first);c.update(gap_scope='joint',gap_shape=shape)
  cfg[f'gapwd-joint-{shape}-001']=c
 record(cfg,'Per-layer fixed-WD64-step accumulation2 and state/RNG checks passed; now separately test joint-uniform and joint-native actual LR rays. Each one B300,1800s maximum.')
 stage('gapwd-joint-')
 for shape in ['uniform','native']:check(f'um-gapwd-joint-{shape}-001')
 record(pilot_configs(),'Run nine matched65.536M-token fixed-WD pilots: per-layer/joint-uniform/joint-native gap LR, and three initial LRs EACH for cosine and shifted reciprocal. Gap arms have no calendar LR schedule. Exactly one B300/job, six-slot queue; finish earlier variable-WD screen alongside.')
 stage('gapwd-pilot-,wd-grid-')
 # Give both prescribed schedules the identical boundary rule, max two rounds.
 for round_index in range(2):
  cfg={}
  for schedule,label in [('cooldown','cosine'),('fw_reciprocal','reciprocal')]:
   g=[r for r in rows() if r['s']['updates']==2000 and not r['c'].get('gap_scope') and r['c'].get('matrix_schedule')==schedule]
   best=min(g,key=score);lrs=[r['c']['matrix_lr'] for r in g];lr=best['c']['matrix_lr']
   new=lr/2 if lr==min(lrs) else lr*2 if lr==max(lrs) else None
   if new is not None:
    c=copy.deepcopy(best['c']);c['matrix_lr']=new;cfg[f'gapwd-edge-{round_index}-{label}-lr{new:g}']=c
  if not cfg:break
  record(cfg,f'Fixed-WD initial-LR boundary expansion round{round_index}: same factor-two rule for both cosine and shifted reciprocal.')
  stage(f'gapwd-edge-{round_index}-')
 cfg={}
 for schedule,label in [('cooldown','cosine'),('fw_reciprocal','reciprocal')]:
  g=[r for r in rows() if r['s']['updates']==2000 and not r['c'].get('gap_scope') and r['c'].get('matrix_schedule')==schedule]
  for rank,r in enumerate(sorted(g,key=score)[:2]):
   c=copy.deepcopy(r['c']);c.update(updates=20000,runtime_limit=2400,heldout=False);cfg[f'gapwd-long-{label}-{rank}']=c
 for label in ['layer','joint','joint-native']:
  r=next(r for r in rows() if r['name']=='um-gapwd-pilot-'+label);c=copy.deepcopy(r['c']);c.update(updates=20000,runtime_limit=5400,heldout=False);cfg[f'gapwd-long-{label}']=c
 record(cfg,'Promote fixed-WD cosine/reciprocal best two initial LRs and all three gap scopes to fresh655M-token full-horizon runs. Native controls2400s; gap LR5400s limits from measured throughput. Same lambda/auxiliary dynamics; all probes charged.')
 stage('gapwd-long-')
 rr=[r for r in rows() if r['s']['updates']==20000 and r['c']['seed']==0 and r['name'].startswith('um-gapwd-long-')]
 selected={}
 for schedule,label in [('cooldown','cosine'),('fw_reciprocal','reciprocal')]:selected[label]=min([r for r in rr if not r['c'].get('gap_scope') and r['c'].get('matrix_schedule')==schedule],key=score)
 for label in ['layer','joint']:selected[label]=next(r for r in rr if r['name']=='um-gapwd-long-'+label)
 native=next(r for r in rr if r['name']=='um-gapwd-long-joint-native')
 if score(native)<score(selected['joint']):selected['joint-native']=native
 cfg={}
 for arm,r in selected.items():
  for seed in [10,11,12]:
   c=copy.deepcopy(r['c']);c.update(seed=seed,heldout=True,gap_confirmation_arm=arm);cfg[f'gapwd-confirm-{arm}-s{seed}']=c
 record(cfg,'Freeze fixed-WD settings using seed0 tuning only. Confirm cosine, shifted reciprocal, per-layer and joint gap LRs on NEW paired seeds10/11/12 and reserved heldout. Add shape-aware joint only if it improves on uniform. Maximum6 one-B300 jobs;30GPUh total cap remains hard.')
 stage('gapwd-confirm-');confirmation()
 record({},'Fixed-WD FW-gap LR campaign completed. See FW_GAP_WD_CONFIRMATION.md and DETAILED_EVAL.md for paired losses, actual eta/gamma, probe costs, and limitations. No theorem validation claim.')

if __name__=='__main__':
 try:main()
 except Exception:
  # No more submissions after a failure; preserve and reap remaining campaign jobs.
  subprocess.run([sys.executable,'-m','research.unnormalized_muon.queue','watch'],cwd=REPO)
  record({},'Fixed-WD staged controller stopped on a failed prerequisite or budget guard. No further stages submitted; remaining jobs preserved/reaped. Exact error is in private gapwd-campaign.log. Inspect before resuming.')
  raise
