import math
from research.unnormalized_muon.cooldown_schedule import reciprocal_cooldown
from research.unnormalized_muon.protocol_math import reciprocal_schedule


def test_reciprocal_cooldown_does_not_double_warmup():
    for t in [0,10,39,40,400,7000]:
        assert reciprocal_cooldown(.005,.18,t)==reciprocal_schedule(.005,.18,t)


def test_final_lr_is_controlled_separately_from_peak():
    eta=reciprocal_schedule(.005,.1837498798375862,20000)
    assert math.isclose(reciprocal_cooldown(.005,.1837498798375862,20000,final=.25),.25*eta)
    assert abs(.25*eta-.000125)<5e-6


def test_time_matched_cooldown_uses_common_clock():
    for p in [0.,.001,.002,.35,.75,1.]:
        assert reciprocal_cooldown(.005,.18,300,time_progress=p)==reciprocal_cooldown(.005,.18,900,time_progress=p)


def test_matrix_only_cooldown_matches_existing_default():
    from research.unnormalized_muon.cooldown_schedule import matrix_cooldown
    from research.unnormalized_muon.fresh_math import schedule
    for t in [0,10,39,40,400,7000,15000,19999,20000]:
        assert math.isclose(matrix_cooldown(.0025,t),.0025*schedule(t,20000),abs_tol=1e-15)


def test_matrix_terminal_control_time_clock_and_endpoint():
    from research.unnormalized_muon.cooldown_schedule import matrix_cooldown
    assert matrix_cooldown(.0025,20000,final=.01)==.000025
    for p in [0.,.001,.002,.35,.75,1.]:
        assert matrix_cooldown(.0025,300,final=.01,time_progress=p)==matrix_cooldown(.0025,900,final=.01,time_progress=p)


def test_cosine_wd_native_schedule_and_time_clock():
    from research.unnormalized_muon.cooldown_schedule import cosine_wd
    assert cosine_wd(.18,0)==.18
    assert math.isclose(cosine_wd(.18,10000),.09)
    assert cosine_wd(.18,20000)==0
    for p in [0.,.001,.35,.75,1.]:
        assert cosine_wd(.18,300,time_progress=p)==cosine_wd(.18,p*20000)


def test_early_reciprocal_exact_baseline_and_late_identity():
    from research.unnormalized_muon.cooldown_schedule import early_reciprocal,matrix_cooldown
    for t in range(20001):
        b=matrix_cooldown(.005,t,final=.01)
        assert early_reciprocal(.005,t)==b
        if t>=7000:
            for k in [1.5,2.]:assert early_reciprocal(.005,t,peak_multiplier=k)==b


def test_early_reciprocal_warmup_join_and_independent_tau():
    from research.unnormalized_muon.cooldown_schedule import early_reciprocal
    for k,tau in [(1.5,13920),(2.,6960)]:
        assert early_reciprocal(.005,39,peak_multiplier=k)==.005*k
        assert early_reciprocal(.005,40,peak_multiplier=k)==.005*k
        assert early_reciprocal(.005,7000,peak_multiplier=k)==.005
        for t in [41,100,1000,6999]:
            assert math.isclose(early_reciprocal(.005,t,peak_multiplier=k),.005*k/(1+(t-40)/tau))
        vals=[early_reciprocal(.005,t,peak_multiplier=k) for t in range(40,7001)]
        assert all(x>=y for x,y in zip(vals,vals[1:]))


def test_early_reciprocal_time_clock():
    from research.unnormalized_muon.cooldown_schedule import early_reciprocal
    for p in [0.,.001,.002,.1,.35,.75,1.]:
        assert early_reciprocal(.005,0,peak_multiplier=2,time_progress=p)==early_reciprocal(.005,900,peak_multiplier=2,time_progress=p)
        if p>=.002:
            assert math.isclose(early_reciprocal(.005,0,peak_multiplier=2,time_progress=p),early_reciprocal(.005,p*20000,peak_multiplier=2))
