import datetime
from research.unnormalized_muon import queue as q


def test_parent_requests_are_reserved_even_without_legacy_jobs(monkeypatch):
 monkeypatch.setattr(q,'cli',lambda *args:'um-ready Running\n')
 monkeypatch.setattr(q,'training_workloads',lambda:{'um-ready':{},'um-accepted':{}})
 assert q.jobs()=={'um-ready':'Running','um-accepted':'PendingController'}


def test_pending_pod_does_not_start_gpu_runtime():
 assert q.allocation_start([{'spec':{},'status':{'startTime':'2026-10-17T10:30:00Z'}}],now=100) is None


def test_assigned_pod_uses_actual_scheduled_time():
 pod={'spec':{'nodeName':'b300-node'},'status':{'startTime':'2026-10-17T10:31:00Z','conditions':[{'type':'PodScheduled','status':'True','lastTransitionTime':'2026-10-17T10:30:59Z'}]}}
 target=datetime.datetime(2026,10,17,10,30,59,tzinfo=datetime.timezone.utc).timestamp()
 assert q.allocation_start([pod])==target


def test_assignment_without_timestamp_is_conservative():
 assert q.allocation_start([{'spec':{'nodeName':'b300-node'}}],now=100)==70


def test_allocation_clock_survives_pod_disappearance():
 assert q.allocation_start([],previous=50,now=100)==50
