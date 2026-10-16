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
