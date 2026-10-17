import math
from research.unnormalized_muon.fresh_math import schedule,momentum,select_grid,paired_stats,mixture_wd


def test_original_horizon_not_continuation_length():
    assert schedule(400)==1 and schedule(1500)<1
    assert schedule(1500)!=schedule(1500,20000)
    assert momentum(400)==.97


def test_selection_cannot_use_check_data():
    assert select_grid([2.,1.,1.],[0.,.5,1.])==1
    x=paired_stats([-2.,-1.,0.]);assert x['mean']==-1 and math.isclose(x['se'],1/math.sqrt(3))


def test_wd_mixing_mapping_and_cooldown():
    lam=.18;peak=.01
    for t in [40,400,1500,1999]:
        eta=peak*schedule(t)
        wd=mixture_wd(t,eta,peak,lam)
        assert math.isclose(eta*wd,2/(2/(lam*peak)+t-40))
        assert 0<=eta*wd<=1
    assert mixture_wd(20,.005,peak,lam)==lam


def test_static_control_matches_only_final_contraction():
    from research.unnormalized_muon.fresh_math import matched_static_wd
    peak=.01;lam=.1837498798375862;fixed=matched_static_wd(peak,lam)
    a=sum(math.log1p(-peak*schedule(t)*fixed) for t in range(2000))
    b=sum(math.log1p(-peak*schedule(t)*mixture_wd(t,peak*schedule(t),peak,lam)) for t in range(2000))
    assert abs(a-b)<1e-10 and fixed!=lam


def test_wd_mixing_equal_time_clock_and_contraction():
    from research.unnormalized_muon.protocol_math import budget_multiplier
    peak=.00125;lam=.1837498798375862
    for progress in [.002,.25,.5,.75,1.]:
        clock=progress*20000;eta=peak*budget_multiplier(progress)
        wd=mixture_wd(clock,eta,peak,lam,20000)
        assert math.isclose(eta*wd,2/(2/(lam*peak)+clock-40))
    terminal=mixture_wd(20000,peak*.05,peak,lam,20000)
    assert terminal>lam
