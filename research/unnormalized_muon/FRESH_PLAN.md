# Fresh-data step-selection diagnosis and a narrow WD follow-up

Requested after the current FW-lens v2 campaign,17 October2026. Follow the
user-supplied16 October dense-nanochat report. This is a preregistered plan,
not new empirical evidence. All work uses the same single submission queue,
one verified B300 per job, maximum6 jobs, and50 B300 GPU-hours PROJECT TOTAL
including all prior attempts. The current campaign finishes first.

## Diagnosis first

One fresh reference control trajectory: native clean Muon, ordinary fixed
lambda=.1837498798375862, CLI LR.04, original2000-update schedule,32768 tokens
per update, dense125,829,354-parameter depth8 model. ClimbMix/32K tokenizer,
BF16/native masters, row equilibration and NorMuon off, native Nesterov,
five Polar Express iterations and Frobenius correction; auxiliary recipe
unchanged. Three discarded kernel-warmup steps precede exact reset.

Save complete branches at40,400,1500 completed updates: model/buffers, full
optimizer, Muon momentum mapped by parameter name, all four RNGs, prefetched
x/y, main loader cursor, immutable file metadata, original horizon/config,
commit and deterministic replay batch count. Original loader row-group resume
is approximate, so exact offline continuation replays packing from origin,
validates file metadata and the exact next-batch hash. This is slower than
serializing internal packing buffers, but restores the actual next input.
No disposable warmup is applied to resumed branches.

At each branch use four construction/fit/check triples. Construction is an
exact independent copy of the following main-stream batches; fit/check use
the last two TRAINING parquet shards, separately, and do not consume the
main loader. Assert that construction/continuation never reaches those
shards. Offset fit/check cursors across checkpoints so batch hashes differ.
The best-fit packer consumes each document once (cropped tails are discarded),
so one document does not cross sequences; per-sequence SE is still only a
local pilot heuristic, not training-seed uncertainty.

Prepare the native next momentum and shape-scaled Q ONCE per construction
batch using disposable inputs to the actual fused native direction kernel.
Freeze P=Q+lambda W and all auxiliary weights. Probe eta/eta_base in
{0,.25,.5,1,2}, capped at1/lambda. Train and fit choose independently; checking
only scores fixed choices against the scheduled step and never selects a
candidate. Persist all per-sequence losses and signed block slopes.

Use a compiled functional per-sequence path for BOTH fit derivatives and
candidate values. Also record the relative difference from the production
scalar-loss construction gradient, rather than hiding a numerical-path
change. Count the extra derivative pass. Validate repeated loss noise and
resolved central finite differences on the fit path; fail diagnosis if none
of three resolutions agrees with the gradient slope within20%. Log every
resolution; the threshold allows finite-precision/nonlinear error and is
an engineering check, not a smoothness certificate.

Compare plain cap eta=.005*s(t), cap/sign, and the existing layer Armijo
proposal with saturated proposal L=1e-16. Record zeta, displacement difference,
fresh check loss and slope sign flips. Armijo L is a proposal parameter,
not evidence of vanishing curvature. Parameters, buffers, .grad, native
optimizer state and all RNGs must remain unchanged after probes. Reloaded
named momentum must match, a prescribed step must agree with the actual
fused step (relative displacement error<2%, momentum error<1e-5), and replayed
fit selection must reproduce its decision. Exact native algebra may still
differ by floating-point rounding, which is measured explicitly.

At update400 compare the scheduled step with at most two FIT-selected
multipliers from the first fit curve. Continue each for32/128 updates with
identical future construction data and native auxiliary rules. Separately
hold the multiplier for128 updates, recomputing momentum/Q every update.
Retain the original2000-update schedule. Evaluate only independent development
data; final-heldout data remains unused. Charge every continuation gradient
and all probe/validation/checkpoint/compile time.

Preregistered gate: fit-selected choices improve check loss in at least8/12
triples, and a fit-selected alternative improves independent continuation CE
by>.001 after BOTH32 and128 updates. This is a conservative pilot gate, not
statistical significance. If it fails, stop online-controller expansion.
If it passes, inspect the full diagnosis before implementing the report's
matched same/fresh-fit held-multiplier controllers. No automatic large online
grid is launched by this diagnosis. Increase to8 triples only if outcomes
are inconclusive and the costs/results justify it.

## Separate WD hypothesis, not a rescue of failed online selection

After diagnosis run TWO short settings, reusing the compatible existing
CLI.04 fixed-WD control as the third comparison. Keep its gradient LR
schedule eta_t. After40-step warmup prescribe

    gamma_t = 2 / (2/(lambda_ref*eta_peak) + t - 40)
    lambda_t = gamma_t / eta_t

During warmup lambda_t=lambda_ref. This tests retaining the contraction
clock through the gradient-LR cooldown. It changes the radius c/lambda_t;
native Nesterov is retained. It is NOT fixed-domain stochastic FW or the
coupled gamma/rho estimator from stochastic FW theory. No cautious masks.
Compare a static lambda chosen to match the exact final sum log(1-eta*lambda)
by bisection. Equal final contraction products do not equal decay histories.
Log actual group WD and cumulative contraction on every update. No new broad
schedule grid or cooldown-removal claim. Further training is conditional on
this narrow screen and fair baseline/decay tuning.

## Execution and records

    python -m research.unnormalized_muon.fresh_campaign

The controller waits for the existing lens campaign and all its registered
jobs to finish. It then prints/submits one diagnosis job (1800s process limit),
followed by the two WD pilots (900s each), through the same locked queue.
Exact commands, commits/configs and raw outputs remain under
nanochat-unnormalized-muon-runs/um-fresh-*/ outside Git. Every job validates
one actual B300. Results/plots publish to FRESH_DIAGNOSIS.md and
fresh_loss_curves.png; failures remain in EXPERIMENTS.csv. No GPU work runs
in the development pod. Stop on failed correctness/gate/budget conditions;
do not claim an incomplete experiment is a method ranking.
