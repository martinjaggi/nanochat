"""Fixed ordinary WD: per-matrix or joint gap LR on the COMPLETE Muon ray."""
import math,time,torch,os
from torch.func import functional_call
from research.unnormalized_muon.protocol_math import contraction
from research.unnormalized_muon.fw import FWMuon,weighted_mean,polar_direction


def reciprocal_eta(eta0,decay,t):
    assert eta0>=0 and decay>0 and t>=0
    return eta0/(1+.5*decay*eta0*t)


def propose_etas(b,v,L,decay,scope,shape=None,max_eta=None):
    """Actual matrix coefficients. No extra shape factor after this function."""
    assert decay>0 and L>0 and math.isfinite(L) and scope in {'layer','joint'}
    assert len(b)==len(v)>0 and all(math.isfinite(x) for x in b+v) and all(x>=0 for x in v)
    cap=min(1/decay,max_eta) if max_eta is not None else 1/decay
    assert cap>=0
    if scope=='layer':return [min(cap,x/(L*y)) if x>0 and y>0 else 0. for x,y in zip(b,v)]
    c=shape if shape is not None else [1.]*len(b)
    assert len(c)==len(b) and all(x>0 for x in c)
    bb=sum(x*z for x,z in zip(b,c));vv=sum(y*z*z for y,z in zip(v,c))
    eta=min(cap/max(c),bb/(L*vv)) if bb>0 and vv>0 else 0.
    return [eta*z for z in c]


def block_backtrack(evaluate, *, f0,b,v,L,decay,scope,shape=None,max_trials=16,tolerance=1e-6,max_eta=None):
    """One loss check for the simultaneously proposed block coefficients."""
    trials=[]
    for _ in range(max_trials):
        etas=propose_etas(b,v,L,decay,scope,shape,max_eta)
        if not any(etas):return etas,L,trials,False
        loss=float(evaluate(etas));linear=sum(e*x for e,x in zip(etas,b));quadratic=sum(e*e*y for e,y in zip(etas,v))
        bound=f0-linear+.5*L*quadratic
        accepted=math.isfinite(loss) and loss<=bound+tolerance*max(1.,abs(f0))
        trials.append(dict(L=L,etas=etas,loss=loss,bound=bound,accepted=accepted,linear_decrease=linear,quadratic_norm=quadratic))
        if accepted:return etas,L,trials,True
        L*=2
    return [0.]*len(b),L,trials,False



def block_armijo(evaluate, *, f0,b,v,L,decay,max_eta=None,sigma=.1,max_trials=16,tolerance=1e-6,proposal=None):
    """Freeze the per-layer proposal; backtrack ONE common multiplier zeta."""
    assert 0<sigma<1
    base=propose_etas(b,v,L,decay,'layer',max_eta=max_eta) if proposal is None else proposal
    slope=sum(e*x for e,x in zip(base,b))
    if slope<=0:return base,L,[],False
    trials=[];zeta=1.
    for _ in range(max_trials):
        etas=[zeta*e for e in base];loss=float(evaluate(etas));bound=f0-sigma*zeta*slope
        accepted=math.isfinite(loss) and loss<=bound+tolerance*max(1.,abs(f0)) and loss<=f0
        trials.append(dict(L=L,zeta=zeta,sigma=sigma,base_etas=base,etas=etas,loss=loss,bound=bound,accepted=accepted))
        if accepted:return etas,L/zeta,trials,True
        zeta*=.5
    return [0.]*len(base),L/zeta,trials,False

