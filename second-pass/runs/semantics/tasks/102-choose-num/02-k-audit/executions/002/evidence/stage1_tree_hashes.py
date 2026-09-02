#!/usr/bin/env python3
"""Independent manifest-style hashes for mounted provenance trees."""

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
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
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
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


with open("/audit-input.json") as stream:
    audit = json.load(stream)
with open("/generation-result.json") as stream:
    result = json.load(stream)
with open("/generation-evidence/usage.json") as stream:
    usage = json.load(stream)

checks = [
    (
        "candidate_workspace_manifest",
        Path("/candidate"),
        result["outputs"]["workspace_sha256"],
    ),
    (
        "trusted_reference_semantics_manifest",
        Path("/reference/reference-semantics"),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "candidate_reference_semantics_manifest",
        Path("/candidate/reference-semantics"),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "generation_trace_manifest",
        Path("/generation-evidence/codex-trace"),
        usage["source_trace_sha256"],
    ),
]

for label, path, expected in checks:
    actual = sha256_tree(path)
    print(label, "expected", expected, "actual", actual, "match", actual == expected)
    assert actual == expected
