#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


def pipeline_sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    entries = []
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
                raise RuntimeError(f"unsupported or linked entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def audit_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    entries = []
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
                raise RuntimeError(f"unsupported or linked entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


with Path("/audit-input.json").open(encoding="utf-8") as stream:
    audit = json.load(stream)
with Path("/generation-result.json").open(encoding="utf-8") as stream:
    generation_result = json.load(stream)
with Path("/generation-evidence/usage.json").open(encoding="utf-8") as stream:
    usage = json.load(stream)

failed = False
for label, path in [
    ("candidate", Path("/candidate")),
    ("candidate_reference_semantics", Path("/candidate/reference-semantics")),
    ("trusted_reference_semantics", Path("/reference/reference-semantics")),
    ("generation_trace", Path("/generation-evidence/codex-trace")),
]:
    # This is an independent content-and-type digest, not a claim about the
    # launcher's separately named alternate digest format.
    print(f"independent_content_digest {label}: {audit_tree_digest(path)}")

pipeline_checks = [
    (
        "candidate",
        Path("/candidate"),
        generation_result["outputs"]["workspace_sha256"],
    ),
    (
        "candidate_reference_semantics",
        Path("/candidate/reference-semantics"),
        audit["manifest"]["inputs"]["reference_semantics_sha256"],
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
for label, path, expected in pipeline_checks:
    actual = pipeline_sha256_tree(path)
    match = actual == expected
    failed = failed or not match
    print(f"pipeline_digest {label}: actual={actual} expected={expected} match={match}")

raise SystemExit(1 if failed else 0)
