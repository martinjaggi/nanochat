import os,importlib.util
import pytest,torch
import nanochat.optim as modified
pytestmark=pytest.mark.skipif(not torch.cuda.is_available(),reason='scheduled B300 only')

@pytest.mark.parametrize('shape',[(2,64,128),(2,128,64)])
def test_compiled_update_and_default_regression(monkeypatch,shape):
    assert torch.cuda.device_count()==1 and 'B300' in torch.cuda.get_device_name(0)
    spec=importlib.util.spec_from_file_location('upstream_optim_gpu',os.environ['UNNORMALIZED_BASE_OPTIM'])
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    torch.manual_seed(42);dev='cuda'
    grad=torch.randn(shape,device=dev)*.1
    p=torch.zeros(shape,device=dev);m=torch.randn_like(p)*.01
    v=torch.ones((shape[0],shape[-2],1) if shape[-2]>=shape[-1] else (shape[0],1,shape[-1]),device=dev)*.1
    def args():return [grad.clone(),p.clone(),m.clone(),v.clone(),torch.tensor(.85),torch.tensor(.01),torch.tensor(0.),torch.tensor(.9),5,-1 if shape[-2]>=shape[-1] else -2]
    a=args();b=args();monkeypatch.setattr(modified,'UNNORMALIZED_MUON',False)
    base.muon_step_fused(*a);modified.muon_step_fused(*b)
    for i in [0,1,2,3]:torch.testing.assert_close(a[i],b[i],rtol=0,atol=0)
    c=args();monkeypatch.setattr(modified,'UNNORMALIZED_MUON',True)
    scale,alignment=modified.muon_step_fused(*c)
    assert bool(torch.isfinite(alignment).all())
    assert scale.shape==(shape[0],1,1) and scale.dtype==torch.float32
    assert bool(((scale>=0)&torch.isfinite(scale)).all())
    # Additional reduction may change compiler fusion; compare against unchanged direction.
    torch.testing.assert_close(c[1],a[1]*scale,rtol=.01,atol=2e-5)
    torch.testing.assert_close(c[2],a[2],rtol=0,atol=0)
    torch.testing.assert_close(c[3],a[3],rtol=0,atol=0)

def test_clean_compiled_normalized_and_unnormalized(monkeypatch):
 monkeypatch.setattr(modified,'MUON_DECAY_MODE','none');monkeypatch.setattr(modified,'CLEAN_MUON',True);monkeypatch.setattr(modified,'RECORD_DUAL_SCALE',True)
 torch.manual_seed(23);g=torch.randn(2,64,128,device='cuda')*.01
 def call(scaled):
  monkeypatch.setattr(modified,'UNNORMALIZED_MUON',scaled)
  p=torch.zeros_like(g);m=torch.zeros_like(g);v=torch.ones(2,1,128,device='cuda')*.123
  s=modified.muon_step_fused(g.clone(),p,m,v,torch.tensor(.85),torch.tensor(.01),torch.tensor(100.),torch.tensor(.9),5,-2)
  return p,m,v,s
 a=call(False);b=call(True)
 torch.testing.assert_close(b[0],a[0]*b[3][0],rtol=.01,atol=1e-5)
 assert torch.equal(a[1],b[1]) and torch.equal(a[2],b[2])
 assert torch.equal(a[2],torch.ones_like(a[2])*.123)

@pytest.mark.parametrize('scaled',[False,True])
@pytest.mark.parametrize('mode',['standard','cautious'])
def test_compiled_clean_decay_rules(monkeypatch,scaled,mode):
 monkeypatch.setattr(modified,'CLEAN_MUON',True);monkeypatch.setattr(modified,'UNNORMALIZED_MUON',scaled)
 monkeypatch.setattr(modified,'RECORD_DUAL_SCALE',False)
 torch.manual_seed(8);g=torch.randn(2,64,128,device='cuda')*.01;p0=torch.randn_like(g)*.1
 def call(rule):
  monkeypatch.setattr(modified,'MUON_DECAY_MODE',rule)
  p=p0.clone();m=torch.zeros_like(g);v=torch.ones(2,1,128,device='cuda')*.123
  modified.muon_step_fused(g.clone(),p,m,v,torch.tensor(.85),torch.tensor(.01),torch.tensor(.3),torch.tensor(.9),5,-2)
  assert torch.equal(v,torch.ones_like(v)*.123)
  return p
 p=call('none');actual=call(mode);direction=(p0-p)/.01
 mask=(direction*p0>=0) if mode=='cautious' else 1
 torch.testing.assert_close(actual,p-.003*p0*mask,rtol=.01,atol=2e-6)
