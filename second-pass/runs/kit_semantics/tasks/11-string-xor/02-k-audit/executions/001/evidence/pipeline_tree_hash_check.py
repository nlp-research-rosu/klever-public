#!/usr/bin/env python3
"""Independently reproduce the pipeline-v3 tree-hash encoding."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def pipeline_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((rel, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((rel, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
task = json.loads(Path("/task.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

checks = [
    (
        "candidate_vs_invocation",
        Path("/candidate"),
        invocation["outputs"]["workspace_sha256"],
    ),
    (
        "candidate_vs_generation_result",
        Path("/candidate"),
        result["outputs"]["workspace_sha256"],
    ),
    (
        "trusted_semantics_vs_task_manifest",
        Path("/reference/reference-semantics"),
        task["inputs"]["reference_semantics_sha256"],
    ),
    (
        "candidate_semantics_vs_task_manifest",
        Path("/candidate/reference-semantics"),
        task["inputs"]["reference_semantics_sha256"],
    ),
    (
        "trusted_semantics_vs_audit_manifest_hash",
        Path("/reference/reference-semantics"),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "trace_vs_usage_source",
        Path("/generation-evidence/codex-trace"),
        usage["source_trace_sha256"],
    ),
]

failures = 0
for label, path, expected in checks:
    actual = pipeline_tree_hash(path)
    matched = actual == expected
    print(
        f"TREE_HASH {label} match={str(matched).lower()}"
        f" expected={expected} actual={actual} path={path}"
    )
    failures += int(not matched)

print(
    "LAUNCHER_AGGREGATES"
    f" candidate_tree_sha256={audit['hashes']['candidate_tree_sha256']}"
    f" candidate_reference_semantics_sha256="
    f"{audit['hashes']['candidate_reference_semantics_sha256']}"
    f" generation_codex_trace_sha256="
    f"{audit['hashes']['generation_codex_trace_sha256']}"
    " note=separate launcher encoding; equality/integrity fields checked independently"
)
print(f"RESULT failures={failures}")
raise SystemExit(1 if failures else 0)
