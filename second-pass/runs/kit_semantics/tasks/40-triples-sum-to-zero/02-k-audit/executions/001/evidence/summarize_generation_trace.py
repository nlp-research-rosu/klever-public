#!/usr/bin/env python3
"""Parse every structured generation trace record as untrusted evidence."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/29/"
    "rollout-2026-07-29T07-43-15-019fade6-8b81-7002-a3c6-c30d24c4d71e.jsonl"
)


def main() -> None:
    records = [json.loads(line) for line in TRACE.read_text().splitlines()]
    print(f"TRACE_RECORDS={len(records)}")
    print("TOP_TYPES=" + repr(collections.Counter(x["type"] for x in records)))
    response = [x["payload"] for x in records if x["type"] == "response_item"]
    print(
        "RESPONSE_TYPES="
        + repr(
            collections.Counter(
                (x.get("type"), x.get("role"), x.get("name")) for x in response
            )
        )
    )
    event_types = collections.Counter(
        x["payload"].get("type") for x in records if x["type"] == "event_msg"
    )
    print("EVENT_TYPES=" + repr(event_types))
    calls = [
        x
        for x in response
        if x.get("type") in {"function_call", "custom_tool_call"}
    ]
    print(f"TOOL_CALLS={len(calls)}")
    for index, call in enumerate(calls, 1):
        payload = str(call.get("arguments") or call.get("input") or "")
        first_line = payload.splitlines()[0][:180] if payload else ""
        digest = hashlib.sha256(payload.encode()).hexdigest()
        print(
            f"CALL {index:03d} name={call.get('name')} "
            f"sha256={digest} first_line={first_line!r}"
        )
    messages = [
        x
        for x in response
        if x.get("type") == "message" and x.get("role") == "assistant"
    ]
    print(f"ASSISTANT_MESSAGES={len(messages)}")
    if messages:
        final_text = "\n".join(
            piece.get("text", "")
            for piece in messages[-1].get("content", [])
            if piece.get("type") in {"output_text", "input_text"}
        )
        print("FINAL_ASSISTANT_CLAIM=" + final_text.replace("\n", "\\n"))

    output = Path("/generation-evidence/codex-output.log").read_text()
    print(f"CODEX_OUTPUT_LINES={len(output.splitlines())}")
    print(f"CODEX_OUTPUT_BYTES={len(output.encode())}")
    print(
        "CODEX_OUTPUT_RESULT_MARKERS="
        + repr(
            [
                line
                for line in output.splitlines()
                if line.startswith("RESULT:") or "RESULT: KPROVE_PASSED" in line
            ][-5:]
        )
    )


if __name__ == "__main__":
    main()
