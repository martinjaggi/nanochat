"""Summarize completed development screens and the frozen confirmation cohort."""
import collections,datetime,json,pathlib,statistics
from research.unnormalized_muon.queue import ROOT,REPO,load
D=REPO/'research/unnormalized_muon'


def read(name):return json.loads((ROOT/name/'summary.json').read_text())


def generate():
 now=datetime.datetime.now(datetime.timezone.utc).isoformat();selection=json.loads((D/'WINDOW_SELECTION.json').read_text())
 rows=[('Original WD: tuned LR and terminal factor','um-window-joint-terminal-lr0p01-f0p01'),('Retuned static WD/LR','um-window-static-terminal-f0p01'),('Static contraction-matched control','um-window-static-matched-contraction'),('Reciprocal-mixing WD','um-window-joint-mixing-x2'),('Native cosine WD','um-window-joint-cosine-wd-lr0p01'),('Reciprocal LR plus cooldown','um-window-schedule-lr0p02-f0p05'),('Cheap gap-sign rule','um-window-cap-tune-x1')]
 lines=['# Three-hour Muon research continuation','',f'Updated{now}. Requested research/submission window17October2026,07:48:18–10:48:18UTC. Existing confirmations were allowed to finish after cluster recovery; no new experiments were launched after the cutoff. All runs use ONE verified B300, at most SIX outstanding requests, and the50B300-hour PROJECT TOTAL cap.','',
 '**Current conclusion: ordinary Muon hyperparameter tuning gives the best development result; none of the tested gap/preset-schedule variants earns a screen win over that stronger static control.** This is not a claim of exhaustive hyperparameter optimality or general algorithmic inferiority.','',
 'Same125,829,354-parameter dense depth8/512 model, native ClimbMix/32K tokenizer, BF16 computation/FP32 Muon masters, sequence1024,32768tokens/update, same auxiliary optimizer. Clean native direction retains Nesterov,5Polar Express iterations and Frobenius correction.20k updates=655.36M tokens (~5.21tokens/parameter).','',
 '## Completed seed0 development screen','', '| Setting | Development CE | CLI peak LR | Matrix WD | Terminal factor |','|---|---:|---:|---:|---:|']
 for label,name in rows:
  s=read(name);c=s['config'];lines.append(f'| {label} | {s["validation"]["loss"]:.6f} | {c["matrix_lr"]:.6g} | {c["fixed_wd"]:.6g}'+(' peak' if c.get('wd_schedule','fixed')!='fixed' else '')+f' | {c.get("reciprocal_final_factor",c.get("matrix_final_factor",.05)):.4g} |')
 lines+=['','Matrix CLI LR times.25 is actual eta; shape is inside Q. The selected static setting uses ordinary unmasked fixed WD, not cautious decay or gap adaptation. [Exact frozen settings](WINDOW_SELECTION.json), [grid and provenance](WINDOW_STATIC_GRID.md), [refinement batch including deferrals](WINDOW_REFINEMENT_SELECTION.json). Lower matrix WD and terminal-factor refinement materially strengthen the control.','',
 '## New paired confirmation','']
 names=[f'um-window-confirm-{arm}-s{seed}' for seed in [40,41,42] for arm in ['reference','candidate']];state=load()
 complete=all((ROOT/n/'summary.json').exists() and state[n].get('status')=='completed' for n in names)
 if complete:
  lines+=['Settings were frozen before NEW seeds40/41/42, with a previously reserved262144-token heldout block4. Initial parameter and heldout-token hashes match within every pair. Three seeds are limited evidence.','', '| Seed | Reference heldout CE | Retuned static heldout CE | Delta | Reference active sec | Retuned active sec |','|---|---:|---:|---:|---:|---:|'];ds=[]
  for seed in [40,41,42]:
   a=read(f'um-window-confirm-reference-s{seed}');b=read(f'um-window-confirm-candidate-s{seed}');assert a['heldout']['validation_hash']==b['heldout']['validation_hash'];d=b['heldout']['loss']-a['heldout']['loss'];ds.append(d)
   lines.append(f'| {seed} | {a["heldout"]["loss"]:.6f} | {b["heldout"]["loss"]:.6f} | {d:+.6f} | {a["training_active_seconds"]:.2f} | {b["training_active_seconds"]:.2f} |')
  lines+=['',f'Paired retuned-minus-reference heldout delta: mean **{statistics.mean(ds):+.6f}CE**, sample SD **{statistics.stdev(ds):.6f}**, n=3. This tests a simpler static recipe; it is not evidence for a new gap algorithm.','', '[Complete paired report](WINDOW_PAIRED.md).']
  if all('bpb' in summaries['heldout'] for summaries in [read(n) for n in names]):
   lines+=['','| Seed | Reference BPB | Retuned BPB |','|---|---:|---:|']
   for seed in [40,41,42]:
    a=read(f'um-window-confirm-reference-s{seed}');b=read(f'um-window-confirm-candidate-s{seed}');lines.append(f'| {seed} | {a["heldout"]["bpb"]:.6f} | {b["heldout"]["bpb"]:.6f} |')
  if (D/'WINDOW_CONFIRMATION_CURVES.png').exists():lines+=['','![Frozen confirmation curves and heldout deltas](WINDOW_CONFIRMATION_CURVES.png)']
 else:lines+=['The six frozen confirmation requests are still pending/running or incomplete. No partial group is called a three-seed confirmation. [Live confirmation state](CONFIRMATION_STATE.md).']
 lines+=['','**Independent equal-training-time reruns were not launched in this window.** A Run:ai admission TLS/controller outage delayed these existing requests before GPU allocation. Token-clock time curves are descriptive and are not independently matched equal-time endpoints. No practical equal-time superiority is claimed for the new static settings.','',
 '## Other evidence and limits','',
 '* Plain reciprocal lost all3NEW paired seeds20/21/22 after fair LR retuning: mean heldout delta+0.044014CE, sample SD.003379, versus the original-WD control with terminal fraction.05. This cohort/reference differs from the final40-series cohort. [Full follow-up](FOLLOWUP_RESULTS.md). Earlier wins against a weaker LR control remain explicitly labelled.\n* The cheap sign rule loses at its best tested LR; after index1000 all skips occur in tiny value-embedding gates. This tested cheap replacement showed no useful screen gain; long Armijo rates largely saturated their caps. [Cap/sign results](CAP_SIGN_RESULTS.md), [long Armijo saturation audit](GAP_SATURATION_AUDIT.md).\n* The fresh-fit controller gate failed7/12 against required8/12, so no new online-controller sweep was launched. [Diagnosis](FRESH_DIAGNOSIS.md).\n* Matching final contraction does not match decay history or weight norms. Changing WD changes the domain; exact FP64 spectral analysis found an early mixing-WD setting outside its final ball. [LR/contraction audit](WINDOW_SCHEDULE_AUDIT.md), [saved-weight audit](WINDOW_WEIGHT_AUDIT.md). Finite NS/Nesterov/BF16 do not validate an exact-FW theorem.', '',
 '## Cost and operational record','']
 counters=collections.Counter(v.get('status','outstanding') for v in state.values());charged=sum(v.get('gpu_seconds',0.) for v in state.values());reserved=sum(v['seconds']+30 for v in state.values() if not v['recorded']);waiting=sum(max(0.,v.get('allocation_start',v['submitted'])-v['submitted']) for n,v in state.items() if n in names)
 lines +=[f'Project ledger: **{charged/3600:.3f}B300 request-hours conservatively charged**, plus{reserved/3600:.3f}reserved. Charge includes queue/startup/cleanup and therefore upper-bounds actual GPU occupancy. The final6requests accumulated{waiting/3600:.3f}summed request-hours BEFORE GPU assignment; that waiting consumed no GPU. Job states:{dict(counters)}. All prior/failed jobs remain included.','',
 'GPU check001 failed an import-order guard before training; fixed check002 passed native/cap checks and64updates. A controller empty-commit resume issue was fixed without losing training. The first confirmation admission was rejected by a server-side webhook certificate error; normal retry succeeded, but controller/scheduler recovery delayed allocation. No TLS bypass, alternate GPU type, or unrelated-job cancellation was used. The queue now reserves TrainingWorkloads before legacy jobs exist and starts runtime enforcement at pod assignment; five focused queue-state checks pass alongside54optimizer/math CPU checks.','',
 'Exact code/configs/results are pushed to `martinjaggi/nanochat:unnormalized-muon`; [minimal changes and reproduction](README.md), [machine-readable ledger](EXPERIMENTS.csv). Raw logs, data and checkpoints stay under `/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/<run_id>/`. The persistent monitor only finishes/records/deletes already accepted requests, with no new submissions.','',
 ('Recommendation: use the retuned ordinary-Muon setting as the token-matched control, provisionally; all three paired seeds improve. ' if complete and all(x<0 for x in ds) else 'Recommendation: retain the new setting as provisional development evidence pending stronger confirmation. ')+'Preserve the negative gap/controller results. A longer-horizon retune and independent full equal-time reruns remain follow-up work, not completed evidence.']
 p=D/'THREE_HOUR_REPORT.md';p.write_text('\n'.join(lines)+'\n');return p

if __name__=='__main__':print(generate())
