"""Cheap FW-inspired reciprocal shape plus a separate stochastic cooldown."""
from research.unnormalized_muon.protocol_math import reciprocal_schedule


def reciprocal_cooldown(eta0,decay,step,*,horizon=20000,warmup=40,final=.25,warmdown_fraction=.65,time_progress=None):
    assert 0<final<=1 and 0<warmdown_fraction<=1 and horizon>0
    clock=min(1.,max(0.,time_progress))*horizon if time_progress is not None else step
    eta=reciprocal_schedule(eta0,decay,step,warmup,time_progress=time_progress,reference_updates=horizon)
    warmdown=round(warmdown_fraction*horizon);start=horizon-warmdown
    multiplier=1. if clock<=start else max(final,final+(1-final)*(horizon-clock)/warmdown)
    return eta*multiplier


def matrix_cooldown(eta0,step,*,horizon=20000,warmup=40,final=.05,time_progress=None):
    from research.unnormalized_muon.protocol_math import budget_multiplier
    if time_progress is not None:
        return eta0*budget_multiplier(time_progress,warmup_fraction=warmup/horizon,final=final,reference_updates=horizon)
    if step<warmup:return eta0*(step+1)/warmup
    end=round(.65*horizon);start=horizon-end
    return eta0*(1. if step<=start else final+(1-final)*(horizon-step)/end)
