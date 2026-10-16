# Muon learning rates through the Frank–Wolfe lens: protocol v2

This applies the user's supplied mathematical note,16 October2026. Earlier v1
runs remain in the ledger; their geometry is different and is not pooled.

For Muon block l: Q_l=c_l NS(M_l), P_l=Q_l+lambda W_l, fixed ordinary unmasked
lambda=.1837498798375862. The ideal spectral ball has radius c_l/lambda.
Actual eta multiplies ALL of P_l; gamma_l=lambda*eta_l. Native fused code
retains LR*c_l for the NS direction and divides its kernel WD coefficient
by c_l, giving unscaled contraction eta*lambda. No extra L2 loss penalty.
Time-varying WD and cautious masks belong to separate earlier experiments.

NS retains native Nesterov/five Polar Express/Frobenius correction; row
 equilibration and NorMuon are disabled in every controlled arm. This is a
practical approximate oracle; exact full-gradient FW convergence guarantees
are not claimed. Initial/final lambda*||W_l||op/c_l are logged, not hidden.
Current raw gradient G measures b_l=<G_l,P_l>, not the momentum input M_l.
Momentum updates ONCE per update, never during a candidate retry.

Joint: eta=min(cap_t,[sum b_l]+/(L sum||P_l||F²)), cap_t<=1/lambda.
Backtrack L from half the previous accepted estimate against the complete
same-minibatch compiled quadratic model. Positive part is AFTER summing.

Layer Armijo: form eta_l=min(cap_t,[b_l]+/(L_l||P_l||F²)); initially all
proposal-curvature L_l share the carried scalar. Freeze the entire proposal
and P, backtrack ONE zeta in(0,1] until f(candidate)<=f0-.1*zeta*sum eta_l*b_l,
with recorded numerical slack and no measured increase allowed. This checks
cross-block changes in the full loss; it is not a block-diagonal Hessian claim.
The earlier layer global-L simultaneous quadratic check remains separately
labelled and was not independent-block-L certification.

First18 short trials: ordinary-WD native cooldown and shifted reciprocal,
three tuned peak CLI LRs each; joint and layer variants each have actual caps
{.005,.02,.08}, stable versus native terminal-cooldown cap. All share warmup40,
32768 fresh tokens/update,sequence1024,depth8,BF16 native precision and fixed
lambda. Auxiliary optimizer/schedules and momentum are identical. Reciprocal
eta0/(1+lambda*eta0*t/2) counts t after warmup; for v2 eta0=CLI_LR*.25, and c
is in Q rather than this LR. Inverse-square-root is optional after main tests.

Refine all six families' best LR/cap with equal boundary/midpoint rules;
check initial-curvature sensitivity in all four gap families. Then creative
one-change tests: per-layer LR proposal EMA beta{.5,.9}, per-layer relative
step cap r{.01,.03}, joint loss-check cadence{2,4}. Relative cap bounds
||eta_l P_l||F by r*max(||W_l||F,.1*(c_l/lambda)*sqrt(min shape)), avoiding
freezing zero-initialized matrices. Smoothed proposals are gated by current
b_l and still Armijo-checked. Intermittent checks use cached L without extra
forwards on intervening updates; those updates are explicitly UNCHECKED.
There is no acceptance certificate on an unchecked step.

All loss checks reuse the exact current effective batch and CPU/CUDA RNG,
freeze AdamW weights, use the same compiled numerical path as training, and
never swap live gradients/weights. Baseline and candidate losses have the
same token weighting across every microbatch. First-step state/RNG audit,
compiled geometry parity, NaN/accounting checks precede screening.

Screen before long promotions: at most10 fresh20000-update runs (655.36M
fresh tokens), retaining both cap policies, tuned control/reciprocal settings
and at most one competitive creative family. Freeze settings before NEW
paired seeds10/11/12; reserve final heldout tokens for reporting only.
Report paired deltas, mean and sample SD; three seeds are limited evidence.

Compute comparisons are separate reruns: H is median control confirmation
training-active time. Rerun control and strongest gap with time-based LR/cap
and auxiliary/momentum clocks for all3 seeds, finishing the last started
update and reporting <=one-update overshoot. Reciprocal remains explicitly
update-indexed/horizon-free if tested in that comparison. Token-curve prefixes
are NOT matched equal-time endpoints with the same LR schedule.

All measured new runs use3 discarded warmup updates, then exact model,
optimizer,data-prefix and CPU/CUDA RNG restoration. Kernel warmup/GC/reset
seconds and gradient/forward counts are charged to total job cost separately.
Active time includes data delivery, probes, optimizer, ordinary logging/GC,
and excludes recorded overlapping compiler events, validation,checkpoint I/O
and one-time setup. E2E/process time and conservative GPU-job charge include
all overhead. Product_t(1-lambda*eta_l,t) and sum eta_l*lambda are both logged;
the product is represented in signed log space to handle zero/underflow.

Use ONE submission queue, exactly ONE verified B300/job, max SIX outstanding.
Hard total50 B300 GPU-hours includes all previous project runs and failures.
Do not exhaust the cap to rescue a negative result; failed prerequisites or
budget guards halt later submissions and preserve/reap jobs. Private raw
outputs stay under nanochat-unnormalized-muon-runs/um-lens-* outside Git.
Push configs, code and concise findings continuously to
martinjaggi/nanochat:unnormalized-muon.
