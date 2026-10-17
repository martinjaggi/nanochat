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
