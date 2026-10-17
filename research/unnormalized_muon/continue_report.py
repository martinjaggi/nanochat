"""Live long-horizon LR fairness and paired reciprocal follow-up evidence."""
import json,pathlib,statistics
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');DEST=pathlib.Path(__file__).resolve().parent


def generate():
    runs=[]
    for p in ROOT.glob('um-follow-*/summary.json'):
        s=json.loads(p.read_text());c=s.get('config',{})
        if s.get('status')=='completed':runs.append((p.parent.name,c,s))
    if not runs:return []
    lines=['# Reciprocal follow-up: long-horizon fairness and equal time','',
        'The earlier campaign COMPLETED. Same-batch gap searches lost at655M tokens and equal time. The fresh-data gate failed7/12 versus8/12, so online-controller expansion remains stopped. A cheap fixed-WD reciprocal schedule improved three original paired seeds, motivating this follow-up; settings here use seed0 development losses only. The old long-horizon control preferred its lower tested LR, so extend its range fairly before claiming superiority.','',
        'All runs: one verified B300, dense125,829,354-parameter depth8/512, ClimbMix/32K tokenizer,32768 tokens/update, fixed ordinary lambda=.1837498798375862, native Nesterov/NS/Frobenius, no row equilibration or NorMuon. Shape stays inside Q. Same auxiliary recipe. Three seeds are limited evidence.','',
        'First complete the missing reciprocal equal-time endpoints on the ORIGINAL frozen settings/seeds10/11/12. Then extend/control BOTH peak-LR searches at20k updates, using the same factor-two edge rule and geometric refinements. Freeze before NEW seeds20/21/22 and NEW disjoint heldout block2. All timed schedules, including matrix reciprocal, use active-time fraction*reference horizon. Time-budget reruns finish the last update; overhead and overshoot are recorded.','',
        '| Run | Updates | Schedule | Peak CLI LR | Seed | Val CE | Heldout CE | Heldout block | Active sec | Process sec | Overshoot sec |','|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for n,c,s in sorted(runs):
        h=s.get('heldout');hv=f'{h["loss"]:.6f}' if h else '—';block=h.get('block_index',1) if h else '—'
        lines.append(f'| {n} | {s["updates"]} | {c["matrix_schedule"]} | {c["matrix_lr"]:.6g} | {c["seed"]} | {s["validation"]["loss"]:.6f} | {hv} | {block} | {s["training_active_seconds"]:.3f} | {s["process_seconds"]:.2f} | {s.get("time_overshoot",0):.5f} |')
    lines+=['','## Paired held-out endpoints','',
        '| Comparison | Seed | Reciprocal minus control CE | Control updates | Reciprocal updates |','|---|---:|---:|---:|---:|']
    specs=[('original-frozen equal time','um-lens-time-control-s','um-follow-first-time-reciprocal-s',[10,11,12])]
    for horizon,seeds in [(20000,[20,21,22]),(40000,[30,31,32])]:
        for kind in ['confirm','time']:
            prefix=f'um-follow-{kind}{horizon}-';specs.append((f'{horizon} {kind}',prefix+'control-s',prefix+'reciprocal-s',seeds))
    for label,cp,rp,seeds in specs:
        ds=[]
        for seed in seeds:
            a=ROOT/f'{cp}{seed}/summary.json';b=ROOT/f'{rp}{seed}/summary.json'
            if not(a.exists() and b.exists()):continue
            sa,sb=json.loads(a.read_text()),json.loads(b.read_text());ha,hb=sa.get('heldout'),sb.get('heldout')
            if not(ha and hb):continue
            assert ha['validation_hash']==hb['validation_hash'],'mismatched heldout tokens'
            delta=hb['loss']-ha['loss'];ds.append(delta)
            lines.append(f'| {label} | {seed} | {delta:+.6f} | {sa["updates"]} | {sb["updates"]} |')
        if len(ds)==3:lines+=['',f'{label}: paired deltas mean {statistics.mean(ds):+.6f}, sample SD {statistics.stdev(ds):.6f}; n=3.','']
        elif ds:lines+=['',f'{label}: incomplete ({len(ds)}/3), no final ranking.','']
    lines+=['','Scale-up gate: only if fresh20k seeds all improve and mean delta<-.003 CE, tune BOTH families again at40k updates (1.31B tokens), then freeze for NEW seeds30/31/32 and NEW heldout block3, with independent equal-time reruns. Otherwise stop scale-up. Larger horizons and extra tuning are reported as follow-up research, not retroactive confirmation of earlier heldout results.','',
        'Job cost includes compilation, validation, warmup, snapshots and checkpoint I/O. Training-active time excludes separately measured one-time/evaluation overhead. No attempt is made to spend the full50GPUh allowance.']
    (DEST/'FOLLOWUP_RESULTS.md').write_text('\n'.join(lines)+'\n');return ['research/unnormalized_muon/FOLLOWUP_RESULTS.md']
