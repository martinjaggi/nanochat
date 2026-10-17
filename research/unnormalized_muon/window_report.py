"""Compact live records for the requested three-hour research window."""
import pathlib,json
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');DEST=pathlib.Path(__file__).resolve().parent


def generate():
    runs=[]
    for p in ROOT.glob('um-window-*/summary.json'):
        s=json.loads(p.read_text());c=s.get('config',{})
        if s.get('status')=='completed':runs.append((p.parent.name,c,s))
    if not runs:return []
    lines=['# Three-hour focused WD and schedule work','',
        'Requested window17 October2026,07:48:18–10:48:18UTC. One locked submission queue,one actual B300/job,max6 jobs,50B300 GPUh PROJECT TOTAL including earlier runs. No new online-controller grid: prior fresh-data promotion gate failed. First compare WD at the same LR as the pending .005 reference; later tune LR/WD interaction using only seed0 development data. Static WD0 is unconstrained; changing reciprocal-mixing WD changes the radius and retains native momentum, so it is not a fixed-domain stochastic FW theorem test.','',
        '| Run | Updates | Seed | CLI LR | Reference lambda | WD rule | Matrix schedule | Validation CE | Heldout CE | Active sec | Process sec |','|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|']
    seed0=[(n,c,ss) for n,c,ss in runs if c.get('seed')==0 and ss.get('updates')==20000 and not c.get('time_budget')]
    if seed0:
        n,c,ss=min(seed0,key=lambda x:x[2]['validation']['loss'])
        lines[4:4]=[f'**Best completed seed-0 development endpoint so far: {ss["validation"]["loss"]:.6f}CE**, `{n}`. This is a tuning result, not a new-seed or equal-time claim.','',
            'Details: [protocol](WINDOW_PROTOCOL.md), [LR/contraction curves](WINDOW_SCHEDULE_AUDIT.md), [exact saved-weight norms](WINDOW_WEIGHT_AUDIT.md), [layer-search saturation](GAP_SATURATION_AUDIT.md), [plain reciprocal follow-up](FOLLOWUP_RESULTS.md).','']
    for filename in ['WINDOW_PAIRED.md','WINDOW_EQUAL_TIME.md','WINDOW_LONG_PAIRED.md']:
        if (DEST/filename).exists():lines[4:4]=[f'Completed confirmation: [{filename}]({filename}).','']
    for n,c,s in sorted(runs):
        h=s.get('heldout');hv=f'{h["loss"]:.6f}' if h else '—'
        lines.append(f'| {n} | {s["updates"]} | {c["seed"]} | {c["matrix_lr"]:.6g} | {c["fixed_wd"]:.6g} | {c.get("wd_schedule","fixed")} | {c["matrix_schedule"]+(" cap/sign" if c.get("cap_sign") else "")} | {s["validation"]["loss"]:.6f} | {hv} | {s["training_active_seconds"]:.3f} | {s["process_seconds"]:.2f} |')
    lines+=['','Additional cheap-schedule hypothesis: reciprocal plus terminal cooldown, keeping fixed lambda. Final factors.05/.25 and fair peak LR boundaries test a terminal noise-floor explanation; no extra queries or exact FW claim. No heldout tokens select settings. If a development candidate improves by>.001CE, freeze against the tuned original-lambda reference and confirm with NEW seeds40/41/42 on NEW heldout block4; paired table in WINDOW_PAIRED.md only after all complete. No equal-time endpoint claim from token-clock prefixes. Actual group WD/contraction histories and costs are in persistent per-update logs.','',
        'Old historical plots remain intact and regenerate only when their input summaries change. Full raw logs remain outside Git; streaming publication parses only required events. Deadline guard declines new runs that cannot reasonably fit in the window; last-started jobs finish/reap normally.']
    (DEST/'WINDOW_RESULTS.md').write_text('\n'.join(lines)+'\n');return ['research/unnormalized_muon/WINDOW_RESULTS.md']
