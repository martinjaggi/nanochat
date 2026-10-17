# Early reciprocal allocation: two-hour experiment report

17 October 2026. Completed within the requested 11:53–13:53 UTC window. All code, configurations and results are pushed to `martinjaggi/nanochat:unnormalized-muon`.

**Retain the tuned plateau-plus-cooldown baseline. Neither tested reciprocal early curve shows a reliable endpoint improvement.** This result concerns this small controlled family; it does not rule out other reciprocal schedules or training horizons.

## Six paired seeds

Every full run uses 20,000 updates and 655.36 million fresh tokens. Ordinary WD stays fixed at 0.04593746995939655. Only the matrix warmup and early plateau change; the complete late 65% cooldown is identical. Negative CE deltas favor the variant. SD is the sample standard deviation across paired seeds.

| Early peak | Tau, updates after warmup | Original 262k heldout: mean delta / SD | Untouched 2M heldout: mean delta / SD | Seeds |
|---|---:|---:|---:|---:|
| 1× baseline | infinity | reference | reference | 6 |
| 1.5× | 13,920 | +0.001538 / 0.002366 | +0.000718 / 0.002512 | 6 |
| 2× | 6,960 | +0.000727 / 0.003945 | +0.000659 / 0.002864 | 6 |

Seed-0 development CE was 3.090447664 for baseline, 3.089904308 for 1.5×, and 3.089890957 for 2×. We froze 2× from this screen and retained the nearly tied 1.5× as a secondary comparison before any fresh heldout endpoint. Seeds 70–72 were followed by a balanced replication of all three frozen curves on seeds 80–82. The extension followed an ambiguous initial result, so the pooled six-seed estimates are descriptive, without a fixed-sample significance claim. Seeds change initialization; the native deterministic data stream is retained.

The baseline repeat differed from its earlier endpoint by +0.000907 CE despite identical initial parameters, LR/WD inputs and data cursors. The first training-loss discrepancy was about 1e-6 at update 11. Compiled BF16 training was not bitwise reproducible across these jobs; no optimizer, model or data-recipe change was found. The tiny single-run screen differences did not identify a stable optimum.

[Every seed and both cohorts](EARLY_ALLOCATION_REPLICATION.md). [All 30 original and larger heldout scores](EARLY_ALLOCATION_LARGE_HELDOUT.md).

![Frozen family: curves and paired endpoints](EARLY_ALLOCATION_REPLICATION.png)

## Contraction controls

The scheduled contraction product is 0.044527729 for baseline, 0.031427187 for 1.5×, and 0.023892497 for 2×. Matching uses the actual matrix LR, including native batch scaling. Executed logs verify these products.

| Comparison | Original heldout mean delta | Larger heldout mean delta | Seeds |
|---|---:|---:|---:|
| 2× vs baseline LR with WD 0.05512714 | +0.000466 | +0.000072 | 3 |
| 1.5× vs baseline LR with WD 0.05108095 | +0.001576 | +0.000169 | 3 |
| 2× with WD 0.03827981 vs original baseline | +0.001475 | +0.001493 | 3 |
| 2× with entire contraction history matched vs original baseline | +0.003186 | +0.003182 | 3 |

No matched comparison shows a consistent advantage. Equal final products do not imply equal decay histories. The stronger history diagnostic sets

`lambda_t = lambda_base * eta_base(t) / eta_early(t)`.

This preserves every scheduled contraction coefficient. WD rises linearly during the reciprocal phase and equals baseline afterwards. Its implied FW radius changes, so this is an empirical diagnostic rather than fixed-domain FW.

Early validation gains fade during the common late cooldown. The history diagnostic also fails the predeclared promotion gate: its seed-0 development CE, 3.090945959, is worse than baseline, and heldout signs are mixed. **No new independent equal-time reruns were launched.** Token-clock curves against seconds are descriptive, not matched equal-time endpoints.

[All control results](EARLY_ALLOCATION_RESULTS.md). [Exact protocol and schedule geometry](EARLY_ALLOCATION_PROTOCOL.md).

![LR, WD and contraction controls](EARLY_ALLOCATION_CONTROLS.png)

## Minimal changes and frozen recipe

The source fork base is `b2bdf9890e028965ee7f2e97acc02d72b3c663ec`. The first schedule implementation is `55c6753066901695dd5fbe81304510c0d130f887`. **This continuation does not change the optimizer direction kernels.**

