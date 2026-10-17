"""Saved-weight diagnostics only: Frobenius norms and spectral lower bounds."""
import torch,pathlib,json,math
R=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');out=pathlib.Path('/tmp/muon-window-audit');out.mkdir(exist_ok=True)
names=['um-follow-first-tune-control-lr0p01','um-follow-mid-reciprocal-high','um-window-schedule-lr0p02-f0p05','um-window-first-wd-mixing','um-window-first-wd-static-product']
allrows=[]
with torch.no_grad():
 for name in names:
  p=R/name
  if not (p/'summary.json').exists():continue
  s=json.loads((p/'summary.json').read_text());m=json.loads((p/'metrics.jsonl').open().readline());state=torch.load(p/'store/base_checkpoints/d8/model_020000.pt',map_location='cpu',weights_only=True,mmap=True)
  rows=[]
  with (p/'metrics.jsonl').open('rb') as stream:
   stream.seek(max(0,(p/'metrics.jsonl').stat().st_size-100000));tail=stream.read().splitlines()
  last=next(json.loads(x) for x in reversed(tail) if b'\"event\": \"update\"' in x)
  for group_index,g in enumerate(m['optimizer_groups']):
   if g['kind']!='muon':continue
   for n in g['names']:
    w=state[n].float();c=math.sqrt(max(1,w.shape[-2]/w.shape[-1]));lam=s['config']['fixed_wd']
    gen=torch.Generator().manual_seed(42);v=torch.randn(w.shape[-1],generator=gen);v/=v.norm()
    for _ in range(50):
     u=w@v;u/=u.norm().clamp_min(1e-30);v=w.T@u;v/=v.norm().clamp_min(1e-30)
    power=float((w@v).norm());frob=float(w.norm());exact=float(torch.linalg.matrix_norm(w.double(),ord=2))
    rows.append(dict(name=n,spectral_svd=exact,spectral_svd_over_final_radius=exact*last['group_weight_decays'][group_index]/c,frobenius=frob,spectral_lower_estimate=power,nominal_radius=c/lam if lam else None,spectral_lower_over_radius=power*lam/c,final_wd=last['group_weight_decays'][group_index],spectral_lower_over_final_radius=power*last['group_weight_decays'][group_index]/c))
  allrows.append(dict(run=name,validation=s['validation']['loss'],global_matrix_frobenius=math.sqrt(sum(x['frobenius']**2 for x in rows)),max_spectral_lower_over_reference_radius=max(x['spectral_lower_over_radius'] for x in rows),max_spectral_svd_over_final_radius=max(x['spectral_svd_over_final_radius'] for x in rows),max_spectral_lower_over_final_radius=max(x['spectral_lower_over_final_radius'] for x in rows),matrices=rows))
  print(name,allrows[-1]['global_matrix_frobenius'],allrows[-1]['max_spectral_svd_over_final_radius'],flush=True)
(out/'weights.json').write_text(json.dumps(allrows,indent=2)+'\n')
