#!/usr/bin/env python3
"""Bounded, readable inventory of the untrusted structured generation trace."""

from __future__ import annotations

import json
import pathlib


path = next(pathlib.Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
for number, line in enumerate(path.read_text().splitlines(), 1):
    payload = json.loads(line).get("payload") or {}
    kind = payload.get("type")
    if kind == "custom_tool_call":
        text = " ".join(str(payload.get("input", "")).split())
        print(f"{number:03d} CALL {payload.get('name')} {text[:700]}")
    elif kind == "custom_tool_call_output":
        text = " ".join(str(payload.get("output", "")).split())
        noteworthy = any(
            marker in text
            for marker in (
                "exit_code",
                "#Top",
                "Error",
                "WarnStuck",
                "<result>",
                "Success",
            )
        )
        if noteworthy:
            print(f"{number:03d} OUTPUT {text[:700]}")
    elif kind == "patch_apply_end":
        changes = payload.get("changes") or {}
        print(
            f"{number:03d} PATCH success={payload.get('success')} "
            f"files={sorted(changes)}"
        )
    elif kind in {"message", "task_complete"}:
        role = payload.get("role", "")
        content = payload.get("content") or payload.get("last_agent_message") or ""
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        text = " ".join(str(content).split())
        print(f"{number:03d} {kind.upper()} {role} {text[:700]}")
