#!/usr/bin/env python3
"""Reimplement pipeline-v3 tree hashing and compare mounted provenance records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def sha256_tree(root: Path) -> str:
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
                raise RuntimeError(f"linked/unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            node_stat = path.stat(follow_symlinks=False)
            digest.update(node_stat.st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def check(label: str, actual: str, expected: str, failures: list[str]) -> None:
    matches = actual == expected
    print(f"{label} actual={actual} expected={expected} match={matches}")
    if not matches:
        failures.append(label)


def main() -> int:
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    audit = json.loads(Path("/audit-input.json").read_text())
    failures: list[str] = []

    candidate_hash = sha256_tree(Path("/candidate"))
    check(
        "candidate_vs_generation_result_workspace",
        candidate_hash,
        result["outputs"]["workspace_sha256"],
        failures,
    )
    check(
        "candidate_vs_invocation_workspace",
        candidate_hash,
        invocation["outputs"]["workspace_sha256"],
        failures,
    )

    trace_hash = sha256_tree(Path("/generation-evidence/codex-trace"))
    check("trace_vs_usage_source_trace", trace_hash, usage["source_trace_sha256"], failures)

    candidate_semantics_hash = sha256_tree(Path("/candidate/reference-semantics"))
    trusted_semantics_hash = sha256_tree(Path("/reference/reference-semantics"))
    check(
        "candidate_semantics_vs_task_manifest",
        candidate_semantics_hash,
        task["inputs"]["reference_semantics_sha256"],
        failures,
    )
    check(
        "trusted_semantics_vs_task_manifest",
        trusted_semantics_hash,
        task["inputs"]["reference_semantics_sha256"],
        failures,
    )
    check(
        "trusted_semantics_vs_audit_manifest",
        trusted_semantics_hash,
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        failures,
    )
    print(
        "launcher_alternate_candidate_tree_sha256="
        f"{audit['hashes']['candidate_tree_sha256']}"
    )
    print(
        "launcher_alternate_trace_tree_sha256="
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )
    print(
        "launcher_alternate_semantics_tree_sha256="
        f"{audit['hashes']['trusted_reference_semantics_sha256']}"
    )
    print(f"FAILURE_COUNT={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
