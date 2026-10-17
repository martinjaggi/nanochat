"""Static-WD/LR tuning grid from recorded seed0 development endpoints only."""
import pathlib,json,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=pathlib.Path('/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs')
OUT=pathlib.Path('/tmp/muon-window-audit');OUT.mkdir(exist_ok=True)
VHASH='a910b47013956661da096091511d8f562a12fdba4a7387ba368d9f7bf2708e4a'
rows=[]
for p in ROOT.glob('um-*/summary.json'):
 s=json.loads(p.read_text());c=s.get('config',{})
 if s.get('status')!='completed' or s.get('updates')!=20000 or c.get('seed')!=0 or c.get('time_budget'):continue
 if not c.get('clean') or c.get('variant') or c.get('cap_sign') or c.get('gap_scope') or c.get('fw'):continue
 if c.get('gap_geometry')!='q_scaled' or c.get('decay_mode')!='standard' or c.get('wd_schedule','fixed')!='fixed':continue
 if c.get('matrix_schedule') not in {'cooldown','cooldown_refined'} or s['validation']['validation_hash']!=VHASH:continue
 rows.append(dict(run=p.parent.name,commit=s['git_commit'],lr=c['matrix_lr'],wd=c['fixed_wd'],final=c.get('matrix_final_factor',.05),ce=s['validation']['loss']))
xs=sorted({r['lr'] for r in rows});ys=sorted({r['wd'] for r in rows});cells=collections.defaultdict(list)
for r in rows:cells[r['final'],r['wd'],r['lr']].append(r['ce'])
vmin=min(r['ce'] for r in rows);vmax=max(r['ce'] for r in rows)
fig,axs=plt.subplots(1,3,figsize=(18,6),sharey=True,layout='constrained')
cmap=plt.colormaps['viridis_r'].copy();cmap.set_bad('#eeeeee')
for ax,final in zip(axs,[.05,.01,.25]):
 z=np.full((len(ys),len(xs)),np.nan)
 for i,y in enumerate(ys):
  for j,x in enumerate(xs):
   vals=cells.get((final,y,x))
   if vals:z[i,j]=np.mean(vals)
 im=ax.imshow(z,vmin=vmin,vmax=vmax,cmap=cmap,aspect='auto')
 for i,y in enumerate(ys):
  for j,x in enumerate(xs):
   vals=cells.get((final,y,x))
   if vals:ax.text(j,i,f'{np.mean(vals):.4f}'+(f'\n(n={len(vals)})' if len(vals)>1 else ''),ha='center',va='center',fontsize=9,color='white' if z[i,j]>(vmin+vmax)/2 else 'black')
 ax.set_xticks(range(len(xs)),[f'{x:.4g}' for x in xs],rotation=45,ha='right');ax.set_yticks(range(len(ys)),[f'{y:.5g}' for y in ys]);ax.set_title(f'Matrix terminal fraction {final:g}');ax.set_xlabel('Peak CLI matrix LR')
axs[0].set_ylabel('Fixed ordinary Muon WD coefficient')
fig.colorbar(im,ax=axs,label='Development CE (nats/token), lower is better',shrink=.8)
fig.suptitle('20k updates / 655.36M tokens, seed0; paired confirmation is separate\nGrey cells untested; mean if repeats, not independent seeds',fontsize=13)
fig.savefig(OUT/'window_static_grid.png',dpi=150);plt.close(fig)
(OUT/'window_static_grid.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Static grid cells',len(cells),'recorded runs',len(rows),'minimum CE',vmin)
