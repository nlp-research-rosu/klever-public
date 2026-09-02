#!/usr/bin/env python3
"""Recompute the pipeline-v3 length-delimited tree digests."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat


def tree_digest(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, pathlib.Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = pathlib.Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


generation_result = json.loads(pathlib.Path("/generation-result.json").read_text())
task = json.loads(pathlib.Path("/task.json").read_text())
usage = json.loads(pathlib.Path("/generation-evidence/usage.json").read_text())

checks = [
    (
        "candidate_vs_generation_result",
        pathlib.Path("/candidate"),
        generation_result["outputs"]["workspace_sha256"],
    ),
    (
        "candidate_semantics_vs_task_manifest",
        pathlib.Path("/candidate/reference-semantics"),
        task["inputs"]["reference_semantics_sha256"],
    ),
    (
        "trusted_semantics_vs_task_manifest",
        pathlib.Path("/reference/reference-semantics"),
        task["inputs"]["reference_semantics_sha256"],
    ),
    (
        "trace_vs_usage_record",
        pathlib.Path("/generation-evidence/codex-trace"),
        usage["source_trace_sha256"],
    ),
]
for label, root, expected in checks:
    actual = tree_digest(root)
    print(label, actual, "MATCH" if actual == expected else f"MISMATCH:{expected}")
    if actual != expected:
        raise SystemExit(1)
