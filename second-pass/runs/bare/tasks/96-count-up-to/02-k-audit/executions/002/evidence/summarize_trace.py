#!/usr/bin/env python3
"""Bounded structural inspection of the untrusted generation JSONL trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
counts: collections.Counter[str] = collections.Counter()
commands: list[str] = []
agent_messages: list[str] = []
tool_results: list[str] = []

for path in sorted(root.rglob("*.jsonl")):
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            event = json.loads(line)
            counts[event.get("type", "<missing>")] += 1
            payload = event.get("payload", {})
            if event.get("type") == "response_item":
                item_type = payload.get("type", "<missing>")
                counts[f"response_item:{item_type}"] += 1
                if item_type == "custom_tool_call":
                    name = payload.get("name", "")
                    tool_input = payload.get("input", "")
                    if name == "exec":
                        commands.append(f"custom_exec: {tool_input}")
                elif item_type == "function_call":
                    name = payload.get("name", "")
                    arguments = payload.get("arguments", "")
                    if name in {"exec_command", "apply_patch"}:
                        commands.append(f"{name}: {arguments}")
                elif item_type == "message" and payload.get("role") == "assistant":
                    text = " ".join(
                        part.get("text", "")
                        for part in payload.get("content", [])
                        if isinstance(part, dict)
                    )
                    if text:
                        agent_messages.append(text)
                elif item_type == "function_call_output":
                    output = str(payload.get("output", ""))
                    if any(
                        marker in output
                        for marker in (
                            "#Top",
                            "WarnStuckClaimState",
                            "Process exited with code",
                            "timed out",
                        )
                    ):
                        tool_results.append(output[-1200:])
            elif event.get("type") == "event_msg":
                if payload.get("type") == "agent_message":
                    agent_messages.append(str(payload.get("message", "")))

print("EVENT_COUNTS")
for key, count in sorted(counts.items()):
    print(f"{key}={count}")

print("\nRELEVANT_GENERATION_COMMANDS")
for index, command in enumerate(commands, 1):
    if any(
        marker in command
        for marker in (
            "kompile",
            "kprove",
            "krun",
            "py2mpy",
            "solution.py",
            "semantic.k",
            "verification.k",
            "spec.k",
            "prove.sh",
        )
    ):
        print(f"[{index}] {command[:4000]}")

print("\nCLAIMED_TOOL_RESULTS_BOUNDED")
for index, result in enumerate(tool_results, 1):
    print(f"[{index}] {result}")

print("\nAGENT_MESSAGES_BOUNDED")
for index, message in enumerate(agent_messages, 1):
    print(f"[{index}] {message[:1200]}")
