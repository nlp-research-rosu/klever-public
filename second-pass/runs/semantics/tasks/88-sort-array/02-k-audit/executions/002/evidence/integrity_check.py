#!/usr/bin/env python3
"""Independent mount, hash, record-layout, and supplied-semantics checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_manifest(root: Path) -> tuple[list[dict[str, object]], str]:
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind = "symlink"
            detail: object = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            kind = "directory"
            detail = None
        elif stat.S_ISREG(info.st_mode):
            kind = "file"
            detail = {"size": info.st_size, "sha256": sha256(path)}
        else:
            kind = f"other:{stat.S_IFMT(info.st_mode)}"
            detail = None
        rows.append({"path": rel, "kind": kind, "detail": detail})
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return rows, hashlib.sha256(encoded).hexdigest()


def compare_trees(left: Path, right: Path) -> None:
    left_rows, left_digest = tree_manifest(left)
    right_rows, right_digest = tree_manifest(right)
    print(f"trusted_semantics_independent_manifest_sha256={left_digest}")
    print(f"candidate_semantics_independent_manifest_sha256={right_digest}")
    assert left_rows == right_rows, "candidate supplied-semantics tree differs"
    assert all(row["kind"] != "symlink" for row in left_rows + right_rows)
    print(f"supplied_semantics_entries={len(left_rows)} exact_match=true symlinks=false")


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit_input["audit_campaign"] == lock
    actual_lock_hash = sha256(LOCK)
    assert actual_lock_hash == audit_input["hashes"]["audit_campaign_lock_sha256"]
    print(f"record_layout={audit_input['record_layout']}")
    print(f"semantics_mode={audit_input['semantics_mode']}")
    print(f"campaign_block_exact_match=true lock_sha256={actual_lock_hash}")

    paths = audit_input["container_paths"]
    for label, raw_path in sorted(paths.items()):
        path = Path(raw_path)
        info = path.lstat()
        assert not path.is_symlink(), f"launcher path is symlinked: {label}={path}"
        if stat.S_ISREG(info.st_mode):
            with path.open("rb") as stream:
                stream.read(1)
            kind = "file"
        elif stat.S_ISDIR(info.st_mode):
            next(path.iterdir(), None)
            kind = "directory"
        else:
            raise AssertionError(f"mistyped launcher path: {label}={path}")
        print(f"container_path {label} {kind} {path}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required.append(usage)
    for path in required:
        require_regular(path)
    print(f"required_layout_records={len(required)} all_regular_readable=true")

    direct_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    if usage.exists():
        direct_hashes[str(usage)] = "generation_usage_sha256"
    for raw_path, key in direct_hashes.items():
        actual = sha256(Path(raw_path))
        expected = audit_input["hashes"][key]
        assert actual == expected, f"hash mismatch: {raw_path}"
        print(f"recorded_hash_match {key} {actual}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    for rel, expected in sorted(generation_result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        require_regular(path)
        actual = sha256(path)
        assert actual == expected, f"generation-result evidence mismatch: {rel}"
        print(f"generation_result_hash_match {rel} {actual}")

    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files, "empty structured trace"
    trace_lines = 0
    for path in trace_files:
        require_regular(path)
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                json.loads(line)
            trace_lines += line_number
    trace_rows, trace_digest = tree_manifest(Path(paths["generation_trace"]))
    assert all(row["kind"] != "symlink" for row in trace_rows)
    print(
        f"structured_trace_files={len(trace_files)} valid_jsonl_lines={trace_lines} "
        f"independent_manifest_sha256={trace_digest} symlinks=false"
    )

    assert Path("/reference/reference-semantics").is_dir()
    compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")

    candidate_rows, candidate_digest = tree_manifest(Path("/candidate"))
    assert all(row["kind"] != "symlink" for row in candidate_rows)
    print(
        f"candidate_independent_manifest_sha256={candidate_digest} "
        f"entries={len(candidate_rows)} symlinks=false"
    )
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
