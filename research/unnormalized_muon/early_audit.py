"""Stream all executed update coefficients; no model execution or GPU use."""
import json,math,hashlib
from research.unnormalized_muon.early_allocation import ROOT,D
from research.unnormalized_muon.cooldown_schedule import early_reciprocal,history_matched_early_wd


def updates(path):
    with path.open() as f:
        for line in f:
            if line.startswith('{"event": "update"'):yield json.loads(line)


def main():
    reference=ROOT/'um-earlyalloc-screen-k1';manifest=json.loads((reference/'metrics.jsonl').open().readline())
    groups=manifest['optimizer_groups'];indices=[i for i,g in enumerate(groups) if g['kind']=='muon'];aux=[i for i,g in enumerate(groups) if g['kind']!='muon']
    assert len(indices)==4 and sum(len(groups[i]['names']) for i in indices)==52
    aux_reference=[([e['group_lrs'][i] for i in aux],[e['group_weight_decays'][i] for i in aux],e['data_state']) for e in updates(reference/'metrics.jsonl')]
    assert len(aux_reference)==20000
    hashes={};rows=[];validation_hash=None;heldout_hash=None
    for p in sorted(ROOT.glob('um-earlyalloc-*/summary.json')):
        s=json.loads(p.read_text());c=s.get('config',{})
        if s.get('evaluation_only') or c.get('time_budget') or s['updates']!=20000:continue
        assert s['status']=='completed' and c['matrix_schedule']=='early_reciprocal'
        assert c['clean'] and not c['variant'] and c['decay_mode']=='standard' and c['gap_geometry']=='q_scaled'
        m=json.loads((p.parent/'metrics.jsonl').open().readline())
        assert m['GPU_count']==1 and 'B300' in m['GPU_model'] and m['model_parameters']==125829354 and not m['FP8']
        assert all(g['names']==h['names'] and g['shapes']==h['shapes'] and g['kind']==h['kind'] for g,h in zip(groups,m['optimizer_groups']))
        seed=c['seed'];initial=m['initial_parameter_hash']
        if seed in hashes:assert hashes[seed]==initial
        hashes[seed]=initial
        if validation_hash is None:validation_hash=s['validation']['validation_hash']
        assert s['validation']['validation_hash']==validation_hash
        if s.get('heldout'):
            assert s['heldout']['tokens']==262144 and s['heldout']['block_index']==6
            if heldout_hash is None:heldout_hash=s['heldout']['validation_hash']
            assert s['heldout']['validation_hash']==heldout_hash
        total=0.;logc=0.;n=0;max_error=0.
        for e in updates(p.parent/'metrics.jsonl'):
            t=e['step'];assert t==n;n+=1
            eta=early_reciprocal(.005,t,peak_multiplier=c['early_peak_multiplier'])
            wd=history_matched_early_wd(c['fixed_wd'],t,peak_multiplier=c['early_peak_multiplier']) if c.get('wd_schedule')=='early_history_matched' else c['fixed_wd']
            a=aux_reference[t]
            assert [e['group_lrs'][i] for i in aux]==a[0] and [e['group_weight_decays'][i] for i in aux]==a[1] and e['data_state']==a[2]
            for i in indices:
                assert math.isclose(e['group_lrs'][i],eta,rel_tol=1e-12,abs_tol=1e-16)
                assert math.isclose(e['group_weight_decays'][i],wd,rel_tol=1e-12,abs_tol=1e-16)
                max_error=max(max_error,abs(e['group_lrs'][i]*e['group_weight_decays'][i]-eta*wd))
            assert 0<=eta*wd<1
            total+=eta*wd;logc+=math.log1p(-eta*wd)
        assert n==20000 and s['fresh_microbatch_gradient_passes']==20000 and s['fresh_tokens']==655360000 and not s.get('extra_forward_evals',0)
        assert all(abs(v['log_abs']-logc)<1e-8 and v['sign']==1 for v in s['muon_contraction'].values())
        assert all(abs(s['decay_exposure'][str(i)]-total)<1e-8 for i in indices)
        rows.append(dict(run_id=p.parent.name,seed=seed,peak=c['early_peak_multiplier'],wd_schedule=c.get('wd_schedule','fixed'),max_gamma_error=max_error,log_contraction=logc,contraction=math.exp(logc),updates=n,config_hash=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()))
    payload=dict(status='passed',completed_full_runs=len(rows),updates_audited=sum(r['updates'] for r in rows),muon_blocks=52,auxiliary_schedules_and_data_cursors_identical=True,validation_hash=validation_hash,heldout_hash=heldout_hash,initial_hashes_by_seed=hashes,runs=rows)
    (D/'EARLY_ALLOCATION_EXECUTION_AUDIT.json').write_text(json.dumps(payload,indent=2)+'\n')
    print('AUDIT',len(rows),'full runs',payload['updates_audited'],'updates')

if __name__=='__main__':main()
