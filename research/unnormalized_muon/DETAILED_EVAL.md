# Detailed clean Muon evaluation

All results use the B300 fork model/data/tokenizer and a fixed tuning-validation prefix. CE is natural-log token cross-entropy; lower is better. Single-seed LR/WD screening is not a confirmation. Final heldout data is reserved for frozen settings. Compare endpoints only at matching token budgets. Wall-time curves include all training work, including FW forward probes; curves with token-based LR schedules are descriptive, not a separately matched equal-time experiment.

## Longer runs

| Method | LR | Updates | Val CE | Training sec | Total process sec |
|---|---:|---:|---:|---:|---:|
| normalized WD none 0 | 0.04 | 20000 | 3.107198 | 668.45 | 743.22 |
| unnormalized cooldown WD none 0 | 0.64 | 20000 | 3.168528 | 705.21 | 779.28 |
| unnormalized constant WD none 0 | 0.64 | 20000 | 3.210816 | 665.00 | 737.52 |
| normalized WD none 0 | 0.08 | 20000 | 3.112453 | 680.91 | 755.24 |
| unnormalized cooldown WD none 0 | 0.32 | 20000 | 3.168984 | 681.31 | 754.69 |
| unnormalized constant WD none 0 | 0.32 | 20000 | 3.209921 | 691.44 | 765.35 |
| normalized WD standard 0 | 0.02 | 20000 | 3.091088 | 722.24 | 784.34 |
| normalized WD standard 0 | 0.02 | 20000 | 3.085667 | 740.05 | 798.23 |
| normalized WD standard 0 | 0.02 | 20000 | 3.089873 | 719.21 | 783.07 |
| normalized WD standard 0 | 0.02 | 20000 | 3.088452 | 736.52 | 794.05 |
| normalized WD standard 0 | 0.02 | 20000 | 3.086768 | 712.18 | 770.47 |
| normalized WD standard 0 | 0.02 | 20000 | 3.097495 | 698.50 | 758.31 |
| normalized WD standard 0 | 0.02 | 20000 | 3.091825 | 685.49 | 747.43 |
| normalized WD standard 0 | 0.02 | 20000 | 3.087015 | 680.93 | 743.56 |
| normalized WD standard 0 | 0.02 | 20000 | 3.091281 | 700.68 | 779.60 |
| normalized WD standard 0 | 0.02 | 20000 | 3.087880 | 726.88 | 806.59 |
| normalized WD standard 0 | 0.02 | 20000 | 3.086275 | 639.78 | 700.68 |
| normalized WD standard 0 | 0.02 | 20000 | 3.098150 | 657.07 | 712.74 |
| normalized WD standard 0 | 0.02 | 20000 | 3.090448 | 708.99 | 783.18 |
| normalized WD standard 0 | 0.02 | 20000 | 3.089904 | 641.82 | 701.43 |
| normalized WD standard 0 | 0.02 | 20000 | 3.089891 | 715.08 | 790.30 |
| normalized WD standard 0 | 0.01 | 20000 | 3.111594 | 669.52 | 729.25 |
| normalized WD standard 0 | 0.01 | 20000 | 3.111298 | 689.36 | 751.79 |
| normalized WD standard 0 | 0.01 | 20000 | 3.110596 | 694.37 | 755.31 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.157425 | 685.59 | 741.30 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.162671 | 684.83 | 745.00 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.149971 | 726.70 | 782.37 |
| normalized WD standard 0 | 0.005 | 20000 | 3.119279 | 661.35 | 719.39 |
| normalized WD standard 0 | 0.02 | 20740 | 3.154321 | 676.22 | 733.36 |
| normalized WD standard 0 | 0.02 | 20007 | 3.156209 | 676.41 | 734.10 |
| normalized WD standard 0 | 0.01 | 20000 | 3.112087 | 703.74 | 777.47 |
| normalized WD standard 0 | 0.02 | 20000 | 3.142251 | 694.30 | 767.69 |
| normalized WD standard 0 | 0.01 | 20000 | 3.156622 | 670.54 | 744.07 |
| normalized WD standard 0 | 0.0141421 | 20000 | 3.122182 | 679.06 | 738.56 |
| normalized WD standard 0 | 0.00707107 | 20000 | 3.113318 | 719.44 | 775.02 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.152773 | 646.68 | 721.58 |
| normalized WD standard 0 | 0.0141421 | 20000 | 3.152943 | 652.84 | 727.28 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.167631 | 658.92 | 741.10 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.164999 | 684.42 | 745.36 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.169816 | 676.02 | 733.38 |
| normalized WD standard 0 | 0.04 | 20000 | 3.198918 | 1844.40 | 1934.59 |
| normalized WD standard 0 | 0.04 | 20000 | 3.201077 | 1891.19 | 1981.90 |
| normalized WD standard 0 | 0.04 | 20000 | 3.206757 | 1936.58 | 2028.32 |
| normalized WD standard 0 | 0.04 | 20000 | 3.197503 | 1783.84 | 1882.20 |
| normalized WD standard 0 | 0.04 | 20000 | 3.201502 | 1640.94 | 1719.76 |
| normalized WD standard 0 | 0.04 | 20000 | 3.202821 | 1578.96 | 1656.38 |
| normalized WD standard 0 | 0.02 | 20000 | 3.151175 | 662.61 | 720.44 |
| normalized WD standard 0 | 0.02 | 20000 | 3.153493 | 657.94 | 718.91 |
| normalized WD standard 0 | 0.02 | 20000 | 3.154174 | 618.61 | 673.99 |
| normalized WD standard 0 | 0.04 | 20000 | 3.199618 | 710.50 | 788.71 |
| normalized WD standard 0 | 0.0282843 | 20000 | 3.168332 | 723.17 | 786.20 |
| normalized WD standard 0 | 0.04 | 20000 | 3.199090 | 1763.98 | 1834.23 |
| normalized WD standard 0 | 0.04 | 20000 | 3.207725 | 1751.45 | 1837.54 |
| normalized WD standard 0 | 0.04 | 20000 | 3.200458 | 1844.61 | 1931.00 |
| normalized WD standard 0 | 0.04 | 20000 | 3.319987 | 1781.19 | 1867.68 |
| normalized WD standard 0 | 0.04 | 20000 | 3.197616 | 1730.24 | 1828.08 |
| normalized WD standard 0 | 0.04 | 20000 | 3.321643 | 1734.89 | 1813.94 |
| normalized WD standard 0 | 0.02 | 20000 | 3.155148 | 710.04 | 770.45 |
| normalized WD standard 0 | 0.04 | 20000 | 3.155272 | 706.85 | 762.24 |
| normalized WD standard 0 | 0.0282843 | 20225 | 3.178579 | 676.45 | 761.22 |
| normalized WD standard 0 | 0.005 | 20000 | 3.121832 | 679.62 | 739.60 |
| normalized WD standard 0 | 0.01 | 20000 | 3.114210 | 721.38 | 776.59 |
| normalized WD standard 0 | 0.02 | 20000 | 3.142147 | 704.53 | 779.55 |
| normalized WD standard 0 | 0.02 | 20000 | 3.087717 | 715.59 | 775.31 |
| normalized WD standard 0 | 0.02 | 20000 | 3.086025 | 678.92 | 734.51 |
| normalized WD standard 0 | 0.02 | 20000 | 3.088866 | 598.29 | 673.18 |
| normalized WD standard 0 | 0.01 | 20000 | 3.103223 | 650.71 | 725.89 |
| normalized WD standard 0 | 0.01 | 20000 | 3.104613 | 591.70 | 666.93 |
| normalized WD standard 0 | 0.01 | 20000 | 3.104400 | 592.06 | 667.35 |
| normalized WD standard 0 | 0.02 | 20000 | 3.096870 | 680.36 | 737.58 |
| normalized WD standard 0 | 0.02 | 20000 | 3.101129 | 677.13 | 734.59 |
| normalized WD standard 0 | 0.005 | 20000 | 3.105714 | 669.92 | 728.95 |
| normalized WD standard 0 | 0.005 | 20000 | 3.103214 | 694.03 | 770.97 |
| normalized WD standard 0 | 0.005 | 20000 | 3.133004 | 720.75 | 798.92 |
| normalized WD standard 0 | 0.005 | 20000 | 3.116976 | 690.43 | 767.80 |
| normalized WD standard 0 | 0.005 | 20000 | 3.104900 | 716.25 | 794.45 |
| normalized WD standard 0 | 0.005 | 20000 | 3.135778 | 713.84 | 772.24 |
| normalized WD standard 0 | 0.005 | 20000 | 3.118502 | 598.82 | 659.14 |
| normalized WD standard 0 | 0.01 | 20000 | 3.094790 | 595.73 | 651.90 |
| normalized WD standard 0 | 0.01 | 20000 | 3.097867 | 669.53 | 730.73 |
| normalized WD standard 0 | 0.02 | 20000 | 3.092627 | 654.56 | 707.60 |
| normalized WD standard 0 | 0.005 | 20000 | 3.120314 | 674.59 | 734.57 |
| normalized WD standard 0 | 0.005 | 20000 | 3.132740 | 714.53 | 770.78 |
| normalized WD standard 0 | 0.01 | 20000 | 3.104185 | 687.27 | 758.60 |
| normalized WD standard 0 | 0.01 | 20000 | 3.170352 | 683.23 | 755.55 |
| normalized WD standard 0 | 0.01 | 20000 | 3.118538 | 717.03 | 790.98 |
| normalized WD standard 0 | 0.02 | 20000 | 3.105875 | 729.67 | 804.53 |
| normalized WD standard 0 | 0.01 | 20000 | 3.097679 | 717.27 | 792.33 |
| normalized WD standard 0 | 0.02 | 20000 | 3.093087 | 702.81 | 777.21 |
| normalized WD standard 0 | 0.01 | 20000 | 3.100060 | 698.63 | 780.80 |
| normalized WD standard 0 | 0.02 | 20000 | 3.106249 | 702.20 | 784.21 |
| normalized WD standard 0 | 0.01 | 20000 | 3.106556 | 691.48 | 750.51 |
| normalized WD standard 0 | 0.02 | 20000 | 3.125062 | 716.99 | 772.65 |
| normalized WD standard 0 | 0.04 | 20000 | 3.107898 | 724.84 | 787.70 |
| normalized WD standard 0 | 0.04 | 20000 | 3.097083 | 693.23 | 773.43 |
| normalized WD standard 0 | 0.01 | 20000 | 3.105950 | 714.00 | 789.58 |
| normalized WD standard 0 | 0.08 | 20000 | 3.104520 | 702.63 | 778.27 |
| normalized WD standard 0 | 0.02 | 20000 | 3.096101 | 636.21 | 711.40 |
| normalized WD standard 0 | 0.02 | 20000 | 3.101839 | 636.04 | 711.22 |
| normalized WD standard 0 | 0.04 | 20000 | 3.096862 | 718.41 | 780.16 |
| normalized WD standard 0 | 0.04 | 20000 | 3.100892 | 641.14 | 714.25 |
| normalized WD standard 0 | 0.04 | 20000 | 3.106810 | 706.08 | 787.45 |
| normalized WD standard 0 | 0.01 | 20000 | 3.094227 | 771.84 | 853.89 |
| normalized WD standard 0 | 0.02 | 20000 | 3.089540 | 691.80 | 772.89 |
| normalized WD standard 0 | 0.0025 | 20000 | 3.147864 | 729.38 | 785.67 |
| normalized WD standard 0 | 0.02 | 20000 | 3.127284 | 736.15 | 797.67 |

