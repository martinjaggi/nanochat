# Live unnormalized-Muon results

One B300 per job. CE is token cross-entropy (nats); lower is better. Rows with different update budgets are not endpoint comparisons. Tuning uses the same fixed validation tokens; held-out scores appear only on final runs. Runtime includes compilation and overhead in process seconds.

| Run | Method | Updates | Seed | CLI matrix LR | Val CE | Val BPB | Heldout CE | Process sec |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| um-fw-diagnostic-001 | FW backtracking | 64 | 0 | 0.02 | 6.469995 | 1.960658 | — | 95.07 |
| um-fw-diagnostic-002 | FW backtracking | 64 | 0 | 0.02 | 6.900428 | 2.091122 | — | 117.14 |
| um-screen-00-0-native-lr0p005 | Native cooldown | 2000 | 0 | 0.005 | 3.734536 | 1.132046 | — | 145.49 |
| um-screen-00-1-scaled-lr0p0002 | Unnormalized cooldown | 2000 | 0 | 0.0002 | 4.818060 | 1.460343 | — | 153.42 |
| um-screen-00-2-constant-lr0p0002 | Unnormalized constant | 2000 | 0 | 0.0002 | 4.581043 | 1.388601 | — | 151.98 |
| um-screen-01-0-native-lr0p01 | Native cooldown | 2000 | 0 | 0.01 | 3.613164 | 1.095335 | — | 144.24 |
| um-screen-01-1-scaled-lr0p0006 | Unnormalized cooldown | 2000 | 0 | 0.0006 | 4.724209 | 1.431941 | — | 154.79 |
| um-smoke-001/native | Native cooldown | 64 | 42 | 0.02 | 6.475706 | 1.962373 | — | 101.57 |
| um-smoke-001/scaled | Unnormalized cooldown | 64 | 42 | 0.002 | 6.492003 | 1.967335 | — | 74.24 |

Review of um-fw-diagnostic-001: Compiled training f0 compared against functional candidate losses; vanishing-step mismatch2-4e-5 exceeded tolerance, leading to curvature1e186 and45 skipped steps. Replaced by paired functional reference and candidates; retain all645 measured forwards and GPUcost.

Conservative charged/reserved total: 1.2011 / 10 B300 GPU-hours. Includes prior smoke/failed attempts and current maximum-duration reservations. Three-slot central queue; one B300 per run.

Core modification: per-matrix nonnegative FP32 inner product of the native Nesterov input with its NS/Frobenius direction. Multiply the native NorMuon direction afterward, then apply native decoupled cautious decay separately. Shape scaling occurs once outside the scalar. Constant schedule changes only matrix LR; auxiliary schedules and momentum remain matched.

FW is a separate fixed-spectral-ball method with shared mixing, same-batch backtracking, frozen auxiliary weights during checks, and no extra matrix decay. Its extra candidate forwards count toward wall time and are logged.
