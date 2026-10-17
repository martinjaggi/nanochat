# Muon experiments on the B300 nanochat fork

Live evidence: [current results](WINDOW_RESULTS.md), [frozen continuation protocol](WINDOW_PROTOCOL.md), [final refinement settings](WINDOW_REFINEMENT_SELECTION.json), [full run ledger](EXPERIMENTS.csv). The three-hour continuation ends17October2026 at10:48:18UTC. Reports distinguish seed0 development screening from paired heldout and independent equal-time confirmation.

The source is Martin Jaggi's nanochat B300 fork, base `b2bdf9890e028965ee7f2e97acc02d72b3c663ec`. Branch `unnormalized-muon` pushes to `martinjaggi/nanochat`. Original data/tokenizer are ClimbMix/32K; no Atlas. Dense depth8/width512 has125,829,354 parameters, including25,166,016 native Muon parameters in52 matrices. Context1024, device batch32, accumulation1,32768 update-data tokens.20k updates=655.36M tokens (~5.21tokens/parameter). One actualB300 per run, at most6outstanding,50B300 GPU-hours PROJECT TOTAL including earlier/failed runs.

## Minimal algorithm changes and conventions

* [nanochat/optim.py](../../nanochat/optim.py): opt-in unnormalization multiplies the existing NS/Frobenius direction by the nonnegative FP32 inner product of the actual PRE-normalization NS input M with that direction. Native momentum/Nesterov is retained. With momentum this is `<M,NS(M)>`, not raw-gradient alignment. The scalar is formed BEFORE shape scaling, then shape is applied once. This is a separate arm from FW gap adaptation.
* The clean flag disables row equilibration and NorMuon, retaining native Nesterov,5 Polar Express iterations and Frobenius renormalization. Native defaults remain available when flags are off. Standard WD is unmasked; cautious coordinate masks are a separately labelled earlier experiment.
* Q includes shape c=sqrt(max(1,out/in)). Canonical matrix update is `W -= eta*(Q+lambda*W)`. The fused kernel receives LR `eta*c`, WD `lambda/c`, so contraction is `1-eta*lambda`. CLI matrix LR times.25 is actual eta for this batch. Muon matrix parameters and direction arithmetic after NS casting retain native FP32 masters; forward/backward use native BF16. NS internally uses BF16. Auxiliary groups retain their native precision/AdamW recipe.
* [gap_wd.py](gap_wd.py) prepares momentum/vertices once and uses CURRENT raw G for b=`<G,Q+lambda*W>`. Joint quadratic backtracking and layer proposals with ONE combined Armijo check are distinct modes. All retries hold the direction and auxiliary parameters fixed. The layer Armijo carried scalar L is a proposal parameter, not measured smoothness. No extra L2 penalty is inserted into trial loss.
* The cap/sign extension in the native fused optimizer saves raw G before native Nesterov mutates stacked gradients. It uses `eta_l=eta_base*I(<G,Q+lambda*W>>0)`, skipping BOTH direction and ordinary decay while advancing native momentum once. No trial losses or extra gradients. [Long-screen result](CAP_SIGN_RESULTS.md): no useful gain; rare skips mostly affect tiny value-embedding gates.
* [cooldown_schedule.py](cooldown_schedule.py), [protocol_math.py](protocol_math.py), and [fresh_math.py](fresh_math.py) define prescribed matrix LR/WD shapes. Matrix-only terminal refinements preserve auxiliary and momentum schedules. Reciprocal plus cooldown, reciprocal-mixing WD and native cosine WD are explicitly named preset schedules, not all adaptive gap methods. Changing WD changes the implied radius; fixed-domain FW guarantees are not claimed.

## Evaluation and state

[run.py](run.py) calls the existing `scripts.base_train` entry point; [record.py](record.py) records actual group rates/WD, active-time and job-cost breakdowns. Three discarded GPU warmup updates are followed by model/optimizer/data/RNG reset. Validation uses262144 fixed target tokens; hashes are checked in paired comparisons. Selection uses seed0 development block0 only. New seeds40/41/42 use previously reserved block4 after settings freeze. Equal-time runs are separate reruns with all schedules driven by shared active-time fraction, not prefixes of token-clock curves.

[fw.py](fw.py) uses functional candidate evaluation and accumulated token-weighted baseline loss, fixing the last-microbatch-only acceptance bug. [fresh_state.py](fresh_state.py) saves exact branch state, named momentum, RNG, cursor and prefetched inputs. Native-to-wrapper momentum and update parity, probe/restore state ownership, finite differences and accumulation checks are documented in [fresh diagnosis](FRESH_DIAGNOSIS.md). Its fresh-fit promotion gate failed; no new fresh-fit controller sweep was launched.

Current checks:54optimizer/math CPU analytic/regression checks plus5queue-state checks passed; cap/sign integration job002 passed native and cap/import checks plus64B300 updates and per-matrix gated-rate/decay accounting. Failed check001 (import-order guard, before training) remains in the ledger with its cost. Compiled default optimizer regression is checked against the archived base; exact spectral SVD diagnostics on saved weights require no new model evaluations.

## Evidence and reproducibility

* [Fair long-horizon follow-up](FOLLOWUP_RESULTS.md): plain reciprocal loses on all3NEW paired seeds after retuning the control; old weaker-control wins remain reported and labelled.
* [Cap/sign and Armijo saturation](GAP_SATURATION_AUDIT.md), [cap/sign loss screen](CAP_SIGN_RESULTS.md).
* [LR and contraction audit](WINDOW_SCHEDULE_AUDIT.md), [exact saved-weight spectral/norm audit](WINDOW_WEIGHT_AUDIT.md), [exact-config reuse map](WINDOW_REUSE.json).
* Paired and time reports are linked from current results only after complete groups. Three seeds are limited evidence; development screens alone do not establish method superiority.

Every scheduler job archives its exact source/base commits and config under `/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/<run_id>/`. Checkpoints, datasets, raw per-update logs and credentials stay outside Git. One locked queue in `queue.py` enforces hardware/resource/deadline guards; `work_window.py` records the staged gates and immutable refinement batch. CPU development is for implementation/analytic and saved-output analysis; all training runs in scheduled one-B300 jobs.

Cluster recovery: six frozen confirmations were accepted but stalled before GPU assignment. `monitor_confirmation.py` monitors ONLY these existing requests, publishes a complete paired report if all succeed, and submits NO new experiments. The queue counts TrainingWorkloads even when legacy RunaiJobs are absent. GPU runtime starts at observed node assignment, with a1hour unallocated-request expiry; it does not consume the runtime allowance while waiting for the controller.

Additional review links: [static LR/WD grid](WINDOW_STATIC_GRID.md), [delayed confirmation state](CONFIRMATION_STATE.md).
