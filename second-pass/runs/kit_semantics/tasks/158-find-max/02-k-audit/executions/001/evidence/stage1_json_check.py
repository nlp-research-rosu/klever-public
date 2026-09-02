#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path


def read_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


audit_input = read_json(Path("/audit-input.json"))
campaign_lock = read_json(Path("/audit-campaign-lock.json"))

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(
    "campaign_block_equal="
    f"{audit_input['audit_campaign'] == campaign_lock}"
)

lock_bytes = Path("/audit-campaign-lock.json").read_bytes()
lock_hash = hashlib.sha256(lock_bytes).hexdigest()
print(f"campaign_lock_sha256={lock_hash}")
print(
    "campaign_hash_equal="
    f"{lock_hash == audit_input['hashes']['audit_campaign_lock_sha256']}"
)

json_paths = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_paths:
    read_json(path)
    print(f"valid_json {path}")

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
regular_files = [path for path in trace_files if path.is_file()]
print(f"trace_regular_files={len(regular_files)}")
event_types = Counter()
payload_types = Counter()
line_count = 0
for path in regular_files:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            event = json.loads(line)
            line_count += 1
            event_types[event.get("type", "<missing>")] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type", "<missing>")] += 1
    print(f"valid_jsonl {path} lines={line_number}")
print(f"trace_lines={line_count}")
print(f"trace_event_types={dict(sorted(event_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")

if audit_input["record_layout"] != "pipeline-v3":
    raise SystemExit("unexpected record layout")
if audit_input["semantics_mode"] != "SUPPLIED_SEMANTICS":
    raise SystemExit("unexpected semantics mode")
if audit_input["audit_campaign"] != campaign_lock:
    raise SystemExit("campaign block mismatch")
if lock_hash != audit_input["hashes"]["audit_campaign_lock_sha256"]:
    raise SystemExit("campaign lock hash mismatch")
