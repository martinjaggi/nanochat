# LR and cumulative matrix-contraction audit

Audit17 October2026 during the authorized three-hour work window. Same seed0/native depth8/ClimbMix/32768-token update stream,20000-update horizon. Matrix direction geometry Q=cNS(M), ordinary WD, no row equilibration or NorMuon. No extra gradients or model evaluations.

For EACH native Muon group, independently recomputed sum gamma and sum log(1-gamma) from the complete configured schedule; all saved group contractions match within1e-7. These use recorded Python LR/WD coefficients; the fused kernel rounds scalars to FP32. The product is the coefficient on an unforced initial iterate, NOT the ratio of final to initial weight norms, because each step also adds a direction.

| Run | Schedule | Peak CLI LR | Reference lambda | Validation CE | Sum gamma | Sum log(1-gamma) | Product contraction |
|---|---|---:|---:|---:|---:|---:|---:|
| um-follow-first-tune-control-lr0p01 | cooldown | 0.01 | 0.18375 | 3.112087 | 6.342116 | -6.343333 | 0.00175843 |
| um-follow-first-tune-control-lr0p02 | cooldown | 0.02 | 0.18375 | 3.142251 | 12.684231 | -12.689102 | 3.08456e-06 |
| um-lens-long-reciprocal-0 | fw_reciprocal | 0.02 | 0.18375 | 3.155148 | 4.657960 | -4.658794 | 0.00947788 |
| um-lens-long-reciprocal-1 | fw_reciprocal | 0.04 | 0.18375 | 3.155272 | 5.962709 | -5.964477 | 0.00256839 |
| um-follow-first-tune-reciprocal-lr0p01 | fw_reciprocal | 0.01 | 0.18375 | 3.156622 | 3.449617 | -3.449996 | 0.0317458 |
| um-lens-long-control-1 | cooldown | 0.0282843 | 0.18375 | 3.168332 | 17.938212 | -17.947956 | 1.60436e-08 |
| um-lens-long-control-0 | cooldown | 0.04 | 0.18375 | 3.199618 | 25.368462 | -25.387958 | 9.42215e-12 |

All 7 eligible completed runs passed the independent arithmetic check.

The old long-run cooldown control LR.028284 had log contraction-17.948 versus-4.659 for reciprocal LR.02. Lowering the cooldown peak to.01 gives-6.343 and improves development CE to3.11209, ahead of reciprocal3.15515. Thus the old reciprocal win cannot isolate LR-shape/curvature effects from peak-LR and decay exposure. The current matched-WD and LR-interaction tests address this; no causal conclusion is drawn before those complete.

Keep the spectral-ball interpretation separate: fixed lambda preserves its radius, while varying lambda_t to prescribe gamma_t changes the radius. Matching the FINAL contraction product does not match its history. All native auxiliary optimizer LR/decay schedules remained common across these token-matched arms. No deterministic FW convergence claim follows from these minibatch/finite-NS experiments.
