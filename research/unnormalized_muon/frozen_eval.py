"""GPU-only frozen-checkpoint evaluation; zero training/gradient updates."""
import os,time,json,argparse,pathlib,hashlib
STARTED=time.perf_counter()
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
os.environ['NANOCHAT_BASE_DIR']=str(ROOT/'assets')
import torch
import numpy as np
from nanochat.common import compute_init,compute_cleanup
from nanochat.checkpoint_manager import build_model
from nanochat.dataloader import tokenizing_distributed_data_loader_with_state_bos_bestfit
from nanochat.tokenizer import get_token_bytes
from research.unnormalized_muon.record import Recorder


class Capture:
    def __init__(self,model):self.model=model;self.enabled=False;self.sums=[];self.counts=[]
    def get_device(self):return self.model.get_device()
    def __call__(self,x,y,**kw):
        loss=self.model(x,y,**kw)
        if self.enabled:
            self.sums.append(loss.detach().view_as(y).sum(1));self.counts.append((y>=0).sum(1))
        return loss


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--config',required=True);a=p.parse_args()
    out=pathlib.Path(a.output);cfg=json.loads(pathlib.Path(a.config).read_text());assert cfg['evaluation_only']
    (out/'resolved_config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    assert cfg['large_start_batch']==64 and cfg['large_batches']==64
    assert torch.cuda.device_count()==1 and 'B300' in torch.cuda.get_device_name(0)
    _,_,_,world,device=compute_init('cuda');assert world==1
    names=cfg['model_run_ids'];assert len(names)==len(set(names))
    for name in names:
        s=json.loads((ROOT/name/'summary.json').read_text());assert s['status']=='completed' and s['updates']==20000
    first=ROOT/names[0];model,tokenizer,meta=build_model(str(first/'store/base_checkpoints/d8'),20000,device,'eval')
    assert sum(p.numel() for p in model.parameters())==125829354
    original=model;model=torch.compile(original,dynamic=False);capture=Capture(model)
    loader=tokenizing_distributed_data_loader_with_state_bos_bestfit(tokenizer,32,1024,split='val',device=device)
    prefix=[];old=[];large=[]
    for i in range(128):
        x,y,state=next(loader);assert state['epoch']==1,'validation wrapped; fresh segment is not disjoint'
        if i<8:prefix.append((x.clone(),y.clone()))
        elif 48<=i<56:old.append((x.clone(),y.clone()))
        elif 64<=i<128:large.append((x.clone(),y.clone()))
    del loader
    assert len(prefix)==8 and len(old)==8 and len(large)==64
    token_bytes=get_token_bytes(device=device);rows=[];validation_seconds=0.;load_seconds=0.;large_hash=None
    for index,name in enumerate(names):
        run=ROOT/name;s=json.loads((run/'summary.json').read_text());mp=run/'store/base_checkpoints/d8'
        assert json.loads((mp/'meta_020000.json').read_text())['model_config']==meta['model_config']
        torch.cuda.synchronize();t=time.perf_counter()
        if index:
            state=torch.load(mp/'model_020000.pt',map_location='cpu',weights_only=True,mmap=True)
            state={k.removeprefix('_orig_mod.'):v for k,v in state.items()}
            own=original.state_dict();assert set(own)==set(state)
            assert all(own[k].shape==state[k].shape and own[k].dtype==state[k].dtype for k in own)
            original.load_state_dict(state,strict=True,assign=False);del state,own
        torch.cuda.synchronize();load_seconds+=time.perf_counter()-t
        rec=Recorder(out/'evaluations'/name/'metrics.jsonl');capture.enabled=False
        rec.evaluate(capture,prefix,8,token_bytes,20000,'tuning');sanity=dict(rec.final)
        assert sanity['validation_hash']==s['validation']['validation_hash']
        assert abs(sanity['loss']-s['validation']['loss'])<1e-5,(name,'checkpoint roundtrip tuning mismatch')
        os.environ['RESEARCH_HELDOUT_BLOCK']='6'
        rec.evaluate(capture,old,8,token_bytes,20000,'heldout');old_score=dict(rec.heldout)
        assert old_score['validation_hash']==s['heldout']['validation_hash']
        assert abs(old_score['loss']-s['heldout']['loss'])<1e-5,(name,'checkpoint roundtrip heldout mismatch')
        capture.sums=[];capture.counts=[];capture.enabled=True;os.environ['RESEARCH_HELDOUT_BLOCK']='8'
        rec.evaluate(capture,large,64,token_bytes,20000,'heldout');score=dict(rec.heldout)
        assert score['tokens']==2097152
        if large_hash is None:large_hash=score['validation_hash']
        assert score['validation_hash']==large_hash
        sums=torch.cat(capture.sums).cpu().numpy();counts=torch.cat(capture.counts).cpu().numpy()
        assert abs(float(sums.astype(np.float64).sum()/counts.sum())-score['loss'])<1e-5
        np.savez_compressed(out/'evaluations'/name/'sequence_losses.npz',nats=sums,tokens=counts)
        validation_seconds+=rec.validation_seconds;rec.file.close()
        row=dict(run_id=name,seed=s['config']['seed'],arm=s['config']['early_arm'],training_commit=s['git_commit'],checkpoint=str(mp/'model_020000.pt'),original_heldout=s['heldout'],roundtrip_tuning=sanity,roundtrip_heldout=old_score,large_heldout=score)
        rows.append(row);(out/'scores.json').write_text(json.dumps(rows,indent=2)+'\n')
        print('FROZEN_SCORE',name,score['loss'],score['bpb'],flush=True)
    torch.cuda.synchronize()
    summary=dict(status='completed',evaluation_only=True,config=cfg,git_commit=os.environ['RESEARCH_COMMIT'],updates=0,fresh_tokens=0,fresh_microbatch_gradient_passes=0,training_seconds=0.,training_active_seconds=0.,validation=rows[0]['roundtrip_tuning'],heldout=None,validation_seconds=validation_seconds,checkpoint_seconds=0.,checkpoint_load_seconds=load_seconds,compile_seconds=None,end_to_end_seconds=time.perf_counter()-STARTED,process_seconds=time.perf_counter()-STARTED,peak_gpu_memory=torch.cuda.max_memory_allocated(),models_scored=len(rows),evaluation_tokens=len(rows)*80*32768,evaluation_microbatch_forwards=len(rows)*80,large_heldout_tokens=2097152,large_heldout_hash=large_hash)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');compute_cleanup()

if __name__=='__main__':main()
