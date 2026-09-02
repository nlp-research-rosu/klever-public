#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_tree_hash(root: Path) -> tuple[str, list[tuple[str, str, str | None]]]:
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
                raise AssertionError(f"unsupported entry: {path}")
    output = []
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        file_hash = None
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            data = path.read_bytes()
            digest.update(data)
            file_hash = hashlib.sha256(data).hexdigest()
        output.append((relative, kind, file_hash))
    return digest.hexdigest(), output


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text(encoding="utf-8"))

trees = {
    "candidate": Path("/candidate"),
    "candidate_reference_semantics": Path("/candidate/reference-semantics"),
    "trusted_reference_semantics": Path("/reference/reference-semantics"),
    "generation_trace": Path("/generation-evidence/codex-trace"),
}

for name, root in trees.items():
    tree_hash, entries = manifest_tree_hash(root)
    print(f"TREE {name} root={root} manifest_hash={tree_hash}")
    for relative, kind, file_hash in entries:
        print(
            f"  {kind} {relative}"
            + (f" sha256={file_hash}" if file_hash is not None else "")
        )

candidate_hash, _ = manifest_tree_hash(trees["candidate"])
reference_hash, _ = manifest_tree_hash(trees["trusted_reference_semantics"])
candidate_reference_hash, _ = manifest_tree_hash(
    trees["candidate_reference_semantics"]
)
trace_hash, _ = manifest_tree_hash(trees["generation_trace"])

checks = {
    "candidate_vs_generation_result_workspace": (
        candidate_hash,
        result["outputs"]["workspace_sha256"],
    ),
    "candidate_vs_invocation_retained_workspace": (
        candidate_hash,
        invocation["retained_workspace_sha256"],
    ),
    "trusted_reference_vs_declared_manifest": (
        reference_hash,
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    "candidate_reference_vs_trusted_reference": (
        candidate_reference_hash,
        reference_hash,
    ),
    "trace_vs_usage_source_trace": (
        trace_hash,
        usage["source_trace_sha256"],
    ),
}
for name, (actual, expected) in checks.items():
    print(f"CHECK {name}: actual={actual} expected={expected} match={actual == expected}")
    if actual != expected:
        raise SystemExit(1)
