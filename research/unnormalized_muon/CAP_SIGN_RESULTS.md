# Cheap complete-gap sign gate: long screen

Three full20k-update seed0 runs, same52 native Muon matrices, ordinary fixed lambda=.1837498798375862, clean native direction and auxiliary recipe. Initial parameter and validation-token hashes match each corresponding control. Actual eta=CLI*.25; both controls and sign gate use original terminal fraction.05. Best LR is interior to this tested grid. No extra model forward/backward evaluations.

| Peak CLI LR | Native CE | Cap/sign CE | Delta | Observed active-time ratio | Skipped matrix updates |
|---|---:|---:|---:|---:|---:|
| 0.005 | 3.119279 | 3.121832 | +0.002553 | 1.028 | 942/1040000 |
| 0.01 | 3.112087 | 3.114210 | +0.002123 | 1.026 | 904/1040000 |
| 0.02 | 3.142251 | 3.142147 | -0.000104 | 1.015 | 646/1040000 |

Best cap/sign CE3.114210 is worse than matching native3.112087; refined native terminal-factor control is stronger still at3.104185. This seed0 screen does not support promoting cap/sign to a large confirmation. Active ratios are observed across different scheduled runs/hardware placements, not independently matched equal-time endpoints.

At central LR, 904 block decisions skip (0.086923%), but parameter-weighted skipped fraction is only0.005945%. Four tiny48-parameter `attn.ve_gate.weight` matrices account for90.04% of skips. All695 skips after optimizer index1000 occur in these tiny gates; their parameter-weighted fraction over remaining updates is0.00000698%. Most large-matrix steps therefore remain ordinary scheduled Muon.

This supports the prior cap/sign saturation diagnosis while finding no useful development-validation gain for the cheap replacement. The old Armijo method matched cap/sign rates after startup, but counterfactual trajectories and rounding need not match. Retain the negative result; do not add a fresh-fit controller grid after its failed gate.

Reproduce with `python research/unnormalized_muon/cap_sign_report.py`; outputs go to `/tmp/muon-window-audit`. All raw logs remain outside Git.
