# Early reciprocal allocation results

Updated 2026-10-17T12:10:11.323254+00:00. Two-hour research window11:53–13:53UTC,17October2026. Exactly one verified B300/run, six-slot central queue,50B300-hour project-total cap.

This is a new WD-independent schedule, distinct from the earlier WD-coupled reciprocal curve multiplied by cooldown. Baseline actual eta .005, fixed ordinary WD .04593746995939655; 40-update warmup, join at7000, original late65% cooldown unchanged to nominal .00005. Full20k updates/655.36M tokens per token-matched run. [Protocol](EARLY_ALLOCATION_PROTOCOL.md).

| Seed0 arm | Development CE | Active seconds | Contraction product |
|---|---:|---:|---:|
| Early peak 1x | 3.090447664 | 711.825 | 0.044527729 |
| Early peak 1.5x | 3.089904308 | 644.464 | 0.031427187 |
| Early peak 2x | 3.089890957 | 718.603 | 0.023892497 |

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

## Limits and accounting

Matching final contraction does not match decay history. Both fixed-WD early-allocation and matched-contraction comparisons are required to separate explanations. Auxiliary LRs/WD and momentum are matched. Per-run schedules/logs/checkpoints and hardware assertions are preserved outside Git. Three paired seeds provide limited evidence. Development and heldout blocks are distinct; block6 is used only after settings freeze. Token-clock time curves are descriptive and are not equal-time endpoints.

Conservative recorded request-hours 37.722460; outstanding reserved hours 0.000000. Includes prior and failed work; queued/startup/cleanup request time upper-bounds GPU occupancy.
