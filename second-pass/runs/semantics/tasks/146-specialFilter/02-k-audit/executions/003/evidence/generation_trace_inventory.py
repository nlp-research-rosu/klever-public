#!/usr/bin/env python3
"""Parse every structured generation-trace record and inventory its actions."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def compact(value: object, limit: int = 1600) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def main() -> int:
    outer_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[tuple[str, str]] = collections.Counter()
    calls: dict[str, tuple[int, str, str]] = {}
    seen_call_outputs: set[str] = set()
    total = 0

    paths = sorted(TRACE_ROOT.rglob("*.jsonl"))
    print(f"trace_files={len(paths)}")
    for path in paths:
        print(f"trace_file={path}")
        with path.open() as stream:
            for line_number, raw in enumerate(stream, 1):
                total += 1
                record = json.loads(raw)
                outer = str(record.get("type"))
                payload = record.get("payload", {})
                inner = str(payload.get("type"))
                outer_counts[outer] += 1
                payload_counts[(outer, inner)] += 1

                if outer == "response_item" and inner in {
                    "function_call",
                    "custom_tool_call",
                }:
                    call_id = str(payload.get("call_id"))
                    name = str(payload.get("name"))
                    arguments = payload.get("arguments", payload.get("input", ""))
                    calls[call_id] = (line_number, name, compact(arguments))
                    print(
                        f"CALL line={line_number} id={call_id} "
                        f"name={name} args={compact(arguments)}"
                    )
                elif outer == "response_item" and inner in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    call_id = str(payload.get("call_id"))
                    seen_call_outputs.add(call_id)
                    output = payload.get("output", "")
                    print(
                        f"OUTPUT line={line_number} id={call_id} "
                        f"summary={compact(output, 900)}"
                    )
                elif outer == "event_msg" and inner in {
                    "agent_message",
                    "task_complete",
                }:
                    print(f"EVENT line={line_number} type={inner} data={compact(payload, 900)}")

    print(f"total_json_records={total}")
    print(f"outer_counts={dict(sorted(outer_counts.items()))}")
    print(
        "payload_counts="
        + repr(
            {
                f"{outer}/{inner}": count
                for (outer, inner), count in sorted(payload_counts.items())
            }
        )
    )
    print(f"calls={len(calls)} outputs={len(seen_call_outputs)}")
    print(f"calls_without_outputs={sorted(set(calls) - seen_call_outputs)}")

    keyword_counts: dict[str, int] = {}
    keywords = [
        "kprove",
        "kompile",
        "krun",
        "#Top",
        "WarnStuckClaimState",
        "[Error]",
        "RESULT:",
        "verification.k",
        "spec.k",
        "solution.mpy",
    ]
    with OUTPUT_LOG.open(errors="replace") as stream:
        for line in stream:
            for keyword in keywords:
                if keyword in line:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    print(f"codex_output_keyword_counts={keyword_counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
