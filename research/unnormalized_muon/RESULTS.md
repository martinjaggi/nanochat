# Live unnormalized-Muon results

One B300 per job. CE is token cross-entropy (nats); lower is better. Rows with different update budgets are not endpoint comparisons. Tuning uses the same fixed validation tokens; held-out scores appear only on final runs. Runtime includes compilation and overhead in process seconds.

| Run | Method | Updates | Seed | CLI matrix LR | Val CE | Val BPB | Heldout CE | Process sec |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| um-clean-calibration-001 | Clean Native cooldown | 256 | 0 | 0.02 | 5.270988 | 1.597709 | — | 86.86 |
| um-clean-fw-accumcheck-001 | Clean FW backtracking momentum Rfactor2 | 16 | 0 | 0.02 | 9.061382 | 2.745550 | — | 124.31 |
| um-clean-grid-00-0-normalized-lr0p005 | Clean Native cooldown | 2000 | 0 | 0.005 | 3.756841 | 1.138807 | — | 157.45 |
| um-clean-grid-00-1-cooldown-lr0p02 | Clean Unnormalized cooldown | 2000 | 0 | 0.02 | 3.859137 | 1.169816 | — | 164.02 |
| um-clean-grid-00-2-constant-lr0p02 | Clean Unnormalized constant | 2000 | 0 | 0.02 | 3.863261 | 1.171071 | — | 157.17 |
| um-clean-grid-01-0-normalized-lr0p01 | Clean Native cooldown | 2000 | 0 | 0.01 | 3.635674 | 1.102157 | — | 142.86 |
| um-clean-grid-01-1-cooldown-lr0p04 | Clean Unnormalized cooldown | 2000 | 0 | 0.04 | 3.828638 | 1.160576 | — | 151.79 |
| um-clean-grid-01-2-constant-lr0p04 | Clean Unnormalized constant | 2000 | 0 | 0.04 | 3.803687 | 1.153028 | — | 146.02 |
| um-clean-grid-02-0-normalized-lr0p02 | Clean Native cooldown | 2000 | 0 | 0.02 | 3.586015 | 1.087084 | — | 147.46 |
| um-clean-grid-02-1-cooldown-lr0p08 | Clean Unnormalized cooldown | 2000 | 0 | 0.08 | 3.786540 | 1.147820 | — | 152.80 |
| um-clean-grid-02-2-constant-lr0p08 | Clean Unnormalized constant | 2000 | 0 | 0.08 | 3.797298 | 1.151089 | — | 148.10 |
| um-clean-grid-03-0-normalized-lr0p04 | Clean Native cooldown | 2000 | 0 | 0.04 | 3.563474 | 1.080265 | — | 138.61 |
| um-clean-grid-03-1-cooldown-lr0p16 | Clean Unnormalized cooldown | 2000 | 0 | 0.16 | 3.731434 | 1.131155 | — | 149.79 |
| um-clean-grid-03-2-constant-lr0p16 | Clean Unnormalized constant | 2000 | 0 | 0.16 | 3.754476 | 1.138109 | — | 146.15 |
| um-clean-grid-04-0-normalized-lr0p08 | Clean Native cooldown | 2000 | 0 | 0.08 | 3.563980 | 1.080480 | — | 145.26 |
| um-clean-grid-04-1-cooldown-lr0p32 | Clean Unnormalized cooldown | 2000 | 0 | 0.32 | 3.698252 | 1.121036 | — | 157.86 |
| um-clean-grid-04-2-constant-lr0p32 | Clean Unnormalized constant | 2000 | 0 | 0.32 | 3.728677 | 1.130279 | — | 151.60 |
| um-clean-grid-05-1-cooldown-lr0p64 | Clean Unnormalized cooldown | 2000 | 0 | 0.64 | 3.683407 | 1.116578 | — | 157.17 |
| um-clean-grid-05-2-constant-lr0p64 | Clean Unnormalized constant | 2000 | 0 | 0.64 | 3.722817 | 1.128555 | — | 158.73 |
| um-clean-grid-06-1-cooldown-lr1p28 | Clean Unnormalized cooldown | 2000 | 0 | 1.28 | 3.785215 | 1.147408 | — | 148.29 |
| um-clean-grid-06-2-constant-lr1p28 | Clean Unnormalized constant | 2000 | 0 | 1.28 | 3.965584 | 1.202138 | — | 158.23 |
| um-clean-grid-07-1-cooldown-lr2p56 | Clean Unnormalized cooldown | 2000 | 0 | 2.56 | 4.333797 | 1.313749 | — | 154.67 |
| um-clean-grid-07-2-constant-lr2p56 | Clean Unnormalized constant | 2000 | 0 | 2.56 | 4.136932 | 1.254105 | — | 149.27 |
| um-clean-grid-08-1-cooldown-lr5p12 | Clean Unnormalized cooldown | 2000 | 0 | 5.12 | 4.498638 | 1.363555 | — | 152.28 |
| um-clean-grid-08-2-constant-lr5p12 | Clean Unnormalized constant | 2000 | 0 | 5.12 | 4.496089 | 1.362771 | — | 153.52 |
| um-clean-long-0-0-normalized-lr0p04 | Clean Native cooldown | 20000 | 0 | 0.04 | 3.107198 | 0.942041 | — | 743.22 |
| um-clean-long-0-1-cooldown-lr0p64 | Clean Unnormalized cooldown | 20000 | 0 | 0.64 | 3.168528 | 0.960609 | — | 779.28 |
| um-clean-long-0-2-constant-lr0p64 | Clean Unnormalized constant | 20000 | 0 | 0.64 | 3.210816 | 0.973451 | — | 737.52 |
| um-fw-diagnostic-001 | FW backtracking momentum Rfactor2 | 64 | 0 | 0.02 | 6.469995 | 1.960658 | — | 95.07 |
| um-fw-diagnostic-002 | FW backtracking momentum Rfactor2 | 64 | 0 | 0.02 | 6.900428 | 2.091122 | — | 117.14 |
| um-screen-00-0-native-lr0p005 | Native cooldown | 2000 | 0 | 0.005 | 3.734536 | 1.132046 | — | 145.49 |
| um-screen-00-1-scaled-lr0p0002 | Unnormalized cooldown | 2000 | 0 | 0.0002 | 4.818060 | 1.460343 | — | 153.42 |
| um-screen-00-2-constant-lr0p0002 | Unnormalized constant | 2000 | 0 | 0.0002 | 4.581043 | 1.388601 | — | 151.98 |
| um-screen-01-0-native-lr0p01 | Native cooldown | 2000 | 0 | 0.01 | 3.613164 | 1.095335 | — | 144.24 |
| um-screen-01-1-scaled-lr0p0006 | Unnormalized cooldown | 2000 | 0 | 0.0006 | 4.724209 | 1.431941 | — | 154.79 |
| um-screen-01-2-constant-lr0p0006 | Unnormalized constant | 2000 | 0 | 0.0006 | 4.532526 | 1.373908 | — | 163.98 |
| um-screen-02-0-native-lr0p02 | Native cooldown | 2000 | 0 | 0.02 | 3.559061 | 1.078945 | — | 151.82 |
| um-screen-02-1-scaled-lr0p002 | Unnormalized cooldown | 2000 | 0 | 0.002 | 4.379024 | 1.327359 | — | 155.31 |
| um-smoke-001/native | Native cooldown | 64 | 42 | 0.02 | 6.475706 | 1.962373 | — | 101.57 |
| um-smoke-001/scaled | Unnormalized cooldown | 64 | 42 | 0.002 | 6.492003 | 1.967335 | — | 74.24 |

Review of um-fw-diagnostic-001: Compiled training f0 compared against functional candidate losses; vanishing-step mismatch2-4e-5 exceeded tolerance, leading to curvature1e186 and45 skipped steps. Replaced by paired functional reference and candidates; retain all645 measured forwards and GPUcost.

Conservative charged/reserved total: 5.5045 / 30 B300 GPU-hours. Includes prior smoke/failed attempts and current maximum-duration reservations. Six-slot central queue; one B300 per run.

CLEAN geometry disables row equilibration and NorMuon. Original clean runs use zero matrix decay; new WD runs explicitly label standard or cautious decay and their CLI coefficient. Same five Polar Express steps and Frobenius correction; scale by the per-matrix nonnegative FP32 inner product of the native Nesterov input with the NS/Frobenius direction. Shape scaling occurs once outside the scalar. Legacy rows retain production extras and must be compared separately. Constant schedule changes only matrix LR; auxiliary schedules and momentum remain matched.

FW is a separate fixed-spectral-ball method with shared mixing, same-batch backtracking, frozen auxiliary weights during checks, and no extra matrix decay. Its extra candidate forwards count toward wall time and are logged.
