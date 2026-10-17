# FW-lens independently scheduled equal-time confirmation

Geometry: Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l, fixed ordinary unmasked lambda=.1837498798375862. Native Nesterov/five NS/Frobenius and AdamW groups retained. Seed0 tuning only; settings frozen before paired seeds10/11/12 and reserved heldout. Three seeds are limited evidence. Approximate NS and minibatch acceptance do not validate deterministic FW convergence theorems.

| Method | Seed | Updates | Active sec | Heldout CE | Paired delta vs control | Extra batch forwards | Process sec | Overshoot sec |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| control | 10 | 20225 | 679.026 | 3.120702 | +0.000000 | 0 | 761.22 | 0.0332 |
| control | 11 | 19762 | 678.994 | 3.113390 | +0.000000 | 0 | 737.06 | 0.0013 |
| control | 12 | 19890 | 679.008 | 3.116667 | +0.000000 | 0 | 732.06 | 0.0148 |

control: paired heldout deltas mean +0.000000, sample SD 0.000000, n=3.

| layer | 10 | 8518 | 679.048 | 3.218791 | +0.098090 | 17036 | 771.10 | 0.0545 |
| layer | 11 | 8406 | 679.060 | 3.218212 | +0.104822 | 16812 | 771.26 | 0.0668 |
| layer | 12 | 7594 | 679.002 | 3.238780 | +0.122113 | 15188 | 770.03 | 0.0089 |

layer: paired heldout deltas mean +0.108342, sample SD 0.012393, n=3.

