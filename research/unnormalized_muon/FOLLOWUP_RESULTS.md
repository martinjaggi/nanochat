# Reciprocal follow-up: long-horizon fairness and equal time

The earlier campaign COMPLETED. Same-batch gap searches lost at655M tokens and equal time. The fresh-data gate failed7/12 versus8/12, so online-controller expansion remains stopped. A cheap fixed-WD reciprocal schedule improved three original paired seeds, motivating this follow-up; settings here use seed0 development losses only. The old long-horizon control preferred its lower tested LR, so extend its range fairly before claiming superiority.

All runs: one verified B300, dense125,829,354-parameter depth8/512, ClimbMix/32K tokenizer,32768 tokens/update, fixed ordinary lambda=.1837498798375862, native Nesterov/NS/Frobenius, no row equilibration or NorMuon. Shape stays inside Q. Same auxiliary recipe. Three seeds are limited evidence.

First complete the missing reciprocal equal-time endpoints on the ORIGINAL frozen settings/seeds10/11/12. Then extend/control BOTH peak-LR searches at20k updates, using the same factor-two edge rule and geometric refinements. Freeze before NEW seeds20/21/22 and NEW disjoint heldout block2. All timed schedules, including matrix reciprocal, use active-time fraction*reference horizon. Time-budget reruns finish the last update; overhead and overshoot are recorded.

| Run | Updates | Schedule | Peak CLI LR | Seed | Val CE | Heldout CE | Heldout block | Active sec | Process sec | Overshoot sec |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| um-follow-confirm20000-control-s20 | 20000 | cooldown | 0.01 | 20 | 3.111594 | 3.112870 | 2 | 672.238 | 729.25 | 0.00000 |
| um-follow-confirm20000-reciprocal-s20 | 20000 | fw_reciprocal | 0.0282843 | 20 | 3.157425 | 3.156672 | 2 | 688.482 | 741.30 | 0.00000 |
| um-follow-edge0-control-lr0p005 | 20000 | cooldown | 0.005 | 0 | 3.119279 | — | — | 664.297 | 719.39 | 0.00000 |
| um-follow-first-time-reciprocal-s10 | 20740 | fw_reciprocal | 0.02 | 10 | 3.154321 | 3.095921 | 1 | 679.004 | 733.36 | 0.01138 |
| um-follow-first-time-reciprocal-s11 | 20007 | fw_reciprocal | 0.02 | 11 | 3.156209 | 3.099467 | 1 | 678.997 | 734.10 | 0.00371 |
| um-follow-first-time-reciprocal-s12 | 18127 | fw_reciprocal | 0.02 | 12 | 3.161711 | 3.105612 | 1 | 679.006 | 750.97 | 0.01322 |
| um-follow-first-tune-control-lr0p01 | 20000 | cooldown | 0.01 | 0 | 3.112087 | — | — | 706.571 | 777.47 | 0.00000 |
| um-follow-first-tune-control-lr0p02 | 20000 | cooldown | 0.02 | 0 | 3.142251 | — | — | 696.905 | 767.69 | 0.00000 |
| um-follow-first-tune-reciprocal-lr0p01 | 20000 | fw_reciprocal | 0.01 | 0 | 3.156622 | — | — | 673.476 | 744.07 | 0.00000 |
| um-follow-mid-control-high | 20000 | cooldown | 0.0141421 | 0 | 3.122182 | — | — | 682.008 | 738.56 | 0.00000 |
| um-follow-mid-control-low | 20000 | cooldown | 0.00707107 | 0 | 3.113318 | — | — | 722.395 | 775.02 | 0.00000 |
| um-follow-mid-reciprocal-high | 20000 | fw_reciprocal | 0.0282843 | 0 | 3.152773 | — | — | 649.252 | 721.58 | 0.00000 |
| um-follow-mid-reciprocal-low | 20000 | fw_reciprocal | 0.0141421 | 0 | 3.152943 | — | — | 655.222 | 727.28 | 0.00000 |

## Paired held-out endpoints

| Comparison | Seed | Reciprocal minus control CE | Control updates | Reciprocal updates |
|---|---:|---:|---:|---:|
| original-frozen equal time | 10 | -0.024781 | 20225 | 20740 |
| original-frozen equal time | 11 | -0.013923 | 19762 | 20007 |
| original-frozen equal time | 12 | -0.011055 | 19890 | 18127 |

original-frozen equal time: paired deltas mean -0.016586, sample SD 0.007240; n=3.

| 20000 confirm | 20 | +0.043802 | 20000 | 20000 |

20000 confirm: incomplete (1/3), no final ranking.


Scale-up gate: only if fresh20k seeds all improve and mean delta<-.003 CE, tune BOTH families again at40k updates (1.31B tokens), then freeze for NEW seeds30/31/32 and NEW heldout block3, with independent equal-time reruns. Otherwise stop scale-up. Larger horizons and extra tuning are reported as follow-up research, not retroactive confirmation of earlier heldout results.

Job cost includes compilation, validation, warmup, snapshots and checkpoint I/O. Training-active time excludes separately measured one-time/evaluation overhead. No attempt is made to spend the full50GPUh allowance.
