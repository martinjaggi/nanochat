# Detailed clean Muon evaluation

All results use the B300 fork model/data/tokenizer and a fixed tuning-validation prefix. CE is natural-log token cross-entropy; lower is better. Single-seed LR/WD screening is not a confirmation. Final heldout data is reserved for frozen settings. Compare endpoints only at matching token budgets. Wall-time curves include all training work, including FW forward probes; curves with token-based LR schedules are descriptive, not a separately matched equal-time experiment.

## Longer runs

| Method | LR | Updates | Val CE | Training sec | Total process sec |
|---|---:|---:|---:|---:|---:|
| normalized WD none 0 | 0.04 | 20000 | 3.107198 | 668.45 | 743.22 |
| unnormalized cooldown WD none 0 | 0.64 | 20000 | 3.168528 | 705.21 | 779.28 |
| unnormalized constant WD none 0 | 0.64 | 20000 | 3.210816 | 665.00 | 737.52 |

## Weight decay search

Clean geometry keeps row equilibration and NorMuon disabled. Standard decay applies W <- (1-eta*lambda)W - eta*a*Q; cautious decay masks its shrinkage by sign((aQ)*W)>=0. The unnormalization factor scales only the directional term. Native batch/model-horizon coefficient scaling and cosine WD schedule remain intact; explicit update count does not change the native compute-optimal model horizon used to scale lambda. Auxiliary AdamW is unchanged.

CLI lambda = 0.28*(0.04/CLI_eta)*strength matches nominal eta*lambda exposure across LRs/methods for the same cooldown horizon and shape. Cautious masks make its logged nominal exposure an upper bound. Strength is tuned independently for each method and rule. Zero-WD controls are reported separately.

| Method | Decay | Strength | CLI LR | CLI WD | Updates | Val CE | Nominal Muon exposure range |
|---|---|---:|---:|---:|---:|---:|---|

## FW gap-based step and line search

Fixed radii R_i=max(1,radius_factor*initial spectral norm(W_i)). A certified spectral-safe approximate polar direction Q_i defines D_i=-R_i Q_i-W_i. One shared gamma=clip(b/(L*v),0,1), b=-sum<G_i,D_i>, v=sum||D_i||F^2. Current-gradient and momentum oracles are separately labelled. With an approximate or momentum oracle, b is a directional gap, not an exact FW optimality certificate. Nonpositive b skips all candidate forwards. No additional matrix decay is applied.

Backtracking compares a same-path functional reference at gamma=0 with candidates on the entire current effective batch, using the same token weighting and preserved RNG. Auxiliary weights are frozen during checks and updated afterward. Same-batch decrease does not guarantee heldout improvement.

| Run | Updates | Val CE | Accepted | Negative b | Extra batch forwards | FW sec | Max spectral ratio |
|---|---:|---:|---:|---:|---:|---:|---:|
| um-check-fw-gradient-001 | 64 | 6.488285 | 64 | 0 | 197 | 22.68 | 0.499329 |
| um-check-fw-momentum-001 | 64 | 6.470441 | 58 | 6 | 183 | 22.14 | 0.499287 |
| um-clean-fw-accumcheck-001 | 16 | 9.061382 | — | — | 63 | 15.85 | 0.499600 |

### um-check-fw-gradient-001

Oracle: gradient; radius factor: 2. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 394. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

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

Oracle: momentum; radius factor: 2. Search state/RNG audit: True. Each extra forward evaluates the entire effective batch; actual microbatch-forward count: 366. Extra diagnostic gradient queries: 0, diagnostic seconds: 0.000.

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
