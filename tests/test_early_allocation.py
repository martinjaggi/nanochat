import math
from research.unnormalized_muon.early_allocation import rates,matching_wd,log_contraction


def test_exact_static_contraction_control_and_wd_independence():
    wd=.04593746995939655
    baseline=rates(1.)
    for k in [1.5,2.]:
        target=log_contraction(rates(k),wd)
        matched=matching_wd(target,baseline)
        assert matched>wd
        assert math.isclose(log_contraction(baseline,matched),target,abs_tol=1e-12)
        assert all(a==b for a,b in zip(rates(k)[7000:],baseline[7000:]))


def test_contraction_control_identity():
    eta=rates(1.)
    assert math.isclose(matching_wd(log_contraction(eta,.04593746995939655),eta),.04593746995939655,rel_tol=1e-14)


def test_full_contraction_history_is_preserved():
    from research.unnormalized_muon.cooldown_schedule import history_matched_early_wd,matrix_cooldown,early_reciprocal
    wd=.04593746995939655
    for k in [1.,1.5,2.]:
        for t in range(20001):
            lam=history_matched_early_wd(wd,t,peak_multiplier=k)
            eta=early_reciprocal(.005,t,peak_multiplier=k)
            assert math.isclose(lam*eta,wd*matrix_cooldown(.005,t,final=.01),rel_tol=1e-14)
            if t>=7000:assert lam==wd


def test_history_match_time_clock():
    from research.unnormalized_muon.cooldown_schedule import history_matched_early_wd,matrix_cooldown,early_reciprocal
    for p in [0.,.001,.002,.1,.35,.75,1.]:
        lam=history_matched_early_wd(.04,600,time_progress=p)
        assert math.isclose(lam*early_reciprocal(.005,600,peak_multiplier=2.,time_progress=p),.04*matrix_cooldown(.005,600,final=.01,time_progress=p),rel_tol=1e-14)


def test_short_check_has_a_valid_early_phase():
    import pytest
    from research.unnormalized_muon.cooldown_schedule import early_reciprocal,history_matched_early_wd,matrix_cooldown
    with pytest.raises(AssertionError):early_reciprocal(.005,0,horizon=64,peak_multiplier=2.)
    for t in range(129):
        eta=early_reciprocal(.005,t,horizon=128,peak_multiplier=2.)
        wd=history_matched_early_wd(.04,t,horizon=128,peak_multiplier=2.)
        assert math.isclose(eta*wd,.04*matrix_cooldown(.005,t,horizon=128,final=.01),rel_tol=1e-14)