## Weight decay search

Clean geometry keeps row equilibration and NorMuon disabled. Standard decay applies W <- (1-eta*lambda)W - eta*a*Q; cautious decay masks its shrinkage by sign((aQ)*W)>=0. The unnormalization factor scales only the directional term. Native batch/model-horizon coefficient scaling and cosine WD schedule remain intact; explicit update count does not change the native compute-optimal model horizon used to scale lambda. Auxiliary AdamW is unchanged.

CLI lambda = 0.28*(0.04/CLI_eta)*strength matches nominal eta*lambda exposure across LRs/methods for the same cooldown horizon and shape. Cautious masks make its logged nominal exposure an upper bound. Strength is tuned independently for each method and rule. Zero-WD controls are reported separately.

| Method | Decay | Strength | CLI LR | CLI WD | Updates | Val CE | Nominal Muon exposure range |
|---|---|---:|---:|---:|---:|---:|---|
| normalized | standard | 0.25 | 0.02 | 0.14 | 2000 | 3.576236 | 0.40773–0.81545 |
| normalized | standard | 0.25 | 0.04 | 0.07 | 2000 | 3.561056 | 0.40773–0.81545 |
| normalized | standard | 0.25 | 0.08 | 0.035 | 2000 | 3.557473 | 0.40773–0.81545 |
| unnormalized | standard | 0.25 | 0.16 | 0.0175 | 2000 | 3.708944 | 0.40773–0.81545 |
| unnormalized | standard | 0.25 | 0.32 | 0.00875 | 2000 | 3.676837 | 0.40773–0.81545 |
| unnormalized | standard | 0.25 | 0.64 | 0.004375 | 2000 | 3.666523 | 0.40773–0.81545 |
| unnormalized | standard | 0.25 | 1.28 | 0.0021875 | 2000 | 3.733659 | 0.40773–0.81545 |
| normalized | cautious | 0.25 | 0.02 | 0.14 | 2000 | 3.580594 | 0.40773–0.81545 |
| normalized | cautious | 0.25 | 0.04 | 0.07 | 2000 | 3.561607 | 0.40773–0.81545 |
| normalized | cautious | 0.25 | 0.08 | 0.035 | 2000 | 3.561807 | 0.40773–0.81545 |
| unnormalized | cautious | 0.25 | 0.16 | 0.0175 | 2000 | 3.703818 | 0.40773–0.81545 |
| unnormalized | cautious | 0.25 | 0.32 | 0.00875 | 2000 | 3.677685 | 0.40773–0.81545 |
| unnormalized | cautious | 0.25 | 0.64 | 0.004375 | 2000 | 3.669621 | 0.40773–0.81545 |
| unnormalized | cautious | 0.25 | 1.28 | 0.0021875 | 2000 | 3.741636 | 0.40773–0.81545 |
| normalized | standard | 1 | 0.02 | 0.56 | 2000 | 3.578252 | 1.6309–3.2618 |
| normalized | standard | 1 | 0.04 | 0.28 | 2000 | 3.568284 | 1.6309–3.2618 |
| normalized | standard | 1 | 0.08 | 0.14 | 2000 | 3.562765 | 1.6309–3.2618 |
| unnormalized | standard | 1 | 0.16 | 0.07 | 2000 | 3.742638 | 1.6309–3.2618 |
| unnormalized | standard | 1 | 0.32 | 0.035 | 2000 | 3.670908 | 1.6309–3.2618 |
| unnormalized | standard | 1 | 0.64 | 0.0175 | 2000 | 3.657862 | 1.6309–3.2618 |
| unnormalized | standard | 1 | 1.28 | 0.00875 | 2000 | 3.692790 | 1.6309–3.2618 |
| normalized | cautious | 1 | 0.02 | 0.56 | 2000 | 3.569451 | 1.6309–3.2618 |
| normalized | cautious | 1 | 0.04 | 0.28 | 2000 | 3.555677 | 1.6309–3.2618 |
| normalized | cautious | 1 | 0.08 | 0.14 | 2000 | 3.556768 | 1.6309–3.2618 |
| unnormalized | cautious | 1 | 0.16 | 0.07 | 2000 | 3.664298 | 1.6309–3.2618 |
| unnormalized | cautious | 1 | 0.32 | 0.035 | 2000 | 3.654365 | 1.6309–3.2618 |
| unnormalized | cautious | 1 | 0.64 | 0.0175 | 2000 | 3.650276 | 1.6309–3.2618 |
| unnormalized | cautious | 1 | 1.28 | 0.00875 | 2000 | 3.684556 | 1.6309–3.2618 |
| normalized | standard | 4 | 0.02 | 2.24 | 2000 | 3.657069 | 6.5236–13.047 |
| normalized | standard | 4 | 0.04 | 1.12 | 2000 | 3.646872 | 6.5236–13.047 |
| normalized | standard | 4 | 0.08 | 0.56 | 2000 | 3.641740 | 6.5236–13.047 |
| unnormalized | standard | 4 | 0.16 | 0.28 | 2000 | 3.856223 | 6.5236–13.047 |
| unnormalized | standard | 4 | 0.32 | 0.14 | 2000 | 3.842443 | 6.5236–13.047 |
| unnormalized | standard | 4 | 0.64 | 0.07 | 2000 | 3.818985 | 6.5236–13.047 |
| unnormalized | standard | 4 | 1.28 | 0.035 | 2000 | 3.746897 | 6.5236–13.047 |
| normalized | cautious | 4 | 0.02 | 2.24 | 2000 | 3.585011 | 6.5236–13.047 |
| normalized | cautious | 4 | 0.04 | 1.12 | 2000 | 3.570390 | 6.5236–13.047 |
| normalized | cautious | 4 | 0.08 | 0.56 | 2000 | 3.572501 | 6.5236–13.047 |
| unnormalized | cautious | 4 | 0.16 | 0.28 | 2000 | 3.677244 | 6.5236–13.047 |
| unnormalized | cautious | 4 | 0.32 | 0.14 | 2000 | 3.656262 | 6.5236–13.047 |
| unnormalized | cautious | 4 | 0.64 | 0.07 | 2000 | 3.660097 | 6.5236–13.047 |
| unnormalized | cautious | 4 | 1.28 | 0.035 | 2000 | 3.642977 | 6.5236–13.047 |

