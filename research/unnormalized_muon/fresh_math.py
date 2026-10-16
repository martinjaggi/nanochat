"""Pure decision rules for frozen-state diagnosis; no check-data selection."""
import math


def schedule(step,horizon=2000,warmup=40,final=.05):
    if step<warmup:return (step+1)/warmup
    warmdown=round(.65*horizon)
    return 1. if step<=horizon-warmdown else final+(1-final)*(horizon-step)/warmdown


def momentum(step,horizon=2000):
    start=horizon-round(.65*horizon)
    if step<400:return .85+.12*step/400
    return .97 if step<start else .97-.07*(step-start)/round(.65*horizon)


def select_grid(losses,rates):
    assert len(losses)==len(rates) and all(math.isfinite(x) for x in losses)
    # Stable tie rule favors the smaller displacement; checking data is absent.
    return min(range(len(rates)),key=lambda i:(losses[i],rates[i]))


def paired_stats(values):
    assert len(values)>=2 and all(math.isfinite(x) for x in values)
    mean=sum(values)/len(values)
    variance=sum((x-mean)**2 for x in values)/(len(values)-1)
    return dict(mean=mean,se=math.sqrt(variance/len(values)),n=len(values))


def mixture_wd(step,eta,eta_peak,lam,horizon=2000):
    """WD-only hypothesis: shifted reciprocal FW mixing, changing domain.

    Retains the baseline gradient LR. gamma=2/(tau+t) after warmup,
    tau=2/(lambda*eta_peak); lambda_t=gamma/eta_t. This is NOT fixed-ball
    stochastic FW with its coupled gradient estimator.
    """
    assert eta>=0 and eta_peak>0 and lam>0
    if step<40:return lam
    gamma=2/(2/(lam*eta_peak)+step-40)
    return gamma/eta if eta>0 else 0.


def matched_static_wd(eta_peak,lam,horizon=2000):
    """Match final log contraction, explicitly not the entire decay history."""
    etas=[eta_peak*schedule(t,horizon) for t in range(horizon)]
    target=sum(math.log1p(-e*mixture_wd(t,e,eta_peak,lam,horizon)) for t,e in enumerate(etas))
    low,high=0.,.999/max(etas)
    for _ in range(80):
        middle=(low+high)/2
        value=sum(math.log1p(-e*middle) for e in etas)
        if value>target:low=middle
        else:high=middle
    return (low+high)/2
