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
| um-lens-confirm-control-s10 | control | 20000 updates | 10 | 3.167631 | 3.114569 | 661.345 | 0 | 33.696 | 741.10 |
| um-lens-confirm-control-s11 | control | 20000 updates | 11 | 3.164999 | 3.110158 | 686.883 | 0 | 25.427 | 745.36 |
| um-lens-confirm-control-s12 | control | 20000 updates | 12 | 3.169816 | 3.114145 | 678.993 | 0 | 23.899 | 733.38 |
| um-lens-confirm-joint-s10 | joint-cooldown | 20000 updates | 10 | 3.198918 | 3.144965 | 1847.886 | 60004 | 38.446 | 1934.59 |
| um-lens-confirm-joint-s11 | joint-cooldown | 20000 updates | 11 | 3.201077 | 3.144870 | 1895.864 | 60004 | 38.133 | 1981.90 |
| um-lens-confirm-joint-s12 | joint-cooldown | 20000 updates | 12 | 3.206757 | 3.150027 | 1940.676 | 60004 | 38.451 | 2028.32 |
| um-lens-creative-ema0p5 | layer-ema | 2000 updates | 0 | 3.555660 | — | 177.247 | 4000 | 33.839 | 247.79 |
| um-lens-creative-ema0p9 | layer-ema | 2000 updates | 0 | 3.558717 | — | 165.360 | 4000 | 31.419 | 229.92 |
| um-lens-creative-periodic2 | joint-periodic | 2000 updates | 0 | 3.554936 | — | 151.717 | 3001 | 43.345 | 243.89 |
| um-lens-creative-periodic4 | joint-periodic | 2000 updates | 0 | 3.556331 | — | 142.721 | 1501 | 43.339 | 235.46 |
| um-lens-creative-relative0p01 | layer-relative | 2000 updates | 0 | 3.568293 | — | 171.388 | 4000 | 43.342 | 263.55 |
| um-lens-creative-relative0p03 | layer-relative | 2000 updates | 0 | 3.553957 | — | 158.188 | 4000 | 43.444 | 249.47 |
| um-lens-long-control-0 | control | 20000 updates | 0 | 3.199618 | — | 713.370 | 0 | 32.972 | 788.71 |
| um-lens-long-control-1 | control | 20000 updates | 0 | 3.168332 | — | 725.928 | 0 | 27.617 | 786.20 |
| um-lens-long-creative-0 | layer-relative | 20000 updates | 0 | 3.199090 | — | 1768.006 | 40000 | 30.485 | 1834.23 |
| um-lens-long-creative-1 | layer-relative | 20000 updates | 0 | 3.207725 | — | 1754.781 | 40000 | 37.338 | 1837.54 |
| um-lens-long-joint-cooldown | joint-cooldown | 20000 updates | 0 | 3.200458 | — | 1848.045 | 60004 | 37.306 | 1931.00 |
| um-lens-long-joint-stable | joint-stable | 20000 updates | 0 | 3.319987 | — | 1784.904 | 59997 | 37.519 | 1867.68 |
| um-lens-long-layer-cooldown | layer-cooldown | 20000 updates | 0 | 3.197616 | — | 1734.180 | 40000 | 40.173 | 1828.08 |
| um-lens-long-layer-stable | layer-stable | 20000 updates | 0 | 3.321643 | — | 1739.162 | 40000 | 33.896 | 1813.94 |
| um-lens-long-reciprocal-0 | reciprocal | 20000 updates | 0 | 3.155148 | — | 713.568 | 0 | 25.885 | 770.45 |
| um-lens-long-reciprocal-1 | reciprocal | 20000 updates | 0 | 3.155272 | — | 710.093 | 0 | 24.827 | 762.24 |
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
| um-lens-refine-joint-cooldown-0 | joint-cooldown | 2000 updates | 0 | 3.623444 | — | 190.861 | 5997 | 38.859 | 274.70 |
| um-lens-refine-joint-cooldown-1 | joint-cooldown | 2000 updates | 0 | 3.555091 | — | 172.412 | 6001 | 38.700 | 256.27 |
| um-lens-refine-joint-stable-0 | joint-stable | 2000 updates | 0 | 3.645341 | — | 173.432 | 5995 | 39.220 | 257.49 |
| um-lens-refine-joint-stable-1 | joint-stable | 2000 updates | 0 | 3.727101 | — | 176.259 | 6001 | 40.371 | 262.87 |
| um-lens-refine-layer-cooldown-0 | layer-cooldown | 2000 updates | 0 | 3.617586 | — | 158.738 | 4000 | 31.476 | 227.00 |
| um-lens-refine-layer-cooldown-1 | layer-cooldown | 2000 updates | 0 | 3.554595 | — | 159.333 | 4000 | 30.112 | 222.00 |
| um-lens-refine-layer-stable-0 | layer-stable | 2000 updates | 0 | 3.648631 | — | 155.370 | 4000 | 39.737 | 239.27 |
| um-lens-refine-layer-stable-1 | layer-stable | 2000 updates | 0 | 3.733664 | — | 152.883 | 4000 | 39.778 | 236.90 |
| um-lens-refine-reciprocal-0 | reciprocal | 2000 updates | 0 | 3.639452 | — | 64.039 | 0 | 25.945 | 120.04 |
| um-lens-startl-joint-cooldown-0 | joint-cooldown | 2000 updates | 0 | 3.560580 | — | 181.701 | 6004 | 32.826 | 251.61 |
| um-lens-startl-joint-cooldown-1 | joint-cooldown | 2000 updates | 0 | 3.561008 | — | 186.784 | 5999 | 32.422 | 256.03 |
| um-lens-startl-joint-stable-0 | joint-stable | 2000 updates | 0 | 3.653051 | — | 163.841 | 6003 | 38.425 | 247.21 |
| um-lens-startl-joint-stable-1 | joint-stable | 2000 updates | 0 | 3.654224 | — | 164.874 | 5999 | 38.396 | 247.97 |
| um-lens-startl-layer-cooldown-0 | layer-cooldown | 2000 updates | 0 | 3.560975 | — | 157.831 | 4000 | 38.386 | 241.03 |
| um-lens-startl-layer-cooldown-1 | layer-cooldown | 2000 updates | 0 | 3.562346 | — | 155.110 | 4000 | 40.323 | 241.40 |
| um-lens-startl-layer-stable-0 | layer-stable | 2000 updates | 0 | 3.654067 | — | 179.069 | 4000 | 31.795 | 247.29 |
| um-lens-startl-layer-stable-1 | layer-stable | 2000 updates | 0 | 3.653376 | — | 169.669 | 4000 | 31.552 | 237.19 |

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
| um-lens-confirm-joint-s10 | 20000/20000 | 0 | 0.0077854 | 0.0014306 | 0.02 | 2 | -25.39 to -25.39 | 0.298774 |
| um-lens-confirm-joint-s11 | 20000/20000 | 0 | 0.0077854 | 0.0014306 | 0.02 | 2 | -25.39 to -25.39 | 0.26652 |
| um-lens-confirm-joint-s12 | 20000/20000 | 0 | 0.0077854 | 0.0014306 | 0.02 | 2 | -25.39 to -25.39 | 0.307328 |
| um-lens-creative-ema0p5 | 2000/2000 | 0 | 0.0075738 | 0.0013917 | 1e-16 | 1 | -2.506 to -2.438 | 0.405719 |
| um-lens-creative-ema0p9 | 2000/2000 | 0 | 0.0074569 | 0.0013702 | 1e-16 | 1 | -2.491 to -2.298 | 0.410554 |
| um-lens-creative-periodic2 | 1000/2000 | 1000 | 0.0075921 | 0.0013951 | 0.01 | 0.5 | -2.507 to -2.507 | 0.389011 |
| um-lens-creative-periodic4 | 500/2000 | 1500 | 0.0075775 | 0.0013924 | 0.01 | 0 | -2.506 to -2.506 | 0.391067 |
| um-lens-creative-relative0p01 | 2000/2000 | 0 | 0.0055887 | 0.0010269 | 1e-16 | 1 | -2.303 to -1.682 | 0.381307 |
| um-lens-creative-relative0p03 | 2000/2000 | 0 | 0.0075885 | 0.0013944 | 1e-16 | 1 | -2.507 to -2.467 | 0.39891 |
| um-lens-long-creative-0 | 20000/20000 | 0 | 0.0077807 | 0.0014297 | 1e-16 | 1 | -25.39 to -24.96 | 0.300626 |
| um-lens-long-creative-1 | 20000/20000 | 0 | 0.0067442 | 0.0012393 | 1e-16 | 1 | -24.86 to -19.56 | 0.305307 |
| um-lens-long-joint-cooldown | 20000/20000 | 0 | 0.0077839 | 0.0014303 | 0.02 | 2 | -25.39 to -25.39 | 0.287582 |
| um-lens-long-joint-stable | 19996/20000 | 0 | 0.0025 | 0.00045937 | 0.04 | 2 | -9.179 to -9.179 | 0.285411 |
| um-lens-long-layer-cooldown | 20000/20000 | 0 | 0.0077807 | 0.0014297 | 1e-16 | 1 | -25.39 to -25.02 | 0.301371 |
| um-lens-long-layer-stable | 20000/20000 | 0 | 0.0025 | 0.00045937 | 1e-16 | 1 | -9.181 to -9.04 | 0.286561 |
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
| um-lens-refine-joint-cooldown-0 | 1996/2000 | 0 | 0.001898 | 0.00034876 | 0.04 | 2 | -0.625 to -0.625 | 0.308598 |
| um-lens-refine-joint-cooldown-1 | 2000/2000 | 0 | 0.0075921 | 0.0013951 | 0.01 | 2 | -2.507 to -2.507 | 0.39888 |
| um-lens-refine-joint-stable-0 | 1996/2000 | 0 | 0.0025 | 0.00045937 | 0.04 | 2 | -0.9084 to -0.9084 | 0.287777 |
| um-lens-refine-joint-stable-1 | 2000/2000 | 0 | 0.01 | 0.0018375 | 0.01 | 2 | -3.642 to -3.642 | 0.361899 |
| um-lens-refine-layer-cooldown-0 | 2000/2000 | 0 | 0.0018953 | 0.00034826 | 1e-16 | 1 | -0.6265 to -0.6088 | 0.305577 |
| um-lens-refine-layer-cooldown-1 | 2000/2000 | 0 | 0.0075885 | 0.0013944 | 1e-16 | 1 | -2.507 to -2.476 | 0.397119 |
| um-lens-refine-layer-stable-0 | 2000/2000 | 0 | 0.0025 | 0.00045937 | 1e-16 | 1 | -0.91 to -0.8921 | 0.286501 |
| um-lens-refine-layer-stable-1 | 2000/2000 | 0 | 0.01 | 0.0018375 | 1e-16 | 1 | -3.643 to -3.604 | 0.375865 |
| um-lens-startl-joint-cooldown-0 | 1999/2000 | 0 | 0.0037961 | 0.00069753 | 0.032 | 2 | -1.249 to -1.249 | 0.330205 |
| um-lens-startl-joint-cooldown-1 | 2000/2000 | 0 | 0.0037961 | 0.00069753 | 0.025 | 2 | -1.251 to -1.251 | 0.329844 |
| um-lens-startl-joint-stable-0 | 1998/2000 | 0 | 0.005 | 0.00091875 | 0.032 | 2 | -1.817 to -1.817 | 0.308162 |
| um-lens-startl-joint-stable-1 | 2000/2000 | 0 | 0.005 | 0.00091875 | 0.025 | 2 | -1.819 to -1.819 | 0.30593 |
| um-lens-startl-layer-cooldown-0 | 2000/2000 | 0 | 0.0037906 | 0.00069652 | 1e-16 | 1 | -1.253 to -1.227 | 0.329018 |
| um-lens-startl-layer-cooldown-1 | 2000/2000 | 0 | 0.0037942 | 0.00069719 | 1e-16 | 1 | -1.253 to -1.229 | 0.32947 |
| um-lens-startl-layer-stable-0 | 2000/2000 | 0 | 0.005 | 0.00091875 | 1e-16 | 1 | -1.82 to -1.801 | 0.306437 |
| um-lens-startl-layer-stable-1 | 2000/2000 | 0 | 0.005 | 0.00091875 | 1e-16 | 1 | -1.82 to -1.793 | 0.309576 |

Curvature values in Armijo variants parameterize proposals; their acceptance is NOT a certificate of the quadratic upper model. Final spectral ratios are lambda*||W_l||op/c_l; native approximate NS output is not certified to have unit spectral norm. Initial/final iterate feasibility alone does not certify oracle accuracy. Cold two-second clock checks intentionally permit one-update overshoot; do not use them as quality endpoints.