## FW gap-based step and line search

Fixed radii R_i=max(1,radius_factor*initial spectral norm(W_i)). A certified spectral-safe approximate polar direction Q_i defines D_i=-R_i Q_i-W_i. One shared gamma=clip(b/(L*v),0,gamma_cap); original runs use gamma_cap=1, while scheduled-cap variants multiply a tuned cap by the common warmup/cooldown LR multiplier. This is an explicit additional safeguard, not automatic shrinking from the gap alone. The gap uses b=-sum<G_i,D_i>, v=sum||D_i||F^2. Current-gradient and momentum oracles are separately labelled. With an approximate or momentum oracle, b is a directional gap, not an exact FW optimality certificate. Nonpositive b skips all candidate forwards. No additional matrix decay is applied.

Strict smoothness backtracking compares a same-path functional reference at gamma=0 with candidates on the entire current effective batch, using the same token weighting and preserved RNG. Auxiliary weights are frozen during checks and updated afterward. The separately labelled Armijo variant accepts f(candidate)<=f0-c*gamma*b with c=.01 and forbids measured increases; it does NOT certify the original quadratic smoothness bound. Same-batch decrease does not guarantee heldout improvement.

| Run | Updates | Val CE | Accepted | Negative b | Extra batch forwards | FW sec | Max spectral ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| um-check-fw-compiled-armijo-001 | 64 | 6.504589 | 64 | 0 | 191 | 25.00 | 0.265840 |
| um-check-fw-compiled-smoothness-001 | 64 | 6.400337 | 64 | 0 | 189 | 17.58 | 0.404534 |
| um-check-fw-derivative-001 | 48 | 6.648578 | 48 | 0 | 179 | 23.38 | 0.499494 |
| um-check-fw-gradient-001 | 64 | 6.488285 | 64 | 0 | 197 | 22.68 | 0.499329 |
| um-check-fw-momentum-001 | 64 | 6.470441 | 58 | 6 | 183 | 22.14 | 0.499287 |
| um-clean-fw-accumcheck-001 | 16 | 9.061382 | — | — | 63 | 15.85 | 0.499600 |
| um-clean-long-2-fw-pilot | 2000 | 4.185817 | 1996 | 4 | 5995 | 233.55 | 0.586020 |

### um-check-fw-compiled-armijo-001

Oracle: gradient; acceptance: armijo; compiled candidates: True; radius factor: 2; gamma cap: 1; scheduled: False. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 191. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 0.000746914 | 0.032649 | 0.0501182 | 0.0638361 | 1 |
| L | 1.95313e-05 | 0.0025 | 0.005 | 0.01 | 0.02 |
| b | 0.0623487 | 1.48228 | 5.98677 | 7.32819 | 11.8296 |
| v | 13429.4 | 18778.2 | 20606.1 | 22511.4 | 34606.8 |
| trials | 1 | 1 | 2 | 2.25 | 6 |
| actual_decrease | 4.57764e-05 | 0.0162783 | 0.0394645 | 0.107543 | 0.259679 |
| predicted_decrease | 2.39049e-05 | 0.0320206 | 0.142492 | 0.209192 | 0.665815 |

FW timing components (seconds): direction=13.360, reference=8.758, candidates=0.940, auxiliary=0.608.
Accepted steps with measured minibatch increase: 0; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

### um-check-fw-compiled-smoothness-001

Oracle: gradient; acceptance: smoothness; compiled candidates: True; radius factor: 2; gamma cap: 0.03; scheduled: True. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 189. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 0.000749173 | 0.00688393 | 0.0118613 | 0.0157784 | 0.0246575 |
| gamma_cap | 0.00075 | 0.00688393 | 0.0125536 | 0.0181875 | 0.03 |
| L | 6.10352e-07 | 0.00125 | 0.0025 | 0.005 | 0.04 |
| b | 0.0623487 | 1.44805 | 1.63643 | 1.98193 | 28.4146 |
| v | 16261.8 | 24379.7 | 25283.1 | 26610.1 | 34487.8 |
| trials | 1 | 1 | 2 | 2 | 9 |
| actual_decrease | 4.57764e-05 | 0.00824916 | 0.0161965 | 0.0227016 | 0.337219 |
| predicted_decrease | 2.38934e-05 | 0.00786625 | 0.0127518 | 0.0188245 | 0.317416 |

FW timing components (seconds): direction=12.878, reference=2.125, candidates=0.878, auxiliary=0.430.
Accepted steps with measured minibatch increase: 0; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

### um-check-fw-derivative-001

Oracle: gradient; acceptance: smoothness; compiled candidates: False; radius factor: 2; gamma cap: 1; scheduled: False. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 358. Extra diagnostic gradient queries: 3, diagnostic seconds: 2.061.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 4.14126e-09 | 4.02707e-07 | 1.69877e-05 | 3.01467e-05 | 0.000277723 |
| L | 0.01 | 0.32 | 1.28 | 204.8 | 335544 |
| b | 0.0623085 | 0.317002 | 0.518499 | 1.1338 | 278.384 |
| v | 16260.3 | 26835.2 | 28929.6 | 36980 | 39119.8 |
| trials | 1 | 1 | 2 | 3 | 12 |
| actual_decrease | -9.53674e-07 | 0 | 0 | 9.53674e-07 | 2.86102e-06 |
| predicted_decrease | 5.63842e-09 | 2.82269e-07 | 4.52352e-06 | 7.22271e-06 | 1.18288e-05 |

FW timing components (seconds): direction=12.952, reference=4.173, candidates=2.238, auxiliary=0.576.
Accepted steps with measured minibatch increase: 6; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

### um-check-fw-gradient-001

Oracle: gradient; acceptance: smoothness; compiled candidates: False; radius factor: 2; gamma cap: 1; scheduled: False. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 394. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 1.08528e-07 | 4.58077e-06 | 1.66769e-05 | 2.85376e-05 | 0.000277723 |
| L | 0.01 | 0.32 | 0.64 | 10.24 | 20971.5 |
| b | 0.0623085 | 0.349596 | 0.439872 | 1.20084 | 114.275 |
| v | 16260.3 | 27179.7 | 35283.3 | 38625.9 | 40282.2 |
| trials | 1 | 1 | 2 | 3 | 6 |
| actual_decrease | -1.90735e-06 | 0 | 2.38419e-07 | 1.54972e-06 | 5.72205e-06 |
| predicted_decrease | 5.21932e-07 | 2.68177e-06 | 4.86751e-06 | 7.26985e-06 | 1.48663e-05 |

FW timing components (seconds): direction=13.074, reference=4.427, candidates=2.912, auxiliary=0.757.
Accepted steps with measured minibatch increase: 11; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

### um-check-fw-momentum-001

Oracle: momentum; acceptance: smoothness; compiled candidates: False; radius factor: 2; gamma cap: 1; scheduled: False. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 366. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 0 | 1.04306e-06 | 3.21422e-05 | 6.50095e-05 | 0.00031704 |
| L | 0.01 | 0.08 | 0.16 | 20.48 | 167772 |
| b | -0.527959 | 0.0788049 | 0.165321 | 0.370019 | 232.949 |
| v | 16261.2 | 24688.5 | 25806.5 | 29741.5 | 34426.9 |
| trials | 0 | 1 | 1 | 3 | 11 |
| actual_decrease | -3.8147e-06 | 0 | 0 | 9.53674e-07 | 7.62939e-06 |
| predicted_decrease | 0 | 4.6859e-07 | 3.15176e-06 | 6.56309e-06 | 1.15503e-05 |

FW timing components (seconds): direction=13.131, reference=4.248, candidates=2.713, auxiliary=0.699.
Accepted steps with measured minibatch increase: 14; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

### um-clean-long-2-fw-pilot

Oracle: momentum; acceptance: smoothness; compiled candidates: False; radius factor: 2; gamma cap: 1; scheduled: False. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 5995. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

