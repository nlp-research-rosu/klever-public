#!/usr/bin/env python3
"""Independently reproduce pipeline-v3 relative-entry tree digests."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def main() -> int:
    audit = json.load(open("/audit-input.json", encoding="utf-8"))
    task = json.load(open("/task.json", encoding="utf-8"))
    result = json.load(open("/generation-result.json", encoding="utf-8"))
    usage = json.load(open("/generation-evidence/usage.json", encoding="utf-8"))
    values = {
        "candidate": tree_sha256(Path("/candidate")),
        "candidate_reference_semantics": tree_sha256(
            Path("/candidate/reference-semantics")
        ),
        "trusted_reference_semantics": tree_sha256(
            Path("/reference/reference-semantics")
        ),
        "generation_trace": tree_sha256(
            Path("/generation-evidence/codex-trace")
        ),
    }
    for key, value in values.items():
        print(f"{key}_pipeline_tree_sha256={value}")
    print(
        "candidate_matches_generation_result_workspace="
        f"{values['candidate'] == result['outputs']['workspace_sha256']}"
    )
    print(
        "candidate_semantics_matches_task_input="
        f"{values['candidate_reference_semantics'] == task['inputs']['reference_semantics_sha256']}"
    )
    print(
        "trusted_semantics_matches_task_input="
        f"{values['trusted_reference_semantics'] == task['inputs']['reference_semantics_sha256']}"
    )
    print(
        "trace_tree_matches_usage_source="
        f"{values['generation_trace'] == usage['source_trace_sha256']}"
    )
    print(
        "audit-input also records launcher snapshot digests under distinct "
        "candidate_* and generation_trace keys; recursive byte/type comparisons "
        "and per-file manifests independently check those mounted sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
