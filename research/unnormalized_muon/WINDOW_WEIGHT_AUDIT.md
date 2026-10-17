# Saved-weight WD diagnostics

CPU-only read of existing final20k-update checkpoints; no training or loss evaluations. All52 native Muon matrices. Global Frobenius norm is sqrt(sum squared matrix Frobenius norms). Spectral norms are computed by FP64 SVD of the stored weights. Fifty deterministic power iterations are also retained as an independent lower estimate; both agree closely here. Radius uses the actual final logged WD coefficient, with shape c included. These final observations do not certify all intervening iterates or the approximate NS oracle.

| Run | Val CE | Global matrix Frobenius | Max spectral norm / final radius |
|---|---:|---:|---:|
| um-follow-first-tune-control-lr0p01 | 3.112087 | 43.4142 | 0.251431 |
| um-follow-mid-reciprocal-high | 3.152773 | 39.8121 | 0.223028 |
| um-window-schedule-lr0p02-f0p05 | 3.096101 | 49.3902 | 0.251467 |
| um-window-first-wd-mixing | 3.105714 | 50.4306 | 1.496699 |
| um-window-first-wd-static-product | 3.103214 | 54.9196 | 0.222371 |

The changing-WD run ends with lambda_t=1.11466 rather than reference lambda=.18375. Its final radius shrinks sufficiently that at least one saved block lies outside that final ball (ratio1.496699). Fixed-WD examples here end inside their balls, with maximum ratios.222–.251; initial feasibility and oracle accuracy are separate. No fixed-domain theorem is claimed for changing WD.

Static matched WD has the same final contraction product as changing WD yet a different final weight norm and slightly better development CE. A contraction product is not a final norm ratio.

Reproduce: `OMP_NUM_THREADS=2 python research/unnormalized_muon/window_weight_audit.py`. Per-matrix scalar results in `WINDOW_WEIGHT_DIAGNOSTICS.json`; checkpoints remain outside Git.
