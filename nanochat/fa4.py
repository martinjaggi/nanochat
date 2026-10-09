"""Compile-safe FA4 bridge, tested with flash-attn-4==4.0.0b32.

CuTe's Python JIT stays outside Dynamo/AOTAutograd. Custom operators declare
shapes and register first-order autograd; the backward runs FA4's actual kernel,
not a recomputed SDPA fallback. This small bridge uses FA4's private fwd/bwd API,
so package upgrades must rerun the CUDA output/gradient/compile tests.
"""
from typing import Optional
import torch
from flash_attn.cute.interface import _flash_attn_fwd, _flash_attn_bwd


@torch.library.custom_op('nanochat::fa4_forward', mutates_args=())
def _forward(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor,
             causal: bool, left: int, right: int,
             scale: Optional[float]) -> tuple[torch.Tensor, torch.Tensor]:
    out, lse, _, _ = _flash_attn_fwd(q, k, v, causal=causal,
            window_size_left=None if left < 0 else left,
            window_size_right=None if right < 0 else right,
            softmax_scale=scale, return_lse=True)
    return out, lse


@_forward.register_fake
def _forward_fake(q, k, v, causal, left, right, scale):
    out = q.new_empty((*q.shape[:-1], v.shape[-1]))
    lse = torch.empty((q.shape[0], q.shape[2], q.shape[1]), dtype=torch.float32, device=q.device)
    return out, lse


@torch.library.custom_op('nanochat::fa4_backward', mutates_args=())
def _backward(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor,
              out: torch.Tensor, grad: torch.Tensor, lse: torch.Tensor,
              causal: bool, left: int, right: int,
              scale: Optional[float]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    dq, dk, dv = _flash_attn_bwd(q, k, v, out, grad.contiguous(), lse,
            softmax_scale=scale, causal=causal,
            window_size_left=None if left < 0 else left,
            window_size_right=None if right < 0 else right)
    return dq.contiguous(), dk.contiguous(), dv.contiguous()


@_backward.register_fake
def _backward_fake(q, k, v, out, grad, lse, causal, left, right, scale):
    return tuple(x.new_empty(x.shape) for x in (q, k, v))


def _setup_context(ctx, inputs, output):
    q, k, v, causal, left, right, scale = inputs
    out, lse = output
    ctx.save_for_backward(q, k, v, out, lse)
    ctx.options = causal, left, right, scale
    ctx.mark_non_differentiable(lse)


def _autograd_backward(ctx, grad, grad_lse):
    q, k, v, out, lse = ctx.saved_tensors
    dq, dk, dv = _backward(q, k, v, out, grad, lse, *ctx.options)
    return dq, dk, dv, None, None, None, None


_forward.register_autograd(_autograd_backward, setup_context=_setup_context)


def flash_attn_func(q, k, v, causal=False, window_size=(-1, -1), softmax_scale=None):
    left, right = (-1 if x is None else x for x in window_size)
    return _forward(q, k, v, causal, left, right, softmax_scale)[0]
