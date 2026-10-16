"""Publish frozen-state diagnosis and the independent WD-mixing pilot."""
import json,pathlib,statistics
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs');DEST=pathlib.Path(__file__).resolve().parent


def generate():
    files=list(ROOT.glob('um-fresh-diagnosis-*/fresh_diagnosis.json'))
    if not files:return []
    p=sorted(files)[-1];r=json.loads(p.read_text());rows=r['probe_rows']
    lines=['# Fresh-data diagnosis of Muon step selection','',
        'One B300, native dense depth8/512,125,829,354 parameters, ClimbMix/32K tokenizer,32768 tokens/update. The control trajectory uses the original2000-update schedule (65.536M tokens,0.521 tokens/parameter). Three exact named-momentum checkpoints preserve prefetched data and CPU/CUDA/Python/NumPy RNG; replay validates immutable files and next-batch hash. Fixed ordinary lambda=.1837498798375862; Q includes shape, and all candidate paths freeze auxiliary parameters.','',
        'Four training/fit/check triples at each of40,400,1500 completed updates. Fit/check use different reserved training shards, disjoint from the construction/continuation prefix. Check batches score fixed train-selected and fit-selected choices; they NEVER select the grid point. Per-sequence losses and signed block slopes are in the private JSON artifact. Sequence SEs are local pilot diagnostics, not training-seed uncertainty or a sequential-testing guarantee.','',
        '| Checkpoint | Triple | Train-selected / baseline LR | Fit-selected / baseline LR | Check CE delta, train-selected | Check CE delta, fit-selected | Fit delta SE | Block slope sign flips |','|---:|---:|---:|---:|---:|---:|---:|---:|']
    for x in rows:
        lines.append(f'| {x["step"]} | {x["triple"]} | {x["grid"][x["selected_train_index"]]/x["eta_base"]:.3g} | {x["grid"][x["selected_fit_index"]]/x["eta_base"]:.3g} | {x["check_delta_train_selected"]["mean"]:+.6g} | {x["check_delta_fit_selected"]["mean"]:+.6g} | {x["check_delta_fit_selected"]["se"]:.4g} | {x["sign_flip_fraction"]:.3f} |')
    lines+=['','## Continuations from update400','',
        'The original2000-update horizon is retained. Only the Muon coefficient changes; native auxiliary LRs and future batch/RNG prefixes match. One-step alternatives revert immediately to the common schedule; held128 retains the selected multiplier while recomputing the direction each update. Development evaluation is independent of probe selection.','',
        '| Policy | Multiplier | Dev CE after32 | Dev CE after128 | Gradient evaluations |','|---|---:|---:|---:|---:|']
    for x in r['continuations']:lines.append(f'| {x["policy"]} | {x["ratio"]:.3g} | {x["evaluations"]["32"]["loss"]:.6f} | {x["evaluations"]["128"]["loss"]:.6f} | {x["gradient_evals"]} |')
    lines+=['',f'Fresh-selected check improvements: {r["fresh_check_improvements"]}/{r["total_probes"]}. Preregistered engineering gate: at least8/12 check improvements AND one fit-selected alternative improving independent continuation CE by>.001 at BOTH32 and128 updates. Gate passed: **{r["gate_passed"]}**. This is a conservative pilot gate, not statistical significance.','',f'Decision: {r["decision"]}.','',f'All probe costs: `{json.dumps(r["cost"],sort_keys=True)}`. Includes parity gradients and explicitly counted continuation gradients; kernel setup, validation and checkpoint I/O remain in end-to-end GPU charge.','',
        'Native prescribed-step parity audits: '+json.dumps(r['parity_audits'],sort_keys=True),
        '',f'Private raw artifact: `{p}`. Frozen-state loss curves, sequence losses, FD/noise checks, cap/sign versus Armijo differences and batch hashes are preserved there.','',
        '## Separate WD-mixing hypothesis','',
        'Keep the successful scheduled gradient LR eta_t. After warmup prescribe gamma_t=2/(2/(lambda_ref*eta_peak)+t-40), and set lambda_t=gamma_t/eta_t. This retains a shifted reciprocal mixing clock through cooldown. It CHANGES the implied radius c/lambda_t and retains native Nesterov: it is not the fixed-domain stochastic FW theorem or its coupled gradient estimator. Compare reference static WD and a static WD matched to the final log contraction; equal final products do not match decay histories. No large new schedule grid is justified by this pilot.','',
        '| Run | WD rule | Actual reference lambda | Validation CE | Active sec |','|---|---|---:|---:|---:|']
    for sp in ROOT.glob('um-fresh-wd-*/summary.json'):
        s=json.loads(sp.read_text());c=s['config'];lines.append(f'| {sp.parent.name} | {c.get("wd_schedule","fixed")} | {c["fixed_wd"]:.9g} | {s["validation"]["loss"]:.6f} | {s["training_active_seconds"]:.3f} |')
    base=ROOT/'um-lens-main-control-lr0p04/summary.json'
    if base.exists():
        s=json.loads(base.read_text());lines.append(f'| reused compatible reference control | fixed | .183749880 | {s["validation"]["loss"]:.6f} | {s["training_active_seconds"]:.3f} |')
    (DEST/'FRESH_DIAGNOSIS.md').write_text('\n'.join(lines)+'\n');paths=['research/unnormalized_muon/FRESH_DIAGNOSIS.md']
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,3.6))
    for step,ax in zip([40,400,1500],axes):
        group=[x for x in rows if x['step']==step]
        for role in ['train','fit','check']:
            curves=[[z-x['loss_curves'][role][0] for z in x['loss_curves'][role]] for x in group]
            ys=[statistics.mean(c[i] for c in curves) for i in range(5)]
            ax.plot([0,.25,.5,1,2],ys,'.-',label=role)
        ax.axhline(0,color='k',lw=.5);ax.set_title(f'Frozen update{step}');ax.set_xlabel('Actual eta / scheduled eta');ax.set_ylabel('CE change from no step');ax.grid(alpha=.2);ax.legend()
    fig.tight_layout();fig.savefig(DEST/'fresh_loss_curves.png',dpi=150);plt.close(fig);paths.append('research/unnormalized_muon/fresh_loss_curves.png');return paths
