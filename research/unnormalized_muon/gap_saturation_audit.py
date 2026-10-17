import pathlib,json,math
R=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');rows=[]
for name in ['um-lens-long-layer-cooldown','um-lens-long-layer-stable']:
 p=R/name/'metrics.jsonl';steps=matches=blocks=nonpositive=trials1=0;worst=0.
 with p.open() as f:
  for line in f:
   if not line.startswith('{"event": "gap_wd_update"'):continue
   e=json.loads(line);steps+=1;trials1+=len(e['trials'])==1
   err=[]
   for eta,b,v in zip(e['actual_etas'],e['b'],e['v']):
    expected=e['eta_cap'] if b>0 and v>0 else 0.;err.append(abs(eta-expected)/max(e['eta_cap'],1e-30));blocks+=1;nonpositive+=b<=0
   maximum=max(err);worst=max(worst,maximum);matches+=maximum<1e-12
 rows.append(dict(run=name,updates=steps,all_block_rates_equal_cap_sign_updates=matches,one_trial_updates=trials1,block_decisions=blocks,nonpositive_gap_blocks=nonpositive,max_relative_rate_discrepancy=worst))
print(json.dumps(rows,indent=2));pathlib.Path('/tmp/muon-window-audit/gap_saturation.json').write_text(json.dumps(rows,indent=2)+'\n')
