#!/usr/bin/env python3
"""Read the complete legacy-selected-stage1 logs and summarize their claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence")
output_text = (root / "codex-output.log").read_text(encoding="utf-8")
last_text = (root / "codex-last.txt").read_text(encoding="utf-8")
prompt_text = (root / "prompt.txt").read_text(encoding="utf-8")
trace_files = sorted((root / "codex-trace").rglob("*.jsonl"))

print(f"codex_output_lines={len(output_text.splitlines())}")
print(f"codex_output_chars={len(output_text)}")
print(f"codex_output_top_count={output_text.count('#Top')}")
print(f"codex_output_kprove_mentions={output_text.count('kprove')}")
print(f"codex_last_marker={'RESULT: KPROVE_PASSED' in last_text}")
print(f"prompt_requires_supplied_semantics={'provided reference semantics' in prompt_text}")
print(f"trace_file_count={len(trace_files)}")

type_counts: collections.Counter[str] = collections.Counter()
call_counts: collections.Counter[str] = collections.Counter()
call_exit_codes: collections.Counter[str] = collections.Counter()
line_count = 0
for trace_file in trace_files:
    for raw_line in trace_file.read_text(encoding="utf-8").splitlines():
        line_count += 1
        event = json.loads(raw_line)
        type_counts[event.get("type", "<none>")] += 1
        payload = event.get("payload", {})
        if isinstance(payload, dict) and payload.get("type") == "function_call":
            call_counts[str(payload.get("name"))] += 1
        if isinstance(payload, dict) and payload.get("type") == "function_call_output":
            output = str(payload.get("output", ""))
            for marker in ("Process exited with code ", "Exit code: "):
                if marker in output:
                    suffix = output.split(marker, 1)[1].splitlines()[0].strip()
                    call_exit_codes[suffix] += 1

print(f"trace_line_count={line_count}")
print(f"trace_type_counts={dict(sorted(type_counts.items()))}")
print(f"trace_function_calls={dict(sorted(call_counts.items()))}")
print(f"trace_reported_exit_codes={dict(sorted(call_exit_codes.items()))}")
print("GENERATION_RECORD_READ=COMPLETE")
