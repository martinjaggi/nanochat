"""Reproduce long cap/sign loss and parameter-weighted gating diagnostics."""
import pathlib,json,math,collections
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
DEST=pathlib.Path('/tmp/muon-window-audit')
PAIRS=[('um-window-cap-tune-x0p5','um-follow-edge0-control-lr0p005'),('um-window-cap-tune-x1','um-follow-first-tune-control-lr0p01'),('um-window-cap-tune-x2','um-follow-first-tune-control-lr0p02')]
rows=[]
for a,b in PAIRS:
 s=json.loads((ROOT/a/'summary.json').read_text());r=json.loads((ROOT/b/'summary.json').read_text())
 m=json.loads((ROOT/a/'metrics.jsonl').open().readline());other=json.loads((ROOT/b/'metrics.jsonl').open().readline())
 assert m['initial_parameter_hash']==other['initial_parameter_hash']
 assert s['validation']['validation_hash']==r['validation']['validation_hash']
 rows.append(dict(run=a,reference=b,lr=s['config']['matrix_lr'],ce=s['validation']['loss'],reference_ce=r['validation']['loss'],delta=s['validation']['loss']-r['validation']['loss'],active_ratio=s['training_active_seconds']/r['training_active_seconds'],skipped=s['cap_sign_statistics']['skipped'],total=s['cap_sign_statistics']['total']))
p=ROOT/'um-window-cap-tune-x1/metrics.jsonl';counts=collections.Counter();late=collections.Counter();updates=0
with p.open() as f:
 for line in f:
  if line.startswith('{"event": "manifest"'):
   m=json.loads(line);groups=[x for x in m['optimizer_groups'] if x['kind']=='muon']
  elif line.startswith('{"event": "update"'):
   x=json.loads(line);updates+=1
   for group,mask in zip(groups,x['cap_sign_gates']):
    for n,on in zip(group['names'],mask):
     if not on:counts[n]+=1;late[n]+=int(x['step']>=1000)
numel={n:math.prod(shape) for g in groups for n,shape in zip(g['names'],g['shapes'])};params=sum(numel.values())
detail=dict(matrix_parameters=params,updates=updates,skipped=dict(counts),skipped_after1000=dict(late),weighted_skipped_fraction=sum(numel[n]*c for n,c in counts.items())/(updates*params),late_weighted_skipped_fraction=sum(numel[n]*c for n,c in late.items())/((updates-1000)*params))
assert sum(counts.values())==rows[1]['skipped']
text=['# Cheap complete-gap sign gate: long screen','', 'Three full20k-update seed0 runs, same52 native Muon matrices, ordinary fixed lambda=.1837498798375862, clean native direction and auxiliary recipe. Initial parameter and validation-token hashes match each corresponding control. Actual eta=CLI*.25; both controls and sign gate use original terminal fraction.05. Best LR is interior to this tested grid. No extra model forward/backward evaluations.','', '| Peak CLI LR | Native CE | Cap/sign CE | Delta | Observed active-time ratio | Skipped matrix updates |','|---|---:|---:|---:|---:|---:|']
for x in rows:text.append(f'| {x["lr"]:.6g} | {x["reference_ce"]:.6f} | {x["ce"]:.6f} | {x["delta"]:+.6f} | {x["active_ratio"]:.3f} | {x["skipped"]}/{x["total"]} |')
text+=['','Best cap/sign CE3.114210 is worse than matching native3.112087; refined native terminal-factor control is stronger still at3.104185. This seed0 screen does not support promoting cap/sign to a large confirmation. Active ratios are observed across different scheduled runs/hardware placements, not independently matched equal-time endpoints.','', f'At central LR, {sum(counts.values())} block decisions skip ({sum(counts.values())/(52*updates):.6%}), but parameter-weighted skipped fraction is only{detail["weighted_skipped_fraction"]:.6%}. Four tiny48-parameter `attn.ve_gate.weight` matrices account for{sum(c for n,c in counts.items() if "ve_gate" in n)/sum(counts.values()):.2%} of skips. All{sum(late.values())} skips after optimizer index1000 occur in these tiny gates; their parameter-weighted fraction over remaining updates is{detail["late_weighted_skipped_fraction"]:.8%}. Most large-matrix steps therefore remain ordinary scheduled Muon.','', 'This supports the prior cap/sign saturation diagnosis while finding no useful development-validation gain for the cheap replacement. The old Armijo method matched cap/sign rates after startup, but counterfactual trajectories and rounding need not match. Retain the negative result; do not add a fresh-fit controller grid after its failed gate.','', 'Reproduce with `python research/unnormalized_muon/cap_sign_report.py`; outputs go to `/tmp/muon-window-audit`. All raw logs remain outside Git.']
DEST.mkdir(exist_ok=True);(DEST/'CAP_SIGN_RESULTS.md').write_text('\n'.join(text)+'\n');(DEST/'cap_sign_audit.json').write_text(json.dumps(dict(rows=rows,detail=detail),indent=2)+'\n');print('\n'.join(text))
