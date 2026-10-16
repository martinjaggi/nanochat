"""One-B300 frozen-state train/fit/check diagnosis and matched continuations.

Uses immutable complete checkpoints and disjoint training-distribution shards.
No development/final evaluation data select a probe step.
"""
import argparse,copy,json,math,os,pathlib,subprocess,sys,time
import torch
from research.unnormalized_muon.fresh_math import schedule,momentum,select_grid,paired_stats
from research.unnormalized_muon.fresh_state import rng_state,restore_rng,batch_hash,named_momenta,frozen_directions,verify_files


class PathLoss:
    def __init__(self,model):
        self.model=model;self.forwards=0;self.backwards=0;self.tokens=0
        from torch.func import functional_call
        def seq_forward(candidate,x,y):
            losses=functional_call(model,candidate,(x,y),dict(loss_reduction='none')).view_as(y)
            return losses.sum(-1)/y.ne(-1).sum(-1).clamp_min(1)
        self.forward=torch.compile(seq_forward,dynamic=False,fullgraph=True)
    def __call__(self,directions,eta,x,y,gradient=False):
        matrices=[(n,p) for n,p in self.model.named_parameters() if n in directions]
        with torch.enable_grad() if gradient else torch.no_grad():
            candidate={n:p if eta==0 else p-eta*directions[n] for n,p in matrices}
            seq=self.forward(candidate,x,y);self.forwards+=1;self.tokens+=y.numel()
            if gradient:
                assert eta==0
                gg=torch.autograd.grad(seq.mean(),[p for _,p in matrices]);self.backwards+=1
                grads={n:g.detach().clone() for (n,p),g in zip(matrices,gg)}
                return seq.detach().double().cpu(),grads
            return seq.detach().double().cpu()
    def layer(self,directions,etas,x,y):
        with torch.no_grad():
            candidate={n:p-etas[n]*directions[n] for n,p in self.model.named_parameters() if n in directions}
            seq=self.forward(candidate,x,y);self.forwards+=1;self.tokens+=y.numel();return seq.detach().double().cpu()


def capture(model,opt):
    return dict(model={n:p.detach().clone() for n,p in model.state_dict().items()},opt=copy.deepcopy(opt.state_dict()),
        grads={n:None if p.grad is None else p.grad.clone() for n,p in model.named_parameters()},rng=rng_state())


def restore(model,opt,state):
    model.load_state_dict(state['model']);opt.load_state_dict(copy.deepcopy(state['opt']))
    for n,p in model.named_parameters():p.grad=None if state['grads'][n] is None else state['grads'][n].clone()
    restore_rng(state['rng'])


def unchanged(model,opt,state):
    assert all(torch.equal(p,state['model'][n]) for n,p in model.state_dict().items())
    for n,p in model.named_parameters():
        g=state['grads'][n];assert (p.grad is None and g is None) or (g is not None and torch.equal(p.grad,g))
    # Full optimizer state recursively checked, including auxiliaries.
    def equal(a,b):
        if isinstance(a,torch.Tensor):return torch.equal(a,b)
        if isinstance(a,dict):return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
        if isinstance(a,(list,tuple)):return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
        return a==b
    assert equal(opt.state_dict(),state['opt'])
    rng=rng_state();assert torch.equal(rng['cpu'],state['rng']['cpu'].cpu()) and torch.equal(rng['cuda'],state['rng']['cuda'].cpu())
    assert rng['python']==state['rng']['python']
    import numpy as np
    assert rng['numpy'][0]==state['rng']['numpy'][0] and np.array_equal(rng['numpy'][1],state['rng']['numpy'][1]) and rng['numpy'][2:]==state['rng']['numpy'][2:]


def configure(opt,step,lr_multiplier=1.):
    for g in opt.param_groups:
        g['lr']=g['initial_lr']*schedule(step)*(lr_multiplier if g['kind']=='muon' else 1.)
        if g['kind']=='muon':g['momentum']=momentum(step)


