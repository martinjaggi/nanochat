# Fixed-family replication extension

17October2026,12:39UTC. The initial primary2x paired heldout deltas on seeds70/71/72 are[-.003867149,+.002515316,+.006819248], mean+.001822472, SD.005376783. No established gain. Before observing any1.5x fresh-seed endpoint, extend ALL THREE previously frozen fixed-WD shapes to new paired seeds80/81/82, with no LR/WD/schedule changes. Nine20k-update/655.36M-token runs, one verified B300 each,1200s limits, same central six-slot/50GPU-hour queue. Expected~2GPUh. No new architecture or hyperparameter choices.

Use the same fixed heldout block6 across both cohorts so paired loss differences have the same evaluation target. The heldout outcomes do not change any settings. Report each new paired difference and each cohort separately, plus descriptive pooled six-seed mean/sampleSD. The extension decision followed the ambiguous first3 result: do not present a six-seed p-value as an originally fixed-sample test. Full static/history contraction controls remain the original3-seed cohort; do not silently claim they have6seeds.

Namesum-earlyalloc-confirm-{baseline,mid,early}-s{80,81,82}; outputs outside Git in the existing project runs root. Every exact scheduler command is printed before submission. No extra online gradient passes or loss searches; only native matrix LR changes.