| Quantity | Min | P25 | Median | P75 | Max |
|---|---:|---:|---:|---:|---:|
| gamma | 0 | 0.019065 | 0.0284537 | 0.045194 | 0.185085 |
| L | 0.000625 | 0.01 | 0.02 | 0.04 | 20971.5 |
| b | -0.623421 | 8.85879 | 13.5343 | 19.285 | 98.3482 |
| v | 15277 | 21450.2 | 24840.4 | 26273 | 39826.5 |
| trials | 0 | 1 | 2 | 3 | 7 |
| actual_decrease | -4.76837e-06 | 0.244338 | 0.286635 | 0.319971 | 0.439672 |
| predicted_decrease | 0 | 0.174015 | 0.218605 | 0.267067 | 0.419033 |

FW timing components (seconds): direction=104.832, reference=43.252, candidates=80.372, auxiliary=2.291.
Accepted steps with measured minibatch increase: 62; acceptance has relative BF16-path numerical slack 1e-6. Reference/candidate forwards and all line-search retries are included in training time and total process time.

## Fixed ordinary WD: per-layer and joint gap LR

This subtopic holds the actual unmasked decay coefficient lambda fixed. P_i=Q_i+lambda W_i includes shrinkage. Native Nesterov/five NS/Frobenius are retained; row equilibration and NorMuon remain off. Native finite NS is approximate: spectral ratios are measured without claiming the exact spectral-ball theorem. Optional certified directions are separately labelled.

Per-layer LR uses eta_i=min(1/lambda,[<G_i,P_i>]_+/(L||P_i||F^2)), proposed simultaneously and accepted using the complete-loss summed quadratic bound. One shared backtracked Frobenius L accounts for cross-layer changes; no52-way independent forward search. Joint-uniform shares one actual eta. Joint-native instead searches c_i P_i, clips outer eta at1/(lambda max c_i), and records actual eta_i=c_i eta; it is not a single common FW mixing coefficient.

The shifted reciprocal control uses eta_i(t)=eta_i0/(1+lambda eta_i0*t/2) after40 warmup updates, with native actual eta_i0=CLI_LR*.25*c_i. This corresponds to gamma_i=2/(t+2/(lambda eta_i0)). Auxiliary schedules and native momentum are held consistent, so convex FW guarantees do not apply directly to this stochastic hybrid optimizer.

| Run | Mode | Fixed lambda | Updates | Val CE | Extra batch forwards | Process sec |
|---|---|---:|---:|---:|---:|---:|
| um-earlyalloc-confirm-baseline-s70 | early_reciprocal native | 0.04593747 | 20000 | 3.091088 | 0 | 784.34 |
| um-earlyalloc-confirm-baseline-s71 | early_reciprocal native | 0.04593747 | 20000 | 3.085667 | 0 | 798.23 |
| um-earlyalloc-confirm-baseline-s72 | early_reciprocal native | 0.04593747 | 20000 | 3.089873 | 0 | 783.07 |
| um-earlyalloc-confirm-early-s70 | early_reciprocal native | 0.04593747 | 20000 | 3.088452 | 0 | 794.05 |
| um-earlyalloc-confirm-early-s71 | early_reciprocal native | 0.04593747 | 20000 | 3.086768 | 0 | 770.47 |
| um-earlyalloc-confirm-early-s72 | early_reciprocal native | 0.04593747 | 20000 | 3.097495 | 0 | 758.31 |
| um-earlyalloc-confirm-matched-s70 | early_reciprocal native | 0.05512714 | 20000 | 3.091825 | 0 | 747.43 |
| um-earlyalloc-confirm-matched-s71 | early_reciprocal native | 0.05512714 | 20000 | 3.087015 | 0 | 743.56 |
| um-earlyalloc-confirm-matched-s72 | early_reciprocal native | 0.05512714 | 20000 | 3.091281 | 0 | 779.60 |
| um-earlyalloc-confirm-neutral-s70 | early_reciprocal native | 0.03827981 | 20000 | 3.087880 | 0 | 806.59 |
| um-earlyalloc-confirm-neutral-s71 | early_reciprocal native | 0.03827981 | 20000 | 3.086275 | 0 | 700.68 |
| um-earlyalloc-confirm-neutral-s72 | early_reciprocal native | 0.03827981 | 20000 | 3.098150 | 0 | 712.74 |
| um-earlyalloc-screen-k1 | early_reciprocal native | 0.04593747 | 20000 | 3.090448 | 0 | 783.18 |
| um-earlyalloc-screen-k1p5 | early_reciprocal native | 0.04593747 | 20000 | 3.089904 | 0 | 701.43 |
| um-earlyalloc-screen-k2 | early_reciprocal native | 0.04593747 | 20000 | 3.089891 | 0 | 790.30 |
| um-follow-confirm20000-control-s20 | cooldown native | 0.1837499 | 20000 | 3.111594 | 0 | 729.25 |
| um-follow-confirm20000-control-s21 | cooldown native | 0.1837499 | 20000 | 3.111298 | 0 | 751.79 |
| um-follow-confirm20000-control-s22 | cooldown native | 0.1837499 | 20000 | 3.110596 | 0 | 755.31 |
| um-follow-confirm20000-reciprocal-s20 | fw_reciprocal native | 0.1837499 | 20000 | 3.157425 | 0 | 741.30 |
| um-follow-confirm20000-reciprocal-s21 | fw_reciprocal native | 0.1837499 | 20000 | 3.162671 | 0 | 745.00 |
| um-follow-confirm20000-reciprocal-s22 | fw_reciprocal native | 0.1837499 | 20000 | 3.149971 | 0 | 782.37 |
| um-follow-edge0-control-lr0p005 | cooldown native | 0.1837499 | 20000 | 3.119279 | 0 | 719.39 |
| um-follow-first-time-reciprocal-s10 | fw_reciprocal native | 0.1837499 | 20740 | 3.154321 | 0 | 733.36 |
| um-follow-first-time-reciprocal-s11 | fw_reciprocal native | 0.1837499 | 20007 | 3.156209 | 0 | 734.10 |
| um-follow-first-time-reciprocal-s12 | fw_reciprocal native | 0.1837499 | 18127 | 3.161711 | 0 | 750.97 |
| um-follow-first-tune-control-lr0p01 | cooldown native | 0.1837499 | 20000 | 3.112087 | 0 | 777.47 |
| um-follow-first-tune-control-lr0p02 | cooldown native | 0.1837499 | 20000 | 3.142251 | 0 | 767.69 |
| um-follow-first-tune-reciprocal-lr0p01 | fw_reciprocal native | 0.1837499 | 20000 | 3.156622 | 0 | 744.07 |
| um-follow-mid-control-high | cooldown native | 0.1837499 | 20000 | 3.122182 | 0 | 738.56 |
| um-follow-mid-control-low | cooldown native | 0.1837499 | 20000 | 3.113318 | 0 | 775.02 |
| um-follow-mid-reciprocal-high | fw_reciprocal native | 0.1837499 | 20000 | 3.152773 | 0 | 721.58 |
| um-follow-mid-reciprocal-low | fw_reciprocal native | 0.1837499 | 20000 | 3.152943 | 0 | 727.28 |
| um-fresh-diagnosis-001 | cooldown native | 0.1837499 | 2000 | 3.557051 | 0 | 340.47 |
| um-fresh-wd-mixing | cooldown native | 0.1837499 | 2000 | 3.555051 | 0 | 149.73 |
| um-fresh-wd-static-product | cooldown native | 0.1538642 | 2000 | 3.553682 | 0 | 123.04 |
| um-gapwd-first-cosine-001 | cooldown native | 0.1837499 | 64 | 6.415227 | 0 | 76.24 |
| um-gapwd-first-layer-001 | layer uniform | 0.1837499 | 64 | 6.463019 | 193 | 91.78 |

um-gapwd-first-layer-001: accepted 64/64; skipped nonpositive blocks 49; median actual eta 0.00378804; median gamma 0.000696053; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.414108. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.513, reference=7.844, candidates=1.032, auxiliary=0.411.

| um-gapwd-first-reciprocal-001 | fw_reciprocal native | 0.1837499 | 64 | 6.374067 | 0 | 77.77 |
| um-gapwd-joint-native-001 | joint native | 0.1837499 | 64 | 6.369767 | 191 | 94.57 |

um-gapwd-joint-native-001: accepted 64/64; skipped nonpositive blocks 39; median actual eta 0.0117936; median gamma 0.00216708; median L 0.005; median trials 2; max measured spectral ratio lambda*||W||op=0.389638. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.301, reference=2.449, candidates=1.028, auxiliary=0.556.

| um-gapwd-joint-uniform-001 | joint uniform | 0.1837499 | 64 | 6.390594 | 191 | 95.12 |

um-gapwd-joint-uniform-001: accepted 64/64; skipped nonpositive blocks 37; median actual eta 0.0125746; median gamma 0.00231058; median L 0.005; median trials 2; max measured spectral ratio lambda*||W||op=0.432438. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.588, reference=2.197, candidates=1.032, auxiliary=0.523.

