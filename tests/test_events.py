import json
from research.unnormalized_muon.events import read_events


def test_reader_preserves_selected_events_and_skips_unneeded_payload(tmp_path):
    p=tmp_path/'log.jsonl';wanted=[dict(event='manifest',seed=1),dict(event='validation',loss=3.1)]
    p.write_text(json.dumps(wanted[0])+'\n'+ '{"event": "gap_wd_update", "ignored": invalid-unparsed-payload}\n'+json.dumps(wanted[1])+'\n')
    assert read_events(p,{'manifest','validation'})==wanted
