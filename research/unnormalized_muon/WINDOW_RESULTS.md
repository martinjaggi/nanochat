# Three-hour focused WD and schedule work

Requested window17 October2026,07:48:18–10:48:18UTC. One locked submission queue,one actual B300/job,max6 jobs,50B300 GPUh PROJECT TOTAL including earlier runs. No new online-controller grid: prior fresh-data promotion gate failed. First compare WD at the same LR as the pending .005 reference; later tune LR/WD interaction using only seed0 development data. Static WD0 is unconstrained; changing reciprocal-mixing WD changes the radius and retains native momentum, so it is not a fixed-domain stochastic FW theorem test.

Completed confirmation: [WINDOW_PAIRED.md](WINDOW_PAIRED.md).

**Best completed seed-0 development endpoint so far: 3.089540CE**, `um-window-static-terminal-f0p01`. This is a tuning result, not a new-seed or equal-time claim.

Details: [protocol](WINDOW_PROTOCOL.md), [LR/contraction curves](WINDOW_SCHEDULE_AUDIT.md), [exact saved-weight norms](WINDOW_WEIGHT_AUDIT.md), [layer-search saturation](GAP_SATURATION_AUDIT.md), [plain reciprocal follow-up](FOLLOWUP_RESULTS.md).

| Run | Updates | Seed | CLI LR | Reference lambda | WD rule | Matrix schedule | Validation CE | Heldout CE | Active sec | Process sec |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|
| um-window-cap-check-002 | 64 | 0 | 0.01 | 0.18375 | fixed | cooldown cap/sign | 6.438628 | — | 2.595 | 61.30 |
| um-window-cap-tune-x0p5 | 20000 | 0 | 0.005 | 0.18375 | fixed | cooldown cap/sign | 3.121832 | — | 682.636 | 739.60 |
| um-window-cap-tune-x1 | 20000 | 0 | 0.01 | 0.18375 | fixed | cooldown cap/sign | 3.114210 | — | 724.767 | 776.59 |
| um-window-cap-tune-x2 | 20000 | 0 | 0.02 | 0.18375 | fixed | cooldown cap/sign | 3.142147 | — | 707.363 | 779.55 |
| um-window-confirm-candidate-s40 | 20000 | 40 | 0.02 | 0.0459375 | fixed | cooldown_refined | 3.087717 | 3.168677 | 718.942 | 775.31 |
| um-window-confirm-candidate-s41 | 20000 | 41 | 0.02 | 0.0459375 | fixed | cooldown_refined | 3.086025 | 3.172236 | 681.483 | 734.51 |
| um-window-confirm-candidate-s42 | 20000 | 42 | 0.02 | 0.0459375 | fixed | cooldown_refined | 3.088866 | 3.171032 | 600.632 | 673.18 |
| um-window-confirm-reference-s40 | 20000 | 40 | 0.01 | 0.18375 | fixed | cooldown_refined | 3.103223 | 3.185633 | 653.259 | 725.89 |
| um-window-confirm-reference-s41 | 20000 | 41 | 0.01 | 0.18375 | fixed | cooldown_refined | 3.104613 | 3.186403 | 593.852 | 666.93 |
| um-window-confirm-reference-s42 | 20000 | 42 | 0.01 | 0.18375 | fixed | cooldown_refined | 3.104400 | 3.190003 | 594.654 | 667.35 |
| um-window-cooled-wd-x0p25 | 20000 | 0 | 0.02 | 0.0459375 | fixed | fw_reciprocal_cooldown | 3.096870 | — | 683.255 | 737.58 |
| um-window-cosine-lr-edge | 20000 | 0 | 0.02 | 0.18375 | cosine_radius | cooldown | 3.101129 | — | 680.241 | 734.59 |
| um-window-first-wd-mixing | 20000 | 0 | 0.005 | 0.18375 | fw_mixing_reciprocal | cooldown | 3.105714 | — | 672.405 | 728.95 |
| um-window-first-wd-static-product | 20000 | 0 | 0.005 | 0.138371 | fixed | cooldown | 3.103214 | — | 696.460 | 770.97 |
| um-window-first-wd-x0 | 20000 | 0 | 0.005 | 0 | fixed | cooldown | 3.133004 | — | 724.601 | 798.92 |
| um-window-first-wd-x0p25 | 20000 | 0 | 0.005 | 0.0459375 | fixed | cooldown | 3.116976 | — | 693.217 | 767.80 |
| um-window-first-wd-x0p5 | 20000 | 0 | 0.005 | 0.0918749 | fixed | cooldown | 3.104900 | — | 720.153 | 794.45 |
| um-window-first-wd-x2 | 20000 | 0 | 0.005 | 0.3675 | fixed | cooldown | 3.135778 | — | 716.690 | 772.24 |
| um-window-joint-cosine-wd-lr0p005 | 20000 | 0 | 0.005 | 0.18375 | cosine_radius | cooldown | 3.118502 | — | 601.961 | 659.14 |
| um-window-joint-cosine-wd-lr0p01 | 20000 | 0 | 0.01 | 0.18375 | cosine_radius | cooldown | 3.094790 | — | 598.498 | 651.90 |
| um-window-joint-mixing-x1 | 20000 | 0 | 0.01 | 0.18375 | fw_mixing_reciprocal | cooldown | 3.097867 | — | 672.643 | 730.73 |
| um-window-joint-mixing-x2 | 20000 | 0 | 0.02 | 0.18375 | fw_mixing_reciprocal | cooldown | 3.092627 | — | 657.099 | 707.60 |
| um-window-joint-terminal-lr0p005-f0p01 | 20000 | 0 | 0.005 | 0.18375 | fixed | cooldown_refined | 3.120314 | — | 677.357 | 734.57 |
| um-window-joint-terminal-lr0p005-f0p25 | 20000 | 0 | 0.005 | 0.18375 | fixed | cooldown_refined | 3.132740 | — | 717.720 | 770.78 |
| um-window-joint-terminal-lr0p01-f0p01 | 20000 | 0 | 0.01 | 0.18375 | fixed | cooldown_refined | 3.104185 | — | 689.960 | 758.60 |
| um-window-joint-terminal-lr0p01-f0p25 | 20000 | 0 | 0.01 | 0.18375 | fixed | cooldown_refined | 3.170352 | — | 686.162 | 755.55 |
| um-window-joint-wd0-x1 | 20000 | 0 | 0.01 | 0 | fixed | cooldown | 3.118538 | — | 720.050 | 790.98 |
| um-window-joint-wd0-x2 | 20000 | 0 | 0.02 | 0 | fixed | cooldown | 3.105875 | — | 733.129 | 804.53 |
| um-window-joint-wd0p25-x1 | 20000 | 0 | 0.01 | 0.0459375 | fixed | cooldown | 3.097679 | — | 720.957 | 792.33 |
| um-window-joint-wd0p25-x2 | 20000 | 0 | 0.02 | 0.0459375 | fixed | cooldown | 3.093087 | — | 706.220 | 777.21 |
| um-window-joint-wd0p5-x1 | 20000 | 0 | 0.01 | 0.0918749 | fixed | cooldown | 3.100060 | — | 701.702 | 780.80 |
| um-window-joint-wd0p5-x2 | 20000 | 0 | 0.02 | 0.0918749 | fixed | cooldown | 3.106249 | — | 705.207 | 784.21 |
| um-window-joint-wd0p753041-x1 | 20000 | 0 | 0.01 | 0.138371 | fixed | cooldown | 3.106556 | — | 694.328 | 750.51 |
| um-window-joint-wd0p753041-x2 | 20000 | 0 | 0.02 | 0.138371 | fixed | cooldown | 3.125062 | — | 720.187 | 772.65 |
| um-window-joint-zero-lr0p04 | 20000 | 0 | 0.04 | 0 | fixed | cooldown | 3.107898 | — | 728.677 | 787.70 |
| um-window-mixing-lr-edge | 20000 | 0 | 0.04 | 0.18375 | fw_mixing_reciprocal | cooldown | 3.097083 | — | 696.151 | 773.43 |
| um-window-schedule-edge0-f0p05 | 20000 | 0 | 0.01 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.105950 | — | 716.757 | 789.58 |
| um-window-schedule-edge0-f0p25 | 20000 | 0 | 0.08 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.104520 | — | 705.623 | 778.27 |
| um-window-schedule-lr0p02-f0p05 | 20000 | 0 | 0.02 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.096101 | — | 638.844 | 711.40 |
| um-window-schedule-lr0p02-f0p25 | 20000 | 0 | 0.02 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.101839 | — | 638.613 | 711.22 |
| um-window-schedule-lr0p04-f0p05 | 20000 | 0 | 0.04 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.096862 | — | 721.605 | 780.16 |
| um-window-schedule-lr0p04-f0p25 | 20000 | 0 | 0.04 | 0.18375 | fixed | fw_reciprocal_cooldown | 3.100892 | — | 643.475 | 714.25 |
| um-window-static-lr-edge | 20000 | 0 | 0.04 | 0.0459375 | fixed | cooldown | 3.106810 | — | 709.487 | 787.45 |
| um-window-static-matched-contraction | 20000 | 0 | 0.01 | 0.116345 | fixed | cooldown_refined | 3.094227 | — | 775.679 | 853.89 |
| um-window-static-terminal-f0p01 | 20000 | 0 | 0.02 | 0.0459375 | fixed | cooldown_refined | 3.089540 | — | 694.791 | 772.89 |
| um-window-terminal-edge-lr0p0025-f0p25 | 20000 | 0 | 0.0025 | 0.18375 | fixed | cooldown_refined | 3.147864 | — | 732.953 | 785.67 |
| um-window-terminal-edge-lr0p02-f0p01 | 20000 | 0 | 0.02 | 0.18375 | fixed | cooldown_refined | 3.127284 | — | 739.787 | 797.67 |

Additional cheap-schedule hypothesis: reciprocal plus terminal cooldown, keeping fixed lambda. Final factors.05/.25 and fair peak LR boundaries test a terminal noise-floor explanation; no extra queries or exact FW claim. No heldout tokens select settings. If a development candidate improves by>.001CE, freeze against the best tested static-WD reference (or static retuning versus original lambda) and confirm with NEW seeds40/41/42 on NEW heldout block4; paired table in WINDOW_PAIRED.md only after all complete. No equal-time endpoint claim from token-clock prefixes. Actual group WD/contraction histories and costs are in persistent per-update logs.

Old historical plots remain intact and regenerate only when their input summaries change. Full raw logs remain outside Git; streaming publication parses only required events. Deadline guard declines new runs that cannot reasonably fit in the window; last-started jobs finish/reap normally.
