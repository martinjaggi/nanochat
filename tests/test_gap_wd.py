import math
import torch
from research.unnormalized_muon.gap_wd import propose_etas,block_backtrack,reciprocal_eta


def test_reciprocal_is_shifted_fw_mixing_per_actual_coefficient():
 for c in [1.,2.]:
  eta0=.01*c;decay=.18;t0=2/(eta0*decay)
  for t in [0,1,100,10000]:
   eta=reciprocal_eta(eta0,decay,t)
   assert math.isclose(eta*decay,2/(t+t0),rel_tol=1e-14)


def test_per_layer_vs_joint_and_complete_decay_direction():
 w=[torch.tensor([.2,-.1],dtype=torch.float64),torch.tensor([-.1,.3],dtype=torch.float64)]
 grads=[2*x for x in w];q=[g/g.norm() for g in grads];lam=.4
 p=[u+lam*x for u,x in zip(q,w)]
 b=[float((g*d).sum()) for g,d in zip(grads,p)];v=[float(d.square().sum()) for d in p]
 eta=propose_etas(b,v,2.,lam,'layer')
 for e,bb,vv in zip(eta,b,v):assert math.isclose(e,min(1/lam,bb/(2*vv)))
 joint=propose_etas(b,v,2.,lam,'joint');assert joint[0]==joint[1]
 assert math.isclose(joint[0],sum(b)/(2*sum(v)))
 # Update is exactly FW mixing on radius1/lambda, including decay.
 for x,u,d,e in zip(w,q,p,eta):
  gamma=e*lam
  torch.testing.assert_close(x-e*d,(1-gamma)*x+gamma*(-u/lam))


def test_layer_skips_only_nonpositive_blocks_but_joint_uses_total():
 assert propose_etas([2.,-1.],[1.,1.],1.,1.,'layer')==[1.,0.]
 assert propose_etas([2.,-1.],[1.,1.],1.,1.,'joint')==[.5,.5]
 assert propose_etas([-2.,1.],[1.,1.],1.,1.,'joint')==[0.,0.]


def test_native_shape_ray_cap_and_no_double_scaling():
 e=propose_etas([100.,100.],[1.,1.],.01,2.,'joint',shape=[1.,2.])
 assert e==[.25,.5] and max(x*2 for x in e)==1.
 assert propose_etas([1.,1.],[1.,1.],10.,2.,'joint',shape=[1.,2.])==[.06,.12]


def test_simultaneous_layer_backtracking_checks_cross_layer_curvature():
 # Coupled quadratic: individual diagonal curvature alone is insufficient.
 A=torch.tensor([[3.,2.],[2.,4.]],dtype=torch.float64);x=torch.tensor([1.,2.],dtype=torch.float64)
 g=A@x;p=torch.tensor([1.,2.],dtype=torch.float64);b=(g*p).tolist();v=p.square().tolist();f0=float(.5*x@A@x)
 original=x.clone()
 def evaluate(etas):
  z=x-torch.tensor(etas)*p
  return float(.5*z@A@z)
 eta,L,trials,ok=block_backtrack(evaluate,f0=f0,b=b,v=v,L=.1,decay=.2,scope='layer',tolerance=0.)
 assert ok and len(trials)>1 and evaluate(eta)<f0 and torch.equal(x,original)
 assert trials[-1]['loss']<=trials[-1]['bound']


def test_no_extra_queries_when_no_descent():
 def never(etas):raise AssertionError('must skip without evaluating')
 e,L,trials,ok=block_backtrack(never,f0=1.,b=[-1.,0.],v=[1.,0.],L=1.,decay=.2,scope='layer')
 assert e==[0.,0.] and not ok and not trials
