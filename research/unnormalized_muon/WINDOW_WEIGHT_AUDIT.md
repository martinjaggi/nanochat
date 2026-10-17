# Saved-weight WD diagnostics

CPU-only read of existing final20k-update checkpoints; no training or loss evaluations. All52 native Muon matrices. Global Frobenius norm is sqrt(sum squared matrix Frobenius norms). Spectral estimates use50 deterministic power iterations, evaluating norm(Wv) for a unit vector: lower estimates, not feasibility certificates. Radius for the last column uses the actual final logged WD coefficient, with shape c included. Values below1 do not certify feasibility; values above1 show a radius violation beyond numerical error.

| Run | Val CE | Global matrix Frobenius | Max spectral lower estimate / final radius |
|---|---:|---:|---:|
| um-follow-first-tune-control-lr0p01 | 3.112087 | 43.4142 | 0.2514 |
| um-follow-mid-reciprocal-high | 3.152773 | 39.8121 | 0.2230 |
| um-window-schedule-lr0p02-f0p05 | 3.096101 | 49.3902 | 0.2515 |
| um-window-first-wd-mixing | 3.105714 | 50.4306 | 1.4967 |
| um-window-first-wd-static-product | 3.103214 | 54.9196 | 0.2224 |

The changing-WD run ends with lambda_t=1.11466 rather than reference lambda=.18375. Its final radius shrinks sufficiently that at least one saved block lies outside that final ball (ratio at least1.497). Thus its update algebra is useful as a schedule hypothesis, but neither fixed-domain FW feasibility nor the corresponding theorem applies. Static matched WD has the same final contraction product yet a different final weight norm and slightly better development CE.

Reproduce with `python research/unnormalized_muon/window_weight_audit.py`. Per-matrix scalar results in `WINDOW_WEIGHT_DIAGNOSTICS.json`; checkpoints remain outside Git.
