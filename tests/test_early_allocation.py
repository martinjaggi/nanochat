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
