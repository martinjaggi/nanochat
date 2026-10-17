"""Single locked queue: 1 B300/job, 6 outstanding jobs, 50 GPU-hours total."""
import argparse,csv,fcntl,json,os,pathlib,shlex,subprocess,tarfile,time
from research.unnormalized_muon.kube import Kube
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
REPO=pathlib.Path(__file__).resolve().parents[2]
HELPER='/mloscratch/homes/mljaggi/rcp-tools/rcp-runai'
BASE='b2bdf9890e028965ee7f2e97acc02d72b3c663ec'
GPU_HOUR_CAP=50
MAX_OUTSTANDING=6
FIELDS='run_id stage status git_commit config job_id GPU_model GPU_count runtime_limit charged_gpu_seconds output validation_loss bpb updates training_seconds process_seconds failure'.split()
def cli(*a):return subprocess.check_output([HELPER,*a,'--project','mlo-mljaggi'],text=True,env=dict(os.environ,SUPPRESS_DEPRECATION_MESSAGE='true'))
def training_workloads(client=None):
 owned=client is None;k=client or Kube()
 try:
  return {x['metadata']['name']:x for x in k.request('GET','/apis/run.ai/v2alpha1/namespaces/'+k.namespace+'/trainingworkloads')['items'] if x['metadata']['name'].startswith('um-')}
 finally:
  if owned:k.close()

def jobs():
 rows={}
 for l in cli('list').splitlines():
  x=l.split()
  if x and x[0].startswith('um-'):rows[x[0]]=x[1]
 for name in training_workloads():
  rows.setdefault(name,'PendingController')
 return rows
def load():
 p=ROOT/'queue.json';return json.loads(p.read_text()) if p.exists() else {}
def save(s):(ROOT/'queue.json').write_text(json.dumps(s,indent=2))
def record(**row):
 p=REPO/'research/unnormalized_muon/EXPERIMENTS.csv';exists=p.exists()
 with p.open('a',newline='') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction='ignore',lineterminator='\n')
  if not exists:w.writeheader()
  w.writerow({k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in row.items()})
def allocation_start(pods,previous=None,now=None):
 import datetime
 starts=[]
 for pod in pods:
  if not pod.get('spec',{}).get('nodeName'):continue
  values=[pod.get('status',{}).get('startTime')]+[c.get('lastTransitionTime') for c in pod.get('status',{}).get('conditions',[]) if c.get('type')=='PodScheduled' and c.get('status')=='True']
  timestamps=[datetime.datetime.fromisoformat(t.replace('Z','+00:00')).timestamp() for t in values if t]
  starts.append(min(timestamps) if timestamps else (time.time() if now is None else now)-30)
 if previous is not None:starts.append(previous)
 return min(starts) if starts else None

def delete_request(name,k,obj):
 if obj is not None:return cli('delete','job',name)
 parent=training_workloads(k).get(name)
 if parent:
  return k.request('DELETE','/apis/run.ai/v2alpha1/namespaces/'+k.namespace+'/trainingworkloads/'+name,json=dict(apiVersion='v1',kind='DeleteOptions',propagationPolicy='Foreground',preconditions=dict(uid=parent['metadata']['uid'])))

def reap():
 s=load();j=jobs();k=Kube();changed=False
 objects={o['metadata']['name']:o for o in k.request('GET','/apis/run.ai/v1/namespaces/'+k.namespace+'/runaijobs')['items']}
 pods_now=k.request('GET','/api/v1/namespaces/'+k.namespace+'/pods')['items']
 for name,v in s.items():
  if v['recorded']:continue
  status=j.get(name,'missing');obj=objects.get(name);out=ROOT/name
  if status=='missing' and time.time()-v['submitted']<120:continue
  deleted=False
  assigned=allocation_start([p for p in pods_now if p['metadata']['name'].startswith(name+'-')],v.get('allocation_start'))
  if assigned is not None:v['allocation_start']=assigned
  if assigned is not None and time.time()-assigned>v['seconds']+60 and status not in ['Succeeded','Completed','Failed']:
   delete_request(name,k,obj);status='controller_timeout';deleted=True
  elif assigned is None and time.time()-v['submitted']>3600 and status not in ['Succeeded','Completed','Failed']:
   delete_request(name,k,obj);status='pending_timeout';deleted=True
  if status not in ['Succeeded','Completed','Failed','missing','controller_timeout','pending_timeout']:continue
  if obj:(out/'scheduler-final.json').write_text(json.dumps(obj,indent=2))
  elapsed=time.time()-v['submitted']
  v['gpu_seconds']=elapsed # conservatively includes queueing, startup and cleanup delay
  summaries=list(out.glob('**/summary.json'));done=status in ['Succeeded','Completed'] and bool(summaries)
  for p in summaries:
   review_path=out/'review.json';review=json.loads(review_path.read_text()) if review_path.exists() else {}
   x=json.loads(p.read_text());record(run_id=name+(':'+p.parent.name if p.parent!=out else ''),stage=v['stage'],status='diagnostic_invalid' if review.get('valid_for_method_comparison') is False else x['status'],failure=review.get('reason',''),git_commit=v['commit'],config=x.get('config'),job_id=name,GPU_model='NVIDIA B300 SXM6 AC',GPU_count=1,runtime_limit=v['seconds'],charged_gpu_seconds=elapsed,output=str(p.parent),validation_loss=x['validation']['loss'],bpb=x['validation']['bpb'],updates=x['updates'],training_seconds=x['training_seconds'],process_seconds=x.get('process_seconds'))
  if not done:
   p=out/'run.log';reason=p.read_text()[-3000:] if p.exists() else status
   record(run_id=name,stage=v['stage'],status='failed',git_commit=v['commit'],job_id=name,GPU_count=1,runtime_limit=v['seconds'],charged_gpu_seconds=elapsed,output=str(out),failure=reason)
  if not deleted and name in jobs():delete_request(name,k,obj)
  # CLI list can cache a deleted job for a minute. Check authoritative
  # objects and pods as well; a stale list must not invalidate completed work.
  removed=False
  for _ in range(120):
   if name not in jobs():removed=True;break
   live=k.request('GET','/apis/run.ai/v1/namespaces/'+k.namespace+'/runaijobs')['items']
   pods=k.request('GET','/api/v1/namespaces/'+k.namespace+'/pods')['items']
   workloads=training_workloads(k)
   if name not in workloads and not any(o['metadata']['name']==name for o in live) and not any(o['metadata']['name'].startswith(name+'-') for o in pods):removed=True;break
   time.sleep(1)
  assert removed,'cleanup still pending'
  changed=True
  v['recorded']=True;v['status']='completed' if done else 'failed'
 k.close();save(s)
 if changed:
  from research.unnormalized_muon.publish import publish
  publish()
 print('QUEUE',jobs(),'charged/reserved GPUh',sum(v.get('gpu_seconds',v['seconds']+30) for v in s.values())/3600,flush=True)
