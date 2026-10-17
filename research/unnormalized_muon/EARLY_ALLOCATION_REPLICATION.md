# Frozen early-allocation family: paired replication

All arms use ordinary fixed WD .04593746995939655, actual join LR .005 and identical late65% cooldown. Peak multipliers1/1.5/2 were frozen using seed0 development only. Initial cohort70/71/72; extension80/81/82. The extension was fixed after the ambiguous initial2x result, before any1.5x heldout endpoint: this is descriptive pilot evidence, not an originally fixed-sample significance test. Same heldoutblock6 and262144 targets. [Extension protocol](EARLY_ALLOCATION_REPLICATION_PROTOCOL.md).

| Seed | Arm | Heldout CE | CE minus paired baseline | Active seconds | Fresh Mtoken/s |
|---|---|---:|---:|---:|---:|
| 70 | baseline | 3.132268906 | +0.000000000 | 725.066 | 0.9039 |
| 70 | mid | 3.130945206 | -0.001323700 | 652.872 | 1.0038 |
| 70 | early | 3.128401756 | -0.003867149 | 739.097 | 0.8867 |
| 71 | baseline | 3.126216650 | +0.000000000 | 743.643 | 0.8813 |
| 71 | mid | 3.127163172 | +0.000946522 | 688.761 | 0.9515 |
| 71 | early | 3.128731966 | +0.002515316 | 714.832 | 0.9168 |
| 72 | baseline | 3.132172585 | +0.000000000 | 722.159 | 0.9075 |
| 72 | mid | 3.137712240 | +0.005539656 | 691.419 | 0.9478 |
| 72 | early | 3.138991833 | +0.006819248 | 701.115 | 0.9347 |
| 80 | baseline | 3.127713203 | +0.000000000 | 635.789 | 1.0308 |
| 81 | baseline | 3.132445335 | +0.000000000 | 666.782 | 0.9829 |
| 82 | baseline | 3.129633188 | +0.000000000 | 647.532 | 1.0121 |

mid/initial3: n=3, mean **+0.001721CE**, sampleSD **0.003497**.

mid/pooled6: n=3, mean **+0.001721CE**, sampleSD **0.003497**.

early/initial3: n=3, mean **+0.001822CE**, sampleSD **0.005377**.

early/pooled6: n=3, mean **+0.001822CE**, sampleSD **0.005377**.

Negative deltas favor the early reciprocal arm. No setting is retuned from these heldout results. Static/history contraction controls have3seeds only and are reported separately. Token-matched endpoints contain the same gradient count and native optimizer pipeline. Different wall times across jobs are descriptive; no independent equal-time result is implied.125829354 trainable parameters,655360000 update-data tokens/run,5.2083tokens/parameter. Finite NS/BF16/Nesterov and these stochastic outcomes establish no deterministic FW theorem.

![Frozen-family replication](EARLY_ALLOCATION_REPLICATION.png)
