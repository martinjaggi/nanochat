"""Show how LR, WD and contraction differ among the frozen causal controls."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from research.unnormalized_muon.early_allocation import rates,D
from research.unnormalized_muon.cooldown_schedule import history_matched_early_wd


def main():
    n=20000;x=np.arange(n);wd=.04593746995939655
    fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for label,k,lam,color,style in [
        ('baseline',1.,wd,'#2468a0','-'),
        ('early2x, fixed WD',2.,wd,'#d96925','-'),
        ('baseline, final-contraction match',1.,.05512713564910121,'#708238','--'),
        ('early2x, final-contraction match',2.,.03827980744972244,'#6b3e91','--'),
        ('early2x, entire-history match',2.,None,'#d13d62',':')]:
        eta=np.asarray(rates(k));w=np.asarray([history_matched_early_wd(wd,t) for t in x]) if lam is None else np.full(n,lam)
        gamma=eta*w;contract=np.exp(np.cumsum(np.log1p(-gamma)))
        for ax,y in zip(axs.flat,[eta,w,gamma,contract]):ax.plot(x,y,color=color,linestyle=style,label=label)
    for ax,title,ylabel in zip(axs.flat,['Directional LR','Ordinary unmasked WD','FW mixing / contraction per update','Cumulative weight retention'],['Actual eta','lambda_t','gamma_t = eta_t lambda_t','Product (1 - gamma_t)']):
        ax.set(xlabel='Update',ylabel=ylabel,title=title);ax.axvline(7000,color='gray',linestyle=':',alpha=.5);ax.grid(alpha=.2)
    axs[1,1].set_yscale('log');axs[0,1].legend(fontsize=8)
    fig.suptitle('Early LR allocation controls: equal final products need not match histories',fontsize=12)
    fig.savefig(D/'EARLY_ALLOCATION_CONTROLS.png',dpi=150);plt.close(fig)

if __name__=='__main__':main()
