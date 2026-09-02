#!/usr/bin/env python3
"""Read and summarize every launcher and generation record required by this audit."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T01-56-23-019f8dc2-d3cd-7731-ab6c-074f3be2c683.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


audit_input = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(f"campaign_block_equals_lock={audit_input['audit_campaign'] == lock}")
print(f"lock_digest={digest(LOCK)}")
print(
    "lock_digest_matches_record="
    f"{digest(LOCK) == audit_input['hashes']['audit_campaign_lock_sha256']}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    OUTPUT,
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required.append(usage)
for path in required:
    print(
        f"required path={path} exists={path.exists()} "
        f"symlink={path.is_symlink()} file={path.is_file()} dir={path.is_dir()}"
    )

trace_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
function_calls: list[tuple[int, str, str]] = []
agent_messages: list[tuple[int, str, str]] = []
with TRACE.open() as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        record_type = str(record.get("type"))
        trace_types[record_type] += 1
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") == "function_call":
                function_calls.append(
                    (
                        line_number,
                        str(payload.get("name")),
                        str(payload.get("arguments", "")),
                    )
                )
            if payload.get("type") == "agent_message":
                agent_messages.append(
                    (
                        line_number,
                        str(payload.get("phase")),
                        str(payload.get("message", "")),
                    )
                )

print(f"trace_lines={sum(trace_types.values())}")
print(f"trace_sha256={digest(TRACE)}")
print(f"trace_record_types={dict(sorted(trace_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"function_call_count={len(function_calls)}")
for line_number, name, arguments in function_calls:
    normalized = " ".join(arguments.split())
    if len(normalized) > 1000:
        normalized = normalized[:1000] + "...[truncated]"
    print(f"trace_call line={line_number} name={name} arguments={normalized}")
for line_number, phase, message in agent_messages:
    normalized = " ".join(message.split())
    if len(normalized) > 1000:
        normalized = normalized[:1000] + "...[truncated]"
    print(f"trace_agent_message line={line_number} phase={phase} text={normalized}")

output_bytes = OUTPUT.read_bytes()
output_text = output_bytes.decode("utf-8", errors="replace")
output_lines = output_text.splitlines()
print(f"codex_output_bytes={len(output_bytes)}")
print(f"codex_output_lines={len(output_lines)}")
print(f"codex_output_sha256={hashlib.sha256(output_bytes).hexdigest()}")
for needle in (
    "kprove",
    "#Top",
    "kompile",
    "krun",
    "Warning",
    "Error",
    "failed",
    "succeeded",
    "RESULT:",
):
    matches = [index for index, line in enumerate(output_lines, 1) if needle in line]
    print(f"codex_output_occurrences needle={needle!r} count={len(matches)} lines={matches}")
