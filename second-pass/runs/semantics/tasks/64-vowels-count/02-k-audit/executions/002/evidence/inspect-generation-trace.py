#!/usr/bin/env python3
"""Parse every generation JSONL record and summarize its structure.

This is an integrity/readability inspection only.  Candidate-generation records
are untrusted and are not used as proof authority.
"""

import collections
import hashlib
import json
import pathlib
import sys


def main() -> int:
    root = pathlib.Path("/generation-evidence/codex-trace")
    paths = sorted(root.rglob("*"))
    files = [path for path in paths if path.is_file()]
    symlinks = [path for path in paths if path.is_symlink()]
    print(f"trace_regular_files={len(files)} trace_symlinks={len(symlinks)}")
    if symlinks:
        for path in symlinks:
            print(f"SYMLINK {path} -> {path.readlink()}")
        return 2

    total_lines = 0
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    last_record = None
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        line_count = 0
        with path.open("r", encoding="utf-8") as handle:
            for line_count, line in enumerate(handle, 1):
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise TypeError(f"{path}:{line_count}: record is not an object")
                top_types[str(record.get("type", "<missing>"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
                    name = payload.get("name")
                    if name is not None:
                        tool_names[str(name)] += 1
                last_record = record
        total_lines += line_count
        print(f"FILE {path.relative_to(root)} lines={line_count} sha256={digest}")

    print(f"total_lines={total_lines}")
    print("top_types=" + json.dumps(dict(sorted(top_types.items())), sort_keys=True))
    print("payload_types=" + json.dumps(dict(sorted(payload_types.items())), sort_keys=True))
    print("tool_names=" + json.dumps(dict(sorted(tool_names.items())), sort_keys=True))
    if last_record is not None:
        print("last_record_type=" + str(last_record.get("type", "<missing>")))
        payload = last_record.get("payload")
        if isinstance(payload, dict):
            print("last_payload_type=" + str(payload.get("type", "<missing>")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
