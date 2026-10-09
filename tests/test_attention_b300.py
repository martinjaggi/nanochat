"""FA4 forward/backward parity including the local windows used in nanochat."""
import pytest
import torch
import nanochat.flash_attention as attention

@pytest.mark.skipif(not attention.HAS_FA4,reason='FA4 on a scheduled Blackwell GPU required')
@pytest.mark.parametrize('window',[(-1,-1),(32,0),(64,0)])
@pytest.mark.parametrize('kv_heads',[4,2])
@pytest.mark.parametrize('compiled',[False,True])
def test_fa4_matches_sdpa_output_and_gradients(window,kv_heads,compiled):
    torch.manual_seed(42)
    tensors=[torch.randn(2,128,h,128,device='cuda',dtype=torch.bfloat16,requires_grad=True) for h in (4,kv_heads,kv_heads)]
    copies=[t.detach().clone().requires_grad_(True) for t in tensors]
    upstream=attention._override_impl;use_fa4=attention.USE_FA4;use_fa3=attention.USE_FA3
    try:
        attention._override_impl='fa4';attention.USE_FA4=True;attention.USE_FA3=False
        operation=torch.compile(attention.flash_attn_func,fullgraph=True,dynamic=False) if compiled else attention.flash_attn_func
        actual=operation(*tensors,causal=True,window_size=window)
        attention._override_impl='sdpa';attention.USE_FA4=False
        expected=attention.flash_attn_func(*copies,causal=True,window_size=window)
        upstream_gradient=torch.randn_like(actual)
        actual.backward(upstream_gradient);expected.backward(upstream_gradient)
        torch.testing.assert_close(actual,expected,atol=.02,rtol=.02)
        for a,b in zip(tensors,copies):torch.testing.assert_close(a.grad,b.grad,atol=.04,rtol=.04)
    finally:
        attention._override_impl=upstream;attention.USE_FA4=use_fa4;attention.USE_FA3=use_fa3
