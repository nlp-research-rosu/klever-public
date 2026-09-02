#!/usr/bin/env python3
"""Independent, read-only checks for the launcher provenance records."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_exact_match={audit['audit_campaign'] == lock}")
print(
    "campaign_lock_hash_match="
    f"{digest(CAMPAIGN_LOCK) == audit['hashes']['audit_campaign_lock_sha256']}"
)

for name, raw_path in audit["container_paths"].items():
    path = Path(raw_path)
    readable = path.exists() and os.access(path, os.R_OK)
    print(
        f"container_path {name}: exists={path.exists()} readable={readable} "
        f"symlink={path.is_symlink()} path={path}"
    )

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required.append(usage)
for path in required:
    print(
        f"required_record {path}: regular={path.is_file()} "
        f"readable={os.access(path, os.R_OK)} symlink={path.is_symlink()}"
    )

expected_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
for raw_path, key in expected_hashes.items():
    path = Path(raw_path)
    actual = digest(path)
    expected = audit["hashes"][key]
    print(f"hash {path}: match={actual == expected} actual={actual} expected={expected}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
declared_evidence = result["outputs"]["evidence"]
print(f"result_invocation_evidence_exact_match={declared_evidence == invocation['outputs']['evidence']}")
for relative, expected in sorted(declared_evidence.items()):
    path = Path("/generation-evidence") / relative
    actual = digest(path)
    print(f"declared_evidence {relative}: match={actual == expected}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
event_counts: collections.Counter[str] = collections.Counter()
payload_counts: collections.Counter[str] = collections.Counter()
malformed: list[tuple[str, int, str]] = []
commands: list[str] = []
custom_calls: list[str] = []
assistant_messages: list[str] = []
for path in trace_files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                event = json.loads(line)
            except Exception as error:  # pragma: no cover - audit diagnostic
                malformed.append((str(path), line_number, str(error)))
                continue
            event_counts[str(event.get("type"))] += 1
            payload = event.get("payload", {})
            payload_counts[str(payload.get("type"))] += 1
            if payload.get("type") == "function_call":
                name = payload.get("name")
                arguments = payload.get("arguments")
                commands.append(f"{name} {arguments}")
            if payload.get("type") == "custom_tool_call":
                name = payload.get("name")
                tool_input = payload.get("input")
                custom_calls.append(f"{name} {tool_input}")
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                for item in payload.get("content", []):
                    text = item.get("text")
                    if text:
                        assistant_messages.append(text)

print(f"trace_file_count={len(trace_files)}")
print(f"trace_malformed_line_count={len(malformed)}")
print(f"trace_event_counts={dict(sorted(event_counts.items()))}")
print(f"trace_payload_counts={dict(sorted(payload_counts.items()))}")
print(f"trace_function_call_count={len(commands)}")
for index, command in enumerate(commands, 1):
    normalized = command.replace("\n", "\\n")
    print(f"trace_command[{index}]={normalized}")
print(f"trace_custom_tool_call_count={len(custom_calls)}")
for index, call in enumerate(custom_calls, 1):
    normalized = call.replace("\n", "\\n")
    print(f"trace_custom_call[{index}]={normalized}")
print(f"trace_assistant_message_count={len(assistant_messages)}")
for index, message in enumerate(assistant_messages, 1):
    normalized = message.replace("\n", "\\n")
    print(f"trace_assistant[{index}]={normalized}")
