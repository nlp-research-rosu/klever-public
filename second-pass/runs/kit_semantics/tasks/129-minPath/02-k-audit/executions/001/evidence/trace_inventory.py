#!/usr/bin/env python3
"""Parse every generation trace line and emit a bounded structural inventory."""

from __future__ import annotations

import collections
import json
from pathlib import Path


TRACE = Path("/generation-evidence/codex-trace/2026/07/31/rollout-2026-07-31T20-44-40-019fbafe-ad5e-76c3-92e9-41b262cfa0c2.jsonl")


def clipped(value: object, limit: int = 420) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "...<clipped>"


def main() -> None:
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    roles: collections.Counter[str] = collections.Counter()
    tools: collections.Counter[str] = collections.Counter()
    commands: list[tuple[int, str, object]] = []
    proof_messages: list[tuple[int, object]] = []
    invalid: list[tuple[int, str]] = []
    total_bytes = 0
    total_lines = 0

    with TRACE.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            total_lines = line_number
            total_bytes += len(line.encode("utf-8"))
            try:
                item = json.loads(line)
            except Exception as error:
                invalid.append((line_number, repr(error)))
                continue
            top_type = str(item.get("type", "<missing>"))
            top_types[top_type] += 1
            payload = item.get("payload", {})
            if isinstance(payload, dict):
                subtype = str(payload.get("type", "<missing>"))
                payload_types[f"{top_type}/{subtype}"] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
                name = payload.get("name")
                if subtype in {"function_call", "custom_tool_call"} and name:
                    tools[str(name)] += 1
                    arguments = payload.get("arguments", payload.get("input", ""))
                    commands.append((line_number, str(name), arguments))
                if subtype in {"message", "agent_message"}:
                    serialized = clipped(payload, 3000)
                    if any(key in serialized for key in (
                        "#Top", "WarnStuckClaimState", "full-domain", "PARTIAL",
                        "downstream", "unproven", "--trusted", "kprove",
                    )):
                        proof_messages.append((line_number, payload))
            else:
                payload_types[f"{top_type}/<non-dict>"] += 1

    print(f"trace={TRACE}")
    print(f"total_lines={total_lines}")
    print(f"total_bytes_read={total_bytes}")
    print(f"invalid_json_lines={len(invalid)} details={invalid}")
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"roles={dict(roles)}")
    print(f"tools={dict(tools)}")
    print(f"tool_calls={len(commands)}")
    for line_number, name, arguments in commands:
        print(f"TOOL line={line_number} name={name} args={clipped(arguments)}")
    print(f"proof_related_messages={len(proof_messages)}")
    for line_number, payload in proof_messages:
        print(f"MESSAGE line={line_number} payload={clipped(payload, 1400)}")


if __name__ == "__main__":
    main()
