# Early reciprocal allocation, 17 October 2026

New two-hour authorization 11:53–13:53 UTC. Total campaign cap remains 50 B300-hours, maximum six outstanding jobs, exactly one verified B300 per run. Prior conservative charge 37.0698 hours. No other campaign jobs active at start.

Starting baseline: clean normalized Muon, native Nesterov/Polar Express/Frobenius correction, ordinary fixed WD 0.04593746995939655, CLI LR .02 = actual eta .005, depth8/125829354 parameters, context1024, 32768 fresh tokens/update, 20000 updates = 655.36M tokens. ClimbMix/native32k tokenizer, BF16 compute/FP32 Muon masters. Auxiliary schedules and momentum unchanged.

Only the matrix early plateau and its warmup change. Warmup indices0–39 reach k*.005; reciprocal starts at index40, s=0; at index7000, s=6960, exactly join .005. Tau=6960/(k-1), independent of WD. k=1 calls original schedule exactly. Indices7000 onward call original matrix_cooldown(...,final=.01) directly, preserving the complete late cooldown. Last realized eta at index19999 is .00005038076923, nominal endpoint .00005. Candidate curves are never multiplied by a second cooldown.

Predeclared seed0 screen k={1,1.5,2}. Rerun k1 for current-code regression against um-window-static-terminal-f0p01. Select by development CE only. For any improvement, run the baseline schedule with static WD solved to match the candidate's full product of (1-lambda*eta); this matches final contraction but not its history. Report both schedules' contraction and changed WD explicitly. Freeze before fresh paired seeds70/71/72 and disjoint final heldout block6. No tuning on heldout. Confirm best candidate even if a small improvement, retaining the original baseline and contraction control. If no improvement, preserve negative result and diagnose early/late curves before any additional targeted run; do not broaden into an unrestricted grid.

No backtracking or extra gradients; these variants differ only in native matrix LR allocation. Token-matched endpoints are primary; timing and end-to-end costs separately reported. Any equal-time comparison requires new time-clock reruns. Training timeout1200s plus controller guard, one central queue. Outputs /mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/um-earlyalloc-* .

## Analytic schedule exposures

```json
[
  {
    "peak_multiplier": 1.0,
    "tau": null,
    "sum_eta": 67.729975,
    "log_contraction": -3.1116431631355974,
    "contraction": 0.044527728872638915
  },
  {
    "peak_multiplier": 1.5,
    "tau": 13920.0,
    "sum_eta": 75.31303231143649,
    "log_contraction": -3.4600819239618636,
    "contraction": 0.03142718727321083
  },
  {
    "peak_multiplier": 2.0,
    "tau": 6960.0,
    "sum_eta": 81.27801885677104,
    "log_contraction": -3.7341908038102747,
    "contraction": 0.023892496965979178
  }
]
```

All nine schedule unit tests pass, including all20001 indices of k1 identity and all late indices for both elevated peaks. No old coupled reciprocal result is treated as evidence against this distinct schedule family.
