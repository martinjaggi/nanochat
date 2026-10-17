# Three-hour focused WD and schedule work

Requested window17 October2026,07:48:18–10:48:18UTC. One locked submission queue,one actual B300/job,max6 jobs,50B300 GPUh PROJECT TOTAL including earlier runs. No new online-controller grid: prior fresh-data promotion gate failed. First compare WD at the same LR as the pending .005 reference; later tune LR/WD interaction using only seed0 development data. Static WD0 is unconstrained; changing reciprocal-mixing WD changes the radius and retains native momentum, so it is not a fixed-domain stochastic FW theorem test.

| Run | Updates | Seed | CLI LR | Reference lambda | WD rule | Matrix schedule | Validation CE | Heldout CE | Active sec | Process sec |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|
| um-window-cap-check-002 | 64 | 0 | 0.01 | 0.18375 | fixed | cooldown cap/sign | 6.438628 | — | 2.595 | 61.30 |
| um-window-first-wd-mixing | 20000 | 0 | 0.005 | 0.18375 | fw_mixing_reciprocal | cooldown | 3.105714 | — | 672.405 | 728.95 |
| um-window-first-wd-static-product | 20000 | 0 | 0.005 | 0.138371 | fixed | cooldown | 3.103214 | — | 696.460 | 770.97 |
| um-window-first-wd-x0 | 20000 | 0 | 0.005 | 0 | fixed | cooldown | 3.133004 | — | 724.601 | 798.92 |
| um-window-first-wd-x0p25 | 20000 | 0 | 0.005 | 0.0459375 | fixed | cooldown | 3.116976 | — | 693.217 | 767.80 |
| um-window-first-wd-x0p5 | 20000 | 0 | 0.005 | 0.0918749 | fixed | cooldown | 3.104900 | — | 720.153 | 794.45 |
| um-window-first-wd-x2 | 20000 | 0 | 0.005 | 0.3675 | fixed | cooldown | 3.135778 | — | 716.690 | 772.24 |
| um-window-schedule-lr0p02-f0p05 | 20000 | 0 | 0.02 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.096101 | — | 638.844 | 711.40 |
| um-window-schedule-lr0p02-f0p25 | 20000 | 0 | 0.02 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.101839 | — | 638.613 | 711.22 |

Additional cheap-schedule hypothesis: reciprocal plus terminal cooldown, keeping fixed lambda. Final factors.05/.25 and fair peak LR boundaries test a terminal noise-floor explanation; no extra queries or exact FW claim. No heldout tokens select settings. If a development candidate improves by>.001CE, freeze against the tuned original-lambda reference and confirm with NEW seeds40/41/42 on NEW heldout block4; paired table in WINDOW_PAIRED.md only after all complete. No equal-time endpoint claim from token-clock prefixes. Actual group WD/contraction histories and costs are in persistent per-update logs.

Old historical plots remain intact and regenerate only when their input summaries change. Full raw logs remain outside Git; streaming publication parses only required events. Deadline guard declines new runs that cannot reasonably fit in the window; last-started jobs finish/reap normally.