class GapWD(FWMuon):
    """Existing native matrix partition/Nesterov; fixed lambda, searched Q+lambda W.

    Layer mode uses one shared Frobenius curvature bound, separate actual LRs,
    and one simultaneous acceptance test. Joint-uniform uses a single actual
    LR. Joint-native searches c_i*(Q_i+lambda W_i), so it is a shape-weighted
    block-FW ray with gamma_i=lambda*c_i*eta_outer, NOT one shared FW mixing.
    """
    def __init__(self,inner,model,recorder,decay,scope='layer',shape_policy='uniform',initial_L=.01,safe_oracle=False):
        assert decay>0 and scope in {'layer','joint'} and shape_policy in {'uniform','native'}
        self.inner=inner;self.model=model;self.recorder=recorder;self.param_groups=inner.param_groups
        self.geometry=os.environ.get('RESEARCH_MUON_GEOMETRY','legacy')
        self.acceptance=os.environ.get('RESEARCH_GAP_ACCEPTANCE','quadratic')
        self.eta_cap=float(os.environ.get('RESEARCH_GAP_ETA_CAP',str(1/decay)))
        self.cap_schedule=os.environ.get('RESEARCH_GAP_CAP_SCHEDULE','none')
        self.sigma=float(os.environ.get('RESEARCH_GAP_ARMIJO_SIGMA','.1'))
        self.proposal_beta=float(os.environ.get('RESEARCH_GAP_PROPOSAL_BETA','0'))
        self.relative_cap=float(os.environ.get('RESEARCH_GAP_RELATIVE_CAP','0'))
        self.probe_every=int(os.environ.get('RESEARCH_GAP_PROBE_EVERY','1'))
        self.previous_etas=None
        assert 0<=self.proposal_beta<1 and self.relative_cap>=0 and self.probe_every>=1
        assert not(self.proposal_beta or self.relative_cap) or (scope=='layer' and self.acceptance=='armijo')
        assert self.acceptance in {'quadratic','armijo'} and self.cap_schedule in {'none','stable','cooldown'}
        assert self.eta_cap>0 and (self.acceptance!='armijo' or scope=='layer')
        assert self.geometry!='q_scaled' or shape_policy=='uniform','q_scaled already includes c inside Q'
        self.decay=decay;self.scope=scope;self.shape_policy=shape_policy;self.safe_oracle=safe_oracle;self.L=initial_L
        self.batch=[];self.losses=[];self.loss_counts=[];self.step_index=0;self.history=[]
        names={id(p):n for n,p in model.named_parameters()}
        self.matrices=[(names[id(p)],p) for g in self.param_groups if g['kind']=='muon' for p in g['params']]
        self.m={n:torch.zeros_like(p) for n,p in self.matrices}
        self.shape=[max(1.,p.shape[-2]/p.shape[-1])**.5 for _,p in self.matrices]
        self.decay_exposure_by_parameter={n:0. for n,p in self.matrices}
        self.contraction_by_parameter={n:contraction(None,0.) for n,p in self.matrices}
        self.extra_forward_evals=0;self.extra_microbatch_forward_evals=0;self.line_seconds=0.
        self.components=dict(direction=0.,reference=0.,candidates=0.,auxiliary=0.)
        def candidate_forward(candidate,x,y):return functional_call(self.model,candidate,(x,y))
        self.candidate_forward=torch.compile(candidate_forward,dynamic=False,fullgraph=True)
        self.initial_feasibility=self.feasibility()
        if safe_oracle:assert max(self.initial_feasibility.values())<=1+1e-5,'fixed WD domain initially infeasible'
        self.recorder.emit('gap_wd_geometry',scope=scope,shape_policy=shape_policy,fixed_lambda=decay,radius=1/decay,
            safe_oracle=safe_oracle,geometry=self.geometry,acceptance=self.acceptance,proposal_beta=self.proposal_beta,relative_cap=self.relative_cap,probe_every=self.probe_every,eta_cap=self.eta_cap,cap_schedule=self.cap_schedule,initial_feasibility=self.initial_feasibility,
            initial_L=initial_L,NS='native five Polar Express/Frobenius; no row equilibration or NorMuon',
            direction='Q+lambda*W, ordinary unmasked decay included in ray; no added L2 penalty',
            shape='actual per-layer LR; no external shape factor applied twice',
            interpretation='exact FW only for feasible initial point and exact polar; native finite NS approximate')
    @torch.no_grad()
    def step(self):
        torch.cuda.synchronize();start=time.perf_counter();directions=[]
        mu=next(g['momentum'] for g in self.param_groups if g['kind']=='muon')
        for (n,p),c in zip(self.matrices,self.shape):
            self.m[n].lerp_(p.grad,1-mu)
            q=polar_direction(p.grad.lerp(self.m[n],mu),safe=self.safe_oracle)
            directions.append((c*q if self.geometry=='q_scaled' else q)+self.decay*p)
        b=[float((p.grad.double()*d.double()).sum()) for (_,p),d in zip(self.matrices,directions)]
        v=[float(d.double().square().sum()) for d in directions]
        torch.cuda.synchronize();direction_seconds=time.perf_counter()-start
        rng=torch.cuda.get_rng_state();cpu_rng=torch.get_rng_state()
        audit=None
        if self.step_index==0:
            audit=[(p,p.detach().clone(),None if p.grad is None else p.grad.clone()) for p in self.model.parameters()]
            buffers=[(p,p.clone()) for p in self.model.buffers()]
        def evaluate(etas):
            try:
                torch.cuda.set_rng_state(rng);torch.set_rng_state(cpu_rng)
                candidate={n:p-e*d for (n,p),e,d in zip(self.matrices,etas,directions)}
                value=weighted_mean([self.candidate_forward(candidate,x,y) for x,y in self.batch],[y.numel() for _,y in self.batch])
                self.extra_forward_evals+=1;self.extra_microbatch_forward_evals+=len(self.batch)
                return float(value)
            finally:torch.cuda.set_rng_state(rng);torch.set_rng_state(cpu_rng)
        reference_start=time.perf_counter()
        shapes=self.shape if self.scope=='joint' and self.shape_policy=='native' else None
        group=next(g for g in self.param_groups if g['kind']=='muon')
        ratio=group['lr']/group['initial_lr']
        cap_multiplier=(min(1.,(self.step_index+1)/40) if self.cap_schedule=='stable' else ratio if self.cap_schedule=='cooldown' else 1.)
        if getattr(self.recorder,'time_budget',0)>0 and self.cap_schedule=='stable':
            cap_multiplier=min(1.,max(self.recorder.active_seconds/self.recorder.time_budget,1/self.recorder.reference_updates)/(40/self.recorder.reference_updates))
        cap=min(1/self.decay,self.eta_cap*cap_multiplier)
        etas=propose_etas(b,v,self.L,self.decay,self.scope,shapes,cap)
        checked=self.step_index%self.probe_every==0
        reference=evaluate([0.]*len(b)) if checked and any(etas) else float(self.loss_before)
        torch.cuda.synchronize();reference_seconds=time.perf_counter()-reference_start
        search_start=time.perf_counter()
        if not checked:
            # Explicitly unchecked cached-curvature step: no reference/candidate
            # forward. This is NOT a validated line search on this iteration.
            trials=[];accepted=False
        elif self.acceptance=='armijo':
            proposal=propose_etas(b,v,max(self.L*.5,1e-16),self.decay,'layer',max_eta=cap)
            if self.previous_etas is not None and self.proposal_beta:
                proposal=[min(cap,self.proposal_beta*old+(1-self.proposal_beta)*new) if bb>0 else 0. for old,new,bb in zip(self.previous_etas,proposal,b)]
            if self.relative_cap:
                for i,((n,p),vv) in enumerate(zip(self.matrices,v)):
                    c=self.shape[i] if self.geometry=='q_scaled' else 1.
                    floor=.1*c/self.decay*math.sqrt(min(p.shape))
                    radius=max(float(p.float().norm()),floor)
                    proposal[i]=min(proposal[i],self.relative_cap*radius/math.sqrt(vv)) if vv>0 else 0.
            etas,self.L,trials,accepted=block_armijo(evaluate,f0=reference,b=b,v=v,L=max(self.L*.5,1e-16),decay=self.decay,max_eta=cap,sigma=self.sigma,proposal=proposal)
        else:
            etas,self.L,trials,accepted=block_backtrack(evaluate,f0=reference,b=b,v=v,L=max(self.L*.5,1e-16),decay=self.decay,scope=self.scope,shape=shapes,max_eta=cap)
        torch.cuda.synchronize();candidate_seconds=time.perf_counter()-search_start
        if audit is not None:
            assert all(torch.equal(p,old) and (g is None or torch.equal(p.grad,g)) for p,old,g in audit),'gap search mutated model/gradients'
            assert all(torch.equal(p,old) for p,old in buffers),'gap search mutated buffers'
            assert torch.equal(torch.cuda.get_rng_state(),rng) and torch.equal(torch.get_rng_state(),cpu_rng),'gap search changed RNG'
            self.recorder.emit('gap_wd_audit',parameters_gradients_buffers_rng_unchanged=True)
        applied=accepted or (not checked and any(etas))
        if applied:
            for (n,p),e,d in zip(self.matrices,etas,directions):
                p.add_(d,alpha=-e)
                self.decay_exposure_by_parameter[n]+=e*self.decay
                self.contraction_by_parameter[n]=contraction(self.contraction_by_parameter[n],e*self.decay)
        self.previous_etas=etas if applied else self.previous_etas
        aux_start=time.perf_counter();original=self.inner.param_groups
        try:
            self.inner.param_groups=[g for g in original if g['kind']=='adamw'];self.inner.step()
        finally:self.inner.param_groups=original
        torch.cuda.synchronize();aux_seconds=time.perf_counter()-aux_start
        elapsed=time.perf_counter()-start;self.line_seconds+=elapsed
        components=dict(direction=direction_seconds,reference=reference_seconds,candidates=candidate_seconds,auxiliary=aux_seconds)
        for k,val in components.items():self.components[k]+=val
        linear=sum(e*x for e,x in zip(etas,b));quad=sum(e*e*y for e,y in zip(etas,v))
        actual=reference-trials[-1]['loss'] if accepted else 0. if checked else None
        row=dict(step=self.step_index,checked=checked,applied=applied,proposal_beta=self.proposal_beta,relative_cap=self.relative_cap,geometry=self.geometry,acceptance=self.acceptance,eta_cap=cap,cap_active_blocks=sum(applied and e>=cap*(1-1e-7) for e in etas),accepted=accepted,L=self.L,b=b,v=v,actual_etas=etas,
            gammas=[e*self.decay for e in etas],native_shape_multipliers=self.shape,
            implied_cli_lrs=[e/.25 if self.geometry=='q_scaled' else e/c/.25 for e,c in zip(etas,self.shape)],negative_blocks=sum(x<=0 for x in b),
            predicted_decrease=linear-.5*self.L*quad,actual_decrease=actual,trials=trials,
            reference_loss=reference,accumulated_fresh_loss=float(self.loss_before),
            reference_delta=reference-float(self.loss_before),component_seconds=components,
            extra_forward_evals=self.extra_forward_evals,extra_microbatch_forward_evals=self.extra_microbatch_forward_evals,
            accumulation_microbatches=len(self.batch))
        self.history.append({k:val for k,val in row.items() if k!='trials'}|dict(trial_count=len(trials)))
        self.recorder.emit('gap_wd_update',**row)
        self.step_index+=1;self.batch=[];self.losses=[];self.loss_counts=[]
    def feasibility(self):
        return {n:self.decay*float(torch.linalg.matrix_norm(p.detach().float(),ord=2))/(max(1.,p.shape[-2]/p.shape[-1])**.5 if self.geometry=='q_scaled' else 1.) for n,p in self.matrices}
    def diagnostics(self):
        def quantiles(values):
            x=torch.tensor(values,dtype=torch.float64)
            return dict(zip(['min','p25','median','p75','max'],x.quantile(torch.tensor([0.,.25,.5,.75,1.],dtype=torch.float64)).tolist()))
        return dict(geometry=self.geometry,acceptance=self.acceptance,eta_cap=self.eta_cap,cap_schedule=self.cap_schedule,scope=self.scope,shape_policy=self.shape_policy,fixed_lambda=self.decay,radius=1/self.decay,
            proposal_beta=self.proposal_beta,relative_cap=self.relative_cap,probe_every=self.probe_every,unchecked_steps=sum(not h["checked"] for h in self.history),applied_steps=sum(h["applied"] for h in self.history),safe_oracle=self.safe_oracle,steps=self.step_index,accepted_steps=sum(h['accepted'] for h in self.history),
            skipped_blocks=sum(h['negative_blocks'] for h in self.history),components=self.components,
            actual_eta_quantiles=quantiles([x for h in self.history for x in h['actual_etas']]),
            gamma_quantiles=quantiles([x for h in self.history for x in h['gammas']]),
            L_quantiles=quantiles([h['L'] for h in self.history]),trial_quantiles=quantiles([h['trial_count'] for h in self.history]),
            actual_decrease_quantiles=quantiles([h['actual_decrease'] for h in self.history if h['actual_decrease'] is not None]))
    def state_dict(self):
        return dict(inner=self.inner.state_dict(),gap_wd=dict(m=self.m,L=self.L,step=self.step_index,decay=self.decay,
            scope=self.scope,shape_policy=self.shape_policy,history=self.history,extra_forward_evals=self.extra_forward_evals,
            extra_microbatch_forward_evals=self.extra_microbatch_forward_evals,line_seconds=self.line_seconds,components=self.components,previous_etas=self.previous_etas,contraction_by_parameter=self.contraction_by_parameter,decay_exposure_by_parameter=self.decay_exposure_by_parameter))
    def load_state_dict(self,state):
        self.inner.load_state_dict(state['inner']);self.param_groups=self.inner.param_groups;s=state['gap_wd'];assert s['decay']==self.decay and s['scope']==self.scope and s['shape_policy']==self.shape_policy
        self.previous_etas=s.get('previous_etas');self.m=s['m'];self.L=s['L'];self.step_index=s['step'];self.history=s['history'];self.extra_forward_evals=s['extra_forward_evals'];self.extra_microbatch_forward_evals=s['extra_microbatch_forward_evals'];self.line_seconds=s['line_seconds'];self.components=s['components'];self.contraction_by_parameter=s.get('contraction_by_parameter',{});self.decay_exposure_by_parameter=s['decay_exposure_by_parameter']
