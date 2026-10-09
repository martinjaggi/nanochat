"""Benchmark the real training entry point on one B300, including data and Muon."""
import argparse,json,os,pathlib,re,statistics,subprocess,sys,time

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',required=True);p.add_argument('--depth',type=int,default=24)
p.add_argument('--batch-size',type=int,default=64);p.add_argument('--steps',type=int,default=80)
a=p.parse_args();out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
assert a.steps>20 and a.batch_size>0
import torch
assert torch.cuda.device_count()==1 and 'B300' in torch.cuda.get_device_name(0),'benchmark requires exactly one scheduled B300'
results=[]
for backend,fp8 in [('sdpa',False),('fa4',False),('fa4',True)]:
    label=f'{backend}-'+('fp8' if fp8 else 'bf16')
    command=[sys.executable,'-m','scripts.base_train',f'--depth={a.depth}',f'--device-batch-size={a.batch_size}',
             f'--total-batch-size={a.batch_size*2048}',f'--num-iterations={a.steps}','--warmup-steps=8',
             '--eval-every=-1','--core-metric-every=-1','--sample-every=-1',f'--model-tag=b300-bench-{label}','--run=dummy']
    if fp8:command.append('--fp8')
    env=dict(os.environ,NANOCHAT_ATTENTION=backend,NANOCHAT_DTYPE='bfloat16')
    started=time.perf_counter();path=out/f'{label}.log'
    with path.open('w') as f:subprocess.run(command,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    text=path.read_text();steps=[]
    for match in re.finditer(r'step (\d+)/(\d+).*?loss: ([\d.]+).*?dt: ([\d.]+)ms.*?tok/sec: ([\d,]+)',text):
        step=int(match[1]);loss=float(match[3]);duration=float(match[4])/1000
        if step>10:steps.append(dict(step=step,loss=loss,seconds=duration,tokens_per_second=int(match[5].replace(',',''))))
    assert len(steps)==a.steps-11,(label,len(steps))
    assert steps[-1]['loss']<steps[0]['loss'],f'loss did not improve: {label}'
    total_tokens=len(steps)*a.batch_size*2048;total_seconds=sum(s['seconds'] for s in steps)
    result=dict(backend=backend,fp8=fp8,depth=a.depth,sequence_length=2048,batch_size=a.batch_size,
                measured_updates=len(steps),measured_tokens=total_tokens,steady_seconds=total_seconds,
                tokens_per_second_per_gpu=total_tokens/total_seconds,
                median_tokens_per_second_per_gpu=statistics.median(s['tokens_per_second'] for s in steps),
                initial_measured_loss=steps[0]['loss'],final_measured_loss=steps[-1]['loss'],
                end_to_end_seconds=time.perf_counter()-started,command=command,log_path=str(path))
    results.append(result);print(json.dumps(result),flush=True)
summary=dict(GPU_model=torch.cuda.get_device_name(0),GPU_count=1,torch_version=torch.__version__,
             results=results,method='real upstream training, data loading and Muon included; first11 compile/warmup steps omitted; evaluation/checkpoint overhead in end-to-end only')
(out/'benchmark.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
