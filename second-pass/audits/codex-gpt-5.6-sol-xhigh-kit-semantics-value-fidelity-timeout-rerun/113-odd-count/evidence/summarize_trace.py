#!/usr/bin/env python3
"""Validate and summarize the untrusted structured generation trace."""

import json
from collections import Counter
from pathlib import Path


traces = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_files={len(traces)}")
for path in traces:
    top_types = Counter()
    payload_types = Counter()
    final_answers = []
    line_count = 0
    with path.open(encoding="utf-8") as source:
        for line_count, line in enumerate(source, start=1):
            record = json.loads(line)
            top_types[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
                if payload.get("phase") == "final_answer":
                    for content in payload.get("content", []):
                        if content.get("type") == "output_text":
                            final_answers.append(content.get("text", ""))
    print(f"path={path}")
    print(f"bytes={path.stat().st_size}")
    print(f"lines={line_count}")
    print(f"top_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"final_answer_count={len(final_answers)}")
    for answer in final_answers:
        print("final_answer_claim_begin")
        print(answer)
        print("final_answer_claim_end")
