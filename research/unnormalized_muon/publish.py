"""Commit small result tables and plots, never logs/checkpoints/data/credentials."""
import json,os,pathlib,subprocess
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
REPO=pathlib.Path(__file__).resolve().parents[2]
DEST=REPO/'research/unnormalized_muon'
def publish():
 runs=[]
 for path in ROOT.glob('um-*/**/summary.json'):
  if '/source/' in str(path) or '/base/' in str(path):continue
  s=json.loads(path.read_text());cfg=s.get('config')
  if cfg is None:
   p=path.parent/'resolved_config.json'
   if not p.exists():continue
   cfg=json.loads(p.read_text())
  arm='FW backtracking' if cfg.get('fw') else ('Unnormalized '+cfg.get('matrix_schedule','cooldown') if cfg['variant'] else 'Native cooldown')
  if cfg.get('clean'):arm='Clean '+arm
  label=str(path.parent.relative_to(ROOT));runs.append((label,arm,cfg,s,path))
 rows=['# Live unnormalized-Muon results','',
  'One B300 per job. CE is token cross-entropy (nats); lower is better. Rows with different update budgets are not endpoint comparisons. Tuning uses the same fixed validation tokens; held-out scores appear only on final runs. Runtime includes compilation and overhead in process seconds.','',
  '| Run | Method | Updates | Seed | CLI matrix LR | Val CE | Val BPB | Heldout CE | Process sec |',
  '|---|---|---:|---:|---:|---:|---:|---:|---:|']
 for name,arm,c,s,p in sorted(runs):
  held=s.get('heldout');hv=f'{held["loss"]:.6f}' if held else '—'
  rows.append(f'| {name} | {arm} | {s["updates"]} | {c["seed"]} | {c["matrix_lr"]:g} | {s["validation"]["loss"]:.6f} | {s["validation"]["bpb"]:.6f} | {hv} | {s.get("process_seconds",s["end_to_end_seconds"]):.2f} |')
 state=json.loads((ROOT/'queue.json').read_text());charged=sum(v.get('gpu_seconds',v['seconds']+30) for v in state.values())/3600
 for review in ROOT.glob('um-*/review.json'):
  x=json.loads(review.read_text());rows+=['',f'Review of {review.parent.name}: {x["reason"]}']
 rows+=['',f'Conservative charged/reserved total: {charged:.4f} / 10 B300 GPU-hours. Includes prior smoke/failed attempts and current maximum-duration reservations. Three-slot central queue; one B300 per run.','',
  'Current CLEAN comparison: no row equilibration, NorMuon, or Muon decay in either arm. Same five Polar Express steps and Frobenius correction; scale by the per-matrix nonnegative FP32 inner product of the native Nesterov input with the NS/Frobenius direction. Shape scaling occurs once outside the scalar. Legacy rows retain production extras and must be compared separately. Constant schedule changes only matrix LR; auxiliary schedules and momentum remain matched.','',
  'FW is a separate fixed-spectral-ball method with shared mixing, same-batch backtracking, frozen auxiliary weights during checks, and no extra matrix decay. Its extra candidate forwards count toward wall time and are logged.']
 (DEST/'RESULTS.md').write_text('\n'.join(rows)+'\n')
 if runs:
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  fig,ax=plt.subplots(figsize=(8,4.5))
  for name,arm,c,s,p in runs:
   if s['updates']<1000:continue
   points=[json.loads(x) for x in (p.parent/'metrics.jsonl').read_text().splitlines() if x.strip()]
   points=[x for x in points if x['event']=='validation' and x['label']=='tuning' and x['step']>0]
   ax.plot([x['step']*32768 for x in points],[x['loss'] for x in points],marker='.',label=f'{arm} lr{c["matrix_lr"]:g}, n{s["updates"]}, seed{c["seed"]}')
  ax.set_xlabel('Fresh training tokens');ax.set_ylabel('Validation CE (nats)');ax.grid(alpha=.2)
  if ax.lines:ax.legend(fontsize=6)
  fig.tight_layout();fig.savefig(DEST/'validation_vs_tokens.png',dpi=140);plt.close(fig)
 paths=['research/unnormalized_muon/EXPERIMENTS.csv','research/unnormalized_muon/STATUS.md','research/unnormalized_muon/RESULTS.md']
 if (DEST/'validation_vs_tokens.png').exists():paths.append('research/unnormalized_muon/validation_vs_tokens.png')
 subprocess.run(['git','add',*paths],cwd=REPO,check=True)
 if subprocess.run(['git','diff','--cached','--quiet'],cwd=REPO).returncode:
  subprocess.run(['git','commit','-m','Update live Muon experiment results'],cwd=REPO,check=True)
 subprocess.run(['git','push','origin','HEAD:unnormalized-muon'],cwd=REPO,check=True,env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes -o UserKnownHostsFile=/tmp/nanochat-github-known-hosts'))
if __name__=='__main__':publish()
