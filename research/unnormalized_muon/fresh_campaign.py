"""Report-inspired diagnosis AFTER the existing campaign, through the same queue."""
import json,pathlib,subprocess,sys,time
from research.unnormalized_muon.queue import ROOT,REPO,load
from research.unnormalized_muon.gap_wd_campaign import record,stage
from research.unnormalized_muon.fresh_math import matched_static_wd
D=REPO/'research/unnormalized_muon';LAM=.1837498798375862


def main():
    # Wait rather than creating a second submission queue or scheduler backlog.
    while subprocess.run(['pgrep','-f',r'python[^ ]* .*research\.unnormalized_muon\.lens_campaign'],stdout=subprocess.DEVNULL).returncode==0 or any(not v['recorded'] for v in load().values()):time.sleep(30)
    c=dict(protocol_version=3,clean=True,variant=False,decay_mode='standard',fixed_wd=LAM,gap_geometry='q_scaled',matrix_lr=.04,matrix_schedule='cooldown',updates=2000,seed=0,depth=8,runtime_limit=1800,warmup_updates=3,fresh_diagnosis=True,branch_steps=[40,400,1500])
    record({'fresh-diagnosis-001':c},'After existing FW-lens campaign: ONE B300 frozen diagnosis,1800s limit, checkpoints40/400/1500 with exact full state and replay; four disjoint training/fit/check triples each, own-path derivative/noise checks, cap/sign comparison and400-step branch continuations. No new online sweep before independent benefit survives continuation. Project total50GPUh, six-slot queue unchanged.')
    stage('fresh-diagnosis-')
    p=ROOT/'um-fresh-diagnosis-001/fresh_diagnosis.json'
    assert p.exists(),'diagnosis failed; inspect preserved logs before proceeding'
    r=json.loads(p.read_text());assert r['status']=='completed'
    from research.unnormalized_muon.publish import publish
    publish()
    record({},'Frozen fresh-data gate '+('PASSED: analyze local transfer before implementing matched same/fresh-fit held-multiplier controllers.' if r['gate_passed'] else 'FAILED: stop online-controller expansion; retain negative diagnosis and cheap-rule evidence.'))
    # Separate, narrowly preregistered hypothesis requested by the user: keep
    # the FW mixing clock through gradient cooldown by changing ordinary WD.
    # This is NOT promotion of a failed online controller.
    base={k:v for k,v in c.items() if k not in ['fresh_diagnosis','branch_steps']};base['runtime_limit']=900
    configs={'fresh-wd-mixing':dict(base,wd_schedule='fw_mixing_reciprocal'),
        'fresh-wd-static-product':dict(base,fixed_wd=matched_static_wd(.01,LAM),wd_schedule='fixed')}
    record(configs,'Separate two-run WD hypothesis screen after diagnosis; reuse exact CLI.04 static-WD reference. Preserve shifted reciprocal FW mixing gamma through scheduled gradient-LR cooldown via lambda_t=gamma_t/eta_t (CHANGING radius); compare fixed lambda matching final log contraction. Native momentum unchanged, no fixed-ball stochastic FW theorem claim. One B300/job,900s,50GPUh total guard. No broad schedule grid.')
    stage('fresh-wd-');publish()
    record({},'Report-inspired diagnosis and narrow WD-mixing pilot completed. Inspect FRESH_DIAGNOSIS.md and frozen plots. Positive online gate requires implementation/review of matched same/fresh-fit controller next; negative gate halts that expansion. No final-heldout tuning or automatic broad sweep.')

if __name__=='__main__':main()
