# FW-lens v2 live evaluation

Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l; fixed ordinary unmasked lambda=.1837498798375862. Unlike v1 native-shaped rays, shape does not multiply decay. Approximate finite NS/Nesterov/minibatch directions do not reproduce deterministic exact-LMO theorems. Row equilibration and NorMuon are off. Auxiliary AdamW stays frozen during loss checks and updates afterward.

Joint uses positive part after summing directional gaps and a checked global quadratic model. Layer Armijo freezes its per-layer proposal and backtracks one shared multiplier. Smoothed/relative-cap proposals retain that check. Periodic-curvature variants explicitly skip loss checks on intervening updates and have no observed-descent guarantee for those steps.

Token-based schedule curves are descriptive. Independently scheduled equal-time endpoints are reported in FW_LENS_EQUAL_TIME.md after completion. Active time excludes recorded overlapping compiler events and separate validation/checkpoint/setup; new measured runs discard3 warmup updates and reset complete model/optimizer/data/RNG first. Warmup gradient/forward counts and seconds remain in total job cost.

| Run | Family | Budget | Seed | Val CE | Heldout CE | Active sec | Extra batch forwards | Warmup sec | Process sec |
|---|---|---|---:|---:|---:|---:|---:|---:|
| um-lens-check-0-control | cooldown | 64 updates | 0 | 6.414393 | — | 9.359 | 0 | 0.000 | 69.03 |
| um-lens-check-1-joint | joint | 64 updates | 0 | 6.423715 | — | 16.385 | 191 | 0.000 | 94.79 |
| um-lens-check-2-layer | layer | 64 updates | 0 | 6.410152 | — | 15.577 | 133 | 0.000 | 91.23 |
| um-lens-check-3-time-control | cooldown | 2.000s | 0 | 10.394322 | — | 6.459 | 0 | 0.000 | 79.20 |
| um-lens-check-4-time-layer | layer | 2.000s | 0 | 10.394308 | — | 8.964 | 2 | 0.000 | 83.55 |
| um-lens-check-5-creative | layer | 64 updates | 0 | 6.337770 | — | 14.474 | 128 | 0.000 | 96.43 |
| um-lens-check-6-periodic | joint | 64 updates | 0 | 6.490925 | — | 14.250 | 48 | 0.000 | 95.36 |
| um-lens-check-7-warm-time-control | cooldown | 5.000s | 0 | 6.041687 | — | 5.034 | 0 | 34.360 | 81.78 |
| um-lens-check-8-warm-time-layer | layer | 5.000s | 0 | 6.365249 | — | 5.016 | 100 | 31.631 | 85.49 |
| um-lens-main-control-lr0p02 | control | 2000 updates | 0 | 3.568986 | — | 71.320 | 0 | 31.621 | 141.52 |
| um-lens-main-control-lr0p04 | control | 2000 updates | 0 | 3.554822 | — | 65.063 | 0 | 30.883 | 133.67 |
| um-lens-main-control-lr0p08 | control | 2000 updates | 0 | 3.586261 | — | 71.566 | 0 | 31.026 | 139.40 |
| um-lens-main-joint-cooldown-cap0p005 | joint-cooldown | 2000 updates | 0 | 3.559877 | — | 179.120 | 6000 | 30.768 | 252.91 |
| um-lens-main-joint-cooldown-cap0p02 | joint-cooldown | 2000 updates | 0 | 3.583797 | — | 177.306 | 6000 | 31.193 | 251.66 |
| um-lens-main-joint-cooldown-cap0p08 | joint-cooldown | 2000 updates | 0 | 3.782362 | — | 185.210 | 5999 | 40.958 | 274.88 |
| um-lens-main-joint-stable-cap0p005 | joint-stable | 2000 updates | 0 | 3.652983 | — | 185.804 | 5997 | 33.556 | 256.79 |
| um-lens-main-joint-stable-cap0p02 | joint-stable | 2000 updates | 0 | 3.850446 | — | 180.007 | 6001 | 34.063 | 249.81 |
| um-lens-main-joint-stable-cap0p08 | joint-stable | 2000 updates | 0 | 4.107661 | — | 181.760 | 5999 | 31.234 | 246.74 |
| um-lens-main-layer-cooldown-cap0p005 | layer-cooldown | 2000 updates | 0 | 3.561886 | — | 159.589 | 4000 | 32.431 | 227.76 |
| um-lens-main-layer-cooldown-cap0p02 | layer-cooldown | 2000 updates | 0 | 3.586478 | — | 162.107 | 4006 | 32.671 | 230.84 |
| um-lens-main-layer-cooldown-cap0p08 | layer-cooldown | 2000 updates | 0 | 3.775003 | — | 161.803 | 4065 | 40.630 | 254.49 |
| um-lens-main-layer-stable-cap0p005 | layer-stable | 2000 updates | 0 | 3.653949 | — | 178.828 | 4000 | 33.361 | 251.43 |
| um-lens-main-layer-stable-cap0p02 | layer-stable | 2000 updates | 0 | 3.843672 | — | 157.288 | 4004 | 31.804 | 226.67 |
| um-lens-main-layer-stable-cap0p08 | layer-stable | 2000 updates | 0 | 4.177053 | — | 159.261 | 4064 | 31.763 | 223.52 |
| um-lens-main-reciprocal-lr0p02 | reciprocal | 2000 updates | 0 | 3.609994 | — | 67.004 | 0 | 26.860 | 123.51 |
| um-lens-main-reciprocal-lr0p04 | reciprocal | 2000 updates | 0 | 3.610242 | — | 65.990 | 0 | 23.884 | 116.29 |
| um-lens-main-reciprocal-lr0p08 | reciprocal | 2000 updates | 0 | 3.617905 | — | 65.564 | 0 | 40.199 | 149.97 |
| um-lens-refine-control-0 | control | 2000 updates | 0 | 3.559476 | — | 63.222 | 0 | 23.534 | 114.70 |
| um-lens-refine-control-1 | control | 2000 updates | 0 | 3.563508 | — | 61.486 | 0 | 24.116 | 115.07 |

