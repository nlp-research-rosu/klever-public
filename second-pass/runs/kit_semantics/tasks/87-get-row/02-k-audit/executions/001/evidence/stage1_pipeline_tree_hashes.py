#!/usr/bin/env python3
"""Reproduce the pipeline-v3 tree digest from mounted bytes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_tree(root: Path) -> str:
    assert root.is_dir() and not root.is_symlink()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked/unsupported entry: {path}")
    digest = hashlib.sha256()
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


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    checks = [
        (
            "candidate",
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
        ),
        (
            "candidate_reference_semantics",
            Path("/candidate/reference-semantics"),
            task["inputs"]["reference_semantics_sha256"],
        ),
        (
            "trusted_reference_semantics",
            Path("/reference/reference-semantics"),
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "generation_trace",
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
        ),
    ]
    for label, root, expected in checks:
        actual = sha256_tree(root)
        print(
            f"{label}: actual={actual} expected={expected} "
            f"match={actual == expected}"
        )
        assert actual == expected
    print("ALL_PIPELINE_TREE_HASHES_MATCH")


if __name__ == "__main__":
    main()
