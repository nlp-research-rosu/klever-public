#!/usr/bin/env python3
"""Read-only integrity and structure checks for launcher-owned audit records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T08-50-49-019fae24-682c-7cc0-b9fe-08e8acabae7a.jsonl"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit_input = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equals_lock={audit_input['audit_campaign'] == lock}")
actual_lock_hash = sha256(LOCK)
recorded_lock_hash = audit_input["hashes"]["audit_campaign_lock_sha256"]
print(f"lock_hash_recorded={recorded_lock_hash}")
print(f"lock_hash_actual={actual_lock_hash}")
print(f"lock_hash_matches={actual_lock_hash == recorded_lock_hash}")

hash_targets = {
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path(
        "/generation-evidence/runtime-metrics.json"
    ),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path(
        "/generation-evidence/codex-output.log"
    ),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}

all_hashes_match = True
for field, path in hash_targets.items():
    recorded = audit_input["hashes"][field]
    actual = sha256(path)
    matches = recorded == actual
    all_hashes_match &= matches
    print(
        f"hash field={field} path={path} recorded={recorded} "
        f"actual={actual} matches={matches}"
    )
print(f"all_individual_recorded_hashes_match={all_hashes_match}")

json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for record in json_records:
    parsed = json.loads(record.read_text())
    print(
        f"json_valid path={record} top_type={type(parsed).__name__} "
        f"top_keys={','.join(sorted(parsed))}"
    )

result = json.loads(Path("/generation-result.json").read_text())
for relative_path, recorded in result["outputs"]["evidence"].items():
    mounted = Path("/generation-evidence") / relative_path
    actual = sha256(mounted)
    print(
        f"result_evidence_hash path={mounted} recorded={recorded} "
        f"actual={actual} matches={recorded == actual}"
    )

trace_top_types: collections.Counter[str] = collections.Counter()
trace_payload_types: collections.Counter[str] = collections.Counter()
trace_lines = 0
trace_session_ids: set[str] = set()
generation_commands: list[str] = []

with TRACE.open() as stream:
    for line_number, line in enumerate(stream, 1):
        event = json.loads(line)
        trace_lines = line_number
        trace_top_types[str(event.get("type"))] += 1
        payload = event.get("payload")
        if isinstance(payload, dict):
            trace_payload_types[str(payload.get("type"))] += 1
            session_id = payload.get("id") if payload.get("type") == "session_meta" else None
            if isinstance(session_id, str):
                trace_session_ids.add(session_id)

            if payload.get("type") == "function_call":
                name = payload.get("name")
                arguments = payload.get("arguments")
                if name == "exec_command" and isinstance(arguments, str):
                    try:
                        decoded = json.loads(arguments)
                    except json.JSONDecodeError:
                        decoded = {"unparsed_arguments": arguments}
                    generation_commands.append(
                        f"trace_line={line_number} name={name} arguments={decoded!r}"
                    )

print(f"trace_json_lines={trace_lines}")
print(f"trace_top_types={dict(sorted(trace_top_types.items()))}")
print(f"trace_payload_types={dict(sorted(trace_payload_types.items()))}")
print(f"trace_session_ids={sorted(trace_session_ids)}")
print(f"trace_exec_command_count={len(generation_commands)}")
Path("/audit-output/evidence/generation-command-inventory.txt").write_text(
    "\n".join(generation_commands) + ("\n" if generation_commands else "")
)

for path in [
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    data = path.read_bytes()
    text = data.decode("utf-8")
    print(
        f"text_record path={path} bytes={len(data)} "
        f"lines={len(text.splitlines())} nul_count={data.count(bytes([0]))}"
    )
