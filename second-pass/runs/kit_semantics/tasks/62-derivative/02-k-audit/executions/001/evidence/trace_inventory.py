#!/usr/bin/env python3
"""Parse every structured generation-trace event and summarize its contents."""

from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path("/generation-evidence/codex-trace")


def main() -> int:
    files = sorted(ROOT.rglob("*"))
    files = [path for path in files if path.is_file() and not path.is_symlink()]
    print(f"FILES={len(files)}")
    top_types: collections.Counter[str] = collections.Counter()
    event_types: collections.Counter[str] = collections.Counter()
    response_types: collections.Counter[str] = collections.Counter()
    response_roles: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    total_lines = 0
    parse_errors = 0

    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"FILE {path.relative_to(ROOT)} SHA256={digest}")
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    item = json.loads(line)
                except Exception as err:
                    parse_errors += 1
                    print(f"PARSE_ERROR {path}:{line_number}: {err}")
                    continue
                item_type = str(item.get("type"))
                top_types[item_type] += 1
                payload = item.get("payload") or {}
                if item_type == "event_msg":
                    event_types[str(payload.get("type"))] += 1
                if item_type == "response_item":
                    response_types[str(payload.get("type"))] += 1
                    response_roles[str(payload.get("role"))] += 1
                    if payload.get("type") in {"function_call", "custom_tool_call"}:
                        tool_names[str(payload.get("name"))] += 1

    print(f"TOTAL_LINES={total_lines}")
    print(f"PARSE_ERRORS={parse_errors}")
    print(f"TOP_TYPES={dict(sorted(top_types.items()))}")
    print(f"EVENT_TYPES={dict(sorted(event_types.items()))}")
    print(f"RESPONSE_TYPES={dict(sorted(response_types.items()))}")
    print(f"RESPONSE_ROLES={dict(sorted(response_roles.items()))}")
    print(f"TOOL_NAMES={dict(sorted(tool_names.items()))}")
    return 0 if files and parse_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
