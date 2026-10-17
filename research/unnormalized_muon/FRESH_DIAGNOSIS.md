# Fresh-data diagnosis of Muon step selection

One B300, native dense depth8/512,125,829,354 parameters, ClimbMix/32K tokenizer,32768 tokens/update. The control trajectory uses the original2000-update schedule (65.536M tokens,0.521 tokens/parameter). Three exact named-momentum checkpoints preserve prefetched data and CPU/CUDA/Python/NumPy RNG; replay validates immutable files and next-batch hash. Fixed ordinary lambda=.1837498798375862; Q includes shape, and all candidate paths freeze auxiliary parameters.

Four training/fit/check triples at each of40,400,1500 completed updates. Fit/check use different reserved training shards, disjoint from the construction/continuation prefix. Check batches score fixed train-selected and fit-selected choices; they NEVER select the grid point. Per-sequence losses and signed block slopes are in the private JSON artifact. Sequence SEs are local pilot diagnostics, not training-seed uncertainty or a sequential-testing guarantee.

| Checkpoint | Triple | Train-selected / baseline LR | Fit-selected / baseline LR | Check CE delta, train-selected | Check CE delta, fit-selected | Fit delta SE | Block slope sign flips |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 40 | 0 | 2 | 2 | +0.000106603 | +0.000106603 | 0.001119 | 0.019 |
| 40 | 1 | 2 | 2 | +0.0014578 | +0.0014578 | 0.001616 | 0.000 |
| 40 | 2 | 2 | 2 | -0.00357199 | -0.00357199 | 0.001199 | 0.000 |
| 40 | 3 | 2 | 1 | +0.00113034 | +0 | 0 | 0.019 |
| 400 | 0 | 2 | 0.5 | +0.0212248 | -0.00232371 | 0.000658 | 0.038 |
| 400 | 1 | 2 | 0.5 | +0.0170429 | -0.00124302 | 0.0005506 | 0.000 |
| 400 | 2 | 2 | 0.5 | +0.011299 | +1.47372e-05 | 0.0004279 | 0.000 |
| 400 | 3 | 2 | 0.5 | +0.0174525 | -0.00202568 | 0.0004807 | 0.058 |
| 1500 | 0 | 2 | 0.5 | +0.00394633 | -0.00016813 | 0.000288 | 0.115 |
| 1500 | 1 | 2 | 0.5 | +0.00392074 | -0.000640154 | 0.0002856 | 0.077 |
| 1500 | 2 | 2 | 0.5 | +0.00394229 | -8.78945e-05 | 0.0002779 | 0.077 |
| 1500 | 3 | 2 | 1 | +0.00184646 | +0 | 0 | 0.154 |

## Continuations from update400

The original2000-update horizon is retained. Only the Muon coefficient changes; native auxiliary LRs and future batch/RNG prefixes match. One-step alternatives revert immediately to the common schedule; held128 retains the selected multiplier while recomputing the direction each update. Development evaluation is independent of probe selection.

| Policy | Multiplier | Dev CE after32 | Dev CE after128 | Gradient evaluations |
|---|---:|---:|---:|---:|
| one_step | 1 | 4.368412 | 4.248385 | 128 |
| one_step | 0.5 | 4.367327 | 4.251448 | 128 |
| one_step | 0.25 | 4.367687 | 4.249002 | 128 |
| held128 | 0.5 | 4.332419 | 4.189805 | 128 |
| held128 | 0.25 | 4.322452 | 4.172127 | 128 |

Fresh-selected check improvements: 7/12. Preregistered engineering gate: at least8/12 check improvements AND one fit-selected alternative improving independent continuation CE by>.001 at BOTH32 and128 updates. Gate passed: **False**. This is a conservative pilot gate, not statistical significance.

Decision: stop online-controller expansion; report negative diagnosis or prefer cap/sign if matched.

All probe costs: `{"continuation_gradient_evals": 640, "continuation_tokens": 20971520, "continuation_validation_forward_evals": 80, "continuation_validation_tokens": 2621440, "forward_evals": 411, "gradient_evals": 39, "probe_tokens": 13467648}`. Includes parity gradients and explicitly counted continuation gradients; kernel setup, validation and checkpoint I/O remain in end-to-end GPU charge.

Native prescribed-step parity audits: [{"forward_evals": 1, "gradient_evals": 1, "max_momentum_relative_error": 0.0, "max_relative_displacement_error": 2.429874257359188e-06, "step": 40}, {"forward_evals": 1, "gradient_evals": 1, "max_momentum_relative_error": 0.0, "max_relative_displacement_error": 1.9873259589076042e-06, "step": 400}, {"forward_evals": 1, "gradient_evals": 1, "max_momentum_relative_error": 0.0, "max_relative_displacement_error": 1.2760375284415204e-05, "step": 1500}]

Private raw artifact: `/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/um-fresh-diagnosis-001/fresh_diagnosis.json`. Frozen-state loss curves, sequence losses, FD/noise checks, cap/sign versus Armijo differences and batch hashes are preserved there.

## Separate WD-mixing hypothesis

Keep the successful scheduled gradient LR eta_t. After warmup prescribe gamma_t=2/(2/(lambda_ref*eta_peak)+t-40), and set lambda_t=gamma_t/eta_t. This retains a shifted reciprocal mixing clock through cooldown. It CHANGES the implied radius c/lambda_t and retains native Nesterov: it is not the fixed-domain stochastic FW theorem or its coupled gradient estimator. Compare reference static WD and a static WD matched to the final log contraction; equal final products do not match decay histories. No large new schedule grid is justified by this pilot.

| Run | WD rule | Actual reference lambda | Validation CE | Active sec |
|---|---|---:|---:|---:|
| reused compatible reference control | fixed | .183749880 | 3.554822 | 65.063 |
