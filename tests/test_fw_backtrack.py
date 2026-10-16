import torch
from research.unnormalized_muon.fw import backtrack,spectral_safe

def test_quadratic_backtracking_and_no_mutation():
 x=torch.tensor([2.,-1.],dtype=torch.float64);d=-x;grad=3*x
 b=float(-(grad*d).sum());v=float(d.square().sum());f0=float(1.5*x.square().sum())
 saved=x.clone()
 def evaluate(gamma):return float(1.5*(x+gamma*d).square().sum())
 gamma,L,trials,accepted=backtrack(evaluate,f0=f0,b=b,v=v,L=.1,tolerance=0.)
 assert accepted and len(trials)>1 and 0<gamma<=1 and L>=3
 assert evaluate(gamma)<f0 and torch.equal(saved,x)

def test_negative_alignment_skips_all_forward_queries():
 def never(gamma):raise AssertionError('must not query')
 assert backtrack(never,f0=1.,b=-1.,v=2.,L=1.)==(0.,1.,[],False)
 assert backtrack(never,f0=1.,b=1.,v=0.,L=1.)==(0.,1.,[],False)

def test_spectral_certificate_and_shared_mixing_feasibility():
 for shape in [(4,3),(3,4)]:
  torch.manual_seed(4);q=spectral_safe(torch.randn(shape,dtype=torch.float64)*3)
  assert torch.linalg.matrix_norm(q,ord=2)<=1
  w=spectral_safe(torch.randn(shape,dtype=torch.float64))
  for gamma in [0.,.2,.8,1.]:
   candidate=(1-gamma)*w+gamma*(-q)
   assert torch.linalg.matrix_norm(candidate,ord=2)<=1+1e-12

def test_accumulated_baseline_matches_token_weighted_candidates():
 from research.unnormalized_muon.fw import FWMuon,weighted_mean
 # Exercise the actual set_loss path: unequal token counts expose accidental
 # averaging of means, while distinct losses expose retaining only the last.
 fw=FWMuon.__new__(FWMuon);fw.batch=[];fw.losses=[];fw.loss_counts=[]
 buffer=torch.tensor(2.)
 fw.set_batch(torch.zeros(1,2),torch.zeros(1,2));fw.set_loss(buffer)
 buffer.fill_(6.)  # a compiled backend may reuse its scalar output storage
 fw.set_batch(torch.zeros(1,6),torch.zeros(1,6));fw.set_loss(buffer)
 assert fw.loss_before.item()==5.
 assert fw.loss_before.item()==weighted_mean([torch.tensor(2.),torch.tensor(6.)],[2,6]).item()
 assert fw.loss_before.item()!=fw.losses[-1].item()

def test_exact_gradient_oracle_gap_matches_nuclear_dual():
 torch.manual_seed(13)
 b=0.;formula=0.;v=0.
 for shape,R in [((3,4),2.),((4,3),3.)]:
  grad=torch.randn(shape,dtype=torch.float64);w=spectral_safe(torch.randn(shape,dtype=torch.float64))*R
  u,s,vh=torch.linalg.svd(grad,full_matrices=False);q=u@vh;d=-R*q-w
  b+=float(-(grad*d).sum());formula+=float((grad*w).sum()+R*s.sum());v+=float(d.square().sum())
 assert abs(b-formula)<1e-12 and b>=0 and v>0
 # The quadratic ray upper bound is minimized by the shared gap-based step.
 L=2.;gamma=min(1.,b/(L*v))
 for candidate in [0.,max(0.,gamma-.01),min(1.,gamma+.01),1.]:
  assert -gamma*b+.5*L*gamma*gamma*v<=-candidate*b+.5*L*candidate*candidate*v+1e-12
