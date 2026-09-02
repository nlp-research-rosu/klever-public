#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script does not import candidate code.  Its tree digest is a local
reimplementation of the manifest digest described by pipeline_contract:
relative path length/path, entry kind, and for files size/content.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T05-54-43-019f8e9d-05e1-74c0-8782-4ca6b7e154ff.jsonl"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_file(path: Path) -> bool:
    return stat.S_ISREG(path.lstat().st_mode)


def real_directory(path: Path) -> bool:
    return stat.S_ISDIR(path.lstat().st_mode)


def entries(root: Path) -> list[tuple[str, str, Path]]:
    assert real_directory(root), f"not a real directory: {root}"
    result: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported entry: {path}")
    return sorted(result)


def manifest_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in entries(root):
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


def compare_trees(left: Path, right: Path) -> None:
    left_entries = [(rel, kind) for rel, kind, _ in entries(left)]
    right_entries = [(rel, kind) for rel, kind, _ in entries(right)]
    assert left_entries == right_entries, "tree entry lists differ"
    for relative, kind in left_entries:
        if kind == "file":
            assert (left / relative).read_bytes() == (right / relative).read_bytes(), (
                f"file content differs: {relative}"
            )


def main() -> None:
    required = [
        AUDIT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        TRACE,
    ]
    for path in required:
        assert regular_file(path), f"missing or non-regular required file: {path}"

    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

    file_hashes = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
    }
    for name, key in file_hashes.items():
        actual = sha256_file(Path(name))
        expected = audit["hashes"][key]
        assert actual == expected, f"{name}: {actual} != {expected}"
        print(f"FILE_OK {actual} {name}")

    usage = Path("/generation-evidence/usage.json")
    assert regular_file(usage)
    assert sha256_file(usage) == audit["hashes"]["generation_usage_sha256"]

    assert Path("/reference/reference-semantics").exists()
    compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    assert (
        manifest_tree_digest(Path("/reference/reference-semantics"))
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    assert (
        manifest_tree_digest(Path("/candidate"))
        == json.loads(Path("/generation-result.json").read_text())["outputs"][
            "workspace_sha256"
        ]
    )
    trace_digest = manifest_tree_digest(Path("/generation-evidence/codex-trace"))
    usage_doc = json.loads(usage.read_text())
    assert trace_digest == usage_doc["source_trace_sha256"]

    parse_errors = 0
    lines = 0
    with TRACE.open() as stream:
        for lines, line in enumerate(stream, 1):
            try:
                parsed = json.loads(line)
                assert isinstance(parsed, dict)
            except Exception:
                parse_errors += 1
    assert lines == 573
    assert parse_errors == 0

    print(
        "TREE_OK",
        manifest_tree_digest(Path("/reference/reference-semantics")),
        "/reference/reference-semantics",
    )
    print(
        "TREE_OK",
        manifest_tree_digest(Path("/candidate/reference-semantics")),
        "/candidate/reference-semantics",
    )
    print("TREE_OK", manifest_tree_digest(Path("/candidate")), "/candidate")
    print("TREE_OK", trace_digest, "/generation-evidence/codex-trace")
    print(f"TRACE_OK lines={lines} parse_errors={parse_errors}")
    print("PROVENANCE_CHECK_PASS")


if __name__ == "__main__":
    main()
