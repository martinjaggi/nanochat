"""Current-gradient complete-gap gate: CPU arithmetic then scheduled B300 compile."""
import pytest,torch
import nanochat.optim as opt


@pytest.fixture(autouse=True)
def isolate_compiler():
    torch._dynamo.reset()
    yield
    torch._dynamo.reset()


def case(monkeypatch,shape,reason,device,compiled):
    monkeypatch.setattr(opt,'CLEAN_MUON',True);monkeypatch.setattr(opt,'UNNORMALIZED_MUON',False)
    monkeypatch.setattr(opt,'RECORD_DUAL_SCALE',False);monkeypatch.setattr(opt,'MUON_DECAY_MODE','standard')
    monkeypatch.setattr(opt,'MUON_GEOMETRY','q_scaled')
    g=torch.ones((2,*shape),device=device);p0=torch.zeros_like(g);m0=torch.zeros_like(g)
    if reason=='decay':p0[1]=-100*g[1];wd=.2
    else:m0[1]=-100*g[1];wd=0.
    vshape=(2,shape[0],1) if shape[0]>=shape[1] else (2,1,shape[1])
    def call(gated):
        monkeypatch.setattr(opt,'CAP_SIGN',gated)
        p=p0.clone();m=m0.clone();v=torch.ones(vshape,device=device)*.123;gg=g.clone()
        fun=opt.muon_step_fused if compiled else opt.muon_step_fused.__wrapped__
        mask=fun(gg,p,m,v,torch.tensor(.85),torch.tensor(.01),torch.tensor(wd),torch.tensor(.9),5,-1 if shape[0]>=shape[1] else -2)
        return p,m,v,gg,mask
    a=call(False);b=call(True)
    assert b[4].flatten().tolist()==[True,False]
    torch.testing.assert_close(a[0][0],b[0][0],rtol=1e-5,atol=2e-6)
    assert torch.equal(b[0][1],p0[1]),'non-descent block must skip direction AND decay'
    assert torch.equal(a[1],b[1]),'momentum must advance once even when the weight step skips'
    assert torch.equal(a[2],b[2]) and torch.equal(a[3],b[3])


@pytest.mark.parametrize('shape',[(4,3),(3,4)])
@pytest.mark.parametrize('reason',['decay','stale_momentum'])
def test_cap_sign_cpu(monkeypatch,shape,reason):case(monkeypatch,shape,reason,'cpu',False)


@pytest.mark.skipif(not torch.cuda.is_available(),reason='one scheduled B300 required')
@pytest.mark.parametrize('shape',[(64,128),(128,64)])
@pytest.mark.parametrize('reason',['decay','stale_momentum'])
def test_cap_sign_b300(monkeypatch,shape,reason):
    assert torch.cuda.device_count()==1 and 'B300' in torch.cuda.get_device_name(0)
    case(monkeypatch,shape,reason,'cuda',True)