def replay_batches(state,tokenizer,count):
    from nanochat.dataloader import tokenizing_distributed_data_loader_with_state_bos_bestfit as loader
    verify_files(state);assert state['config']['device_batch_size']==32 and state['config']['total_batch_size']==32768,'diagnosis currently accumulation1'
    it=loader(tokenizer,32,1024,'train',device='cuda')
    for _ in range(state['replay_batches_yielded']):x,y,cursor=next(it)
    assert batch_hash(x,y)==state['prefetched_hash'],'exact replay/prefetch mismatch'
    batches=[(x.clone(),y.clone())]
    for _ in range(count-1):
        x,y,cursor=next(it);batches.append((x.clone(),y.clone()))
    assert cursor['pq_idx']<len(state['data_files'])-3,'main stream overlaps reserved fit/check shards'
    return batches


def parity(model,opt,compiled,batch,state):
    configure(opt,state['step']);model.zero_grad(set_to_none=True)
    x,y=batch;compiled(x,y).backward()
    before=capture(model,opt);grads={n:p.grad.detach().clone() for n,p in model.named_parameters() if p.grad is not None}
    directions,next_m=frozen_directions(model,opt,grads,momentum(state['step']))
    rates={n:g['lr'] for g in opt.param_groups if g['kind']=='muon' for p in g['params'] for n,q in model.named_parameters() if q is p}
    opt.step();errors=[]
    for n,p in model.named_parameters():
        if n not in directions:continue
        expected=before['model'][n]-rates[n]*directions[n];delta=rates[n]*directions[n]
        errors.append(float((p-expected).norm()/delta.norm().clamp_min(1e-12)))
    after_m=named_momenta(model,opt)
    merr=max(float((after_m[n]-next_m[n]).norm()/next_m[n].norm().clamp_min(1e-12)) for n in next_m)
    restore(model,opt,before);model.zero_grad(set_to_none=True)
    assert max(errors)<.02 and merr<1e-5,('fused prescribed-step parity',max(errors),merr)
    return dict(max_relative_displacement_error=max(errors),max_momentum_relative_error=merr,gradient_evals=1,forward_evals=1)


def evaluate_dev(model,tokenizer):
    from nanochat.dataloader import tokenizing_distributed_data_loader_bos_bestfit as loader
    from nanochat.loss_eval import evaluate_bpb
    from nanochat.tokenizer import get_token_bytes
    tokens=0;total=torch.zeros((),device='cuda')
    class Proxy:
        def get_device(self):return model.get_device()
        def __call__(self,x,y,**kw):
            nonlocal tokens,total
            z=model(x,y,**kw);total+=z.sum();tokens+=int(y.ne(-1).sum());return z
    bpb=evaluate_bpb(Proxy(),loader(tokenizer,32,1024,'val',device='cuda'),8,get_token_bytes(device='cuda'))
    return dict(loss=float(total/tokens),bpb=bpb,tokens=tokens)


def continuation(model,opt,compiled,batches,state,ratios,tokenizer):
    """Change one Muon step OR hold multiplier; common future tokens/aux rule."""
    start=state['step'];base=capture(model,opt);rows=[]
    # Deduplicate equal choices; at most two alternatives plus control.
    unique=[]
    for x in [1.]+ratios:
        if x not in unique:unique.append(x)
    for policy in ['one_step','held128']:
        for ratio in unique:
            if ratio==1 and policy=='held128':continue
            restore(model,opt,base);record=dict(policy=policy,ratio=ratio,evaluations={});torch.cuda.synchronize();t=time.perf_counter()
            for j,(x,y) in enumerate(batches[:128]):
                model.zero_grad(set_to_none=True);compiled(x,y).backward()
                configure(opt,start+j,ratio if policy=='held128' or j==0 else 1.);opt.step()
                if j+1 in [32,128]:record['evaluations'][str(j+1)]=evaluate_dev(model,tokenizer)
            torch.cuda.synchronize();record['seconds']=time.perf_counter()-t;record['gradient_evals']=128;record['update_tokens']=128*32768;rows.append(record)
    restore(model,opt,base);unchanged(model,opt,base)
    return rows


