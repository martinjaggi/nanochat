# Fixed ordinary WD and FW-gap LR

Separate subtopic from unnormalization and earlier arbitrary-radius FW runs.
User requested per-layer actual LR first, then joint LR. All use the d8 B300
fork model, ClimbMix and original tokenizer, sequence1024,32768 fresh tokens/update.
No Atlas. No row equilibration or NorMuon. Keep the existing Muon/AdamW partition.

Ordinary unmasked decay is fixed at actual lambda=0.1837498798375862, the
fork's resolved coefficient for CLI WD0.28 at this architecture/batch. Thus
R=1/lambda. It does not follow the baseline cosine decay-of-WD schedule.
The full matrix ray is P_i=Q_i+lambda W_i; adding an L2 loss penalty would
change the experiment. Q_i uses native Nesterov, five Polar Express steps
and Frobenius correction. This approximate direction is not an exact polar
LMO. Measure lambda*||W_i||op at initialization/final; do not hide violations
or claim exact FW guarantees. An optional certified direction is labelled.

For layer mode, b_i=<G_i,P_i>, v_i=||P_i||F², eta_i=min(1/lambda,[b_i]+/(L v_i)).
Use zero when v_i=0. Propose all matrix steps at once. Backtrack the single
Frobenius curvature L until the full same-batch compiled loss satisfies
f(candidate)<=f0-sum eta_i*b_i+L/2*sum eta_i²*v_i. Nonpositive blocks stay fixed.
This is per-layer LR selection with a shared curvature bound and combined
acceptance, not52 separate coordinate searches. Cross-layer changes are
included in the complete-loss check. L starts from half its previous value.

Joint-uniform mode uses one actual eta=min(1/lambda,[sum b_i]+/(L sum v_i)).
The exact algebra is gamma=lambda*eta, W+=(1-gamma)W+gamma*(-Q/lambda).
Do not apply the fork's shape factor a second time to these actual LRs.
Log native c_i and the implied CLI LR eta_i/(0.25*c_i).

The separately labelled joint-native ablation preserves native layer
multipliers by searching c_i P_i. It uses b=sum c_i*b_i, v=sum c_i²*v_i,
eta_outer<=1/(lambda*max c_i); actual eta_i=c_i*eta_outer. This gives
layer-dependent gamma_i=lambda*c_i*eta_outer, not one shared FW mixing.

The shifted reciprocal control uses native actual eta_i0=CLI_LR*0.25*c_i,
40-update linear warmup, then eta_i(t)=eta_i0/(1+lambda*eta_i0*t/2), counting
t after warmup. Hence gamma_i=2/(t+2/(lambda*eta_i0)). Auxiliary AdamW follows
its unchanged native schedule. Native momentum is also retained; this is
not the gradient-estimation schedule of a convex stochastic FW theorem.
An existing native LR cooldown with the SAME fixed lambda is the control.

Per effective batch: capture all microbatch inputs before loader reuse,
clone/token-weight fresh losses, accumulate gradients once, freeze auxiliary
weights for all candidate checks, then apply only native AdamW groups.
Functional candidates are compiled with the same numerical strategy as
training. No live weight/.grad swaps. First-step audit checks parameters,
gradients,buffers,RNG. Count every effective/microbatch forward probe.
Actual decay exposure for gap arms is sum actual_eta_i*lambda per matrix.
Nominal inner optimizer LR metadata is not the actual searched LR.

Initial stage:64 updates per-layer gap/reciprocal/fixed-WD cosine with
microbatch16,accumulation2; then64-update joint-uniform/joint-native checks.
Next: matched2000-update pilot and outer initial-LR search for reciprocal
and fixed-WD cosine; tune initial curvature only if sensitivity warrants it.
Promote selected settings to20000 updates and new paired seeds after a
cost estimate. Same tuning/heldout separation as the surrounding campaign.

Exactly one verified B300/job, maximum6 outstanding in the ONE central queue,
30GPUh aggregate INCLUDING all previous project runs. Per-run immutable
source/configs/logs/checkpoints live outside Git in
/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/um-gapwd-*.
All configs, findings and detailed summaries are pushed to
martinjaggi/nanochat:unnormalized-muon. No credentials/data/raw checkpoints in Git.
