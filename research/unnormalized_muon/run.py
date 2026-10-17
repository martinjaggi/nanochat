"""Launch the native entry point with explicit, recorded settings."""
import argparse,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--config',required=True);a=p.parse_args()
 out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);cfg=json.load(open(a.config));
 assert cfg.get('heldout_block',1)>=1
 if cfg.get('gap_geometry')=='q_scaled':assert cfg.get('decay_mode')=='standard' and 'fixed_wd' in cfg and cfg['fixed_wd']>=0, 'c-inside-Q explicit nonnegative ordinary WD required'
 if cfg.get('matrix_schedule','').startswith('fw_reciprocal'):assert cfg.get('fixed_wd',0)>0 and 0<cfg.get('reciprocal_final_factor',.25)<=1
 if cfg.get('matrix_schedule')=='early_reciprocal':
  h=cfg.get('reference_updates',cfg['updates']) if cfg.get('time_budget') else cfg['updates']
  assert 40<h-round(.65*h), 'early reciprocal requires LR warmup to finish before cooldown; reference_updates overrides the horizon only in time-budget runs'
 if cfg.get('cap_sign'):assert cfg.get('clean') and not cfg.get('variant') and not cfg.get('gap_scope') and not cfg.get('fw') and not cfg.get('fresh_diagnosis') and cfg.get('gap_geometry')=='q_scaled' and cfg.get('decay_mode')=='standard'
 if cfg.get('wd_schedule'):assert not cfg.get('gap_scope'), 'changing WD domain is a separate native diagnostic'
 if cfg.get('wd_schedule')=='early_history_matched':assert cfg.get('matrix_schedule')=='early_reciprocal' and cfg.get('gap_geometry')=='q_scaled' and cfg.get('clean') and not cfg.get('variant'), 'history-matched contraction diagnostic uses clean normalized early-reciprocal Muon'
 if cfg.get('wd_schedule')=='cosine_radius':assert cfg.get('matrix_schedule')=='cooldown' and cfg.get('fixed_wd',0)>0 and not cfg.get('variant'), 'native cosine-WD control keeps original matrix LR schedule'
 if cfg.get('wd_schedule')=='fw_mixing_reciprocal':assert cfg.get('matrix_schedule')=='cooldown', 'mixing WD diagnostic keeps the baseline gradient LR schedule'
 if cfg.get('gap_scope'):assert not cfg['variant'] and not cfg.get('fw') and cfg.get('decay_mode')=='standard' and cfg.get('fixed_wd',0)>0, 'fixed-WD normalized gap arm required'
 if cfg.get('fw'):assert cfg.get('decay_mode','none')=='none', 'FW shrinkage already belongs to its constrained step'
 (out/'resolved_config.json').write_text(json.dumps(cfg,indent=2))
 store=out/'store';store.mkdir(exist_ok=True)
 for n in ['base_data_climbmix','tokenizer']:
  target=ROOT/'assets'/n;link=store/n
  if not link.exists():link.symlink_to(target,target_is_directory=True)
 env=dict(os.environ,RESEARCH_EARLY_PEAK=str(cfg.get("early_peak_multiplier",1.)),RESEARCH_MATRIX_FINAL=str(cfg.get("matrix_final_factor",.05)),NANOCHAT_CAP_SIGN=str(int(cfg.get("cap_sign",False))),RESEARCH_RECIPROCAL_FINAL=str(cfg.get("reciprocal_final_factor",.25)),RESEARCH_HELDOUT_BLOCK=str(cfg.get("heldout_block",1)),RESEARCH_BRANCH_STEPS=",".join(map(str,cfg.get("branch_steps",[]))),RESEARCH_WD_SCHEDULE=cfg.get("wd_schedule","fixed"),NANOCHAT_BASE_DIR=str(store),RESEARCH_WARMUP_UPDATES=str(cfg.get("warmup_updates",0)),RESEARCH_MUON_GEOMETRY=cfg.get("gap_geometry","legacy"),RESEARCH_GAP_PROPOSAL_BETA=str(cfg.get("gap_proposal_beta",0)),RESEARCH_GAP_RELATIVE_CAP=str(cfg.get("gap_relative_cap",0)),RESEARCH_GAP_PROBE_EVERY=str(cfg.get("gap_probe_every",1)),RESEARCH_GAP_ACCEPTANCE=cfg.get("gap_acceptance","quadratic"),RESEARCH_GAP_ETA_CAP=str(cfg.get("gap_eta_cap",1/cfg["fixed_wd"] if cfg.get("fixed_wd") else 1.)),RESEARCH_GAP_CAP_SCHEDULE=cfg.get("gap_cap_schedule","none"),RESEARCH_GAP_ARMIJO_SIGMA=str(cfg.get("gap_armijo_sigma",.1)),RESEARCH_TIME_BUDGET=str(cfg.get("time_budget",0)),RESEARCH_REFERENCE_UPDATES=str(cfg.get("reference_updates",cfg["updates"])),RESEARCH_FIXED_WD=str(cfg.get("fixed_wd","")),RESEARCH_GAP_WD=cfg.get("gap_scope",""),RESEARCH_GAP_SHAPE=cfg.get("gap_shape","uniform"),RESEARCH_GAP_L=str(cfg.get("gap_initial_L",.01)),RESEARCH_GAP_SAFE=str(int(cfg.get("gap_safe_oracle",False))),NANOCHAT_UNNORMALIZED_MUON=str(int(cfg['variant'])),RESEARCH_LOG=str(out/'metrics.jsonl'),RESEARCH_SEED=str(cfg['seed']),RESEARCH_COMMIT=os.environ['RESEARCH_COMMIT'],RESEARCH_HELDOUT=str(int(cfg.get('heldout',False))),RESEARCH_MATRIX_SCHEDULE=cfg.get('matrix_schedule','cooldown'),RESEARCH_FW=str(int(cfg.get('fw',False))),RESEARCH_FW_L=str(cfg.get('fw_L',.01)),NANOCHAT_CLEAN_MUON=str(int(cfg.get('clean',False))),RESEARCH_MUON_DECAY=cfg.get("decay_mode","none" if cfg.get("clean") else "cautious"),RESEARCH_FW_RADIUS_FACTOR=str(cfg.get("fw_radius_factor",2.)),RESEARCH_FW_ORACLE=cfg.get("fw_oracle","momentum"),RESEARCH_FW_DERIVATIVE_PROBES=str(int(cfg.get("fw_derivative_probes",False))),RESEARCH_FW_ACCEPTANCE=cfg.get("fw_acceptance","smoothness"),RESEARCH_FW_ARMIJO_C=str(cfg.get("fw_armijo_c",.01)),RESEARCH_FW_COMPILE_CANDIDATES=str(int(cfg.get("fw_compile_candidates",False))),RESEARCH_FW_GAMMA_CAP=str(cfg.get("fw_gamma_cap",1.)),RESEARCH_FW_SCHEDULE_GAMMA=str(int(cfg.get("fw_schedule_gamma",False))),RESEARCH_DUAL_DIAGNOSTICS=str(int(cfg.get('record_dual_scale',False))))
 flags=dict(depth=cfg.get('depth',8),max_seq_len=1024,device_batch_size=cfg.get("microbatch_size",32),total_batch_size=32768,
  num_iterations=cfg.get('max_updates',max(200000,cfg['updates'])) if cfg.get('time_budget') else cfg['updates'],matrix_lr=cfg['matrix_lr'],weight_decay=cfg.get('weight_decay',0. if cfg.get('clean') else .28),warmup_steps=40,
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
