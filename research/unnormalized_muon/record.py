"""Opt-in metrics around the unchanged native trainer; no extra gradient passes."""
import hashlib,json,math,os,pathlib,time
import torch
from nanochat.loss_eval import evaluate_bpb

class Recorder:
    def __init__(self,path):
        self.path=pathlib.Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        self.file=self.path.open('w',buffering=65536);self.started=time.perf_counter()
        self.train_seconds=0.;self.steady_seconds=0.;self.validation_seconds=0.;self.checkpoint_seconds=0.
        self.final={};self.validation_hash=None;self.exposure={};self.last_step=-1
    def emit(self,event,**kw):
        self.file.write(json.dumps(dict(event=event,**kw),allow_nan=False)+'\n')
        if event!='update' or kw.get('step',0)%25==0:self.file.flush()
    def initialize(self,model,opt,config,total_batch_size):
        self.model=model;self.opt=opt;self.config=config;self.batch=total_batch_size
        self.exposure={str(i):0. for i in range(len(opt.param_groups))}
        self.names={id(p):n for n,p in model.named_parameters()}
        initial=hashlib.sha256()
        for n,p in model.named_parameters():
            initial.update(n.encode());initial.update(p.detach().cpu().reshape(-1).view(torch.uint8).numpy().tobytes())
        self.emit('manifest',base_commit='b2bdf9890e028965ee7f2e97acc02d72b3c663ec',
            git_commit=os.environ['RESEARCH_COMMIT'],seed=int(os.environ['RESEARCH_SEED']),
            variant=os.environ.get('NANOCHAT_UNNORMALIZED_MUON','0')=='1',matrix_schedule=os.environ.get('RESEARCH_MATRIX_SCHEDULE','cooldown'),fw=os.environ.get('RESEARCH_FW')=='1',clean=os.environ.get('NANOCHAT_CLEAN_MUON')=='1',config=config,
            decay_mode=os.environ.get('RESEARCH_MUON_DECAY','native'),fixed_wd=os.environ.get('RESEARCH_FIXED_WD',''),gap_scope=os.environ.get('RESEARCH_GAP_WD',''),gap_shape=os.environ.get('RESEARCH_GAP_SHAPE','uniform'),
            decay_exposure_definition='sum eta*shape*lambda; nominal upper exposure for cautious masked decay',
            initial_parameter_hash=initial.hexdigest(),model_parameters=sum(p.numel() for p in model.parameters()),
            GPU_model=torch.cuda.get_device_name(0),GPU_count=torch.cuda.device_count(),
            total_batch_size=total_batch_size,FP8=False,precision='native BF16 compute/embeddings; native FP32 matrices',
            optimizer_groups=[dict(kind=g['kind'],lr=g['lr'],weight_decay=g['weight_decay'],
                names=[self.names[id(p)] for p in g['params']],shapes=[list(p.shape) for p in g['params']]) for g in opt.param_groups])
    def evaluate(self,model,batches,steps,token_bytes,step,label='tuning'):
        torch.cuda.synchronize();start=time.perf_counter();owner=self
        total=torch.zeros((),device='cuda');count=0;digest=hashlib.sha256()
        class Proxy:
            def get_device(self):return model.get_device()
            def __call__(self,x,y,**kw):
                nonlocal total,count
                loss=model(x,y,**kw)
                total+=loss.sum();count+=int((y>=0).sum())
                digest.update(x.cpu().numpy().tobytes());digest.update(y.cpu().numpy().tobytes())
                return loss
        bpb=evaluate_bpb(Proxy(),batches,steps,token_bytes)
        ce=float(total/count);torch.cuda.synchronize();seconds=time.perf_counter()-start
        self.validation_seconds+=seconds;h=digest.hexdigest()
        if label=='tuning':
            if self.validation_hash is not None:assert self.validation_hash==h,'validation tokens changed'
            self.validation_hash=h
        assert math.isfinite(ce) and math.isfinite(bpb)
        result=dict(step=step,label=label,loss=ce,bpb=bpb,tokens=count,validation_hash=h,seconds=seconds,
                    training_seconds=self.train_seconds,steady_training_seconds=self.steady_seconds)
        self.emit('validation',**result)
        if label=='tuning':self.final=result
        else:self.heldout=result
        return bpb
    def update(self,step,loss,dt,opt,loader_state):
        start=time.perf_counter();assert math.isfinite(loss),'nonfinite training loss'
        self.last_step=step;self.train_seconds+=dt
        if step>10:self.steady_seconds+=dt
        for i,g in enumerate(opt.param_groups):
            p=g['params'][0];shape=max(1.,p.shape[-2]/p.shape[-1])**.5 if g['kind']=='muon' else 1.
            if g['kind']=='muon' and hasattr(opt,'decay_exposure_by_parameter'):
                continue
            self.exposure[str(i)]+=g['lr']*shape*g['weight_decay']
        if hasattr(opt,'decay_exposure_by_parameter'):
            self.exposure.update({'actual_muon:'+k:v for k,v in opt.decay_exposure_by_parameter.items()})
        fields={}
        if step%25==0:
            assert all(bool(torch.isfinite(p).all()) for p in self.model.parameters()),'nonfinite parameters'
            scales=getattr(opt,'last_dual_scales',[])
            if scales:
                flat=torch.cat([x.flatten() for x in scales]);assert bool(torch.isfinite(flat).all() & (flat>=0).all())
                fields['dual_scales']=[dict(names=[self.names[id(p)] for p in g['params']],values=s.flatten().cpu().tolist(),shape_multiplier=max(1.,g['params'][0].shape[-2]/g['params'][0].shape[-1])**.5,
                    effective_directional_lrs=(s.flatten()*g['lr']*max(1.,g['params'][0].shape[-2]/g['params'][0].shape[-1])**.5).cpu().tolist())
                    for g,s in zip((g for g in opt.param_groups if g['kind']=='muon'),scales)]
                align=torch.cat([s.flatten() for s in opt.last_current_alignments])
                fields['current_gradient_alignments']=align.cpu().tolist()
                fields['negative_alignment_fraction']=float((align<0).float().mean())
                fields['scale_mean']=float(flat.mean())
                fields['scale_min']=float(flat.min());fields['scale_median']=float(flat.median());fields['scale_max']=float(flat.max())
                rank=torch.cat([torch.full_like(s.flatten(),min(g['params'][0].shape)) for g,s in zip((g for g in opt.param_groups if g['kind']=='muon'),scales)])
                fields['scale_weighted_rms']=float((torch.sum(rank*flat.square())/rank.sum()).sqrt())
                update_weight=torch.cat([torch.full_like(s.flatten(),min(g['params'][0].shape)*max(1.,g['params'][0].shape[-2]/g['params'][0].shape[-1])) for g,s in zip((g for g in opt.param_groups if g['kind']=='muon'),scales)])
                fields['scale_update_weighted_rms']=float((torch.sum(update_weight*flat.square())/update_weight.sum()).sqrt())
        self.emit('update',step=step,loss=loss,seconds=dt,training_seconds=self.train_seconds,steady_training_seconds=self.steady_seconds,
            group_lrs=[g['lr'] for g in opt.param_groups],decay_exposure=self.exposure,data_state=loader_state,**fields)
        logging=time.perf_counter()-start;self.train_seconds+=logging
        if step>10:self.steady_seconds+=logging
    def finish(self,step):
        from torch._dynamo.utils import get_compilation_metrics
        intervals=[]
        for m in get_compilation_metrics():
            a=getattr(m,'start_time_us',None);b=getattr(m,'end_time_us',None)
            if a is not None and b is not None:intervals.append((a/1e6,b/1e6))
        compile_seconds=0.;end=-float('inf')
        for a,b in sorted(intervals):compile_seconds+=max(0.,b-max(a,end));end=max(end,b)
        summary=dict(status='completed',updates=step,fresh_tokens=step*self.batch,fresh_microbatch_gradient_passes=step*self.batch//(self.config['device_batch_size']*self.config['max_seq_len']),training_seconds=self.train_seconds,
            steady_training_seconds=self.steady_seconds,steady_time_definition='native steps after first11, plus measured research logging',
            validation_seconds=self.validation_seconds,checkpoint_seconds=self.checkpoint_seconds,compile_seconds=compile_seconds,
            end_to_end_seconds=time.perf_counter()-self.started,peak_gpu_memory=torch.cuda.max_memory_allocated(),
            validation=self.final,heldout=getattr(self,'heldout',None),decay_exposure=self.exposure)
        if hasattr(self,'gap_wd'):
            summary['gap_diagnostics']=self.gap_wd.diagnostics()
            summary['gap_feasibility']=self.gap_wd.feasibility()
            summary['extra_forward_evals']=self.gap_wd.extra_forward_evals
            summary['extra_microbatch_forward_evals']=self.gap_wd.extra_microbatch_forward_evals
            summary['gap_seconds']=self.gap_wd.line_seconds
        if hasattr(self,'fw'):
            summary['fw_feasibility']=self.fw.feasibility()
            summary['extra_forward_evals']=self.fw.extra_forward_evals
            summary['extra_microbatch_forward_evals']=self.fw.extra_microbatch_forward_evals
            summary['fw_seconds']=self.fw.line_seconds
            summary['fw_diagnostics']=self.fw.diagnostics()
        (self.path.parent/'summary.json').write_text(json.dumps(summary,indent=2));self.emit('summary',**summary);self.file.close()
