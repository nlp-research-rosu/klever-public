#!/usr/bin/env python3
"""Summarize candidate-authored metadata/log/trace claims without trusting them."""

from __future__ import annotations

import glob
import json
from collections import Counter
from pathlib import Path


candidate = Path("/candidate")
run_input = json.loads((candidate / "run-input.json").read_text(encoding="utf-8"))
metrics = json.loads((candidate / "metrics.json").read_text(encoding="utf-8"))
last = (candidate / "codex-last.txt").read_text(encoding="utf-8")
output = (candidate / "codex-output.log").read_text(encoding="utf-8")

print("UNTRUSTED run-input claim:")
print(json.dumps(run_input, sort_keys=True))
print("UNTRUSTED metrics claim:")
print(json.dumps(metrics, sort_keys=True))
print(f"UNTRUSTED codex-last bytes={len(last.encode())}")
print(last.rstrip())
print(f"UNTRUSTED codex-output bytes={len(output.encode())}")
for needle in ("RESULT: KPROVE_PASSED", "VALIDATED", "#Top"):
    print(f"codex-output occurrences {needle!r}: {output.count(needle)}")

trace_paths = sorted(
    Path(path)
    for path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True)
)
print(f"structured trace files={len(trace_paths)}")
for path in trace_paths:
    top = Counter()
    payload = Counter()
    commands = []
    messages = []
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            item = json.loads(line)
            top[item.get("type", "<none>")] += 1
            body = item.get("payload") or {}
            payload[body.get("type", "<none>")] += 1
            if body.get("type") in {"function_call", "custom_tool_call"}:
                commands.append((line_no, body.get("name")))
            if body.get("type") in {"message", "agent_message"}:
                text = body.get("message") or body.get("content")
                if text:
                    messages.append((line_no, str(text)))
    print(f"trace={path.relative_to(candidate)}")
    print(f"top-level event counts={dict(top)}")
    print(f"payload event counts={dict(payload)}")
    print(f"tool calls={len(commands)} last-five={commands[-5:]}")
    print(f"messages={len(messages)}")
    if messages:
        print(f"final-message-line={messages[-1][0]}")
        print(f"final-message-prefix={messages[-1][1][:800]}")
