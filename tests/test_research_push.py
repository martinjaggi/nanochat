import subprocess
import pytest
from research.unnormalized_muon import gap_wd_campaign as campaign


def fake_push(monkeypatch,remote,local):
    monkeypatch.setattr(campaign.subprocess,'run',lambda *a,**kw:subprocess.CompletedProcess(a[0],1))
    def output(args,**kw):return remote+' refs/heads/unnormalized-muon\n' if args[1]=='ls-remote' else local+'\n'
    monkeypatch.setattr(campaign.subprocess,'check_output',output)


def test_equivalent_concurrent_push_is_success(monkeypatch):
    fake_push(monkeypatch,'a'*40,'a'*40)
    campaign.push()


def test_different_remote_failure_remains_failure(monkeypatch):
    fake_push(monkeypatch,'b'*40,'a'*40)
    with pytest.raises(subprocess.CalledProcessError):campaign.push()
