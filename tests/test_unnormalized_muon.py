"""Analytic scale identities and exact regression against the base optimizer."""
import importlib.util, os
import pytest
import torch
import nanochat.optim as modified

@pytest.mark.parametrize('shape',[(4,3),(3,4),(4,4)])
def test_polar_inner_product_is_nuclear_norm(shape):
    torch.manual_seed(12)
    g=torch.randn(2,*shape)
    u,s,vh=torch.linalg.svd(g,full_matrices=False)
    scale=modified.nonnegative_dual_scale(g,u@vh).flatten()
    torch.testing.assert_close(scale,s.sum(-1),rtol=1e-5,atol=1e-6)

def test_negative_zero_and_independent_matrix_scales():
    g=torch.stack([torch.ones(3,4),3*torch.ones(3,4),torch.zeros(3,4)])
    u=torch.ones_like(g)
    assert modified.nonnegative_dual_scale(g,u).flatten().tolist()==[12,36,0]
    assert not modified.nonnegative_dual_scale(g,-u).any()

@pytest.mark.parametrize('shape',[(2,4,3),(2,3,4)])
def test_fused_step_and_disabled_upstream_parity(monkeypatch,shape):
    path=os.environ['UNNORMALIZED_BASE_OPTIM']
    spec=importlib.util.spec_from_file_location('upstream_optim',path); base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    # Eager CPU math check; real compiled/BF16 integration is separately scheduled on B300.
    torch.manual_seed(42)
    grad=torch.randn(shape); p=torch.zeros(shape); m=torch.randn(shape)*.1
    vshape=(*shape[:-1],1) if shape[-2]>=shape[-1] else (shape[0],1,shape[-1])
    v=torch.ones(vshape)*.1
    def args():return [grad.clone(),p.clone(),m.clone(),v.clone(),torch.tensor(.85),torch.tensor(.01),torch.tensor(0.),torch.tensor(.95),5,-1 if shape[-2]>=shape[-1] else -2]
    a=args(); b=args(); monkeypatch.setattr(modified,'UNNORMALIZED_MUON',False)
    base.muon_step_fused.__wrapped__(*a);modified.muon_step_fused.__wrapped__(*b)
    for i in [0,1,2,3]:assert torch.equal(a[i],b[i])
    c=args();monkeypatch.setattr(modified,'UNNORMALIZED_MUON',True)
    captured=[];original=modified.nonnegative_dual_scale
    def capture(g,u):
        expected=grad.lerp(m.lerp(grad,.15),.85)
        torch.testing.assert_close(g,expected)
        captured.append(original(g,u));
        capture.expected_alignment=(grad*u).sum(dim=(-2,-1),keepdim=True)
        return captured[-1]
    monkeypatch.setattr(modified,'nonnegative_dual_scale',capture)
    scale,alignment=modified.muon_step_fused.__wrapped__(*c)
    torch.testing.assert_close(alignment,capture.expected_alignment)
    torch.testing.assert_close(c[1],a[1]*scale)
    assert torch.equal(c[2],a[2]) and torch.equal(c[3],a[3])
    assert bool(torch.isfinite(scale).all() & (scale>=0).all())