| um-gapwd-pilot-cosine-lr0p02 | cooldown native | 0.1837499 | 2000 | 3.577361 | 0 | 142.48 |
| um-gapwd-pilot-cosine-lr0p04 | cooldown native | 0.1837499 | 2000 | 3.575844 | 0 | 135.71 |
| um-gapwd-pilot-cosine-lr0p08 | cooldown native | 0.1837499 | 2000 | 3.610093 | 0 | 136.39 |
| um-gapwd-pilot-joint | joint uniform | 0.1837499 | 2000 | 4.149021 | 5999 | 254.05 |

um-gapwd-pilot-joint: accepted 2000/2000; skipped nonpositive blocks 198; median actual eta 0.0861453; median gamma 0.0158292; median L 0.0025; median trials 2; max measured spectral ratio lambda*||W||op=0.710394. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=56.478, reference=15.382, candidates=27.426, auxiliary=2.070.

| um-gapwd-pilot-joint-native | joint native | 0.1837499 | 2000 | 4.120519 | 5999 | 266.55 |

um-gapwd-pilot-joint-native: accepted 2000/2000; skipped nonpositive blocks 235; median actual eta 0.0678755; median gamma 0.0124721; median L 0.0025; median trials 2; max measured spectral ratio lambda*||W||op=0.758705. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=64.083, reference=15.966, candidates=28.437, auxiliary=2.179.

| um-gapwd-pilot-layer | layer uniform | 0.1837499 | 2000 | 4.186773 | 5999 | 269.44 |

um-gapwd-pilot-layer: accepted 2000/2000; skipped nonpositive blocks 379; median actual eta 0.080241; median gamma 0.0147443; median L 0.0025; median trials 2; max measured spectral ratio lambda*||W||op=0.708825. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=64.952, reference=16.005, candidates=28.579, auxiliary=2.107.

| um-gapwd-pilot-reciprocal-lr0p02 | fw_reciprocal native | 0.1837499 | 2000 | 3.622123 | 0 | 144.58 |
| um-gapwd-pilot-reciprocal-lr0p04 | fw_reciprocal native | 0.1837499 | 2000 | 3.625030 | 0 | 138.08 |
| um-gapwd-pilot-reciprocal-lr0p08 | fw_reciprocal native | 0.1837499 | 2000 | 3.627100 | 0 | 138.60 |
| um-lens-check-0-control | cooldown native | 0.1837499 | 64 | 6.414393 | 0 | 69.03 |
| um-lens-check-1-joint | joint native | 0.1837499 | 64 | 6.423715 | 191 | 94.79 |

um-lens-check-1-joint: accepted 64/64; skipped nonpositive blocks 53; median actual eta 0.00955982; median gamma 0.00175661; median L 0.005; median trials 1; max measured spectral ratio lambda*||W||op=0.379967. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.893, reference=2.163, candidates=1.007, auxiliary=0.729.

| um-lens-check-2-layer | layer native | 0.1837499 | 64 | 6.410152 | 133 | 91.23 |

um-lens-check-2-layer: accepted 64/64; skipped nonpositive blocks 53; median actual eta 0.015; median gamma 0.00275625; median L 2.79397e-11; median trials 1; max measured spectral ratio lambda*||W||op=0.40221. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.358, reference=2.128, candidates=0.566, auxiliary=0.640.

| um-lens-check-3-time-control | cooldown native | 0.1837499 | 1 | 10.394322 | 0 | 79.20 |
| um-lens-check-4-time-layer | layer native | 0.1837499 | 1 | 10.394308 | 2 | 83.55 |

um-lens-check-4-time-layer: accepted 1/1; skipped nonpositive blocks 36; median actual eta 0; median gamma 0; median L 0.005; median trials 1; max measured spectral ratio lambda*||W||op=0.368177. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=4.543, reference=1.568, candidates=0.012, auxiliary=0.608.

| um-lens-check-5-creative | layer native | 0.1837499 | 64 | 6.337770 | 128 | 96.43 |

um-lens-check-5-creative: accepted 64/64; skipped nonpositive blocks 57; median actual eta 0.011606; median gamma 0.00213259; median L 1.74623e-12; median trials 1; max measured spectral ratio lambda*||W||op=0.379675. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=5.960, reference=2.037, candidates=0.608, auxiliary=0.600.

| um-lens-check-6-periodic | joint native | 0.1837499 | 64 | 6.490925 | 48 | 95.36 |

um-lens-check-6-periodic: accepted 16/64; skipped nonpositive blocks 59; median actual eta 0.00428424; median gamma 0.000787229; median L 0.0075; median trials 0; max measured spectral ratio lambda*||W||op=0.366569. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=6.270, reference=1.728, candidates=0.259, auxiliary=0.606.

| um-lens-check-7-warm-time-control | cooldown native | 0.1837499 | 96 | 6.041687 | 0 | 81.78 |
| um-lens-check-8-warm-time-layer | layer native | 0.1837499 | 50 | 6.365249 | 100 | 85.49 |

um-lens-check-8-warm-time-layer: accepted 50/50; skipped nonpositive blocks 70; median actual eta 0.02; median gamma 0.003675; median L 2.23517e-10; median trials 1; max measured spectral ratio lambda*||W||op=0.537713. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=1.317, reference=0.399, candidates=0.395, auxiliary=0.041.

| um-lens-confirm-control-s10 | cooldown native | 0.1837499 | 20000 | 3.167631 | 0 | 741.10 |
| um-lens-confirm-control-s11 | cooldown native | 0.1837499 | 20000 | 3.164999 | 0 | 745.36 |
| um-lens-confirm-control-s12 | cooldown native | 0.1837499 | 20000 | 3.169816 | 0 | 733.38 |
| um-lens-confirm-joint-s10 | joint native | 0.1837499 | 20000 | 3.198918 | 60004 | 1934.59 |

um-lens-confirm-joint-s10: accepted 20000/20000; skipped nonpositive blocks 392; median actual eta 0.0077854; median gamma 0.00143057; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.298774. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=599.766, reference=146.716, candidates=287.547, auxiliary=17.974.

| um-lens-confirm-joint-s11 | joint native | 0.1837499 | 20000 | 3.201077 | 60004 | 1981.90 |

um-lens-confirm-joint-s11: accepted 20000/20000; skipped nonpositive blocks 376; median actual eta 0.0077854; median gamma 0.00143057; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.26652. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=631.967, reference=149.317, candidates=291.686, auxiliary=18.663.

| um-lens-confirm-joint-s12 | joint native | 0.1837499 | 20000 | 3.206757 | 60004 | 2028.32 |

um-lens-confirm-joint-s12: accepted 20000/20000; skipped nonpositive blocks 465; median actual eta 0.0077854; median gamma 0.00143057; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.307328. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=687.736, reference=150.582, candidates=295.063, auxiliary=18.164.

| um-lens-confirm-layer-s10 | layer native | 0.1837499 | 20000 | 3.197503 | 40000 | 1882.20 |

um-lens-confirm-layer-s10: accepted 20000/20000; skipped nonpositive blocks 410; median actual eta 0.00778065; median gamma 0.00142969; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.31436. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=661.032, reference=151.402, candidates=147.486, auxiliary=18.910.

| um-lens-confirm-layer-s11 | layer native | 0.1837499 | 20000 | 3.201502 | 40000 | 1719.76 |

um-lens-confirm-layer-s11: accepted 20000/20000; skipped nonpositive blocks 331; median actual eta 0.00778212; median gamma 0.00142996; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.264642. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=552.798, reference=147.342, candidates=143.959, auxiliary=18.877.

| um-lens-confirm-layer-s12 | layer native | 0.1837499 | 20000 | 3.202821 | 40000 | 1656.38 |

um-lens-confirm-layer-s12: accepted 20000/20000; skipped nonpositive blocks 466; median actual eta 0.00777992; median gamma 0.00142956; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.261988. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=570.370, reference=146.431, candidates=141.366, auxiliary=18.228.

| um-lens-confirm-reciprocal-s10 | fw_reciprocal native | 0.1837499 | 20000 | 3.151175 | 0 | 720.44 |
| um-lens-confirm-reciprocal-s11 | fw_reciprocal native | 0.1837499 | 20000 | 3.153493 | 0 | 718.91 |
| um-lens-confirm-reciprocal-s12 | fw_reciprocal native | 0.1837499 | 20000 | 3.154174 | 0 | 673.99 |
| um-lens-creative-ema0p5 | layer native | 0.1837499 | 2000 | 3.555660 | 4000 | 247.79 |

