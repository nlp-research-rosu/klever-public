#!/usr/bin/env python3
"""Independent, read-only validation of launcher and generation records."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat

AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(root: Path) -> tuple[list[dict[str, object]], str]:
    entries: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        mode = path.lstat().st_mode
        item: dict[str, object] = {
            "path": path.relative_to(root).as_posix(),
            "type": (
                "symlink"
                if stat.S_ISLNK(mode)
                else "file"
                if stat.S_ISREG(mode)
                else "dir"
                if stat.S_ISDIR(mode)
                else "special"
            ),
            "mode": stat.S_IMODE(mode),
        }
        if stat.S_ISREG(mode):
            item["size"] = path.lstat().st_size
            item["sha256"] = digest(path)
        elif stat.S_ISLNK(mode):
            item["target"] = os.readlink(path)
        entries.append(item)
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_object_matches_lock={audit['audit_campaign'] == lock}")
print(f"audit_campaign_lock_actual={digest(LOCK)}")
print(f"audit_campaign_lock_recorded={audit['hashes']['audit_campaign_lock_sha256']}")

required_keys = [
    "audit_campaign_lock",
    "candidate",
    "canonical",
    "generation_last",
    "generation_manifest",
    "generation_metrics",
    "generation_output",
    "generation_root",
    "generation_trace",
    "run_manifest",
    "stage1_result",
    "task_manifest",
    "translator",
    "trusted_prompt",
]
for key in required_keys:
    path = Path(audit["container_paths"][key])
    print(
        f"container_path {key}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
        f"symlink={path.is_symlink()} path={path}"
    )

file_expectations = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, field in file_expectations.items():
    actual = digest(path)
    expected = audit["hashes"][field]
    print(f"hash {path}: match={actual == expected} actual={actual} expected={expected}")

trace_root = Path("/generation-evidence/codex-trace")
trace_entries, trace_inventory_digest = inventory(trace_root)
trace_files = [e for e in trace_entries if e["type"] == "file"]
print(f"trace_inventory_entries={len(trace_entries)} files={len(trace_files)}")
print(f"reviewer_trace_inventory_sha256={trace_inventory_digest}")

result = json.loads(Path("/generation-result.json").read_text())
declared_trace = {
    k: v
    for k, v in result["outputs"]["evidence"].items()
    if k.startswith("codex-trace/")
}
actual_trace = {
    f"codex-trace/{e['path']}": e["sha256"] for e in trace_files
}
print(f"trace_manifest_exact_match={declared_trace == actual_trace}")

event_counts: collections.Counter[tuple[str, str]] = collections.Counter()
jsonl_lines = 0
jsonl_errors = 0
function_calls: collections.Counter[str] = collections.Counter()
function_outputs = 0
agent_messages = 0
for entry in trace_files:
    path = trace_root / str(entry["path"])
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            jsonl_lines += 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as error:
                jsonl_errors += 1
                print(f"trace_parse_error={path}:{line_number}:{error}")
                continue
            outer = str(obj.get("type"))
            payload = obj.get("payload")
            inner = str(payload.get("type")) if isinstance(payload, dict) else ""
            event_counts[(outer, inner)] += 1
            if outer == "response_item" and inner == "function_call":
                function_calls[str(payload.get("name"))] += 1
            elif outer == "response_item" and inner == "function_call_output":
                function_outputs += 1
            elif outer == "event_msg" and inner == "agent_message":
                agent_messages += 1
print(f"trace_jsonl_lines={jsonl_lines} parse_errors={jsonl_errors}")
print(f"trace_event_counts={dict(sorted(event_counts.items()))}")
print(f"trace_function_calls={dict(sorted(function_calls.items()))}")
print(f"trace_function_outputs={function_outputs} agent_messages={agent_messages}")

for root in (
    Path("/candidate"),
    Path("/candidate/reference-semantics"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence"),
):
    entries, reviewer_digest = inventory(root)
    bad = [e for e in entries if e["type"] in {"symlink", "special"}]
    print(
        f"inventory {root}: entries={len(entries)} reviewer_sha256={reviewer_digest} "
        f"symlink_or_special={bad}"
    )
