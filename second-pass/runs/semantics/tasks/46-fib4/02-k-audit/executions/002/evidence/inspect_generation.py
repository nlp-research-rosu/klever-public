#!/usr/bin/env python3
import collections
import hashlib
import json
from pathlib import Path


def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal={audit['audit_campaign'] == lock}")

hashes = audit["hashes"]
mounted = {
    "audit_campaign_lock_sha256": "/audit-campaign-lock.json",
    "canonical_sha256": "/reference/canonical.py",
    "trusted_prompt_sha256": "/reference/prompt.py",
    "trusted_translator_sha256": "/reference/py2mpy.py",
    "candidate_prompt_sha256": "/candidate/prompt.py",
    "candidate_translator_sha256": "/candidate/py2mpy.py",
    "run_manifest_sha256": "/run.json",
    "task_manifest_sha256": "/task.json",
    "stage1_result_sha256": "/generation-result.json",
    "stage1_invocation_sha256": "/generation-evidence/invocation.json",
    "generation_metrics_sha256": "/generation-evidence/metrics.json",
    "generation_codex_last_sha256": "/generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": "/generation-evidence/codex-output.log",
    "generation_prompt_sha256": "/generation-evidence/prompt.txt",
    "generation_usage_sha256": "/generation-evidence/usage.json",
}
for key, path in mounted.items():
    actual = sha256(path)
    expected = hashes[key]
    print(f"HASH {key} expected={expected} actual={actual} match={actual == expected}")

invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
for relative, expected in invocation["outputs"]["evidence"].items():
    path = "/generation-evidence/" + relative
    actual = sha256(path)
    print(
        f"INVOCATION_HASH {relative} expected={expected} actual={actual} "
        f"match={actual == expected}"
    )

trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T23-54-55-019f8d53-a024-7c12-a582-699955cf5142.jsonl"
)
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
parse_errors = []
last_records = collections.deque(maxlen=8)
with trace_path.open() as handle:
    for line_number, line in enumerate(handle, 1):
        try:
            record = json.loads(line)
        except Exception as error:
            parse_errors.append((line_number, str(error)))
            continue
        top_types[str(record.get("type", ""))] += 1
        payload = record.get("payload") or {}
        payload_types[str(payload.get("type", ""))] += 1
        name = payload.get("name")
        if name:
            tool_names[str(name)] += 1
        role = payload.get("role")
        if role:
            roles[str(role)] += 1
        last_records.append(
            (
                line_number,
                record.get("type"),
                payload.get("type"),
                payload.get("role"),
                payload.get("name"),
            )
        )

print(f"TRACE lines={sum(top_types.values())} parse_errors={parse_errors}")
print(f"TRACE top_types={dict(top_types)}")
print(f"TRACE payload_types={dict(payload_types)}")
print(f"TRACE tool_names={dict(tool_names)}")
print(f"TRACE roles={dict(roles)}")
print(f"TRACE last_records={list(last_records)}")

for optional in (
    "/generation-evidence/legacy-run-input.json",
    "/generation-evidence/legacy-metrics.json",
):
    value = json.loads(Path(optional).read_text())
    print(f"OPTIONAL_RECORD {optional}={json.dumps(value, sort_keys=True)}")