um-lens-creative-ema0p5: accepted 2000/2000; skipped nonpositive blocks 90; median actual eta 0.00757385; median gamma 0.00139169; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.405719. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=58.611, reference=15.033, candidates=14.694, auxiliary=1.983.

| um-lens-creative-ema0p9 | layer native | 0.1837499 | 2000 | 3.558717 | 4000 | 229.92 |

um-lens-creative-ema0p9: accepted 2000/2000; skipped nonpositive blocks 226; median actual eta 0.00745692; median gamma 0.00137021; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.410554. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=57.344, reference=14.477, candidates=14.332, auxiliary=1.791.

| um-lens-creative-periodic2 | joint native | 0.1837499 | 2000 | 3.554936 | 3001 | 243.89 |

um-lens-creative-periodic2: accepted 1000/2000; skipped nonpositive blocks 100; median actual eta 0.00759212; median gamma 0.00139505; median L 0.01; median trials 0.5; max measured spectral ratio lambda*||W||op=0.389011. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=53.072, reference=7.217, candidates=13.954, auxiliary=1.784.

| um-lens-creative-periodic4 | joint native | 0.1837499 | 2000 | 3.556331 | 1501 | 235.46 |

um-lens-creative-periodic4: accepted 500/2000; skipped nonpositive blocks 90; median actual eta 0.0075775; median gamma 0.00139236; median L 0.01; median trials 0; max measured spectral ratio lambda*||W||op=0.391067. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=53.416, reference=3.742, candidates=7.040, auxiliary=1.803.

| um-lens-creative-relative0p01 | layer native | 0.1837499 | 2000 | 3.568293 | 4000 | 263.55 |

um-lens-creative-relative0p01: accepted 2000/2000; skipped nonpositive blocks 98; median actual eta 0.00558868; median gamma 0.00102692; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.381307. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=59.462, reference=14.180, candidates=17.665, auxiliary=1.646.

| um-lens-creative-relative0p03 | layer native | 0.1837499 | 2000 | 3.553957 | 4000 | 249.47 |

um-lens-creative-relative0p03: accepted 2000/2000; skipped nonpositive blocks 100; median actual eta 0.00758846; median gamma 0.00139438; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.39891. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.636, reference=14.182, candidates=17.375, auxiliary=1.741.

| um-lens-long-control-0 | cooldown native | 0.1837499 | 20000 | 3.199618 | 0 | 788.71 |
| um-lens-long-control-1 | cooldown native | 0.1837499 | 20000 | 3.168332 | 0 | 786.20 |
| um-lens-long-creative-0 | layer native | 0.1837499 | 20000 | 3.199090 | 40000 | 1834.23 |

um-lens-long-creative-0: accepted 20000/20000; skipped nonpositive blocks 437; median actual eta 0.00778065; median gamma 0.00142969; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.300626. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=622.508, reference=149.101, candidates=182.732, auxiliary=18.600.

| um-lens-long-creative-1 | layer native | 0.1837499 | 20000 | 3.207725 | 40000 | 1837.54 |

um-lens-long-creative-1: accepted 20000/20000; skipped nonpositive blocks 302; median actual eta 0.00674423; median gamma 0.00123925; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.305307. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=601.929, reference=146.306, candidates=181.080, auxiliary=17.769.

| um-lens-long-joint-cooldown | joint native | 0.1837499 | 20000 | 3.200458 | 60004 | 1931.00 |

um-lens-long-joint-cooldown: accepted 20000/20000; skipped nonpositive blocks 426; median actual eta 0.00778394; median gamma 0.0014303; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.287582. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=626.609, reference=147.527, candidates=289.369, auxiliary=17.911.

| um-lens-long-joint-stable | joint native | 0.1837499 | 20000 | 3.319987 | 59997 | 1867.68 |

um-lens-long-joint-stable: accepted 19996/20000; skipped nonpositive blocks 725; median actual eta 0.0025; median gamma 0.000459375; median L 0.04; median trials 2; max measured spectral ratio lambda*||W||op=0.285411. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=539.257, reference=145.317, candidates=284.106, auxiliary=18.299.

| um-lens-long-layer-cooldown | layer native | 0.1837499 | 20000 | 3.197616 | 40000 | 1828.08 |

um-lens-long-layer-cooldown: accepted 20000/20000; skipped nonpositive blocks 416; median actual eta 0.00778065; median gamma 0.00142969; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.301371. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=610.972, reference=149.920, candidates=145.930, auxiliary=18.931.

| um-lens-long-layer-stable | layer native | 0.1837499 | 20000 | 3.321643 | 40000 | 1813.94 |

um-lens-long-layer-stable: accepted 20000/20000; skipped nonpositive blocks 720; median actual eta 0.0025; median gamma 0.000459375; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.286561. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=629.681, reference=150.001, candidates=147.010, auxiliary=18.681.

| um-lens-long-reciprocal-0 | fw_reciprocal native | 0.1837499 | 20000 | 3.155148 | 0 | 770.45 |
| um-lens-long-reciprocal-1 | fw_reciprocal native | 0.1837499 | 20000 | 3.155272 | 0 | 762.24 |
| um-lens-main-control-lr0p02 | cooldown native | 0.1837499 | 2000 | 3.568986 | 0 | 141.52 |
| um-lens-main-control-lr0p04 | cooldown native | 0.1837499 | 2000 | 3.554822 | 0 | 133.67 |
| um-lens-main-control-lr0p08 | cooldown native | 0.1837499 | 2000 | 3.586261 | 0 | 139.40 |
| um-lens-main-joint-cooldown-cap0p005 | joint native | 0.1837499 | 2000 | 3.559877 | 6000 | 252.91 |

um-lens-main-joint-cooldown-cap0p005: accepted 2000/2000; skipped nonpositive blocks 207; median actual eta 0.00379606; median gamma 0.000697525; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.331184. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.921, reference=14.497, candidates=28.220, auxiliary=1.887.

| um-lens-main-joint-cooldown-cap0p02 | joint native | 0.1837499 | 2000 | 3.583797 | 6000 | 251.66 |

um-lens-main-joint-cooldown-cap0p02: accepted 2000/2000; skipped nonpositive blocks 78; median actual eta 0.0148773; median gamma 0.0027337; median L 0.01; median trials 2; max measured spectral ratio lambda*||W||op=0.424789. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.577, reference=14.677, candidates=28.621, auxiliary=1.908.

| um-lens-main-joint-cooldown-cap0p08 | joint native | 0.1837499 | 2000 | 3.782362 | 5999 | 274.88 |

um-lens-main-joint-cooldown-cap0p08: accepted 2000/2000; skipped nonpositive blocks 227; median actual eta 0.0384805; median gamma 0.0070708; median L 0.005; median trials 2; max measured spectral ratio lambda*||W||op=0.444955. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=60.204, reference=14.729, candidates=28.415, auxiliary=1.871.

| um-lens-main-joint-stable-cap0p005 | joint native | 0.1837499 | 2000 | 3.652983 | 5997 | 256.79 |

um-lens-main-joint-stable-cap0p005: accepted 1997/2000; skipped nonpositive blocks 193; median actual eta 0.005; median gamma 0.000918749; median L 0.02; median trials 2; max measured spectral ratio lambda*||W||op=0.305381. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.880, reference=14.718, candidates=28.253, auxiliary=1.893.

| um-lens-main-joint-stable-cap0p02 | joint native | 0.1837499 | 2000 | 3.850446 | 6001 | 249.81 |

um-lens-main-joint-stable-cap0p02: accepted 2000/2000; skipped nonpositive blocks 78; median actual eta 0.02; median gamma 0.003675; median L 0.01; median trials 2; max measured spectral ratio lambda*||W||op=0.455097. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=60.891, reference=14.582, candidates=28.241, auxiliary=1.806.

| um-lens-main-joint-stable-cap0p08 | joint native | 0.1837499 | 2000 | 4.107661 | 5999 | 246.74 |

um-lens-main-joint-stable-cap0p08: accepted 2000/2000; skipped nonpositive blocks 368; median actual eta 0.0572021; median gamma 0.0105109; median L 0.0025; median trials 2; max measured spectral ratio lambda*||W||op=0.780575. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=61.373, reference=14.545, candidates=28.102, auxiliary=1.799.

| um-lens-main-layer-cooldown-cap0p005 | layer native | 0.1837499 | 2000 | 3.561886 | 4000 | 227.76 |

um-lens-main-layer-cooldown-cap0p005: accepted 2000/2000; skipped nonpositive blocks 248; median actual eta 0.00379058; median gamma 0.000696518; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.330668. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.259, reference=14.516, candidates=14.228, auxiliary=1.866.

| um-lens-main-layer-cooldown-cap0p02 | layer native | 0.1837499 | 2000 | 3.586478 | 4006 | 230.84 |