## Adaptive diagnostics and contraction

Contraction is the actual coefficient product_t(1-lambda*eta_l,t), represented in signed log space when necessary. It is not the parameter-norm ratio because the directional term also changes weights. Different schedules retain the same lambda/domain geometry but can have very different cumulative contraction.

| Run | Checked accepted / updates | Unchecked | Median eta | Median gamma | Median curvature | Median backtracks | Contraction log range | Final spectral ratio max |
|---|---|---:|---:|---:|---:|---:|---|---:|
| um-lens-check-1-joint | 64/64 | 0 | 0.0095598 | 0.0017566 | 0.005 | 1 | -0.1136 to -0.1136 | 0.379967 |
| um-lens-check-2-layer | 64/64 | 0 | 0.015 | 0.0027562 | 2.794e-11 | 1 | -0.1571 to -0.1473 | 0.40221 |
| um-lens-check-4-time-layer | 1/1 | 0 | 0 | 0 | 0.005 | 1 | -9.188e-05 to 0 | 0.368177 |
| um-lens-check-5-creative | 64/64 | 0 | 0.011606 | 0.0021326 | 1.7462e-12 | 1 | -0.1297 to -0.09009 | 0.379675 |
| um-lens-check-6-periodic | 16/64 | 48 | 0.0042842 | 0.00078723 | 0.0075 | 0 | -0.06363 to -0.06363 | 0.366569 |
| um-lens-check-8-warm-time-layer | 50/50 | 0 | 0.02 | 0.003675 | 2.2352e-10 | 1 | -0.179 to -0.1481 | 0.537713 |
| um-lens-main-joint-cooldown-cap0p005 | 2000/2000 | 0 | 0.0037961 | 0.00069753 | 0.02 | 2 | -1.251 to -1.251 | 0.331184 |
| um-lens-main-joint-cooldown-cap0p02 | 2000/2000 | 0 | 0.014877 | 0.0027337 | 0.01 | 2 | -4.967 to -4.967 | 0.424789 |
| um-lens-main-joint-cooldown-cap0p08 | 2000/2000 | 0 | 0.038481 | 0.0070708 | 0.005 | 2 | -14.06 to -14.06 | 0.444955 |
| um-lens-main-joint-stable-cap0p005 | 1997/2000 | 0 | 0.005 | 0.00091875 | 0.02 | 2 | -1.817 to -1.817 | 0.305381 |
| um-lens-main-joint-stable-cap0p02 | 2000/2000 | 0 | 0.02 | 0.003675 | 0.01 | 2 | -7.221 to -7.221 | 0.455097 |
| um-lens-main-joint-stable-cap0p08 | 2000/2000 | 0 | 0.057202 | 0.010511 | 0.0025 | 2 | -20.46 to -20.46 | 0.780575 |
| um-lens-main-layer-cooldown-cap0p005 | 2000/2000 | 0 | 0.0037906 | 0.00069652 | 1e-16 | 1 | -1.253 to -1.225 | 0.330668 |
| um-lens-main-layer-cooldown-cap0p02 | 2000/2000 | 0 | 0.015118 | 0.002778 | 1e-16 | 1 | -5.01 to -4.851 | 0.420678 |
| um-lens-main-layer-cooldown-cap0p08 | 2000/2000 | 0 | 0.058428 | 0.010736 | 1e-16 | 1 | -19.79 to -18.76 | 0.404548 |
| um-lens-main-layer-stable-cap0p005 | 2000/2000 | 0 | 0.005 | 0.00091875 | 1e-16 | 1 | -1.82 to -1.8 | 0.305951 |
| um-lens-main-layer-stable-cap0p02 | 2000/2000 | 0 | 0.02 | 0.003675 | 1e-16 | 1 | -7.286 to -7.098 | 0.460939 |
| um-lens-main-layer-stable-cap0p08 | 2000/2000 | 0 | 0.08 | 0.0147 | 1e-16 | 1 | -28.98 to -27.8 | 0.790492 |

Curvature values in Armijo variants parameterize proposals; their acceptance is NOT a certificate of the quadratic upper model. Final spectral ratios are lambda*||W_l||op/c_l; native approximate NS output is not certified to have unit spectral norm. Initial/final iterate feasibility alone does not certify oracle accuracy. Cold two-second clock checks intentionally permit one-update overshoot; do not use them as quality endpoints.
