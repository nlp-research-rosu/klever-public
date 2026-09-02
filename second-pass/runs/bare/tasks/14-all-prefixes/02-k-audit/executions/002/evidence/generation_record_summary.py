#!/usr/bin/env python3
"""Complete structural pass over the untrusted legacy-selected generation records."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


trace = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
type_counts: collections.Counter[str] = collections.Counter()
payload_type_counts: collections.Counter[str] = collections.Counter()
tool_counts: collections.Counter[str] = collections.Counter()
malformed = []
final_messages = []

with trace.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            malformed.append((line_number, str(error)))
            continue
        type_counts[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_type_counts[str(payload.get("type"))] += 1
            if payload.get("type") == "custom_tool_call":
                tool_counts[str(payload.get("name"))] += 1
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                content = payload.get("content")
                if isinstance(content, list):
                    texts = [
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict) and item.get("type") == "output_text"
                    ]
                    if texts:
                        final_messages.append("\n".join(texts))

output_text = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
last_text = Path("/generation-evidence/codex-last.txt").read_text(
    encoding="utf-8", errors="replace"
)
prompt_text = Path("/generation-evidence/prompt.txt").read_text(
    encoding="utf-8", errors="replace"
)

print(f"trace_path={trace}")
print(f"trace_sha256={hashlib.sha256(trace.read_bytes()).hexdigest()}")
print(f"trace_line_count={sum(type_counts.values())}")
print(f"trace_record_types={dict(sorted(type_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_type_counts.items()))}")
print(f"trace_tool_counts={dict(sorted(tool_counts.items()))}")
print(f"trace_malformed_count={len(malformed)}")
print(f"output_line_count={len(output_text.splitlines())}")
print(f"output_top_literal_count={output_text.count('#Top')}")
print(f"output_kprove_text_count={output_text.count('kprove')}")
print(f"output_error_text_count={output_text.count('[Error]')}")
print(f"prompt_line_count={len(prompt_text.splitlines())}")
print(f"last_result_marker_present={'RESULT: KPROVE_PASSED' in last_text}")
print(f"trace_final_marker_present={any('RESULT: KPROVE_PASSED' in x for x in final_messages)}")
print("classification=untrusted_generation_claims_only")
raise SystemExit(1 if malformed else 0)