um-lens-main-layer-cooldown-cap0p02: accepted 2000/2000; skipped nonpositive blocks 107; median actual eta 0.0151185; median gamma 0.00277802; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.420678. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.305, reference=14.700, candidates=14.387, auxiliary=1.893.

| um-lens-main-layer-cooldown-cap0p08 | layer native | 0.1837499 | 2000 | 3.775003 | 4065 | 254.49 |

um-lens-main-layer-cooldown-cap0p08: accepted 2000/2000; skipped nonpositive blocks 254; median actual eta 0.0584277; median gamma 0.0107361; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.404548. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.186, reference=14.371, candidates=14.569, auxiliary=1.747.

| um-lens-main-layer-stable-cap0p005 | layer native | 0.1837499 | 2000 | 3.653949 | 4000 | 251.43 |

um-lens-main-layer-stable-cap0p005: accepted 2000/2000; skipped nonpositive blocks 223; median actual eta 0.005; median gamma 0.000918749; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.305951. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=71.458, reference=14.916, candidates=14.601, auxiliary=1.790.

| um-lens-main-layer-stable-cap0p02 | layer native | 0.1837499 | 2000 | 3.843672 | 4004 | 226.67 |

um-lens-main-layer-stable-cap0p02: accepted 2000/2000; skipped nonpositive blocks 111; median actual eta 0.02; median gamma 0.003675; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.460939. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.553, reference=14.339, candidates=14.183, auxiliary=1.862.

| um-lens-main-layer-stable-cap0p08 | layer native | 0.1837499 | 2000 | 4.177053 | 4064 | 223.52 |

um-lens-main-layer-stable-cap0p08: accepted 2000/2000; skipped nonpositive blocks 282; median actual eta 0.08; median gamma 0.0147; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.790492. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.587, reference=14.607, candidates=14.695, auxiliary=1.890.

| um-lens-main-reciprocal-lr0p02 | fw_reciprocal native | 0.1837499 | 2000 | 3.609994 | 0 | 123.51 |
| um-lens-main-reciprocal-lr0p04 | fw_reciprocal native | 0.1837499 | 2000 | 3.610242 | 0 | 116.29 |
| um-lens-main-reciprocal-lr0p08 | fw_reciprocal native | 0.1837499 | 2000 | 3.617905 | 0 | 149.97 |
| um-lens-refine-control-0 | cooldown native | 0.1837499 | 2000 | 3.559476 | 0 | 114.70 |
| um-lens-refine-control-1 | cooldown native | 0.1837499 | 2000 | 3.563508 | 0 | 115.07 |
| um-lens-refine-joint-cooldown-0 | joint native | 0.1837499 | 2000 | 3.623444 | 5997 | 274.70 |

um-lens-refine-joint-cooldown-0: accepted 1996/2000; skipped nonpositive blocks 252; median actual eta 0.00189803; median gamma 0.000348763; median L 0.04; median trials 2; max measured spectral ratio lambda*||W||op=0.308598. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=67.685, reference=15.124, candidates=28.658, auxiliary=1.924.

| um-lens-refine-joint-cooldown-1 | joint native | 0.1837499 | 2000 | 3.555091 | 6001 | 256.27 |

um-lens-refine-joint-cooldown-1: accepted 2000/2000; skipped nonpositive blocks 97; median actual eta 0.00759212; median gamma 0.00139505; median L 0.01; median trials 2; max measured spectral ratio lambda*||W||op=0.39888. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=57.274, reference=14.257, candidates=27.698, auxiliary=1.720.

| um-lens-refine-joint-stable-0 | joint native | 0.1837499 | 2000 | 3.645341 | 5995 | 257.49 |

um-lens-refine-joint-stable-0: accepted 1996/2000; skipped nonpositive blocks 239; median actual eta 0.0025; median gamma 0.000459375; median L 0.04; median trials 2; max measured spectral ratio lambda*||W||op=0.287777. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=55.058, reference=14.577, candidates=28.078, auxiliary=1.955.

| um-lens-refine-joint-stable-1 | joint native | 0.1837499 | 2000 | 3.727101 | 6001 | 262.87 |

um-lens-refine-joint-stable-1: accepted 2000/2000; skipped nonpositive blocks 94; median actual eta 0.01; median gamma 0.0018375; median L 0.01; median trials 2; max measured spectral ratio lambda*||W||op=0.361899. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.074, reference=14.283, candidates=27.896, auxiliary=1.739.

| um-lens-refine-layer-cooldown-0 | layer native | 0.1837499 | 2000 | 3.617586 | 4000 | 227.00 |

um-lens-refine-layer-cooldown-0: accepted 2000/2000; skipped nonpositive blocks 188; median actual eta 0.00189529; median gamma 0.000348259; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.305577. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=56.684, reference=14.195, candidates=13.854, auxiliary=1.740.

| um-lens-refine-layer-cooldown-1 | layer native | 0.1837499 | 2000 | 3.554595 | 4000 | 222.00 |

um-lens-refine-layer-cooldown-1: accepted 2000/2000; skipped nonpositive blocks 94; median actual eta 0.00758846; median gamma 0.00139438; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.397119. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=56.742, reference=14.521, candidates=14.085, auxiliary=1.897.

| um-lens-refine-layer-stable-0 | layer native | 0.1837499 | 2000 | 3.648631 | 4000 | 239.27 |

um-lens-refine-layer-stable-0: accepted 2000/2000; skipped nonpositive blocks 176; median actual eta 0.0025; median gamma 0.000459375; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.286501. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=54.514, reference=14.300, candidates=13.885, auxiliary=1.736.

| um-lens-refine-layer-stable-1 | layer native | 0.1837499 | 2000 | 3.733664 | 4000 | 236.90 |

um-lens-refine-layer-stable-1: accepted 2000/2000; skipped nonpositive blocks 86; median actual eta 0.01; median gamma 0.0018375; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.375865. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=52.040, reference=14.468, candidates=14.006, auxiliary=1.846.

| um-lens-refine-reciprocal-0 | fw_reciprocal native | 0.1837499 | 2000 | 3.639452 | 0 | 120.04 |
| um-lens-startl-joint-cooldown-0 | joint native | 0.1837499 | 2000 | 3.560580 | 6004 | 251.61 |

um-lens-startl-joint-cooldown-0: accepted 1999/2000; skipped nonpositive blocks 202; median actual eta 0.00379606; median gamma 0.000697525; median L 0.032; median trials 2; max measured spectral ratio lambda*||W||op=0.330205. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=62.092, reference=14.699, candidates=28.514, auxiliary=1.841.

| um-lens-startl-joint-cooldown-1 | joint native | 0.1837499 | 2000 | 3.561008 | 5999 | 256.03 |

um-lens-startl-joint-cooldown-1: accepted 2000/2000; skipped nonpositive blocks 202; median actual eta 0.00379606; median gamma 0.000697525; median L 0.025; median trials 2; max measured spectral ratio lambda*||W||op=0.329844. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=61.952, reference=14.957, candidates=28.374, auxiliary=1.913.

| um-lens-startl-joint-stable-0 | joint native | 0.1837499 | 2000 | 3.653051 | 6003 | 247.21 |

um-lens-startl-joint-stable-0: accepted 1998/2000; skipped nonpositive blocks 189; median actual eta 0.005; median gamma 0.000918749; median L 0.032; median trials 2; max measured spectral ratio lambda*||W||op=0.308162. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=51.510, reference=14.283, candidates=27.637, auxiliary=1.877.

| um-lens-startl-joint-stable-1 | joint native | 0.1837499 | 2000 | 3.654224 | 5999 | 247.97 |

um-lens-startl-joint-stable-1: accepted 2000/2000; skipped nonpositive blocks 182; median actual eta 0.005; median gamma 0.000918749; median L 0.025; median trials 2; max measured spectral ratio lambda*||W||op=0.30593. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=52.457, reference=14.308, candidates=27.553, auxiliary=1.883.

| um-lens-startl-layer-cooldown-0 | layer native | 0.1837499 | 2000 | 3.560975 | 4000 | 241.03 |

um-lens-startl-layer-cooldown-0: accepted 2000/2000; skipped nonpositive blocks 233; median actual eta 0.00379058; median gamma 0.000696518; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.329018. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=57.040, reference=14.616, candidates=14.026, auxiliary=1.813.

| um-lens-startl-layer-cooldown-1 | layer native | 0.1837499 | 2000 | 3.562346 | 4000 | 241.40 |

um-lens-startl-layer-cooldown-1: accepted 2000/2000; skipped nonpositive blocks 227; median actual eta 0.00379423; median gamma 0.000697189; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.32947. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=52.435, reference=14.308, candidates=13.883, auxiliary=1.796.

