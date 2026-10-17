"""Stream selected recorder events without parsing unrelated tensor diagnostics."""
import json


def read_events(path,names):
    wanted={'"'+name+'"' for name in names};out=[]
    with path.open() as stream:
        for line in stream:
            # Recorder writes the event field first. Leave large unrequested
            # per-update arrays unparsed; still stream the immutable raw log.
            header=line.split(',',1)[0]
            if any(name in header for name in wanted):out.append(json.loads(line))
    return out