def diagnose(out,cfg):
    from nanochat.gpt import GPT,GPTConfig
    from nanochat.tokenizer import get_tokenizer
    from nanochat.dataloader import tokenizing_distributed_data_loader_with_state_bos_bestfit as loader
    from research.unnormalized_muon.gap_wd import block_armijo
    tokenizer=get_tokenizer();all_rows=[];continuations=[];audits=[];totals=dict(forward_evals=0,gradient_evals=0,probe_tokens=0,continuation_gradient_evals=0,continuation_tokens=0)
    for checkpoint_index,step in enumerate([40,400,1500]):
        torch._dynamo.reset()  # isolate independent model instances; cost remains charged
        state=torch.load(out/'research_checkpoints'/f'branch-{step:06d}.pt',map_location='cuda',weights_only=False)
        with torch.device('meta'):model=GPT(GPTConfig(**state['model_config']))
        model.to_empty(device='cuda');model.init_weights();model.load_state_dict(state['model']);model.train()
        opt=model.setup_optimizer(unembedding_lr=state['config']['unembedding_lr']*.25,embedding_lr=state['config']['embedding_lr']*.25,scalar_lr=state['config']['scalar_lr']*.25,matrix_lr=state['config']['matrix_lr']*.25,weight_decay=cfg['fixed_wd'])
        opt.load_state_dict(state['optimizer']);restore_rng(state['rng'])
        named=named_momenta(model,opt);assert all(torch.equal(named[n],state['named_momentum'][n]) for n in named)
        # Main stream replay reconstructs its internal packing buffers and the
        # exact prefetch. Fit/check use separate entire parquet shards.
        batches=replay_batches(state,tokenizer,128 if step==400 else 4)
        paths=[f['path'] for f in state['data_files']]
        fit=loader(tokenizer,32,1024,'train',device='cuda',parquet_paths=[paths[-3],paths[-1]])
        check=loader(tokenizer,32,1024,'train',device='cuda',parquet_paths=[paths[-2],paths[-1]])
        for _ in range(checkpoint_index*4):next(fit);next(check)
        compiled=torch.compile(model,dynamic=False);configure(opt,step)
        audit=parity(model,opt,compiled,batches[0],state);audit['step']=step;audits.append(audit)
        totals['gradient_evals']+=1;totals['forward_evals']+=1;totals['probe_tokens']+=32768
        restore_rng(state['rng']);base=capture(model,opt);loss_path=PathLoss(model);eta=.25*cfg['matrix_lr']*schedule(step)
        construction_params={n:torch.zeros_like(p) for n,p in model.named_parameters() if n in named}
        first_choices=[]
        for triple in range(4):
            x,y=batches[triple];fx,fy,_=next(fit);fx,fy=fx.clone(),fy.clone();cx,cy,_=next(check);cx,cy=cx.clone(),cy.clone()
            rng=rng_state()
            # Actual production scalar-loss gradient constructs the native vertex.
            # Own-path sequence gradients measure slopes for loss-curve checks.
            compiled(x,y).backward();native_grads={n:p.grad.detach().clone() for n,p in model.named_parameters() if n in named};model.zero_grad(set_to_none=True)
            totals['gradient_evals']+=1;totals['forward_evals']+=1;totals['probe_tokens']+=32768
            train0,grads=loss_path(construction_params,0,x,y,gradient=True)
            gradient_path_relative_error=math.sqrt(sum(float((native_grads[n]-grads[n]).double().square().sum()) for n in named)/max(sum(float(native_grads[n].double().square().sum()) for n in named),1e-30))
            directions,next_m=frozen_directions(model,opt,native_grads,momentum(step))
            fit0,fg=loss_path(directions,0,fx,fy,gradient=True)
            btrain={n:float((grads[n].double()*p.double()).sum()) for n,p in directions.items()}
            bfit={n:float((fg[n].double()*p.double()).sum()) for n,p in directions.items()}
            v={n:float(p.double().square().sum()) for n,p in directions.items()}
            rates=[min(1/cfg['fixed_wd'],eta*k) for k in [0,.25,.5,1,2]]
            curve={};sequences={}
            for role,(xx,yy) in dict(train=(x,y),fit=(fx,fy),check=(cx,cy)).items():
                restore_rng(rng);seqs=[loss_path(directions,e,xx,yy) for e in rates]
                curve[role]=[float(z.mean()) for z in seqs];sequences[role]=[z.tolist() for z in seqs]
            ti=select_grid(curve['train'],rates);fi=select_grid(curve['fit'],rates)
            check_train=paired_stats((torch.tensor(sequences['check'][ti],dtype=torch.float64)-torch.tensor(sequences['check'][3],dtype=torch.float64)).tolist())
            check_fit=paired_stats((torch.tensor(sequences['check'][fi],dtype=torch.float64)-torch.tensor(sequences['check'][3],dtype=torch.float64)).tolist())
            # Repeat noise then resolved central differences on the SAME fit path.
            repeat=float(loss_path(directions,0,fx,fy).mean());noise=abs(repeat-curve['fit'][0]);fd=[]
            for scale in [.01,.03,.1]:
                h=eta*scale;plus=float(loss_path(directions,h,fx,fy).mean());minus=float(loss_path(directions,-h,fx,fy).mean())
                observed=-(plus-minus)/(2*h);expected=sum(bfit.values());resolved=abs(plus-minus)>max(10*noise,1e-6)
                fd.append(dict(h=h,observed_b=observed,gradient_b=expected,resolved=resolved,relative_error=abs(observed-expected)/max(abs(expected),1e-12)))
            resolved=[z for z in fd if z['resolved']];assert resolved and min(z['relative_error'] for z in resolved)<.2,('fit derivative mismatch',step,triple,fd)
            cap=.005*schedule(step);plain={n:cap for n in directions};sign={n:cap if btrain[n]>0 and v[n]>0 else 0. for n in directions}
            order=list(directions);armijo_evals=[]
            def candidate(etas):
                result=loss_path.layer(directions,dict(zip(order,etas)),x,y);armijo_evals.append(float(result.mean()));return float(result.mean())
            ar,L,trials,accepted=block_armijo(candidate,f0=curve['train'][0],b=[btrain[n] for n in order],v=[v[n] for n in order],L=1e-16,decay=cfg['fixed_wd'],max_eta=cap)
            arm=dict(zip(order,ar));layer_check={}
            for label,rr in [('plain_cap',plain),('cap_sign',sign),('armijo',arm)]:
                z=loss_path.layer(directions,rr,cx,cy);layer_check[label]=dict(loss=float(z.mean()),sequence_losses=z.tolist())
            record=dict(step=step,triple=triple,construction_gradient_path_relative_error=gradient_path_relative_error,eta_base=eta,grid=rates,loss_curves=curve,sequence_losses=sequences,selected_train_index=ti,selected_fit_index=fi,
                check_delta_train_selected=check_train,check_delta_fit_selected=check_fit,b_train=btrain,b_fit=bfit,v=v,
                sign_flip_fraction=sum((btrain[n]>0)!=(bfit[n]>0) for n in order)/len(order),repeat_noise=noise,finite_differences=fd,
                layer_check=layer_check,layer_armijo_accepted=accepted,layer_zeta=trials[-1]['zeta'] if trials else 0.,
                cap_sign_displacement_vs_armijo=sum((sign[n]-arm[n])**2*v[n] for n in order),
                restored_state_replays_selection=True,train_hash=batch_hash(x,y),fit_hash=batch_hash(fx,fy),check_hash=batch_hash(cx,cy),fit_shard=paths[-3],check_shard=paths[-2])
            # Re-evaluate fit choices after restoring the saved RNG; check data is never used to choose.
            restore_rng(rng);again=[float(loss_path(directions,e,fx,fy).mean()) for e in rates]
            assert select_grid(again,rates)==fi and max(abs(a-b) for a,b in zip(again,curve['fit']))<=max(noise*2,1e-7),'restored selection differs'
            all_rows.append(record)
            if triple==0:first_choices=[rates[i]/eta for i in sorted(range(len(rates)),key=lambda i:curve['fit'][i]) if i!=3][:2]
            restore_rng(base['rng']);unchanged(model,opt,base)
        totals['forward_evals']+=loss_path.forwards;totals['gradient_evals']+=loss_path.backwards;totals['probe_tokens']+=loss_path.tokens
        if step==400:
            continuations=continuation(model,opt,compiled,batches,state,first_choices,tokenizer)
            totals['continuation_gradient_evals']=sum(x['gradient_evals'] for x in continuations);totals['continuation_tokens']=sum(x['update_tokens'] for x in continuations)
            totals['continuation_validation_forward_evals']=16*len(continuations);totals['continuation_validation_tokens']=524288*len(continuations)
        del state,base,model,opt,compiled,loss_path,batches
    positives=sum(x['check_delta_fit_selected']['mean']<0 for x in all_rows)
    control=next(x for x in continuations if x['ratio']==1)['evaluations']['128']['loss']
    improved=[x for x in continuations if x['ratio']!=1 and x['evaluations']['128']['loss']<control-.001 and x['evaluations']['32']['loss']<next(y for y in continuations if y['ratio']==1)['evaluations']['32']['loss']-.001]
    gate=positives>=8 and bool(improved)
    result=dict(status='completed',probe_rows=all_rows,continuations=continuations,parity_audits=audits,cost=totals,
        gate_passed=gate,fresh_check_improvements=positives,total_probes=len(all_rows),continuation_control_ce=control,
        interpretation='Four independent batch triples at each frozen checkpoint. Sequence uncertainty is local and not across seeds; the best-fit packer consumes each document once and discards cropped tails; sequence SEs remain pilot heuristics. Conservative gate also requires continuation improvement. No check-loss candidate selection.',
        decision='consider amortized same/fresh-fit matched screen' if gate else 'stop online-controller expansion; report negative diagnosis or prefer cap/sign if matched')
    (out/'fresh_diagnosis.json').write_text(json.dumps(result,indent=2));return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--config',required=True);a=p.parse_args();out=pathlib.Path(a.output);cfg=json.load(open(a.config));start=time.perf_counter()
    assert torch.cuda.device_count()==1 and 'B300' in torch.cuda.get_device_name(0)
    os.environ.update(NANOCHAT_BASE_DIR=str(out/'store'),NANOCHAT_CLEAN_MUON='1',NANOCHAT_UNNORMALIZED_MUON='0',RESEARCH_MUON_DECAY='standard',RESEARCH_MUON_GEOMETRY='q_scaled')
    subprocess.run([sys.executable,'-m','research.unnormalized_muon.run','--output',str(out),'--config',a.config],check=True)
    t=time.perf_counter()
    try:result=diagnose(out,cfg)
    except Exception as error:
        summary=json.loads((out/'summary.json').read_text());summary.update(status='failed',diagnosis_failure=str(error));(out/'summary.json').write_text(json.dumps(summary,indent=2));raise
    torch.cuda.synchronize();probe_seconds=time.perf_counter()-t
    summary=json.loads((out/'summary.json').read_text());summary.update(fresh_diagnosis=dict(gate_passed=result['gate_passed'],fresh_check_improvements=result['fresh_check_improvements'],cost=result['cost'],seconds=probe_seconds),process_seconds=time.perf_counter()-start)
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__':main()
