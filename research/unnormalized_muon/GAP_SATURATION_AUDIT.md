# Long layer-search saturation audit

Read-only parse of every recorded layer Armijo update in two completed20k-update runs. This audit uses logged signed current-gradient gap b, complete-direction norm v, actual applied rates and contemporaneous cap. No extra model evaluations.

| Existing run | All block rates equal cap/sign | Accepted on first trial | Nonpositive gap blocks |
|---|---:|---:|---:|
| um-lens-long-layer-cooldown | 19995/20000 | 20000/20000 | 416/1040000 |
| um-lens-long-layer-stable | 19995/20000 | 20000/20000 | 720/1040000 |

In BOTH runs only optimizer indices1–5 differed from eta_l=cap*I(b_l>0 and v_l>0). Index0 and every index6–19999 matched exactly in logged arithmetic. All20,000 updates accepted the first candidate; the carried Armijo proposal parameter L is not a measured smoothness estimate.

This motivates a cheap cap/sign comparison but does not establish identical counterfactual trajectories: changing the startup steps can change subsequent directions, and the native fused implementation has different rounding from the wrapper. The new variant therefore requires independent training comparisons, not reuse of these losses. It skips the full direction and ordinary decay for nonpositive blocks, retaining one native momentum transition and unchanged auxiliary updates.

Reproduce: `python research/unnormalized_muon/gap_saturation_audit.py`. Persistent raw logs are outside Git.
