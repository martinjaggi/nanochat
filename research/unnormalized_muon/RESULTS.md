# Live unnormalized-Muon results

One B300 per job. CE is token cross-entropy (nats); lower is better. Rows with different update budgets are not endpoint comparisons. Tuning uses the same fixed validation tokens; held-out scores appear only on final runs. Runtime includes compilation and overhead in process seconds.

| Run | Method | Updates | Seed | CLI matrix LR | Val CE | Val BPB | Heldout CE | Process sec |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| um-check-fw-compiled-armijo-001 | Clean FW backtracking gradient Rfactor2 armijo compiled | 64 | 0 | 0.02 | 6.504589 | 1.971300 | — | 98.66 |
| um-check-fw-compiled-smoothness-001 | Clean FW backtracking gradient Rfactor2 smoothness compiled | 64 | 0 | 0.02 | 6.400337 | 1.939558 | — | 82.56 |
| um-check-fw-derivative-001 | Clean FW backtracking gradient Rfactor2 smoothness eager | 48 | 0 | 0.02 | 6.648578 | 2.014818 | — | 121.14 |
| um-check-fw-gradient-001 | Clean FW backtracking gradient Rfactor2 smoothness eager | 64 | 0 | 0.02 | 6.488285 | 1.966192 | — | 110.84 |
| um-check-fw-momentum-001 | Clean FW backtracking momentum Rfactor2 smoothness eager | 64 | 0 | 0.02 | 6.470441 | 1.960795 | — | 110.11 |
| um-check-wd-002 | Clean Unnormalized cooldown WD:standard(0.0175) | 64 | 0 | 0.64 | 6.607081 | 2.002237 | — | 85.90 |
| um-clean-calibration-001 | Clean Native cooldown | 256 | 0 | 0.02 | 5.270988 | 1.597709 | — | 86.86 |
| um-clean-fw-accumcheck-001 | Clean FW backtracking momentum Rfactor2 smoothness eager | 16 | 0 | 0.02 | 9.061382 | 2.745550 | — | 124.31 |
| um-clean-grid-00-0-normalized-lr0p005 | Clean Native cooldown | 2000 | 0 | 0.005 | 3.756841 | 1.138807 | — | 157.45 |
| um-clean-grid-00-1-cooldown-lr0p02 | Clean Unnormalized cooldown | 2000 | 0 | 0.02 | 3.859137 | 1.169816 | — | 164.02 |
| um-clean-grid-00-2-constant-lr0p02 | Clean Unnormalized constant | 2000 | 0 | 0.02 | 3.863261 | 1.171071 | — | 157.17 |
| um-clean-grid-01-0-normalized-lr0p01 | Clean Native cooldown | 2000 | 0 | 0.01 | 3.635674 | 1.102157 | — | 142.86 |
| um-clean-grid-01-1-cooldown-lr0p04 | Clean Unnormalized cooldown | 2000 | 0 | 0.04 | 3.828638 | 1.160576 | — | 151.79 |
| um-clean-grid-01-2-constant-lr0p04 | Clean Unnormalized constant | 2000 | 0 | 0.04 | 3.803687 | 1.153028 | — | 146.02 |
| um-clean-grid-02-0-normalized-lr0p02 | Clean Native cooldown | 2000 | 0 | 0.02 | 3.586015 | 1.087084 | — | 147.46 |
| um-clean-grid-02-1-cooldown-lr0p08 | Clean Unnormalized cooldown | 2000 | 0 | 0.08 | 3.786540 | 1.147820 | — | 152.80 |
| um-clean-grid-02-2-constant-lr0p08 | Clean Unnormalized constant | 2000 | 0 | 0.08 | 3.797298 | 1.151089 | — | 148.10 |
| um-clean-grid-03-0-normalized-lr0p04 | Clean Native cooldown | 2000 | 0 | 0.04 | 3.563474 | 1.080265 | — | 138.61 |
| um-clean-grid-03-1-cooldown-lr0p16 | Clean Unnormalized cooldown | 2000 | 0 | 0.16 | 3.731434 | 1.131155 | — | 149.79 |
| um-clean-grid-03-2-constant-lr0p16 | Clean Unnormalized constant | 2000 | 0 | 0.16 | 3.754476 | 1.138109 | — | 146.15 |
| um-clean-grid-04-0-normalized-lr0p08 | Clean Native cooldown | 2000 | 0 | 0.08 | 3.563980 | 1.080480 | — | 145.26 |
| um-clean-grid-04-1-cooldown-lr0p32 | Clean Unnormalized cooldown | 2000 | 0 | 0.32 | 3.698252 | 1.121036 | — | 157.86 |
| um-clean-grid-04-2-constant-lr0p32 | Clean Unnormalized constant | 2000 | 0 | 0.32 | 3.728677 | 1.130279 | — | 151.60 |
| um-clean-grid-05-1-cooldown-lr0p64 | Clean Unnormalized cooldown | 2000 | 0 | 0.64 | 3.683407 | 1.116578 | — | 157.17 |
| um-clean-grid-05-2-constant-lr0p64 | Clean Unnormalized constant | 2000 | 0 | 0.64 | 3.722817 | 1.128555 | — | 158.73 |
| um-clean-grid-06-1-cooldown-lr1p28 | Clean Unnormalized cooldown | 2000 | 0 | 1.28 | 3.785215 | 1.147408 | — | 148.29 |
| um-clean-grid-06-2-constant-lr1p28 | Clean Unnormalized constant | 2000 | 0 | 1.28 | 3.965584 | 1.202138 | — | 158.23 |
| um-clean-grid-07-1-cooldown-lr2p56 | Clean Unnormalized cooldown | 2000 | 0 | 2.56 | 4.333797 | 1.313749 | — | 154.67 |
| um-clean-grid-07-2-constant-lr2p56 | Clean Unnormalized constant | 2000 | 0 | 2.56 | 4.136932 | 1.254105 | — | 149.27 |
| um-clean-grid-08-1-cooldown-lr5p12 | Clean Unnormalized cooldown | 2000 | 0 | 5.12 | 4.498638 | 1.363555 | — | 152.28 |
| um-clean-grid-08-2-constant-lr5p12 | Clean Unnormalized constant | 2000 | 0 | 5.12 | 4.496089 | 1.362771 | — | 153.52 |
| um-clean-long-0-0-normalized-lr0p04 | Clean Native cooldown | 20000 | 0 | 0.04 | 3.107198 | 0.942041 | — | 743.22 |
| um-clean-long-0-1-cooldown-lr0p64 | Clean Unnormalized cooldown | 20000 | 0 | 0.64 | 3.168528 | 0.960609 | — | 779.28 |
| um-clean-long-0-2-constant-lr0p64 | Clean Unnormalized constant | 20000 | 0 | 0.64 | 3.210816 | 0.973451 | — | 737.52 |
| um-clean-long-1-0-normalized-lr0p08 | Clean Native cooldown | 20000 | 0 | 0.08 | 3.112453 | 0.943630 | — | 755.24 |
| um-clean-long-1-1-cooldown-lr0p32 | Clean Unnormalized cooldown | 20000 | 0 | 0.32 | 3.168984 | 0.960728 | — | 754.69 |
| um-clean-long-1-2-constant-lr0p32 | Clean Unnormalized constant | 20000 | 0 | 0.32 | 3.209921 | 0.973169 | — | 765.35 |
| um-clean-long-2-fw-pilot | Clean FW backtracking momentum Rfactor2 smoothness eager | 2000 | 0 | 0.02 | 4.185817 | 1.268782 | — | 409.98 |
| um-earlyalloc-confirm-baseline-s70 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 70 | 0.02 | 3.091088 | 0.937149 | 3.132269 | 784.34 |
| um-earlyalloc-confirm-baseline-s71 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 71 | 0.02 | 3.085667 | 0.935485 | 3.126217 | 798.23 |
| um-earlyalloc-confirm-baseline-s72 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 72 | 0.02 | 3.089873 | 0.936781 | 3.132173 | 783.07 |
| um-earlyalloc-confirm-baseline-s80 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 80 | 0.02 | 3.085548 | 0.935477 | 3.127713 | 695.15 |
| um-earlyalloc-confirm-baseline-s81 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 81 | 0.02 | 3.086114 | 0.935633 | 3.132445 | 720.02 |
| um-earlyalloc-confirm-baseline-s82 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 82 | 0.02 | 3.088922 | 0.936494 | 3.129633 | 707.03 |
| um-earlyalloc-confirm-early-s70 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 70 | 0.02 | 3.088452 | 0.936346 | 3.128402 | 794.05 |
| um-earlyalloc-confirm-early-s71 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 71 | 0.02 | 3.086768 | 0.935854 | 3.128732 | 770.47 |
| um-earlyalloc-confirm-early-s72 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 72 | 0.02 | 3.097495 | 0.939100 | 3.138992 | 758.31 |
| um-earlyalloc-confirm-early-s80 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 80 | 0.02 | 3.090832 | 0.937032 | 3.130208 | 759.04 |
| um-earlyalloc-confirm-early-s81 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 81 | 0.02 | 3.090599 | 0.937002 | 3.131149 | 753.52 |
| um-earlyalloc-confirm-early-s82 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 82 | 0.02 | 3.085357 | 0.935421 | 3.127331 | 790.92 |
| um-earlyalloc-confirm-history-check-002 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 128 | 0 | 0.02 | 5.910295 | 1.791403 | — | 61.07 |
| um-earlyalloc-confirm-matched-s70 | Clean Native cooldown fixed_lambda=0.0551271 WD:standard(0) | 20000 | 70 | 0.02 | 3.091825 | 0.937357 | 3.133393 | 747.43 |
| um-earlyalloc-confirm-matched-s71 | Clean Native cooldown fixed_lambda=0.0551271 WD:standard(0) | 20000 | 71 | 0.02 | 3.087015 | 0.935905 | 3.127414 | 743.56 |
| um-earlyalloc-confirm-matched-s72 | Clean Native cooldown fixed_lambda=0.0551271 WD:standard(0) | 20000 | 72 | 0.02 | 3.091281 | 0.937221 | 3.133921 | 779.60 |
| um-earlyalloc-confirm-mid-s70 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 70 | 0.02 | 3.088300 | 0.936291 | 3.130945 | 714.18 |
| um-earlyalloc-confirm-mid-s71 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 71 | 0.02 | 3.085330 | 0.935397 | 3.127163 | 769.38 |
| um-earlyalloc-confirm-mid-s72 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 72 | 0.02 | 3.098647 | 0.939434 | 3.137712 | 771.85 |
| um-earlyalloc-confirm-mid-s80 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 80 | 0.02 | 3.088423 | 0.936321 | 3.130561 | 740.81 |
| um-earlyalloc-confirm-mid-s81 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 81 | 0.02 | 3.090870 | 0.937089 | 3.133066 | 717.19 |
| um-earlyalloc-confirm-mid-s82 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 82 | 0.02 | 3.088668 | 0.936423 | 3.130228 | 696.33 |
| um-earlyalloc-confirm-neutral-s70 | Clean Native cooldown fixed_lambda=0.0382798 WD:standard(0) | 20000 | 70 | 0.02 | 3.087880 | 0.936181 | 3.128062 | 806.59 |
| um-earlyalloc-confirm-neutral-s71 | Clean Native cooldown fixed_lambda=0.0382798 WD:standard(0) | 20000 | 71 | 0.02 | 3.086275 | 0.935689 | 3.128008 | 700.68 |
| um-earlyalloc-confirm-neutral-s72 | Clean Native cooldown fixed_lambda=0.0382798 WD:standard(0) | 20000 | 72 | 0.02 | 3.098150 | 0.939295 | 3.139013 | 712.74 |
| um-earlyalloc-screen-k1 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.090448 | 0.936955 | — | 783.18 |
| um-earlyalloc-screen-k1p5 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.089904 | 0.936790 | — | 701.43 |
| um-earlyalloc-screen-k2 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.089891 | 0.936781 | — | 790.30 |
| um-follow-confirm20000-control-s20 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 20 | 0.01 | 3.111594 | 0.943356 | 3.112870 | 729.25 |
| um-follow-confirm20000-control-s21 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 21 | 0.01 | 3.111298 | 0.943268 | 3.113533 | 751.79 |
| um-follow-confirm20000-control-s22 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 22 | 0.01 | 3.110596 | 0.943063 | 3.113324 | 755.31 |
| um-follow-confirm20000-reciprocal-s20 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 20 | 0.0282843 | 3.157425 | 0.957236 | 3.156672 | 741.30 |
| um-follow-confirm20000-reciprocal-s21 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 21 | 0.0282843 | 3.162671 | 0.958888 | 3.161026 | 745.00 |
| um-follow-confirm20000-reciprocal-s22 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 22 | 0.0282843 | 3.149971 | 0.955006 | 3.154069 | 782.37 |
| um-follow-edge0-control-lr0p005 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.119279 | 0.945707 | — | 719.39 |
| um-follow-first-time-reciprocal-s10 | Clean Muon shifted reciprocal time679.0s fixed_lambda=0.18375 WD:standard(0) | 20740 | 10 | 0.02 | 3.154321 | 0.956268 | 3.095921 | 733.36 |
| um-follow-first-time-reciprocal-s11 | Clean Muon shifted reciprocal time679.0s fixed_lambda=0.18375 WD:standard(0) | 20007 | 11 | 0.02 | 3.156209 | 0.956928 | 3.099467 | 734.10 |
| um-follow-first-time-reciprocal-s12 | Clean Muon shifted reciprocal time679.0s fixed_lambda=0.18375 WD:standard(0) | 18127 | 12 | 0.02 | 3.161711 | 0.958558 | 3.105612 | 750.97 |
| um-follow-first-tune-control-lr0p01 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.112087 | 0.943514 | — | 777.47 |
| um-follow-first-tune-control-lr0p02 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.142251 | 0.952650 | — | 767.69 |
| um-follow-first-tune-reciprocal-lr0p01 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.156622 | 0.957022 | — | 744.07 |
| um-follow-mid-control-high | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.0141421 | 3.122182 | 0.946575 | — | 738.56 |
| um-follow-mid-control-low | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.00707107 | 3.113318 | 0.943880 | — | 775.02 |
| um-follow-mid-reciprocal-high | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.0282843 | 3.152773 | 0.955841 | — | 721.58 |
| um-follow-mid-reciprocal-low | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.0141421 | 3.152943 | 0.955902 | — | 727.28 |
| um-fresh-diagnosis-001 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.557051 | 1.078327 | — | 340.47 |
| um-fresh-wd-mixing | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.555051 | 1.077723 | — | 149.73 |
| um-fresh-wd-static-product | Clean Native cooldown fixed_lambda=0.153864 WD:standard(0) | 2000 | 0 | 0.04 | 3.553682 | 1.077298 | — | 123.04 |
| um-fw-diagnostic-001 | FW backtracking momentum Rfactor2 smoothness eager | 64 | 0 | 0.02 | 6.469995 | 1.960658 | — | 95.07 |
| um-fw-diagnostic-002 | FW backtracking momentum Rfactor2 smoothness eager | 64 | 0 | 0.02 | 6.900428 | 2.091122 | — | 117.14 |
| um-gapwd-first-cosine-001 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.415227 | 1.944031 | — | 76.24 |
| um-gapwd-first-layer-001 | Clean GapWD layer uniform quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.463019 | 1.958715 | — | 91.78 |
| um-gapwd-first-reciprocal-001 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.374067 | 1.931619 | — | 77.77 |
| um-gapwd-joint-native-001 | Clean GapWD joint native quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.369767 | 1.930554 | — | 94.57 |
| um-gapwd-joint-uniform-001 | Clean GapWD joint uniform quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.390594 | 1.936845 | — | 95.12 |
| um-gapwd-pilot-cosine-lr0p02 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.02 | 3.577361 | 1.084476 | — | 142.48 |
| um-gapwd-pilot-cosine-lr0p04 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.575844 | 1.084019 | — | 135.71 |
| um-gapwd-pilot-cosine-lr0p08 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.08 | 3.610093 | 1.094412 | — | 136.39 |
| um-gapwd-pilot-joint | Clean GapWD joint uniform quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 4.149021 | 1.257653 | — | 254.05 |
| um-gapwd-pilot-joint-native | Clean GapWD joint native quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 4.120519 | 1.249007 | — | 266.55 |
| um-gapwd-pilot-layer | Clean GapWD layer uniform quadratic cap0/none fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 4.186773 | 1.269013 | — | 269.44 |
| um-gapwd-pilot-reciprocal-lr0p02 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.02 | 3.622123 | 1.098062 | — | 144.58 |
| um-gapwd-pilot-reciprocal-lr0p04 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.625030 | 1.098942 | — | 138.08 |
| um-gapwd-pilot-reciprocal-lr0p08 | Clean Muon shifted reciprocal fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.08 | 3.627100 | 1.099613 | — | 138.60 |
| um-lens-check-0-control | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.414393 | 1.943777 | — | 69.03 |
| um-lens-check-1-joint | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.423715 | 1.946793 | — | 94.79 |
| um-lens-check-2-layer | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.410152 | 1.942776 | — | 91.23 |
| um-lens-check-3-time-control | Clean Native cooldown v2 c-in-Q time2.0s fixed_lambda=0.18375 WD:standard(0) | 1 | 0 | 0.04 | 10.394322 | 3.148570 | — | 79.20 |
| um-lens-check-4-time-layer | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/stable time2.0s fixed_lambda=0.18375 WD:standard(0) | 1 | 0 | 0.04 | 10.394308 | 3.148566 | — | 83.55 |
| um-lens-check-5-creative | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.337770 | 1.920751 | — | 96.43 |
| um-lens-check-6-periodic | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.04 | 6.490925 | 1.967030 | — | 95.36 |
| um-lens-check-7-warm-time-control | Clean Native cooldown v2 c-in-Q time5.0s fixed_lambda=0.18375 WD:standard(0) | 96 | 0 | 0.04 | 6.041687 | 1.831145 | — | 81.78 |
| um-lens-check-8-warm-time-layer | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/stable time5.0s fixed_lambda=0.18375 WD:standard(0) | 50 | 0 | 0.04 | 6.365249 | 1.929079 | — | 85.49 |
| um-lens-confirm-control-s10 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 10 | 0.0282843 | 3.167631 | 0.960357 | 3.114569 | 741.10 |
| um-lens-confirm-control-s11 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 11 | 0.0282843 | 3.164999 | 0.959575 | 3.110158 | 745.36 |
| um-lens-confirm-control-s12 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 12 | 0.0282843 | 3.169816 | 0.960987 | 3.114145 | 733.38 |
| um-lens-confirm-joint-s10 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 10 | 0.04 | 3.198918 | 0.969828 | 3.144965 | 1934.59 |
| um-lens-confirm-joint-s11 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 11 | 0.04 | 3.201077 | 0.970477 | 3.144870 | 1981.90 |
| um-lens-confirm-joint-s12 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 12 | 0.04 | 3.206757 | 0.972214 | 3.150027 | 2028.32 |
| um-lens-confirm-layer-s10 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 10 | 0.04 | 3.197503 | 0.969383 | 3.142940 | 1882.20 |
| um-lens-confirm-layer-s11 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 11 | 0.04 | 3.201502 | 0.970638 | 3.146095 | 1719.76 |
| um-lens-confirm-layer-s12 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 12 | 0.04 | 3.202821 | 0.970995 | 3.147678 | 1656.38 |
| um-lens-confirm-reciprocal-s10 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 10 | 0.02 | 3.151175 | 0.955328 | 3.095999 | 720.44 |
| um-lens-confirm-reciprocal-s11 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 11 | 0.02 | 3.153493 | 0.956068 | 3.094969 | 718.91 |
| um-lens-confirm-reciprocal-s12 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 12 | 0.02 | 3.154174 | 0.956249 | 3.100018 | 673.99 |
| um-lens-creative-ema0p5 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.555660 | 1.077899 | — | 247.79 |
| um-lens-creative-ema0p9 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.558717 | 1.078825 | — | 229.92 |
| um-lens-creative-periodic2 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.554936 | 1.077708 | — | 243.89 |
| um-lens-creative-periodic4 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.556331 | 1.078132 | — | 235.46 |
| um-lens-creative-relative0p01 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.568293 | 1.081739 | — | 263.55 |
| um-lens-creative-relative0p03 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.553957 | 1.077399 | — | 249.47 |
| um-lens-long-control-0 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.199618 | 0.970057 | — | 788.71 |
| um-lens-long-control-1 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.0282843 | 3.168332 | 0.960556 | — | 786.20 |
| um-lens-long-creative-0 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.199090 | 0.969892 | — | 1834.23 |
| um-lens-long-creative-1 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.207725 | 0.972496 | — | 1837.54 |
| um-lens-long-joint-cooldown | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.200458 | 0.970313 | — | 1931.00 |
| um-lens-long-joint-stable | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.0025/stable fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.319987 | 1.006466 | — | 1867.68 |
| um-lens-long-layer-cooldown | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.197616 | 0.969468 | — | 1828.08 |
| um-lens-long-layer-stable | Clean GapWD layer uniform v2 c-in-Q armijo cap0.0025/stable fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.321643 | 1.007028 | — | 1813.94 |
| um-lens-long-reciprocal-0 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.155148 | 0.956583 | — | 770.45 |
| um-lens-long-reciprocal-1 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.155272 | 0.956567 | — | 762.24 |
| um-lens-main-control-lr0p02 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.02 | 3.568986 | 1.081936 | — | 141.52 |
| um-lens-main-control-lr0p04 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.554822 | 1.077668 | — | 133.67 |
| um-lens-main-control-lr0p08 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.08 | 3.586261 | 1.087199 | — | 139.40 |
| um-lens-main-joint-cooldown-cap0p005 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.559877 | 1.079192 | — | 252.91 |
| um-lens-main-joint-cooldown-cap0p02 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.02/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.583797 | 1.086460 | — | 251.66 |
| um-lens-main-joint-cooldown-cap0p08 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.08/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.782362 | 1.146569 | — | 274.88 |
| um-lens-main-joint-stable-cap0p005 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.652983 | 1.107410 | — | 256.79 |
| um-lens-main-joint-stable-cap0p02 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.850446 | 1.167314 | — | 249.81 |
| um-lens-main-joint-stable-cap0p08 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.08/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 4.107661 | 1.245115 | — | 246.74 |
| um-lens-main-layer-cooldown-cap0p005 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.561886 | 1.079815 | — | 227.76 |
| um-lens-main-layer-cooldown-cap0p02 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.586478 | 1.087264 | — | 230.84 |
| um-lens-main-layer-cooldown-cap0p08 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.08/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.775003 | 1.144357 | — | 254.49 |
| um-lens-main-layer-stable-cap0p005 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.653949 | 1.107712 | — | 251.43 |
| um-lens-main-layer-stable-cap0p02 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.02/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.843672 | 1.165215 | — | 226.67 |
| um-lens-main-layer-stable-cap0p08 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.08/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 4.177053 | 1.266205 | — | 223.52 |
| um-lens-main-reciprocal-lr0p02 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.02 | 3.609994 | 1.094386 | — | 123.51 |
| um-lens-main-reciprocal-lr0p04 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.610242 | 1.094431 | — | 116.29 |
| um-lens-main-reciprocal-lr0p08 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.08 | 3.617905 | 1.096810 | — | 149.97 |
| um-lens-refine-control-0 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.0282843 | 3.559476 | 1.079044 | — | 114.70 |
| um-lens-refine-control-1 | Clean Native cooldown v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.0565685 | 3.563508 | 1.080334 | — | 115.07 |
| um-lens-refine-joint-cooldown-0 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.0025/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.623444 | 1.098428 | — | 274.70 |
| um-lens-refine-joint-cooldown-1 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.555091 | 1.077761 | — | 256.27 |
| um-lens-refine-joint-stable-0 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.0025/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.645341 | 1.105051 | — | 257.49 |
| um-lens-refine-joint-stable-1 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.01/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.727101 | 1.129865 | — | 262.87 |
| um-lens-refine-layer-cooldown-0 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.0025/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.617586 | 1.096649 | — | 227.00 |
| um-lens-refine-layer-cooldown-1 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.554595 | 1.077588 | — | 222.00 |
| um-lens-refine-layer-stable-0 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.0025/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.648631 | 1.106064 | — | 239.27 |
| um-lens-refine-layer-stable-1 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.733664 | 1.131851 | — | 236.90 |
| um-lens-refine-reciprocal-0 | Clean Muon shifted reciprocal v2 c-in-Q fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.01 | 3.639452 | 1.103271 | — | 120.04 |
| um-lens-startl-joint-cooldown-0 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.560580 | 1.079401 | — | 251.61 |
| um-lens-startl-joint-cooldown-1 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.561008 | 1.079554 | — | 256.03 |
| um-lens-startl-joint-stable-0 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.653051 | 1.107413 | — | 247.21 |
| um-lens-startl-joint-stable-1 | Clean GapWD joint uniform v2 c-in-Q quadratic cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.654224 | 1.107785 | — | 247.97 |
| um-lens-startl-layer-cooldown-0 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.560975 | 1.079534 | — | 241.03 |
| um-lens-startl-layer-cooldown-1 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/cooldown fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.562346 | 1.079948 | — | 241.40 |
| um-lens-startl-layer-stable-0 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.654067 | 1.107714 | — | 247.29 |
| um-lens-startl-layer-stable-1 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.005/stable fixed_lambda=0.18375 WD:standard(0) | 2000 | 0 | 0.04 | 3.653376 | 1.107509 | — | 237.19 |
| um-lens-time-control-s10 | Clean Native cooldown v2 c-in-Q time679.0s fixed_lambda=0.18375 WD:standard(0) | 20225 | 10 | 0.0282843 | 3.178579 | 0.963716 | 3.120702 | 761.22 |
| um-lens-time-control-s11 | Clean Native cooldown v2 c-in-Q time679.0s fixed_lambda=0.18375 WD:standard(0) | 19762 | 11 | 0.0282843 | 3.169040 | 0.960766 | 3.113390 | 737.06 |
| um-lens-time-control-s12 | Clean Native cooldown v2 c-in-Q time679.0s fixed_lambda=0.18375 WD:standard(0) | 19890 | 12 | 0.0282843 | 3.169580 | 0.960944 | 3.116667 | 732.06 |
| um-lens-time-layer-s10 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown time679.0s fixed_lambda=0.18375 WD:standard(0) | 8518 | 10 | 0.04 | 3.272616 | 0.992150 | 3.218791 | 771.10 |
| um-lens-time-layer-s11 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown time679.0s fixed_lambda=0.18375 WD:standard(0) | 8406 | 11 | 0.04 | 3.274756 | 0.992869 | 3.218212 | 771.26 |
| um-lens-time-layer-s12 | Clean GapWD layer uniform v2 c-in-Q armijo cap0.01/cooldown time679.0s fixed_lambda=0.18375 WD:standard(0) | 7594 | 12 | 0.04 | 3.293004 | 0.998353 | 3.238780 | 770.03 |
| um-screen-00-0-native-lr0p005 | Native cooldown | 2000 | 0 | 0.005 | 3.734536 | 1.132046 | — | 145.49 |
| um-screen-00-1-scaled-lr0p0002 | Unnormalized cooldown | 2000 | 0 | 0.0002 | 4.818060 | 1.460343 | — | 153.42 |
| um-screen-00-2-constant-lr0p0002 | Unnormalized constant | 2000 | 0 | 0.0002 | 4.581043 | 1.388601 | — | 151.98 |
| um-screen-01-0-native-lr0p01 | Native cooldown | 2000 | 0 | 0.01 | 3.613164 | 1.095335 | — | 144.24 |
| um-screen-01-1-scaled-lr0p0006 | Unnormalized cooldown | 2000 | 0 | 0.0006 | 4.724209 | 1.431941 | — | 154.79 |
| um-screen-01-2-constant-lr0p0006 | Unnormalized constant | 2000 | 0 | 0.0006 | 4.532526 | 1.373908 | — | 163.98 |
| um-screen-02-0-native-lr0p02 | Native cooldown | 2000 | 0 | 0.02 | 3.559061 | 1.078945 | — | 151.82 |
| um-screen-02-1-scaled-lr0p002 | Unnormalized cooldown | 2000 | 0 | 0.002 | 4.379024 | 1.327359 | — | 155.31 |
| um-smoke-001/native | Native cooldown | 64 | 42 | 0.02 | 6.475706 | 1.962373 | — | 101.57 |
| um-smoke-001/scaled | Unnormalized cooldown | 64 | 42 | 0.002 | 6.492003 | 1.967335 | — | 74.24 |
| um-wd-grid-0-0-norm-lr0p02 | Clean Native cooldown WD:standard(0.14) | 2000 | 0 | 0.02 | 3.576236 | 1.084133 | — | 164.96 |
| um-wd-grid-0-0-norm-lr0p04 | Clean Native cooldown WD:standard(0.07) | 2000 | 0 | 0.04 | 3.561056 | 1.079537 | — | 164.28 |
| um-wd-grid-0-0-norm-lr0p08 | Clean Native cooldown WD:standard(0.035) | 2000 | 0 | 0.08 | 3.557473 | 1.078491 | — | 156.53 |
| um-wd-grid-0-0-unnorm-lr0p16 | Clean Unnormalized cooldown WD:standard(0.0175) | 2000 | 0 | 0.16 | 3.708944 | 1.124338 | — | 158.20 |
| um-wd-grid-0-0-unnorm-lr0p32 | Clean Unnormalized cooldown WD:standard(0.00875) | 2000 | 0 | 0.32 | 3.676837 | 1.114554 | — | 166.58 |
| um-wd-grid-0-0-unnorm-lr0p64 | Clean Unnormalized cooldown WD:standard(0.004375) | 2000 | 0 | 0.64 | 3.666523 | 1.111479 | — | 160.43 |
| um-wd-grid-0-0-unnorm-lr1p28 | Clean Unnormalized cooldown WD:standard(0.0021875) | 2000 | 0 | 1.28 | 3.733659 | 1.131831 | — | 172.41 |
| um-wd-grid-0-1-norm-lr0p02 | Clean Native cooldown WD:cautious(0.14) | 2000 | 0 | 0.02 | 3.580594 | 1.085443 | — | 141.57 |
| um-wd-grid-0-1-norm-lr0p04 | Clean Native cooldown WD:cautious(0.07) | 2000 | 0 | 0.04 | 3.561607 | 1.079701 | — | 152.81 |
| um-wd-grid-0-1-norm-lr0p08 | Clean Native cooldown WD:cautious(0.035) | 2000 | 0 | 0.08 | 3.561807 | 1.079804 | — | 154.83 |
| um-wd-grid-0-1-unnorm-lr0p16 | Clean Unnormalized cooldown WD:cautious(0.0175) | 2000 | 0 | 0.16 | 3.703818 | 1.122786 | — | 144.31 |
| um-wd-grid-0-1-unnorm-lr0p32 | Clean Unnormalized cooldown WD:cautious(0.00875) | 2000 | 0 | 0.32 | 3.677685 | 1.114818 | — | 155.90 |
| um-wd-grid-0-1-unnorm-lr0p64 | Clean Unnormalized cooldown WD:cautious(0.004375) | 2000 | 0 | 0.64 | 3.669621 | 1.112408 | — | 151.25 |
| um-wd-grid-0-1-unnorm-lr1p28 | Clean Unnormalized cooldown WD:cautious(0.0021875) | 2000 | 0 | 1.28 | 3.741636 | 1.134185 | — | 154.48 |
| um-wd-grid-1-0-norm-lr0p02 | Clean Native cooldown WD:standard(0.56) | 2000 | 0 | 0.02 | 3.578252 | 1.084742 | — | 123.82 |
| um-wd-grid-1-0-norm-lr0p04 | Clean Native cooldown WD:standard(0.28) | 2000 | 0 | 0.04 | 3.568284 | 1.081754 | — | 129.82 |
| um-wd-grid-1-0-norm-lr0p08 | Clean Native cooldown WD:standard(0.14) | 2000 | 0 | 0.08 | 3.562765 | 1.080099 | — | 138.94 |
| um-wd-grid-1-0-unnorm-lr0p16 | Clean Unnormalized cooldown WD:standard(0.07) | 2000 | 0 | 0.16 | 3.742638 | 1.134564 | — | 154.08 |
| um-wd-grid-1-0-unnorm-lr0p32 | Clean Unnormalized cooldown WD:standard(0.035) | 2000 | 0 | 0.32 | 3.670908 | 1.112798 | — | 148.24 |
| um-wd-grid-1-0-unnorm-lr0p64 | Clean Unnormalized cooldown WD:standard(0.0175) | 2000 | 0 | 0.64 | 3.657862 | 1.108874 | — | 157.59 |
| um-wd-grid-1-0-unnorm-lr1p28 | Clean Unnormalized cooldown WD:standard(0.00875) | 2000 | 0 | 1.28 | 3.692790 | 1.119391 | — | 152.71 |
| um-wd-grid-1-1-norm-lr0p02 | Clean Native cooldown WD:cautious(0.56) | 2000 | 0 | 0.02 | 3.569451 | 1.082082 | — | 139.64 |
| um-wd-grid-1-1-norm-lr0p04 | Clean Native cooldown WD:cautious(0.28) | 2000 | 0 | 0.04 | 3.555677 | 1.077910 | — | 120.97 |
| um-wd-grid-1-1-norm-lr0p08 | Clean Native cooldown WD:cautious(0.14) | 2000 | 0 | 0.08 | 3.556768 | 1.078267 | — | 150.59 |
| um-wd-grid-1-1-unnorm-lr0p16 | Clean Unnormalized cooldown WD:cautious(0.07) | 2000 | 0 | 0.16 | 3.664298 | 1.110830 | — | 163.56 |
| um-wd-grid-1-1-unnorm-lr0p32 | Clean Unnormalized cooldown WD:cautious(0.035) | 2000 | 0 | 0.32 | 3.654365 | 1.107747 | — | 158.83 |
| um-wd-grid-1-1-unnorm-lr0p64 | Clean Unnormalized cooldown WD:cautious(0.0175) | 2000 | 0 | 0.64 | 3.650276 | 1.106549 | — | 142.00 |
| um-wd-grid-1-1-unnorm-lr1p28 | Clean Unnormalized cooldown WD:cautious(0.00875) | 2000 | 0 | 1.28 | 3.684556 | 1.116968 | — | 145.98 |
| um-wd-grid-2-0-norm-lr0p02 | Clean Native cooldown WD:standard(2.24) | 2000 | 0 | 0.02 | 3.657069 | 1.108646 | — | 135.74 |
| um-wd-grid-2-0-norm-lr0p04 | Clean Native cooldown WD:standard(1.12) | 2000 | 0 | 0.04 | 3.646872 | 1.105549 | — | 119.10 |
| um-wd-grid-2-0-norm-lr0p08 | Clean Native cooldown WD:standard(0.56) | 2000 | 0 | 0.08 | 3.641740 | 1.104011 | — | 114.78 |
| um-wd-grid-2-0-unnorm-lr0p16 | Clean Unnormalized cooldown WD:standard(0.28) | 2000 | 0 | 0.16 | 3.856223 | 1.168961 | — | 132.42 |
| um-wd-grid-2-0-unnorm-lr0p32 | Clean Unnormalized cooldown WD:standard(0.14) | 2000 | 0 | 0.32 | 3.842443 | 1.164750 | — | 128.86 |
| um-wd-grid-2-0-unnorm-lr0p64 | Clean Unnormalized cooldown WD:standard(0.07) | 2000 | 0 | 0.64 | 3.818985 | 1.157711 | — | 129.55 |
| um-wd-grid-2-0-unnorm-lr1p28 | Clean Unnormalized cooldown WD:standard(0.035) | 2000 | 0 | 1.28 | 3.746897 | 1.135835 | — | 139.44 |
| um-wd-grid-2-1-norm-lr0p02 | Clean Native cooldown WD:cautious(2.24) | 2000 | 0 | 0.02 | 3.585011 | 1.086767 | — | 113.19 |
| um-wd-grid-2-1-norm-lr0p04 | Clean Native cooldown WD:cautious(1.12) | 2000 | 0 | 0.04 | 3.570390 | 1.082385 | — | 113.38 |
| um-wd-grid-2-1-norm-lr0p08 | Clean Native cooldown WD:cautious(0.56) | 2000 | 0 | 0.08 | 3.572501 | 1.083022 | — | 134.62 |
| um-wd-grid-2-1-unnorm-lr0p16 | Clean Unnormalized cooldown WD:cautious(0.28) | 2000 | 0 | 0.16 | 3.677244 | 1.114736 | — | 139.96 |
| um-wd-grid-2-1-unnorm-lr0p32 | Clean Unnormalized cooldown WD:cautious(0.14) | 2000 | 0 | 0.32 | 3.656262 | 1.108381 | — | 128.41 |
| um-wd-grid-2-1-unnorm-lr0p64 | Clean Unnormalized cooldown WD:cautious(0.07) | 2000 | 0 | 0.64 | 3.660097 | 1.109567 | — | 126.67 |
| um-wd-grid-2-1-unnorm-lr1p28 | Clean Unnormalized cooldown WD:cautious(0.035) | 2000 | 0 | 1.28 | 3.642977 | 1.104366 | — | 128.87 |
| um-window-cap-check-002 | Clean Native cooldown cap/sign fixed_lambda=0.18375 WD:standard(0) | 64 | 0 | 0.01 | 6.438628 | 1.951138 | — | 61.30 |
| um-window-cap-tune-x0p5 | Clean Native cooldown cap/sign fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.121832 | 0.946452 | — | 739.60 |
| um-window-cap-tune-x1 | Clean Native cooldown cap/sign fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.114210 | 0.944143 | — | 776.59 |
| um-window-cap-tune-x2 | Clean Native cooldown cap/sign fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.142147 | 0.952621 | — | 779.55 |
| um-window-confirm-candidate-s40 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 40 | 0.02 | 3.087717 | 0.936117 | 3.168677 | 775.31 |
| um-window-confirm-candidate-s41 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 41 | 0.02 | 3.086025 | 0.935604 | 3.172236 | 734.51 |
| um-window-confirm-candidate-s42 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 42 | 0.02 | 3.088866 | 0.936487 | 3.171032 | 673.18 |
| um-window-confirm-reference-s40 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 40 | 0.01 | 3.103223 | 0.940818 | 3.185633 | 725.89 |
| um-window-confirm-reference-s41 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 41 | 0.01 | 3.104613 | 0.941244 | 3.186403 | 666.93 |
| um-window-confirm-reference-s42 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 42 | 0.01 | 3.104400 | 0.941187 | 3.190003 | 667.35 |
| um-window-cooled-wd-x0p25 | Clean Muon shifted reciprocal +cooldown0.05 fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.096870 | 0.938922 | — | 737.58 |
| um-window-cosine-lr-edge | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.101129 | 0.940186 | — | 734.59 |
| um-window-first-wd-mixing | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.105714 | 0.941595 | — | 728.95 |
| um-window-first-wd-static-product | Clean Native cooldown fixed_lambda=0.138371 WD:standard(0) | 20000 | 0 | 0.005 | 3.103214 | 0.940837 | — | 770.97 |
| um-window-first-wd-x0 | Clean Native cooldown WD:standard(0) | 20000 | 0 | 0.005 | 3.133004 | 0.949842 | — | 798.92 |
| um-window-first-wd-x0p25 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.005 | 3.116976 | 0.945011 | — | 767.80 |
| um-window-first-wd-x0p5 | Clean Native cooldown fixed_lambda=0.0918749 WD:standard(0) | 20000 | 0 | 0.005 | 3.104900 | 0.941332 | — | 794.45 |
| um-window-first-wd-x2 | Clean Native cooldown fixed_lambda=0.3675 WD:standard(0) | 20000 | 0 | 0.005 | 3.135778 | 0.950699 | — | 772.24 |
| um-window-joint-cosine-wd-lr0p005 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.118502 | 0.945456 | — | 659.14 |
| um-window-joint-cosine-wd-lr0p01 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.094790 | 0.938262 | — | 651.90 |
| um-window-joint-mixing-x1 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.097867 | 0.939196 | — | 730.73 |
| um-window-joint-mixing-x2 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.092627 | 0.937609 | — | 707.60 |
| um-window-joint-terminal-lr0p005-f0p01 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.120314 | 0.945998 | — | 734.57 |
| um-window-joint-terminal-lr0p005-f0p25 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.005 | 3.132740 | 0.949796 | — | 770.78 |
| um-window-joint-terminal-lr0p01-f0p01 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.104185 | 0.941123 | — | 758.60 |
| um-window-joint-terminal-lr0p01-f0p25 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.170352 | 0.961133 | — | 755.55 |
| um-window-joint-wd0-x1 | Clean Native cooldown WD:standard(0) | 20000 | 0 | 0.01 | 3.118538 | 0.945488 | — | 790.98 |
| um-window-joint-wd0-x2 | Clean Native cooldown WD:standard(0) | 20000 | 0 | 0.02 | 3.105875 | 0.941649 | — | 804.53 |
| um-window-joint-wd0p25-x1 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.01 | 3.097679 | 0.939163 | — | 792.33 |
| um-window-joint-wd0p25-x2 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.093087 | 0.937762 | — | 777.21 |
| um-window-joint-wd0p5-x1 | Clean Native cooldown fixed_lambda=0.0918749 WD:standard(0) | 20000 | 0 | 0.01 | 3.100060 | 0.939872 | — | 780.80 |
| um-window-joint-wd0p5-x2 | Clean Native cooldown fixed_lambda=0.0918749 WD:standard(0) | 20000 | 0 | 0.02 | 3.106249 | 0.941739 | — | 784.21 |
| um-window-joint-wd0p753041-x1 | Clean Native cooldown fixed_lambda=0.138371 WD:standard(0) | 20000 | 0 | 0.01 | 3.106556 | 0.941828 | — | 750.51 |
| um-window-joint-wd0p753041-x2 | Clean Native cooldown fixed_lambda=0.138371 WD:standard(0) | 20000 | 0 | 0.02 | 3.125062 | 0.947431 | — | 772.65 |
| um-window-joint-zero-lr0p04 | Clean Native cooldown WD:standard(0) | 20000 | 0 | 0.04 | 3.107898 | 0.942247 | — | 787.70 |
| um-window-mixing-lr-edge | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.097083 | 0.938931 | — | 773.43 |
| um-window-schedule-edge0-f0p05 | Clean Muon shifted reciprocal +cooldown0.05 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.01 | 3.105950 | 0.941635 | — | 789.58 |
| um-window-schedule-edge0-f0p25 | Clean Muon shifted reciprocal +cooldown0.25 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.08 | 3.104520 | 0.941213 | — | 778.27 |
| um-window-schedule-lr0p02-f0p05 | Clean Muon shifted reciprocal +cooldown0.05 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.096101 | 0.938674 | — | 711.40 |
| um-window-schedule-lr0p02-f0p25 | Clean Muon shifted reciprocal +cooldown0.25 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.101839 | 0.940430 | — | 711.22 |
| um-window-schedule-lr0p04-f0p05 | Clean Muon shifted reciprocal +cooldown0.05 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.096862 | 0.938917 | — | 780.16 |
| um-window-schedule-lr0p04-f0p25 | Clean Muon shifted reciprocal +cooldown0.25 fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.04 | 3.100892 | 0.940085 | — | 714.25 |
| um-window-static-lr-edge | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.04 | 3.106810 | 0.941914 | — | 787.45 |
| um-window-static-matched-contraction | Clean Native cooldown fixed_lambda=0.116345 WD:standard(0) | 20000 | 0 | 0.01 | 3.094227 | 0.938106 | — | 853.89 |
| um-window-static-terminal-f0p01 | Clean Native cooldown fixed_lambda=0.0459375 WD:standard(0) | 20000 | 0 | 0.02 | 3.089540 | 0.936699 | — | 772.89 |
| um-window-terminal-edge-lr0p0025-f0p25 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.0025 | 3.147864 | 0.954340 | — | 785.67 |
| um-window-terminal-edge-lr0p02-f0p01 | Clean Native cooldown fixed_lambda=0.18375 WD:standard(0) | 20000 | 0 | 0.02 | 3.127284 | 0.948107 | — | 797.67 |

