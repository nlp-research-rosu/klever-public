#!/usr/bin/env python3
"""Bounded structural inspection of the complete untrusted generation records."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path("/generation-evidence")
TRACE = next((ROOT / "codex-trace").rglob("*.jsonl"))
OUTPUT = ROOT / "codex-output.log"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


lines = TRACE.read_text(encoding="utf-8").splitlines()
records = [json.loads(line) for line in lines]
outer_types = Counter(record.get("type") for record in records)
payload_types = Counter(
    record.get("payload", {}).get("type")
    for record in records
    if isinstance(record.get("payload"), dict)
)
calls = [
    (number, record["payload"])
    for number, record in enumerate(records, 1)
    if record.get("payload", {}).get("type") == "custom_tool_call"
]
outputs = [
    (number, record["payload"])
    for number, record in enumerate(records, 1)
    if record.get("payload", {}).get("type") == "custom_tool_call_output"
]

print(f"trace={TRACE}")
print(f"trace_lines={len(lines)} sha256={digest(TRACE)}")
print(f"outer_types={dict(sorted(outer_types.items(), key=lambda item: str(item[0])))}")
print(
    f"payload_types={dict(sorted(payload_types.items(), key=lambda item: str(item[0])))}"
)
print(f"tool_calls={len(calls)} tool_outputs={len(outputs)}")
for number, payload in calls:
    arguments = payload.get("arguments") or payload.get("input") or ""
    compact = re.sub(r"\s+", " ", str(arguments)).strip()
    print(
        f"call_line={number} name={payload.get('name')} "
        f"argument_chars={len(str(arguments))} preview={compact[:300]}"
    )
for number, payload in outputs:
    rendered = json.dumps(payload.get("output", ""), ensure_ascii=False)
    exits = re.findall(r"exit(?:_code)?[=:]\\s*(-?\\d+)", rendered)
    markers = []
    for marker in ("#Top", "WarnStuckClaimState", "[Error]", "KPROVE_PASSED"):
        if marker in rendered:
            markers.append(marker)
    print(
        f"output_line={number} chars={len(rendered)} "
        f"exits={exits} markers={markers}"
    )

output_text = OUTPUT.read_text(encoding="utf-8")
print(
    f"codex_output_lines={len(output_text.splitlines())} "
    f"bytes={len(output_text.encode())} sha256={digest(OUTPUT)}"
)
for marker in (
    "#Top",
    "WarnStuckClaimState",
    "[Error]",
    "RESULT: KPROVE_PASSED",
    "semantic.k",
    "verification.k",
    "spec.k",
):
    print(f"codex_output_occurrences[{marker!r}]={output_text.count(marker)}")
