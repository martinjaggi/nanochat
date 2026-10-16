"""Explicit fixed-spectral-ball FW; separate from the production Muon change."""
import math,time,torch
from torch.func import functional_call
from nanochat.optim import polar_express_coeffs


def backtrack(evaluate, *, f0,b,v,L,max_trials=16,tolerance=1e-6):
    """Pure ray search. evaluate(gamma) must not mutate the live model/state."""
    assert L>0 and v>=0
    if b<=0 or v==0:return 0.,L,[],False
    trials=[]
    for _ in range(max_trials):
        gamma=min(1.,b/(L*v));loss=float(evaluate(gamma))
        bound=f0-gamma*b+.5*L*gamma*gamma*v
        accepted=math.isfinite(loss) and loss<=bound+tolerance*max(1.,abs(f0))
        trials.append(dict(gamma=gamma,L=L,loss=loss,bound=bound,accepted=accepted))
        if accepted:return gamma,L,trials,True
        L*=2
    return 0.,L,trials,False


def spectral_safe(direction):
    """Gershgorin upper certificate, not a power-iteration lower estimate."""
    q=direction.double()
    gram=q.mT@q if q.shape[-2]>=q.shape[-1] else q@q.mT
    upper=gram.abs().sum(-1).amax().sqrt()*(1+1e-6)
    return direction/upper.clamp_min(1.).to(direction.dtype)


@torch.no_grad()
def polar_direction(g):
    x=g.bfloat16()
    target=x.float().norm()/math.sqrt(x.shape[-2])
    row_norm=x.float().norm(dim=-1,keepdim=True).clamp_min(1e-6)
    x=x*(target/row_norm).to(x.dtype)
    x=x/(x.norm()*1.01+1e-6)
    for a,b,c in polar_express_coeffs:
        if x.shape[-2]>x.shape[-1]:
            a0=x.mT@x;z=b*a0+c*(a0@a0);x=a*x+x@z
        else:
            a0=x@x.mT;z=b*a0+c*(a0@a0);x=a*x+z@x
    x=x.float();x=x*(math.sqrt(min(x.shape))/x.norm().clamp_min(1e-6))
    return spectral_safe(x)


class FWMuon:
    """Native AdamW plus one shared FW step; auxiliary weights frozen in search."""
    def __init__(self,inner,model,recorder,initial_L=.01,radius_factor=2.):
        self.inner=inner;self.model=model;self.recorder=recorder
        self.param_groups=inner.param_groups;self.L=initial_L;self.batch=[];self.step_index=0
        names={id(p):n for n,p in model.named_parameters()}
        self.matrices=[(names[id(p)],p) for g in self.param_groups if g['kind']=='muon' for p in g['params']]
        self.m={n:torch.zeros_like(p) for n,p in self.matrices};self.radii={}
        for n,p in self.matrices:
            norm=float(torch.linalg.matrix_norm(p.detach().float(),ord=2))
            self.radii[n]=max(1.,radius_factor*norm)
        self.extra_forward_evals=0;self.line_seconds=0.;self.negative_steps=0
        self.recorder.emit('fw_geometry',radii=self.radii,initial_L=initial_L,
            certificate='FP64 Gram induced-infinity upper bound, safety1e-6',
            shape_scaling='none: fixed per-matrix radii define geometry',Muon_decay='none')
    def set_batch(self,x,y):self.batch.append((x.clone(),y.clone()))
    def set_loss(self,loss):self.loss_before=loss.detach()
    @torch.no_grad()
    def step(self):
        torch.cuda.synchronize();start=time.perf_counter();directions={}
        mu=next(g['momentum'] for g in self.param_groups if g['kind']=='muon')
        for n,p in self.matrices:
            self.m[n].lerp_(p.grad,1-mu)
            q=polar_direction(p.grad.lerp(self.m[n],mu))
            directions[n]=-self.radii[n]*q-p
        b=float(-sum((p.grad.double()*directions[n].double()).sum() for n,p in self.matrices))
        v=float(sum(d.double().square().sum() for d in directions.values()))
        before_rng=torch.cuda.get_rng_state();after_cpu=torch.get_rng_state()
        def evaluate(gamma):
            try:
                torch.cuda.set_rng_state(before_rng);torch.set_rng_state(after_cpu)
                candidate={n:p+gamma*directions[n] for n,p in self.matrices}
                count=sum(y.numel() for _,y in self.batch)
                loss=sum(functional_call(self.model,candidate,(x,y))*y.numel()/count for x,y in self.batch)
                self.extra_forward_evals+=1
                return float(loss)
            finally:
                torch.cuda.set_rng_state(before_rng);torch.set_rng_state(after_cpu)
        gamma,self.L,trials,accepted=backtrack(evaluate,f0=float(self.loss_before),b=b,v=v,L=self.L)
        if b<=0:self.negative_steps+=1
        if accepted:
            for n,p in self.matrices:p.add_(directions[n],alpha=gamma)
        # Apply only the original AdamW groups, after the line search.
        original=self.inner.param_groups
        try:
            self.inner.param_groups=[g for g in original if g['kind']=='adamw']
            self.inner.step()
        finally:self.inner.param_groups=original
        torch.cuda.synchronize();elapsed=time.perf_counter()-start;self.line_seconds+=elapsed
        self.recorder.emit('fw_update',step=self.step_index,gamma=gamma,L=self.L,b=b,v=v,
            accepted=accepted,trials=trials,extra_forward_evals=self.extra_forward_evals,
            total_fw_direction_and_search_seconds=self.line_seconds,negative_steps=self.negative_steps)
        self.step_index+=1;self.batch=[]
    def state_dict(self):
        return dict(inner=self.inner.state_dict(),fw=dict(m=self.m,radii=self.radii,L=self.L,
            steps=self.step_index,extra_forward_evals=self.extra_forward_evals,line_seconds=self.line_seconds))
    def feasibility(self):
        ratios={n:float(torch.linalg.matrix_norm(p.detach().float(),ord=2))/self.radii[n] for n,p in self.matrices}
        assert max(ratios.values())<=1+1e-5,'FW spectral ball violated'
        return ratios