def submit(stage,name,seconds,config=None):
 window_path=ROOT/'work-window.json'
 if window_path.exists():
  window=json.loads(window_path.read_text())
  if window.get('active'):
   expected=(float(config.get('time_budget',0)) if config and config.get('time_budget') else .04*float(config.get('updates',2000)) if config else seconds)+90
   assert time.time()+min(seconds,expected)<=window['deadline_epoch'],'requested three-hour work window has insufficient time for a new run; preserve/reap existing jobs'
 s=load();j=jobs();assert name.startswith('um-') and len(name)<=55 and name not in s and name not in j
 assert len(set(j)|{n for n,v in s.items() if not v['recorded']})<MAX_OUTSTANDING,'six-slot cap'
 assert sum(v.get('gpu_seconds',v['seconds']+30) for v in s.values())+seconds+30<=GPU_HOUR_CAP*3600,f'{GPU_HOUR_CAP} GPU-hour cap'
 dirty=subprocess.check_output(['git','status','--porcelain'],cwd=REPO,text=True).splitlines()
 assert all(x[3:] in ['research/unnormalized_muon/STATUS.md','research/unnormalized_muon/EXPERIMENTS.csv'] for x in dirty),'commit code/config first'
 out=ROOT/name;out.mkdir(exist_ok=False);commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 for label,ref in [('source',commit),('base',BASE)]:
  dst=out/label;dst.mkdir();p=out/(label+'.tar')
  with p.open('wb') as f:subprocess.run(['git','archive',ref],cwd=REPO,stdout=f,check=True)
  with tarfile.open(p) as tar:tar.extractall(dst,filter='data')
  p.unlink()
 if config:(out/'config.json').write_text(json.dumps(config,indent=2))
 command=[HELPER,'submit','--name',name,'--project','mlo-mljaggi','--image','ic-registry.epfl.ch/mlo/mlo-base:uv1','--gpu','1','--node-pools','b300','--cpu','12','--memory','96G','--existing-pvc','claimname=mlo-scratch,path=/mloscratch','--pod-running-timeout','10m','--run-as-uid','177449','--run-as-gid','83070','--backoff-limit','0','--environment',f'RESEARCH_COMMIT={commit}','--command','--','timeout','--signal=TERM','--kill-after=30s',str(seconds)+'s','bash',str(out/'source/research/unnormalized_muon/job.sh'),str(out)]
 print('EXACT COMMAND:',shlex.join(command),flush=True);print('ONE B300; limit',seconds,'seconds; output',out,flush=True)
 (out/'submission.json').write_text(json.dumps(dict(command=command,commit=commit,config=config),indent=2))
 subprocess.run(command,check=True,env=dict(os.environ,SUPPRESS_DEPRECATION_MESSAGE='true'))
 s[name]=dict(stage=stage,commit=commit,seconds=seconds,submitted=time.time(),recorded=False);save(s)
 record(run_id=name,stage=stage,status='submitted',git_commit=commit,config=config,job_id=name,GPU_count=1,runtime_limit=seconds,output=str(out))
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['submit','reap','status','watch','sweep']);p.add_argument('--name');p.add_argument('--stage',default='smoke');p.add_argument('--seconds',type=int,default=1800);p.add_argument('--prefix');a=p.parse_args()
 while True:
  with (ROOT/'queue.lock').open('w') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX)
   if a.action=='submit':
    config_path=REPO/'research/unnormalized_muon/configs'/(a.stage+'.json')
    cfg=json.loads(config_path.read_text()) if config_path.exists() else None
    submit(a.stage,a.name,a.seconds,cfg);return
   if a.action=='status':print(jobs());return
   reap()
   if a.action=='sweep':
    s=load();known={v['stage'] for v in s.values()};pending=[p for p in sorted((REPO/'research/unnormalized_muon/configs').glob('*.json')) if p.stem not in known and any(p.stem.startswith(prefix) for prefix in a.prefix.split(','))]
    while pending and len(set(jobs())|{n for n,v in load().items() if not v['recorded']})<MAX_OUTSTANDING:
     p=pending.pop(0);cfg=json.loads(p.read_text());submit(p.stem,'um-'+p.stem.replace('.','p').lower(),cfg.get('runtime_limit',1800),cfg)
   else:pending=[]
   if a.action=='reap' or (not jobs() and not pending):return
  time.sleep(20)
if __name__=='__main__':main()
