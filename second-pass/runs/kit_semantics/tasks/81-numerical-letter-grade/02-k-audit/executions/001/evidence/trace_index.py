#!/usr/bin/env python3
"""Parse every structured trace line and summarize its untrusted event record."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")


def main() -> int:
    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    malformed: list[str] = []
    finals: list[dict] = []
    total = 0

    for path in files:
        relative = path.relative_to(TRACE_ROOT)
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    event = json.loads(line)
                except Exception as error:
                    malformed.append(f"{relative}:{line_number}: {error}")
                    continue
                event_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type"))
                    payload_types[payload_type] += 1
                    name = payload.get("name")
                    if name:
                        tool_names[str(name)] += 1
                    if payload_type in {"message", "agent_message"}:
                        role = payload.get("role")
                        content = payload.get("content")
                        text = json.dumps(content, ensure_ascii=False)
                        if role == "assistant" and (
                            "RESULT:" in text or "Implemented and formally validated" in text
                        ):
                            finals.append(
                                {
                                    "file": str(relative),
                                    "line": line_number,
                                    "role": role,
                                    "content": content,
                                }
                            )

    print(f"trace_files={len(files)}")
    for path in files:
        print(f"trace_file={path.relative_to(TRACE_ROOT)}")
    print(f"total_lines={total}")
    print(f"malformed_lines={len(malformed)}")
    for item in malformed:
        print(f"malformed={item}")
    print("event_types=" + json.dumps(event_types, sort_keys=True))
    print("payload_types=" + json.dumps(payload_types, sort_keys=True))
    print("tool_names=" + json.dumps(tool_names, sort_keys=True))
    print(f"candidate_final_claim_count={len(finals)}")
    for item in finals:
        print("candidate_final_claim=" + json.dumps(item, ensure_ascii=False, sort_keys=True))
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
