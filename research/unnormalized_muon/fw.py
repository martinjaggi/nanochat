"""Explicit fixed-spectral-ball FW; separate from the production Muon change."""
import math,time,torch,os
from torch.func import functional_call
from nanochat.optim import polar_express_coeffs, CLEAN_MUON


def weighted_mean(losses,counts):
    """Same token weights for fresh accumulated loss and every candidate loss."""
    assert len(losses)==len(counts) and len(losses)>0 and sum(counts)>0
    return sum(loss*n for loss,n in zip(losses,counts))/sum(counts)


def backtrack(evaluate, *, f0,b,v,L,max_trials=16,tolerance=1e-6,acceptance="smoothness",armijo_c=.01):
    """Pure ray search. evaluate(gamma) must not mutate the live model/state."""
    assert acceptance in {"smoothness","armijo"} and 0<armijo_c<1
    assert math.isfinite(L) and L>0 and math.isfinite(v) and v>=0 and math.isfinite(b) and math.isfinite(f0)
    if b<=0 or v==0:return 0.,L,[],False
    trials=[]
    for _ in range(max_trials):
        gamma=min(1.,b/(L*v));loss=float(evaluate(gamma))
        bound=f0-gamma*b+.5*L*gamma*gamma*v if acceptance=="smoothness" else f0-armijo_c*gamma*b
        accepted=math.isfinite(loss) and loss<=bound+tolerance*max(1.,abs(f0)) and (acceptance!="armijo" or loss<=f0)
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
    if not CLEAN_MUON:
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
    def __init__(self,inner,model,recorder,initial_L=.01,radius_factor=2.,oracle="momentum"):
        assert oracle in {"momentum","gradient"} and radius_factor>=1
        self.oracle=oracle;self.radius_factor=radius_factor;self.history=[]
        self.acceptance=os.environ.get("RESEARCH_FW_ACCEPTANCE","smoothness")
        self.armijo_c=float(os.environ.get("RESEARCH_FW_ARMIJO_C",".01"))
        self.compiled_candidates=os.environ.get("RESEARCH_FW_COMPILE_CANDIDATES")=="1"
        def candidate_forward(candidate,x,y):return functional_call(self.model,candidate,(x,y))
        self.candidate_forward=torch.compile(candidate_forward,dynamic=False,fullgraph=True) if self.compiled_candidates else candidate_forward
        self.derivative_probes=os.environ.get("RESEARCH_FW_DERIVATIVE_PROBES")=="1"
        self.diagnostic_gradient_evals=0;self.diagnostic_seconds=0.
        self.component_seconds=dict(direction=0.,reference=0.,candidates=0.,auxiliary=0.)
        self.inner=inner;self.model=model;self.recorder=recorder
        self.param_groups=inner.param_groups;self.L=initial_L;self.batch=[];self.losses=[];self.loss_counts=[];self.step_index=0
        names={id(p):n for n,p in model.named_parameters()}
        self.matrices=[(names[id(p)],p) for g in self.param_groups if g['kind']=='muon' for p in g['params']]
        self.m={n:torch.zeros_like(p) for n,p in self.matrices};self.radii={}
        for n,p in self.matrices:
            norm=float(torch.linalg.matrix_norm(p.detach().float(),ord=2))
            self.radii[n]=max(1.,radius_factor*norm)
        self.extra_forward_evals=0;self.extra_microbatch_forward_evals=0;self.line_seconds=0.;self.negative_steps=0
        self.recorder.emit('fw_geometry',radii=self.radii,initial_L=initial_L,oracle=oracle,radius_factor=radius_factor,acceptance=self.acceptance,armijo_c=self.armijo_c,compiled_candidates=self.compiled_candidates,
            gap_definition='b=-<fresh_gradient,D>; directional gap with approximate oracle, not an exact LMO certificate',
            certificate='FP64 Gram induced-infinity upper bound, safety1e-6',
            shape_scaling='none: fixed per-matrix radii define geometry',Muon_decay='none')
    def set_batch(self,x,y):self.batch.append((x.clone(),y.clone()))
    def set_loss(self,loss):
        self.losses.append(loss.detach().clone())
        self.loss_counts.append(self.batch[-1][1].numel())
    @property
    def loss_before(self):
        return weighted_mean(self.losses,self.loss_counts)
    @torch.no_grad()
    def step(self):
        torch.cuda.synchronize();start=time.perf_counter();directions={}
        mu=next(g['momentum'] for g in self.param_groups if g['kind']=='muon')
        for n,p in self.matrices:
            self.m[n].lerp_(p.grad,1-mu)
            q=polar_direction(p.grad if self.oracle=="gradient" else p.grad.lerp(self.m[n],mu))
            directions[n]=-self.radii[n]*q-p
        b=float(-sum((p.grad.double()*directions[n].double()).sum() for n,p in self.matrices))
        v=float(sum(d.double().square().sum() for d in directions.values()))
        torch.cuda.synchronize();direction_seconds=time.perf_counter()-start
        # First-step audit: line search must preserve all live parameters, raw
        # gradients, buffers and both RNG states until an accepted update.
        audit=None
        if self.step_index==0:
            audit=[(p,p.detach().clone(),None if p.grad is None else p.grad.clone()) for p in self.model.parameters()]
            saved_buffers=[(p,p.clone()) for p in self.model.buffers()]
        per_matrix=None
        if self.step_index%25==0:
            per_matrix={n:dict(directional_gap=float(-(p.grad.double()*directions[n].double()).sum()),
                displacement_norm_squared=float(directions[n].double().square().sum()),
                gradient_norm=float(p.grad.float().norm()),weight_norm=float(p.float().norm())) for n,p in self.matrices}
        before_rng=torch.cuda.get_rng_state();after_cpu=torch.get_rng_state()
        def evaluate(gamma):
            try:
                torch.cuda.set_rng_state(before_rng);torch.set_rng_state(after_cpu)
                candidate={n:p+gamma*directions[n] for n,p in self.matrices}
                count=sum(y.numel() for _,y in self.batch)
                loss=weighted_mean([self.candidate_forward(candidate,x,y) for x,y in self.batch],
                    [y.numel() for _,y in self.batch])
                self.extra_forward_evals+=1
                self.extra_microbatch_forward_evals+=len(self.batch)
                return float(loss)
            finally:
                torch.cuda.set_rng_state(before_rng);torch.set_rng_state(after_cpu)
        # Match reference and candidate execution paths; compiled/eager BF16 loss
        # differences must not masquerade as curvature at a vanishing step.
        torch.cuda.synchronize();reference_start=time.perf_counter()
        reference=evaluate(0.) if b>0 and v>0 else float(self.loss_before)
        torch.cuda.synchronize();reference_seconds=time.perf_counter()-reference_start
        fresh_reference_delta=reference-float(self.loss_before)
        if self.derivative_probes and self.step_index in [0,16,32]:
            torch.cuda.synchronize();probe_start=time.perf_counter()
            # Explicit extra gradient query, never writes live .grad buffers.
            with torch.enable_grad():
                probe_loss=weighted_mean([self.model(x,y) for x,y in self.batch],[y.numel() for _,y in self.batch])
                gs=torch.autograd.grad(probe_loss,[p for _,p in self.matrices],allow_unused=True)
            self.diagnostic_gradient_evals+=1
            eager_gap=float(-sum((g.double()*directions[n].double()).sum() for (n,p),g in zip(self.matrices,gs) if g is not None))
            error=sum((g.double()-p.grad.double()).square().sum() for (n,p),g in zip(self.matrices,gs) if g is not None)
            norm=sum(p.grad.double().square().sum() for _,p in self.matrices)
            samples=[]
            for probe_gamma in [1e-6,1e-5,1e-4,1e-3,1e-2]:
                plus=evaluate(probe_gamma);minus=evaluate(-probe_gamma)
                samples.append(dict(gamma=probe_gamma,plus_loss=plus,minus_loss=minus,central_gap=(minus-plus)/(2*probe_gamma)))
            torch.cuda.set_rng_state(before_rng);torch.set_rng_state(after_cpu)
            torch.cuda.synchronize();self.diagnostic_seconds+=time.perf_counter()-probe_start
            self.recorder.emit('fw_derivative_probe',step=self.step_index,fresh_gap=b,eager_gap=eager_gap,
                relative_gradient_error=float((error/norm.clamp_min(1e-30)).sqrt()),samples=samples,
                diagnostic_gradient_evals=self.diagnostic_gradient_evals,diagnostic_seconds=self.diagnostic_seconds)
        candidate_start=time.perf_counter()
        gamma,self.L,trials,accepted=backtrack(evaluate,f0=reference,b=b,v=v,L=max(self.L*.5,1e-16),acceptance=self.acceptance,armijo_c=self.armijo_c)
        torch.cuda.synchronize();candidate_seconds=time.perf_counter()-candidate_start
        if audit is not None:
            assert all(torch.equal(p,old) and (grad is None or torch.equal(p.grad,grad)) for p,old,grad in audit), 'FW search mutated live state'
            assert all(torch.equal(p,old) for p,old in saved_buffers), 'FW search mutated buffers'
            assert torch.equal(torch.cuda.get_rng_state(),before_rng) and torch.equal(torch.get_rng_state(),after_cpu), 'FW search changed RNG'
            self.recorder.emit('fw_search_audit',parameters_gradients_buffers_rng_unchanged=True)
        if b<=0:self.negative_steps+=1
        if accepted:
            for n,p in self.matrices:p.add_(directions[n],alpha=gamma)
        # Apply only the original AdamW groups, after the line search.
        torch.cuda.synchronize();aux_start=time.perf_counter()
        original=self.inner.param_groups
        try:
            self.inner.param_groups=[g for g in original if g['kind']=='adamw']
            self.inner.step()
        finally:self.inner.param_groups=original
        torch.cuda.synchronize();aux_seconds=time.perf_counter()-aux_start
        elapsed=time.perf_counter()-start;self.line_seconds+=elapsed
        components=dict(direction=direction_seconds,reference=reference_seconds,candidates=candidate_seconds,auxiliary=aux_seconds)
        for k,value in components.items():self.component_seconds[k]+=value
        actual_decrease=reference-trials[-1]['loss'] if accepted else 0.
        predicted_decrease=gamma*b-.5*self.L*gamma*gamma*v
        stats=dict(gamma=gamma,L=self.L,b=b,v=v,accepted=accepted,trials=len(trials),actual_decrease=actual_decrease,predicted_decrease=predicted_decrease)
        self.history.append(stats)
        self.recorder.emit('fw_update',step=self.step_index,gamma=gamma,L=self.L,b=b,v=v,
            accepted=accepted,trials=trials,per_matrix=per_matrix,component_seconds=components,actual_decrease=actual_decrease,predicted_decrease=predicted_decrease,accumulation_microbatches=len(self.batch),accumulated_fresh_loss=float(self.loss_before),reference_loss=reference,extra_microbatch_forward_evals=self.extra_microbatch_forward_evals,fresh_vs_functional_reference_delta=fresh_reference_delta,extra_forward_evals=self.extra_forward_evals,
            total_fw_direction_and_search_seconds=self.line_seconds,negative_steps=self.negative_steps)
        self.step_index+=1;self.batch=[];self.losses=[];self.loss_counts=[]
    def diagnostics(self):
        def quantiles(key):
            x=torch.tensor([h[key] for h in self.history],dtype=torch.float64)
            return dict(zip(['min','p25','median','p75','max'],x.quantile(torch.tensor([0.,.25,.5,.75,1.],dtype=torch.float64)).tolist()))
        return dict(oracle=self.oracle,radius_factor=self.radius_factor,acceptance=self.acceptance,armijo_c=self.armijo_c,compiled_candidates=self.compiled_candidates,steps=len(self.history),
            accepted_steps=sum(h['accepted'] for h in self.history),negative_alignment_steps=self.negative_steps,
            component_seconds=self.component_seconds,diagnostic_gradient_evals=self.diagnostic_gradient_evals,diagnostic_seconds=self.diagnostic_seconds,statistics={k:quantiles(k) for k in ['gamma','L','b','v','trials','actual_decrease','predicted_decrease']})
    def state_dict(self):
        return dict(inner=self.inner.state_dict(),fw=dict(m=self.m,radii=self.radii,L=self.L,
            steps=self.step_index,extra_forward_evals=self.extra_forward_evals,line_seconds=self.line_seconds))
    def feasibility(self):
        ratios={n:float(torch.linalg.matrix_norm(p.detach().float(),ord=2))/self.radii[n] for n,p in self.matrices}
        assert max(ratios.values())<=1+1e-5,'FW spectral ball violated'
        return ratios
