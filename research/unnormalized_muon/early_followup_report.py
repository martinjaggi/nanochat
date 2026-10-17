"""Append predeclared secondary/history evidence to the primary experiment report."""
import json,statistics
from research.unnormalized_muon.early_allocation import ROOT,D,report
from research.unnormalized_muon.events import read_events


def main():
    report();p=D/'EARLY_ALLOCATION_RESULTS.md';lines=[]
    for title,arm,prefix,control in [
        ('Predeclared near-tied1.5x confirmation','mid','earlyalloc-secondary-mid','baseline'),
        ('1.5x final-contraction-matched control','midmatched','earlyalloc-secondary-midmatched','baseline'),
        ('2x with complete contraction history matched','history','earlyalloc-history','baseline')]:
        lines+=['',f'## {title}','','| Seed | Heldout CE | Delta vs original baseline | Active seconds | Contraction product |','|---|---:|---:|---:|---:|'];ds=[];ss={}
        for seed in [70,71,72]:
            a=ROOT/f'um-{prefix}-s{seed}'/'summary.json';b=ROOT/f'um-earlyalloc-confirm-baseline-s{seed}'/'summary.json'
            if not a.exists() or not b.exists():continue
            s=json.loads(a.read_text());base=json.loads(b.read_text());ss[seed]=s
            assert s['heldout']['validation_hash']==base['heldout']['validation_hash']
            e=read_events(a.parent/'metrics.jsonl',{'manifest'})[0];f=read_events(b.parent/'metrics.jsonl',{'manifest'})[0]
            assert e['initial_parameter_hash']==f['initial_parameter_hash']
            delta=s['heldout']['loss']-base['heldout']['loss'];ds.append(delta)
            contraction=next(iter(s['muon_contraction'].values()))['value']
            if arm=='history':assert all(abs(x['log_abs']-y['log_abs'])<1e-8 for x,y in zip(s['muon_contraction'].values(),base['muon_contraction'].values()))
            lines.append(f'| {seed} | {s["heldout"]["loss"]:.9f} | {delta:+.9f} | {s["training_active_seconds"]:.3f} | {contraction:.9f} |')
        if len(ds)==3:lines+=['',f'Mean paired delta **{statistics.mean(ds):+.6f} CE**, sample SD **{statistics.stdev(ds):.6f}**, n=3.']
        else:lines+=['',f'{len(ds)}/3 paired endpoints completed; do not treat an incomplete group as confirmation.']
        if arm=='mid' and len(ss)==3:
            pairs=[]
            for seed in [70,71,72]:
                x=ROOT/f'um-earlyalloc-secondary-midmatched-s{seed}'/'summary.json'
                if x.exists():
                    c=json.loads(x.read_text());pairs.append(ss[seed]['heldout']['loss']-c['heldout']['loss'])
                    assert all(abs(a['log_abs']-b['log_abs'])<1e-8 for a,b in zip(ss[seed]['muon_contraction'].values(),c['muon_contraction'].values()))
            if len(pairs)==3:lines+=['',f'1.5x minus its final-contraction-matched baseline: mean **{statistics.mean(pairs):+.6f} CE**, sample SD **{statistics.stdev(pairs):.6f}**.']
    check=ROOT/'um-earlyalloc-history-check-001'/'summary.json'
    if check.exists():
        s=json.loads(check.read_text());lines+=['','History-matched64-update B300 integration job: '+s['status']+'. Actual per-update gamma is audited before full diagnostic runs.']
    lines+=['','The1.5x secondary arm and history-matched diagnostic were committed before any fresh heldout endpoints. They are reported alongside the primary2x selection, not chosen after test-set inspection. History matching deliberately varies WD/the implied domain; it is a diagnostic of LR allocation, not a fixed-WD FW method.']
    p.write_text(p.read_text()+'\n'.join(lines)+'\n')

if __name__=='__main__':main()
