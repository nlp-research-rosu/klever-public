#!/usr/bin/env python3
"""Bounded semantic summary after reading every required generation record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
for path in json_records:
    data = json.loads(path.read_text(encoding="utf-8"))
    print(
        f"json_record path={path} sha256={sha256(path)} "
        f"top_level_keys={sorted(data)}"
    )

for path in [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/prompt.txt"),
]:
    text = path.read_text(encoding="utf-8")
    print(
        f"text_record path={path} sha256={sha256(path)} "
        f"lines={len(text.splitlines())} bytes={len(text.encode('utf-8'))}"
    )

output_path = Path("/generation-evidence/codex-output.log")
output = output_path.read_text(encoding="utf-8")
print(
    f"codex_output sha256={sha256(output_path)} "
    f"lines={len(output.splitlines())} bytes={len(output.encode('utf-8'))}"
)
for marker in [
    "KPROVE_PASSED",
    "#Top",
    "WarnStuckClaimState",
    "verification.k",
    "spec.k",
    "kprove ",
]:
    print(f"codex_output_occurrences marker={marker!r} count={output.count(marker)}")
print(f"codex_output_final_500_chars={output[-500:]!r}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
roles: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
all_text: list[str] = []
line_count = 0
for path in trace_files:
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            line_count += 1
            record = json.loads(line)
            top_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
                if isinstance(payload.get("name"), str):
                    tool_names[payload["name"]] += 1
            all_text.extend(strings(record))

joined_text = "\n".join(all_text)
print(f"trace_files={len(trace_files)}")
print(f"trace_lines_read={line_count}")
print(f"trace_top_types={dict(sorted(top_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_roles={dict(sorted(roles.items()))}")
print(f"trace_tool_names={dict(sorted(tool_names.items()))}")
for marker in ["KPROVE_PASSED", "#Top", "WarnStuckClaimState"]:
    print(f"trace_string_occurrences marker={marker!r} count={joined_text.count(marker)}")
print("classification=untrusted_generation_claims_only")
