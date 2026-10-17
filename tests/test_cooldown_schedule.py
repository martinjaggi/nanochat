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