- [early_reciprocal](cooldown_schedule.py) and one matrix-only branch in [base_train.py](../../scripts/base_train.py) implement the schedule. [run.py](run.py) forwards the peak multiplier.
- After warmup, `s = t - 40`, `T = 6960`, `eta = 0.005*k/(1+s/tau)`, and `tau = T/(k-1)`. Warmup reaches `k*0.005`. At update 7,000 the rate is exactly 0.005. From that point the original cooldown function is called directly. The last realized rate is 0.00005038076923. Tau is independent of WD.
- The history diagnostic adds a separate WD hook. Parameter directions and auxiliary updates remain unchanged.
- Dense depth 8, width 512, four heads, context 1,024; 125,829,354 total parameters and 25,166,016 Muon parameters in 52 native matrices. Device batch 32, accumulation one: 32,768 fresh tokens/update, or 5.2083 tokens per total parameter per run.
- Native ClimbMix, BOS packing and 32k tokenizer; no Atlas assets. Native BF16 computation/embedding storage and FP32 Muon parameters/momentum; FP8 disabled.
- Clean normalized Muon retains native Nesterov, five Polar Express iterations and Frobenius correction. Row equilibration and NorMuon are disabled. Shape factors stay inside the direction; ordinary unmasked WD is used.
- CLI LR 0.02 gives actual join LR 0.005. Baseline WD is 0.04593746995939655. There are 40 warmup updates and a final 65% linear matrix cooldown to 0.01 of the join rate. Auxiliary AdamW schedules and native momentum, 0.85 → 0.97 → 0.90, are unchanged.

## Checks and reproducibility

- 67 CPU optimizer, math and queue checks passed, plus two focused concurrent-push checks. Four GPU-only checks were skipped on the CPU development pod. The B300 integration check covers 128 updates and all schedule phases; maximum error in `eta*lambda` is 5.42e-20.
- [The full execution audit](EARLY_ALLOCATION_EXECUTION_AUDIT.json) passes for 36 full runs and 720,000 updates: native parameter partition, paired initial hashes, intended LR/WD, unchanged auxiliary schedules/data cursors, fixed validation hashes, gradient counts and contraction exposure.
- All 30 frozen checkpoints reproduce both original CE and BPB scores **exactly**, with identical data hashes, before larger scoring. The allowed tolerance was 1e-5. Cached validation batches are cloned because the loader reuses buffers; validation epoch one prevents wrapping.
- Larger scoring uses 2,097,152 targets at native validation batch positions 64–127, disjoint from prior blocks 0–7. It never selects LR or WD settings. Per-sequence nats/counts stay outside Git; packed sequences are not assumed independent.
- Finite NS, native momentum and stochastic training differ from exact FW assumptions. No theorem is validated by these runs.

## Timing and budget

| Arm | Median training-active seconds | Median training-process seconds | Median fresh million tokens/second |
|---|---:|---:|---:|
| baseline | 694.471 | 751.546 | 0.9452 |
| mid | 661.025 | 728.998 | 0.9916 |
| early | 707.874 | 764.754 | 0.9259 |
| history | 689.480 | 746.393 | 0.9505 |

Job throughput varies across scheduled devices and time. These timings do not establish a method speed advantage. Every full run has 20,000 fresh forward/backward evaluations, the same direction pipeline and no extra optimizer probes. Compilation, warmup, evaluation and checkpoint costs are recorded separately and included in process/job cost; overlapping clocks should not be summed blindly.

The continuation completed 36 full training runs, one 128-update check and one 30-checkpoint evaluation; one failed short check is preserved. It used **8.118327 conservatively charged B300 request-hours**. Previous work used 37.069782, making the project total **45.188109 / 50 hours**. Reservations are zero. All campaign workload requests, jobs and pods are released. Every job used exactly one verified B300; at most six requests were outstanding.

The larger evaluation took 114.259 worker seconds, including 9.764 compilation seconds. It performed 2,400 evaluation microbatch forwards over 78,643,200 targets, with zero training updates or gradients. Exact commands, limits, source commits and output paths are in each run's `submission.json` and [EXPERIMENTS.csv](EXPERIMENTS.csv). Raw logs, checkpoints and data remain outside Git under `/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/<run_id>/`.

The 64-update check failed because its cooldown began before the fixed 40-update warmup ended; the replacement uses 128 updates and fail-fast validation. A redundant Git push raced with a publisher that had already pushed the same HEAD; no result was lost. The push helper now accepts only an identical remote/local tip and preserves real failures. No branch reset, forcepush, alternate GPU or unrelated job deletion was used.

Keep the baseline for this setup. Other curves or longer horizons remain new hypotheses requiring a fair baseline; remaining budget is not a spending target.
