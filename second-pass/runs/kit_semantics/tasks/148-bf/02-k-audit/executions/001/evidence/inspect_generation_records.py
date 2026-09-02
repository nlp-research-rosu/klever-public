#!/usr/bin/env python3
"""Parse every structured-trace record and summarize untrusted generation claims."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
OUTPUT = Path("/generation-evidence/codex-output.log")


def main() -> int:
    outer = Counter()
    payload_types = Counter()
    tool_names = Counter()
    parse_errors = []
    final_messages = []
    commands = []

    for line_number, line in enumerate(TRACE.read_text().splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as err:
            parse_errors.append((line_number, str(err)))
            continue
        outer[record.get("type", "<missing>")] += 1
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            payload_type = payload.get("type", "<missing>")
            payload_types[payload_type] += 1
            if payload_type in {"function_call", "custom_tool_call"}:
                name = payload.get("name", "<missing>")
                tool_names[name] += 1
                material = payload.get("input", payload.get("arguments", ""))
                commands.append((line_number, name, str(material).replace("\n", " ")[:500]))
            if payload_type in {"agent_message", "message"}:
                text = payload.get("message")
                if isinstance(text, str) and "RESULT:" in text:
                    final_messages.append((line_number, text.replace("\n", " ")))
                content = payload.get("content", [])
                if isinstance(content, list):
                    joined = " ".join(
                        item.get("text", "")
                        for item in content
                        if isinstance(item, dict)
                    )
                    if "RESULT:" in joined:
                        final_messages.append((line_number, joined.replace("\n", " ")))

    output_text = OUTPUT.read_text(errors="replace")
    print(f"TRACE_PATH={TRACE}")
    print(f"TRACE_LINES={sum(outer.values())}")
    print(f"TRACE_PARSE_ERRORS={len(parse_errors)}")
    print(f"OUTER_TYPES={dict(sorted(outer.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
    print(f"TOOL_NAMES={dict(sorted(tool_names.items()))}")
    print(f"TOOL_CALLS={len(commands)}")
    for line_number, name, material in commands:
        print(f"TRACE_CALL line={line_number} name={name} material={material}")
    for line_number, message in final_messages:
        print(f"UNTRUSTED_FINAL line={line_number} text={message[:1000]}")
    print(f"CODEX_OUTPUT_LINES={len(output_text.splitlines())}")
    print(f"CODEX_OUTPUT_TOP_COUNT={output_text.count('#Top')}")
    print(f"CODEX_OUTPUT_STUCK_COUNT={output_text.count('WarnStuckClaimState')}")
    print(f"CODEX_OUTPUT_RESULT_COUNT={output_text.count('RESULT:')}")
    for error in parse_errors:
        print(f"PARSE_ERROR={error!r}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
