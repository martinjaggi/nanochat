# Independent recorded-schedule audit

Read-only audit of all20,000 recorded update coefficients per row; no new model evaluations. Recomputed sum log(1-eta*lambda) matches each summary within1e-9. These are seed0 development results. Product is the initial-iterate coefficient, not the final weight-norm ratio.

| Method | Val CE | Final actual LR | Final lambda | Log contraction | Active seconds |
|---|---:|---:|---:|---:|---:|
| Cooldown final .01, CLI .01 | 3.104185 | 2.5190385e-05 | 0.1837499 | -6.223885 | 689.960 |
| Cooldown final .05, CLI .01 | 3.112087 | 0.00012518269 | 0.1837499 | -6.343333 | 706.571 |
| Reciprocal, CLI .0283 | 3.152773 | 0.00050628982 | 0.1837499 | -5.301866 | 649.252 |
| Reciprocal + cooldown, CLI .02 | 3.096101 | 2.4621277e-05 | 0.1837499 | -3.940495 | 638.844 |
| Changing WD, LR .005 | 3.105714 | 6.2591346e-05 | 1.114657 | -2.388109 | 672.405 |
| Static matched WD, LR .005 | 3.103214 | 6.2591346e-05 | 0.1383712 | -2.388109 | 696.460 |

The refined ordinary control and cooled reciprocal now have near-matched final actual LRs (~2.5e-5), but different cumulative contraction. The reciprocal/cooldown seed0 gain versus this stronger original-lambda control is.008084CE. A static-WD control matching the cooled run final log contraction is prespecified before final confirmation, alongside static-WD/terminal-factor refinement. Matching the final product does not match histories.

Changing WD and its first static counterpart match FINAL log contraction exactly; the static counterpart currently performs better. Native auxiliary rules are identical. Different scheduled GPU placements confound small raw time differences; token-clock curves are not independently matched equal-time endpoints.

![Validation, actual LR and contraction histories](window_schedule_diagnostics.png)

Reproduce: `python research/unnormalized_muon/window_diagnostics.py`; output `/tmp/muon-window-audit`, reading persistent logs.
