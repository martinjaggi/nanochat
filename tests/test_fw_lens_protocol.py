import math
import torch
import pytest
from research.unnormalized_muon.protocol_math import contraction,overlap_seconds,budget_multiplier
from research.unnormalized_muon.gap_wd import block_armijo,propose_etas


def test_c_inside_q_means_unscaled_decay_and_shared_mixing():
 torch.manual_seed(6);lam=.18;eta=.03
 for c in [1.,2.]:
  w=torch.randn(4,3,dtype=torch.float64)*.1;g=torch.randn_like(w)
  u,_,vh=torch.linalg.svd(g,full_matrices=False);q=c*(u@vh);p=q+lam*w
  torch.testing.assert_close(w-eta*p,(1-lam*eta)*w+lam*eta*(-q/lam))
  assert torch.linalg.matrix_norm(-q/lam,ord=2)<=c/lam+1e-12


def test_layer_armijo_holds_proposal_fixed_under_common_multiplier():
 # First block is capped, second isn't. Re-solving after doubling L would
 # change their relative rates; Armijo must preserve the proposed block ray.
 b=[100.,.1];v=[1.,1.];L=1.;cap=.5;base=propose_etas(b,v,L,1.,'layer',max_eta=cap)
 calls=[]
 def f(eta):
  calls.append(eta);return 1.-sum(e*x for e,x in zip(eta,b))+500*sum(e*e*y for e,y in zip(eta,v))
 eta,curvature,trials,ok=block_armijo(f,f0=1.,b=b,v=v,L=L,decay=1.,max_eta=cap,tolerance=0.)
 assert ok and len(trials)>1
 for rates in calls:assert math.isclose(rates[0]/rates[1],base[0]/base[1])
 assert trials[-1]['zeta']<1 and f(eta)<=trials[-1]['bound']
 assert curvature==L/trials[-1]['zeta']


def test_contraction_product_tracks_zero_underflow_and_sign():
 state=None;direct=1.
 for gamma in [.01,.03,0.,.02]:
  state=contraction(state,gamma);direct*=1-gamma
 assert math.isclose(state['value'],direct,rel_tol=1e-14)
 state=contraction(state,1.);assert state['value']==0 and state['log_abs'] is None
 assert contraction(state,.2)['value']==0
 assert contraction(None,1.2)['sign']==-1


def test_compile_time_overlap_unions_and_clips_nested_events():
 assert overlap_seconds([(0.,4.),(2.,6.),(3.,4.),(7.,10.)],1.,8.)==6.
 assert overlap_seconds([(0.,1.),(4.,5.)],2.,3.)==0.
 assert overlap_seconds([(0.,100.)],2.,3.)==1.


def test_time_budget_lr_schedule_endpoints_and_warmup():
 assert budget_multiplier(0.)==.025
 assert budget_multiplier(.002)==1.
 assert budget_multiplier(.35)==1.
 assert math.isclose(budget_multiplier(1.),.05)
 assert budget_multiplier(.6)>budget_multiplier(.9)


@pytest.mark.parametrize('shape',[(4,2),(2,4)])
def test_actual_optimizer_q_scaled_geometry_does_not_scale_decay_twice(monkeypatch,shape):
 import nanochat.optim as opt
 monkeypatch.setattr(opt,'CLEAN_MUON',True);monkeypatch.setattr(opt,'MUON_DECAY_MODE','standard')
 monkeypatch.setattr(opt,'UNNORMALIZED_MUON',False);monkeypatch.setattr(opt,'RECORD_DUAL_SCALE',False)
 monkeypatch.setattr(opt,'muon_step_fused',opt.muon_step_fused.__wrapped__)
 torch.manual_seed(3);initial=torch.randn(shape);grad=torch.randn(shape)
 def run(geometry):
  monkeypatch.setattr(opt,'MUON_GEOMETRY',geometry)
  p=torch.nn.Parameter(initial.clone());p.grad=grad.clone()
  o=opt.MuonAdamW([dict(params=[p],kind='muon',lr=.01,momentum=.85,ns_steps=5,beta2=.9,weight_decay=.2)])
  o.step();return p.detach()
 legacy=run('legacy');inside=run('q_scaled');c=max(1.,shape[0]/shape[1])**.5
 torch.testing.assert_close(inside,legacy+.01*.2*(c-1)*initial,rtol=1e-5,atol=2e-7)


def test_reciprocal_equal_time_clock_ignores_update_count():
 from research.unnormalized_muon.protocol_math import reciprocal_schedule
 eta=.005;lam=.18
 for r in [0.,.001,.002,.25,.75,1.]:
  assert reciprocal_schedule(eta,lam,300,time_progress=r)==reciprocal_schedule(eta,lam,900,time_progress=r)
 assert reciprocal_schedule(eta,lam,0,time_progress=0)==eta/40
 assert reciprocal_schedule(eta,lam,1,time_progress=.002)==eta
 assert reciprocal_schedule(eta,lam,0)==eta/40
 assert reciprocal_schedule(eta,lam,39)==eta
 assert reciprocal_schedule(eta,lam,400)==eta/(1+.5*lam*eta*360)