| um-lens-startl-layer-stable-0 | layer native | 0.1837499 | 2000 | 3.654067 | 4000 | 247.29 |

um-lens-startl-layer-stable-0: accepted 2000/2000; skipped nonpositive blocks 205; median actual eta 0.005; median gamma 0.000918749; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.306437. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=68.799, reference=15.065, candidates=14.671, auxiliary=1.925.

| um-lens-startl-layer-stable-1 | layer native | 0.1837499 | 2000 | 3.653376 | 4000 | 237.19 |

um-lens-startl-layer-stable-1: accepted 2000/2000; skipped nonpositive blocks 226; median actual eta 0.005; median gamma 0.000918749; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.309576. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=60.805, reference=14.714, candidates=14.296, auxiliary=1.824.

| um-lens-time-control-s10 | cooldown native | 0.1837499 | 20225 | 3.178579 | 0 | 761.22 |
| um-lens-time-control-s11 | cooldown native | 0.1837499 | 19762 | 3.169040 | 0 | 737.06 |
| um-lens-time-control-s12 | cooldown native | 0.1837499 | 19890 | 3.169580 | 0 | 732.06 |
| um-lens-time-layer-s10 | layer native | 0.1837499 | 8518 | 3.272616 | 17036 | 771.10 |

um-lens-time-layer-s10: accepted 8518/8518; skipped nonpositive blocks 312; median actual eta 0.00798851; median gamma 0.00146789; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.319904. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=227.194, reference=61.903, candidates=60.476, auxiliary=7.953.

| um-lens-time-layer-s11 | layer native | 0.1837499 | 8406 | 3.274756 | 16812 | 771.26 |

um-lens-time-layer-s11: accepted 8406/8406; skipped nonpositive blocks 262; median actual eta 0.00796131; median gamma 0.00146289; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.313068. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=229.890, reference=61.673, candidates=60.315, auxiliary=7.876.

| um-lens-time-layer-s12 | layer native | 0.1837499 | 7594 | 3.293004 | 15188 | 770.03 |

um-lens-time-layer-s12: accepted 7594/7594; skipped nonpositive blocks 287; median actual eta 0.00803841; median gamma 0.00147706; median L 1e-16; median trials 1; max measured spectral ratio lambda*||W||op=0.308425. Native approximate NS can violate the ideal unit-oracle premise; this is recorded, not hidden.

Timing seconds: direction=272.800, reference=57.289, candidates=55.597, auxiliary=6.868.

| um-window-cap-check-002 | cooldown native | 0.1837499 | 64 | 6.438628 | 0 | 61.30 |
| um-window-cap-tune-x0p5 | cooldown native | 0.1837499 | 20000 | 3.121832 | 0 | 739.60 |
| um-window-cap-tune-x1 | cooldown native | 0.1837499 | 20000 | 3.114210 | 0 | 776.59 |
| um-window-cap-tune-x2 | cooldown native | 0.1837499 | 20000 | 3.142147 | 0 | 779.55 |
| um-window-confirm-candidate-s40 | cooldown_refined native | 0.04593747 | 20000 | 3.087717 | 0 | 775.31 |
| um-window-confirm-candidate-s41 | cooldown_refined native | 0.04593747 | 20000 | 3.086025 | 0 | 734.51 |
| um-window-confirm-candidate-s42 | cooldown_refined native | 0.04593747 | 20000 | 3.088866 | 0 | 673.18 |
| um-window-confirm-reference-s40 | cooldown_refined native | 0.1837499 | 20000 | 3.103223 | 0 | 725.89 |
| um-window-confirm-reference-s41 | cooldown_refined native | 0.1837499 | 20000 | 3.104613 | 0 | 666.93 |
| um-window-confirm-reference-s42 | cooldown_refined native | 0.1837499 | 20000 | 3.104400 | 0 | 667.35 |
| um-window-cooled-wd-x0p25 | fw_reciprocal_cooldown native | 0.04593747 | 20000 | 3.096870 | 0 | 737.58 |
| um-window-cosine-lr-edge | cooldown native | 0.1837499 | 20000 | 3.101129 | 0 | 734.59 |
| um-window-first-wd-mixing | cooldown native | 0.1837499 | 20000 | 3.105714 | 0 | 728.95 |
| um-window-first-wd-static-product | cooldown native | 0.1383712 | 20000 | 3.103214 | 0 | 770.97 |
| um-window-first-wd-x0 | cooldown native | 0 | 20000 | 3.133004 | 0 | 798.92 |
| um-window-first-wd-x0p25 | cooldown native | 0.04593747 | 20000 | 3.116976 | 0 | 767.80 |
| um-window-first-wd-x0p5 | cooldown native | 0.09187494 | 20000 | 3.104900 | 0 | 794.45 |
| um-window-first-wd-x2 | cooldown native | 0.3674998 | 20000 | 3.135778 | 0 | 772.24 |
| um-window-joint-cosine-wd-lr0p005 | cooldown native | 0.1837499 | 20000 | 3.118502 | 0 | 659.14 |
| um-window-joint-cosine-wd-lr0p01 | cooldown native | 0.1837499 | 20000 | 3.094790 | 0 | 651.90 |
| um-window-joint-mixing-x1 | cooldown native | 0.1837499 | 20000 | 3.097867 | 0 | 730.73 |
| um-window-joint-mixing-x2 | cooldown native | 0.1837499 | 20000 | 3.092627 | 0 | 707.60 |
| um-window-joint-terminal-lr0p005-f0p01 | cooldown_refined native | 0.1837499 | 20000 | 3.120314 | 0 | 734.57 |
| um-window-joint-terminal-lr0p005-f0p25 | cooldown_refined native | 0.1837499 | 20000 | 3.132740 | 0 | 770.78 |
| um-window-joint-terminal-lr0p01-f0p01 | cooldown_refined native | 0.1837499 | 20000 | 3.104185 | 0 | 758.60 |
| um-window-joint-terminal-lr0p01-f0p25 | cooldown_refined native | 0.1837499 | 20000 | 3.170352 | 0 | 755.55 |
| um-window-joint-wd0-x1 | cooldown native | 0 | 20000 | 3.118538 | 0 | 790.98 |
| um-window-joint-wd0-x2 | cooldown native | 0 | 20000 | 3.105875 | 0 | 804.53 |
| um-window-joint-wd0p25-x1 | cooldown native | 0.04593747 | 20000 | 3.097679 | 0 | 792.33 |
| um-window-joint-wd0p25-x2 | cooldown native | 0.04593747 | 20000 | 3.093087 | 0 | 777.21 |
| um-window-joint-wd0p5-x1 | cooldown native | 0.09187494 | 20000 | 3.100060 | 0 | 780.80 |
| um-window-joint-wd0p5-x2 | cooldown native | 0.09187494 | 20000 | 3.106249 | 0 | 784.21 |
| um-window-joint-wd0p753041-x1 | cooldown native | 0.1383712 | 20000 | 3.106556 | 0 | 750.51 |
| um-window-joint-wd0p753041-x2 | cooldown native | 0.1383712 | 20000 | 3.125062 | 0 | 772.65 |
| um-window-joint-zero-lr0p04 | cooldown native | 0 | 20000 | 3.107898 | 0 | 787.70 |
| um-window-mixing-lr-edge | cooldown native | 0.1837499 | 20000 | 3.097083 | 0 | 773.43 |
| um-window-schedule-edge0-f0p05 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.105950 | 0 | 789.58 |
| um-window-schedule-edge0-f0p25 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.104520 | 0 | 778.27 |
| um-window-schedule-lr0p02-f0p05 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.096101 | 0 | 711.40 |
| um-window-schedule-lr0p02-f0p25 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.101839 | 0 | 711.22 |
| um-window-schedule-lr0p04-f0p05 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.096862 | 0 | 780.16 |
| um-window-schedule-lr0p04-f0p25 | fw_reciprocal_cooldown native | 0.1837499 | 20000 | 3.100892 | 0 | 714.25 |
| um-window-static-lr-edge | cooldown native | 0.04593747 | 20000 | 3.106810 | 0 | 787.45 |
| um-window-static-matched-contraction | cooldown_refined native | 0.1163448 | 20000 | 3.094227 | 0 | 853.89 |
| um-window-static-terminal-f0p01 | cooldown_refined native | 0.04593747 | 20000 | 3.089540 | 0 | 772.89 |
| um-window-terminal-edge-lr0p0025-f0p25 | cooldown_refined native | 0.1837499 | 20000 | 3.147864 | 0 | 785.67 |
| um-window-terminal-edge-lr0p02-f0p01 | cooldown_refined native | 0.1837499 | 20000 | 3.127284 | 0 | 797.67 |
