# FW-lens paired token-matched confirmation

Geometry: Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l, fixed ordinary unmasked lambda=.1837498798375862. Native Nesterov/five NS/Frobenius and AdamW groups retained. Seed0 tuning only; settings frozen before paired seeds10/11/12 and reserved heldout. Three seeds are limited evidence. Approximate NS and minibatch acceptance do not validate deterministic FW convergence theorems.

| Method | Seed | Updates | Active sec | Heldout CE | Paired delta vs control | Extra batch forwards | Process sec | Overshoot sec |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| control | 10 | 20000 | 661.345 | 3.114569 | +0.000000 | 0 | 741.10 | 0.0000 |
| control | 11 | 20000 | 686.883 | 3.110158 | +0.000000 | 0 | 745.36 | 0.0000 |
| control | 12 | 20000 | 678.993 | 3.114145 | +0.000000 | 0 | 733.38 | 0.0000 |

control: paired heldout deltas mean +0.000000, sample SD 0.000000, n=3.

| joint | 10 | 20000 | 1847.886 | 3.144965 | +0.030396 | 60004 | 1934.59 | 0.0000 |
| joint | 11 | 20000 | 1895.864 | 3.144870 | +0.034712 | 60004 | 1981.90 | 0.0000 |
| joint | 12 | 20000 | 1940.676 | 3.150027 | +0.035882 | 60004 | 2028.32 | 0.0000 |

joint: paired heldout deltas mean +0.033663, sample SD 0.002889, n=3.

| layer | 10 | 20000 | 1787.653 | 3.142940 | +0.028371 | 40000 | 1882.20 | 0.0000 |
| layer | 11 | 20000 | 1644.674 | 3.146095 | +0.035937 | 40000 | 1719.76 | 0.0000 |
| layer | 12 | 20000 | 1582.715 | 3.147678 | +0.033533 | 40000 | 1656.38 | 0.0000 |

layer: paired heldout deltas mean +0.032614, sample SD 0.003866, n=3.

| reciprocal | 10 | 20000 | 665.399 | 3.095999 | -0.018570 | 0 | 720.44 | 0.0000 |
| reciprocal | 11 | 20000 | 660.731 | 3.094969 | -0.015189 | 0 | 718.91 | 0.0000 |
| reciprocal | 12 | 20000 | 620.926 | 3.100018 | -0.014127 | 0 | 673.99 | 0.0000 |

reciprocal: paired heldout deltas mean -0.015962, sample SD 0.002320, n=3.

