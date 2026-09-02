#!/usr/bin/env python3
"""Read the complete untrusted generation trace and emit a bounded summary."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def main() -> int:
    trace_path = pathlib.Path(sys.argv[1])
    outer_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    relevant_calls: list[tuple[str, str, str]] = []
    malformed: list[tuple[int, str]] = []

    with trace_path.open("r", encoding="utf-8") as trace:
        for line_number, line in enumerate(trace, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                malformed.append((line_number, str(error)))
                continue
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            name = payload.get("name")
            if name:
                tool_names[str(name)] += 1
            call_text = str(payload.get("input") or payload.get("arguments") or "")
            if any(token in call_text for token in ("kompile", "kprove", "krun")):
                compact = " ".join(call_text.split())
                relevant_calls.append(
                    (str(record.get("timestamp")), str(name or payload_type), compact[:800])
                )

    print(f"trace={trace_path}")
    print(f"parsed_lines={sum(outer_types.values())}")
    print(f"malformed_lines={len(malformed)}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"tool_names={dict(sorted(tool_names.items()))}")
    print(f"relevant_build_or_proof_calls={len(relevant_calls)}")
    for timestamp, name, call in relevant_calls[-30:]:
        print(f"CALL {timestamp} {name}: {call}")
    for line_number, error in malformed:
        print(f"MALFORMED line={line_number}: {error}")
    return 1 if malformed else 0


if __name__ == "__main__":
    raise SystemExit(main())
