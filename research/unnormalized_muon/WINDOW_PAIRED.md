# Three-hour WD/schedule comparison

Focused seed0 tuning first, then settings frozen for NEW paired seeds[40, 41, 42]; matched heldout block recorded in each config. Fixed standard WD and a changing-radius reciprocal-mixing WD hypothesis are separately labelled. Same native direction and auxiliary rules; one B300/run. Three seeds are limited evidence.

Frozen comparison: **static WD/LR retuning; no tested schedule/gap screen win**. Reference `um-window-joint-terminal-lr0p01-f0p01`, candidate `um-window-static-terminal-f0p01`. See [full settings](WINDOW_SELECTION.json). Static retuning is not evidence of adaptive-gap superiority.

| Arm | Seed | Heldout CE | Delta vs reference | Updates | Active sec | Process sec |
|---|---:|---:|---:|---:|---:|---:|
| reference | 40 | 3.185633 | +0.000000 | 20000 | 653.259 | 725.89 |
| candidate | 40 | 3.168677 | -0.016956 | 20000 | 718.942 | 775.31 |
| reference | 41 | 3.186403 | +0.000000 | 20000 | 593.852 | 666.93 |
| candidate | 41 | 3.172236 | -0.014166 | 20000 | 681.483 | 734.51 |
| reference | 42 | 3.190003 | +0.000000 | 20000 | 594.654 | 667.35 |
| candidate | 42 | 3.171032 | -0.018971 | 20000 | 600.632 | 673.18 |

Candidate paired heldout deltas mean -0.016698; sample SD 0.002413; n=3.
