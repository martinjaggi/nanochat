"""Finish monitoring already accepted requests; never submit new experiments."""
import datetime,fcntl,json,pathlib,subprocess,sys,time
from research.unnormalized_muon.queue import ROOT,REPO,load
from research.unnormalized_muon.work_window import paired_report,commit_if_changed
from research.unnormalized_muon.gap_wd_campaign import record,push
D=REPO/'research/unnormalized_muon'
NAMES=[f'um-window-confirm-{arm}-s{seed}' for seed in [40,41,42] for arm in ['reference','candidate']]


def heartbeat(note):
 s=load();(ROOT/'work-window-heartbeat.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),note=note,confirmation_slots_reserved=sum(not s[n]['recorded'] for n in NAMES),new_submissions_enabled=False),indent=2)+'\n')


def main():
 while True:
  with (ROOT/'confirmation-monitor.log').open('a') as log:
   proc=subprocess.Popen([sys.executable,'-u','-m','research.unnormalized_muon.queue','watch'],cwd=REPO,stdout=log,stderr=subprocess.STDOUT)
   while proc.poll() is None:
    heartbeat('monitoring six already accepted confirmations; no new experiments');time.sleep(20)
  state=load()
  if all(state[n]['recorded'] for n in NAMES):break
  heartbeat('monitor restart after cluster/read/cleanup error; six requests stay reserved');time.sleep(30)
 with (ROOT/'queue.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  completed=all((ROOT/n/'summary.json').exists() and state[n].get('status')=='completed' for n in NAMES)
  if completed:
   paired_report('window-confirm',[40,41,42])
   note='Delayed NEW paired confirmation completed and published after scheduler recovery. No new equal-time or other experiment was submitted by this monitor; equal-time work remains separate and uncompleted.'
  else:
   note='Delayed confirmation group ended with one or more failed requests; no partial seed group is reported as a completed paired comparison. Inspect per-run failure records and frozen configs before a uniquely named retry.'
  p=D/'CONFIRMATION_STATE.md'
  p.write_text('# Delayed confirmation state\n\n'+note+'\n\n'+'\n'.join(f'- `{n}`: {state[n].get("status","unknown")}; `{ROOT/n}`' for n in NAMES)+'\n')
  subprocess.run(['git','add',str(p.relative_to(REPO))],cwd=REPO,check=True);commit_if_changed('Record delayed confirmation outcome');push();record({},note)
 heartbeat(note)

if __name__=='__main__':main()
