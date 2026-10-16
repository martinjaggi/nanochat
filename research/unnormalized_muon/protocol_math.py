"""Pure arithmetic for contraction, timing and FW-lens schedules."""
import math


def contraction(previous,gamma):
    """Signed log product; gamma=1 represented without non-JSON infinities."""
    assert math.isfinite(gamma)
    state=dict(previous) if previous else dict(sign=1,log_abs=0.)
    factor=1-gamma
    if factor==0 or state['sign']==0:return dict(sign=0,log_abs=None,value=0.)
    state['sign']*=1 if factor>0 else -1
    state['log_abs']+=math.log1p(-gamma) if factor>0 else math.log(abs(factor))
    state['value']=state['sign']*math.exp(state['log_abs'])
    return state


def overlap_seconds(intervals,start,end):
    segments=sorted((max(a,start),min(b,end)) for a,b in intervals if b>start and a<end)
    total=0.;last=start
    for a,b in segments:
        total+=max(0.,b-max(a,last));last=max(last,b)
    return min(end-start,total)


def budget_multiplier(progress,warmup_fraction=.002,warmdown_fraction=.65,final=.05,reference_updates=20000):
    r=min(1.,max(0.,progress));effective=max(r,1/reference_updates)
    if r<warmup_fraction:return min(1.,effective/warmup_fraction)
    if r<=1-warmdown_fraction:return 1.
    return final+(1-final)*(1-r)/warmdown_fraction
