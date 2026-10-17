"""Report all frozen-model scores on both original and larger heldout sets."""
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research.unnormalized_muon.early_allocation import ROOT,D


def main(name='um-earlyalloc-large-eval-001'):
    out=ROOT/name;scores=json.loads((out/'scores.json').read_text());summary=json.loads((out/'summary.json').read_text())
    assert summary['status']=='completed' and len(scores)==summary['models_scored']==30
    assert summary['updates']==summary['fresh_microbatch_gradient_passes']==0
    assert len({r['large_heldout']['validation_hash'] for r in scores})==1
    lookup={(r['arm'],r['seed']):r for r in scores}
    lines=['# Larger untouched heldout evaluation','',
    'All30already-frozen final checkpoints scored on the SAME2097152target tokens, native validation batch positions64–127. Validation epoch1 is asserted; these positions are disjoint from original tuning/heldout blocks0–7. Same ClimbMix/native32k tokenizer,32x1024, native BF16 compute/FP32 matrix parameters and compiled loss path. NO training or gradient evaluations. Every checkpoint reproduced its ORIGINAL tuning and heldout hashes/scores within1e-5 before larger scoring.','',
    'This adds a new evaluation segment without replacing the original outcomes or changing any settings. Absolute CE differs across segments; compare paired method differences within a segment. The fixed-WD family has6seeds; contraction controls have3. Per-sequence nats/counts are retained outside Git; packed sequences can be dependent, so no independent-sequence significance claim is made.','',
    '| Seed | Arm | Original paired CE delta | Larger paired CE delta | Larger CE | Larger BPB |','|---|---|---:|---:|---:|---:|']
    stats={};fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    colors=dict(mid='#6b3e91',early='#d96925',matched='#708238',neutral='#8b5e3c',midmatched='#438d8b',history='#d13d62')
    for r in sorted(scores,key=lambda r:(r['seed'],r['arm'])):
        b=lookup['baseline',r['seed']];old=r['original_heldout']['loss']-b['original_heldout']['loss'];new=r['large_heldout']['loss']-b['large_heldout']['loss']
        lines.append(f'| {r["seed"]} | {r["arm"]} | {old:+.9f} | {new:+.9f} | {r["large_heldout"]["loss"]:.9f} | {r["large_heldout"]["bpb"]:.9f} |')
    for arm in colors:
        rr=[r for r in scores if r['arm']==arm];old=[r['original_heldout']['loss']-lookup['baseline',r['seed']]['original_heldout']['loss'] for r in rr];new=[r['large_heldout']['loss']-lookup['baseline',r['seed']]['large_heldout']['loss'] for r in rr]
        assert len(rr)==(6 if arm in ['mid','early'] else 3)
        x=dict(n=len(rr),original_mean=statistics.mean(old),large_mean=statistics.mean(new),large_sample_sd=statistics.stdev(new),seeds=[r['seed'] for r in rr],large_deltas=new);stats[arm]=x
        lines+=['',f'{arm}: n={len(rr)}, original mean delta{x["original_mean"]:+.6f}; larger-set mean **{x["large_mean"]:+.6f}CE**, sampleSD **{x["large_sample_sd"]:.6f}**.']
        axs[0].scatter(old,new,color=colors[arm],label=f'{arm} n={len(rr)}')
        axs[1].plot([r['seed'] for r in rr],new,'o',color=colors[arm],label=arm)
    for arm,control in [('early','matched'),('mid','midmatched')]:
        rr=[r for r in scores if r['arm']==control];ds=[lookup[arm,r['seed']]['large_heldout']['loss']-r['large_heldout']['loss'] for r in rr]
        key=arm+'_vs_'+control;stats[key]=dict(n=len(ds),large_mean=statistics.mean(ds),large_sample_sd=statistics.stdev(ds),large_deltas=ds)
        lines+=['',f'Final-contraction-controlled {arm} minus {control}: larger-set mean **{statistics.mean(ds):+.6f}CE**, sampleSD **{statistics.stdev(ds):.6f}**, n=3.']
    max_roundtrip=max(abs(r['roundtrip_tuning']['loss']-json.loads((ROOT/r['run_id']/'summary.json').read_text())['validation']['loss']) for r in scores)
    lines+=['',f'Evaluation job `{name}`: worker elapsed{summary["end_to_end_seconds"]:.3f}s, all scoring{summary["validation_seconds"]:.3f}s (includes first compilation), compilation{summary["compile_seconds"]:.3f}s; checkpoint copies{summary["checkpoint_load_seconds"]:.3f}s;{summary["evaluation_microbatch_forwards"]}actual evaluation microbatch forwards/{summary["evaluation_tokens"]}evaluated targets. Zero fresh gradients or optimizer updates. Maximum tuning roundtrip error{max_roundtrip:.3g}CE. Target hash`{summary["large_heldout_hash"]}`.','',
    '![Original versus larger paired heldout differences](EARLY_ALLOCATION_LARGE_HELDOUT.png)']
    (D/'EARLY_ALLOCATION_LARGE_HELDOUT.md').write_text('\n'.join(lines)+'\n');(D/'EARLY_ALLOCATION_LARGE_HELDOUT.json').write_text(json.dumps(stats,indent=2)+'\n')
    limits=axs[0].axis();lo=min(limits[0],limits[2]);hi=max(limits[1],limits[3]);axs[0].plot([lo,hi],[lo,hi],':',color='gray')
    for ax in axs:ax.axhline(0,color='gray',lw=1);ax.grid(alpha=.2);ax.legend(fontsize=8)
    axs[0].axvline(0,color='gray',lw=1);axs[0].set(xlabel='Original262k paired CE delta',ylabel='Larger2M paired CE delta',title='Frozen methods; different untouched segments')
    axs[1].set(xlabel='Paired seed',ylabel='Larger-set CE delta vs baseline',title='Negative favors the variant')
    fig.savefig(D/'EARLY_ALLOCATION_LARGE_HELDOUT.png',dpi=150);plt.close(fig)

if __name__=='__main__':main()
