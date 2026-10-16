"""Full named optimizer state and deterministic replay recipe for exact branches."""
import copy,hashlib,os,pathlib,random,torch
import numpy as np


def rng_state():
    return dict(cpu=torch.get_rng_state(),cuda=torch.cuda.get_rng_state(),python=random.getstate(),numpy=np.random.get_state())


def restore_rng(state):
    torch.set_rng_state(state['cpu'].cpu());torch.cuda.set_rng_state(state['cuda'].cpu());random.setstate(state['python']);np.random.set_state(state['numpy'])


def batch_hash(x,y):
    h=hashlib.sha256()
    for p in (x,y):h.update(p.detach().cpu().numpy().tobytes())
    return h.hexdigest()


def named_momenta(model,optimizer):
    names={id(p):n for n,p in model.named_parameters()};out={}
    for group in optimizer.param_groups:
        if group['kind']!='muon':continue
        params=group['params'];state=optimizer.state.get(params[0],{})
        stack=state.get('momentum_buffer')
        assert stack is not None and stack.shape[0]==len(params),'single-rank initialized fused momentum required'
        for i,p in enumerate(params):out[names[id(p)]]=stack[i].detach().clone()
    return out


def save_branch(path,model,optimizer,*,step,x,y,cursor,config,model_config):
    from nanochat.dataset import list_parquet_files
    paths=list_parquet_files();files=[dict(path=p,size=os.stat(p).st_size,mtime_ns=os.stat(p).st_mtime_ns) for p in paths]
    state=dict(model=model.state_dict(),optimizer=optimizer.state_dict(),named_momentum=named_momenta(model,optimizer),rng=rng_state(),
        step=step,horizon=config['num_iterations'],config=config,model_config=model_config,cursor=copy.deepcopy(cursor),
        prefetched_x=x.detach().cpu(),prefetched_y=y.detach().cpu(),prefetched_hash=batch_hash(x,y),
        replay_batches_yielded=step*(config['total_batch_size']//(config['device_batch_size']*config['max_seq_len']))+1,
        data_files=files,commit=os.environ['RESEARCH_COMMIT'],resume_policy='replay immutable deterministic loader from origin; validate exact prefetched batch; native row-group cursor alone is approximate')
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True);torch.save(state,path)


def verify_files(state):
    for f in state['data_files']:
        s=os.stat(f['path']);assert (s.st_size,s.st_mtime_ns)==(f['size'],f['mtime_ns']),'data changed since checkpoint'


@torch.no_grad()
def frozen_directions(model,optimizer,grads,mu):
    """Use the ACTUAL fused NS implementation on disposable tensors.

    No mutation of production gradients/momentum. LR=1, WD=0 and zero dummy
    weights expose raw NS output; c is then included in Q exactly once.
    """
    from nanochat.optim import muon_step_fused
    names={id(p):n for n,p in model.named_parameters()};directions={};next_m={}
    named=named_momenta(model,optimizer)
    for group in optimizer.param_groups:
        if group['kind']!='muon':continue
        params=group['params'];gg=torch.stack([grads[names[id(p)]] for p in params]);mm=torch.stack([named[names[id(p)]] for p in params])
        ww=torch.zeros_like(gg);shape=params[0].shape
        second=torch.zeros((len(params),shape[0],1) if shape[0]>=shape[1] else (len(params),1,shape[1]),device=ww.device)
        cpu=lambda z:torch.tensor(float(z),dtype=torch.float32)
        muon_step_fused(gg,ww,mm,second,cpu(mu),cpu(1),cpu(0),cpu(group['beta2']),group['ns_steps'],-1 if shape[0]>=shape[1] else -2)
        c=max(1.,shape[0]/shape[1])**.5
        for i,p in enumerate(params):
            n=names[id(p)];directions[n]=-c*ww[i]+group['weight_decay']*p.detach();next_m[n]=mm[i].clone()
    return directions,next_m
