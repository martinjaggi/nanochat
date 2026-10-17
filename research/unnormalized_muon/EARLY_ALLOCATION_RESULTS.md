# Early reciprocal allocation results

Updated 2026-10-17T13:34:51.558731+00:00. Two-hour research window11:53–13:53UTC,17October2026. Exactly one verified B300/run, six-slot central queue,50B300-hour project-total cap.

This is a new WD-independent schedule, distinct from the earlier WD-coupled reciprocal curve multiplied by cooldown. Baseline actual eta .005, fixed ordinary WD .04593746995939655; 40-update warmup, join at7000, original late65% cooldown unchanged to nominal .00005. Full20k updates/655.36M tokens per token-matched run. [Protocol](EARLY_ALLOCATION_PROTOCOL.md).

| Seed0 arm | Development CE | Active seconds | Contraction product |
|---|---:|---:|---:|
| Early peak 1x | 3.090447664 | 711.825 | 0.044527729 |
| Early peak 1.5x | 3.089904308 | 644.464 | 0.031427187 |
| Early peak 2x | 3.089890957 | 718.603 | 0.023892497 |
| Baseline LR, matched WD 0.055127136 | 3.091718435 | 690.056 | 0.023892497 |

Frozen seed0-only selection:
```json
{
  "neutral_early_wd": 0.03827980744972244,
  "peak_multiplier": 2.0,
  "tau_updates": 6960.0,
  "fixed_wd": 0.04593746995939655,
  "matched_baseline_wd": 0.05512713564910121,
  "seed0_ce": 3.089890956878662,
  "baseline_seed0_ce": 3.0904476642608643,
  "regression": {
    "new_ce": 3.0904476642608643,
    "old_ce": 3.0895402431488037,
    "delta": 0.0009074211120605469,
    "first_training_loss_difference": {
      "step": 11,
      "old_loss": 9.97259521484375,
      "new_loss": 9.972596168518066
    },
    "exact_schedule_initial_parameters_and_data_cursors": true,
    "bitwise_trajectory": false
  },
  "frozen_before_heldout": true,
  "confirmation_seeds": [
    70,
    71,
    72
  ],
  "heldout_block": 6
}
```

## Token-matched fresh seeds

| Seed | Arm | Heldout CE | Delta vs baseline | Active seconds | Updates |
|---|---|---:|---:|---:|---:|
| 70 | baseline | 3.132268906 | +0.000000000 | 725.066 | 20000 |
| 70 | early | 3.128401756 | -0.003867149 | 739.097 | 20000 |
| 70 | matched | 3.133392572 | +0.001123667 | 688.329 | 20000 |
| 70 | neutral | 3.128061533 | -0.004207373 | 730.148 | 20000 |
| 71 | baseline | 3.126216650 | +0.000000000 | 743.643 | 20000 |
| 71 | early | 3.128731966 | +0.002515316 | 714.832 | 20000 |
| 71 | matched | 3.127413750 | +0.001197100 | 683.594 | 20000 |
| 71 | neutral | 3.128008127 | +0.001791477 | 641.967 | 20000 |
| 72 | baseline | 3.132172585 | +0.000000000 | 722.159 | 20000 |
| 72 | early | 3.138991833 | +0.006819248 | 701.115 | 20000 |
| 72 | matched | 3.133921146 | +0.001748562 | 703.406 | 20000 |
| 72 | neutral | 3.139013052 | +0.006840467 | 659.319 | 20000 |

early minus baseline: mean **+0.001822 CE**, sample SD **0.005377**, n=3.

matched minus baseline: mean **+0.001356 CE**, sample SD **0.000342**, n=3.

neutral minus baseline: mean **+0.001475 CE**, sample SD **0.005531**, n=3.

## Limits and accounting

Matching final contraction does not match decay history. Both fixed-WD early-allocation and matched-contraction comparisons are required to separate explanations. Auxiliary LRs/WD and momentum are matched. Per-run schedules/logs/checkpoints and hardware assertions are preserved outside Git. Three paired seeds provide limited evidence. Development and heldout blocks are distinct; block6 is used only after settings freeze. Token-clock time curves are descriptive and are not equal-time endpoints.

Conservative recorded request-hours 45.146974; outstanding reserved hours 0.000000. Includes prior and failed work; queued/startup/cleanup request time upper-bounds GPU occupancy.
