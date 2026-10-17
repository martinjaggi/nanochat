# Early reciprocal allocation results

Updated 2026-10-17T11:57:18.034200+00:00. Two-hour research window11:53–13:53UTC,17October2026. Exactly one verified B300/run, six-slot central queue,50B300-hour project-total cap.

This is a new WD-independent schedule, distinct from the earlier WD-coupled reciprocal curve multiplied by cooldown. Baseline actual eta .005, fixed ordinary WD .04593746995939655; 40-update warmup, join at7000, original late65% cooldown unchanged to nominal .00005. Full20k updates/655.36M tokens per token-matched run. [Protocol](EARLY_ALLOCATION_PROTOCOL.md).

| Seed0 arm | Development CE | Active seconds | Contraction product |
|---|---:|---:|---:|

## Limits and accounting

Matching final contraction does not match decay history. Both fixed-WD early-allocation and matched-contraction comparisons are required to separate explanations. Auxiliary LRs/WD and momentum are matched. Per-run schedules/logs/checkpoints and hardware assertions are preserved outside Git. Three paired seeds provide limited evidence. Development and heldout blocks are distinct; block6 is used only after settings freeze. Token-clock time curves are descriptive and are not equal-time endpoints.

Conservative recorded request-hours 37.069782; outstanding reserved hours 1.025000. Includes prior and failed work; queued/startup/cleanup request time upper-bounds GPU occupancy.