Review of um-fw-diagnostic-001: Compiled training f0 compared against functional candidate losses; vanishing-step mismatch2-4e-5 exceeded tolerance, leading to curvature1e186 and45 skipped steps. Replaced by paired functional reference and candidates; retain all645 measured forwards and GPUcost.

Review of um-earlyalloc-confirm-history-check-001: Invalid short check: horizon64 gives cooldown join22 before warmup40. Non-time runs intentionally ignore reference_updates override. early_reciprocal asserts warmup<join on first measured step. Fix check002 horizon128/join45 and fail-fast launcher validation; full20k arms unaffected.

Conservative charged/reserved total: 44.8337 / 50 B300 GPU-hours. Includes prior smoke/failed attempts and current maximum-duration reservations. Six-slot central queue; one B300 per run.

CLEAN geometry disables row equilibration and NorMuon. Original clean runs use zero matrix decay; new WD runs explicitly label standard or cautious decay and their CLI coefficient. Same five Polar Express steps and Frobenius correction; scale by the per-matrix nonnegative FP32 inner product of the native Nesterov input with the NS/Frobenius direction. Shape scaling occurs once outside the scalar. Legacy rows retain production extras and must be compared separately. Constant schedule changes only matrix LR; auxiliary schedules and momentum remain matched.

FW is a separate fixed-spectral-ball method with shared mixing, same-batch backtracking, frozen auxiliary weights during checks, and no extra matrix decay. Its extra candidate forwards count toward wall time and are logged.
