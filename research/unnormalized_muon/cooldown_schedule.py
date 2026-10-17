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


def cosine_wd(reference,step,*,horizon=20000,time_progress=None):
    import math
    assert reference>=0 and horizon>0
    r=min(1.,max(0.,time_progress if time_progress is not None else step/horizon))
    return reference*.5*(1+math.cos(math.pi*r))


def early_reciprocal(eta_join,step,*,peak_multiplier=1.,horizon=20000,warmup=40,final=.01,time_progress=None):
    """WD-independent reciprocal early allocation; baseline late phase is exact.

    Warmup ends at index warmup-1. The plateau begins at warmup and
    joins at horizon-round(.65*horizon), inclusive. tau=T/(peak-1).
    """
    assert peak_multiplier>=1 and 0<=warmup<horizon-round(.65*horizon)
    baseline=matrix_cooldown(eta_join,step,horizon=horizon,warmup=warmup,final=final,time_progress=time_progress)
    clock=min(1.,max(0.,time_progress))*horizon if time_progress is not None else step
    join=horizon-round(.65*horizon)
    if peak_multiplier==1 or clock>=join:return baseline
    if clock<warmup:return baseline*peak_multiplier
    length=join-warmup
    return eta_join*peak_multiplier/(1+(clock-warmup)*(peak_multiplier-1)/length)


def history_matched_early_wd(reference,step,*,peak_multiplier=2.,horizon=20000,warmup=40,final=.01,time_progress=None):
    """Diagnostic: retain baseline gamma_t while reallocating directional LR.

    This changes lambda_t/the implied domain and is not a fixed-WD FW arm.
    Only the early phase changes: lambda_t=reference*eta_base/eta_early.
    """
    assert reference>=0
    kw=dict(horizon=horizon,warmup=warmup,final=final,time_progress=time_progress)
    baseline=matrix_cooldown(1.,step,**kw)
    early=early_reciprocal(1.,step,peak_multiplier=peak_multiplier,**kw)
    return reference*baseline/early
