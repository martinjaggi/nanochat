"""Launch the native entry point with explicit, recorded settings."""
import argparse,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--config',required=True);a=p.parse_args()
 out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);cfg=json.load(open(a.config));
 if cfg.get('fw'):assert cfg.get('decay_mode','none')=='none', 'FW shrinkage already belongs to its constrained step'
 (out/'resolved_config.json').write_text(json.dumps(cfg,indent=2))
 store=out/'store';store.mkdir(exist_ok=True)
 for n in ['base_data_climbmix','tokenizer']:
  target=ROOT/'assets'/n;link=store/n
  if not link.exists():link.symlink_to(target,target_is_directory=True)
 env=dict(os.environ,NANOCHAT_BASE_DIR=str(store),NANOCHAT_UNNORMALIZED_MUON=str(int(cfg['variant'])),RESEARCH_LOG=str(out/'metrics.jsonl'),RESEARCH_SEED=str(cfg['seed']),RESEARCH_COMMIT=os.environ['RESEARCH_COMMIT'],RESEARCH_HELDOUT=str(int(cfg.get('heldout',False))),RESEARCH_MATRIX_SCHEDULE=cfg.get('matrix_schedule','cooldown'),RESEARCH_FW=str(int(cfg.get('fw',False))),RESEARCH_FW_L=str(cfg.get('fw_L',.01)),NANOCHAT_CLEAN_MUON=str(int(cfg.get('clean',False))),RESEARCH_MUON_DECAY=cfg.get("decay_mode","none" if cfg.get("clean") else "cautious"),RESEARCH_FW_RADIUS_FACTOR=str(cfg.get("fw_radius_factor",2.)),RESEARCH_FW_ORACLE=cfg.get("fw_oracle","momentum"),RESEARCH_FW_DERIVATIVE_PROBES=str(int(cfg.get("fw_derivative_probes",False))),RESEARCH_DUAL_DIAGNOSTICS=str(int(cfg.get('record_dual_scale',False))))
 flags=dict(depth=cfg.get('depth',8),max_seq_len=1024,device_batch_size=cfg.get("microbatch_size",32),total_batch_size=32768,
  num_iterations=cfg['updates'],matrix_lr=cfg['matrix_lr'],weight_decay=cfg.get('weight_decay',0. if cfg.get('clean') else .28),warmup_steps=40,
  eval_every=max(1,cfg['updates']//4),eval_tokens=262144,core_metric_every=-1,sample_every=-1,model_tag='d8',run='dummy')
 command=[sys.executable,'-m','scripts.base_train']+[f'--{k.replace("_","-")}={v}' for k,v in flags.items()]
 (out/'command.json').write_text(json.dumps(dict(command=command,config=cfg,commit=env['RESEARCH_COMMIT']),indent=2))
 print('TRAIN COMMAND',command,flush=True);start=time.perf_counter()
 try:
  subprocess.run(command,env=env,check=True)
 except Exception as e:
  (out/'failure.json').write_text(json.dumps(dict(status='failed',reason=str(e),elapsed=time.perf_counter()-start)));raise
 summary=json.loads((out/'summary.json').read_text());summary.update(config=cfg,git_commit=env['RESEARCH_COMMIT'],process_seconds=time.perf_counter()-start)
 (out/'summary.json').write_text(json.dumps(summary,indent=2))
if __name__=='__main__':main()
