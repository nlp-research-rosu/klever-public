#!/usr/bin/env python3
import collections
import json
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/26/"
    "rollout-2026-07-26T03-06-58-019f9d76-8573-7e33-a377-c0ff76387c31.jsonl"
)
RAW_LOG = Path("/generation-evidence/codex-output.log")


def main() -> None:
    top = collections.Counter()
    payload_types = collections.Counter()
    calls = []
    outputs = []
    final_messages = []
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            top[item.get("type")] += 1
            payload = item.get("payload", {})
            payload_types[(item.get("type"), payload.get("type"))] += 1
            if item.get("type") == "response_item" and payload.get("type") == "function_call":
                calls.append(
                    (
                        line_number,
                        payload.get("name"),
                        payload.get("arguments", ""),
                    )
                )
            elif (
                item.get("type") == "response_item"
                and payload.get("type") == "function_call_output"
            ):
                output = payload.get("output", "")
                outputs.append((line_number, len(output), output[-400:]))
            elif (
                item.get("type") == "event_msg"
                and payload.get("type") == "agent_message"
            ):
                final_messages.append((line_number, payload.get("message", "")))

    raw = RAW_LOG.read_bytes()
    print(f"TRACE parsed_lines={sum(top.values())} bytes={TRACE.stat().st_size}")
    print("TRACE top_level_counts", dict(sorted(top.items())))
    print(
        "TRACE payload_type_counts",
        {str(k): v for k, v in sorted(payload_types.items(), key=lambda x: str(x[0]))},
    )
    print(f"TRACE calls={len(calls)} outputs={len(outputs)} agent_messages={len(final_messages)}")
    for line_number, name, arguments in calls:
        print(f"CALL line={line_number} name={name} arguments={arguments}")
    for line_number, length, tail in outputs:
        print(f"OUTPUT line={line_number} chars={length} tail={tail!r}")
    for line_number, message in final_messages:
        print(f"AGENT_MESSAGE line={line_number} chars={len(message)} text={message!r}")
    print(
        f"RAW_LOG bytes={len(raw)} lines={raw.count(bytes([10]))} "
        f"nul_bytes={raw.count(bytes([0]))} decoded_utf8={bool(raw.decode('utf-8'))}"
    )


if __name__ == "__main__":
    main()
