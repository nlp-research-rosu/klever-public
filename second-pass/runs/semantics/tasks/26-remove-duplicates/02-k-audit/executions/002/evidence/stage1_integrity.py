#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
    result: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported entry: {path}")
    return sorted(result)


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplementation of the launcher's length/type/size tree digest."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def compare_trees(left: Path, right: Path) -> None:
    left_entries = [(rel, kind) for rel, kind, _ in tree_entries(left)]
    right_entries = [(rel, kind) for rel, kind, _ in tree_entries(right)]
    assert left_entries == right_entries, "tree entry/type mismatch"
    for relative, kind in left_entries:
        if kind == "file":
            lp = left / relative
            rp = right / relative
            assert lp.read_bytes() == rp.read_bytes(), f"changed file: {relative}"


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit_input["mount_reference_semantics"] is True
    assert audit_input["audit_campaign"] == lock
    assert (
        sha256_file(LOCK)
        == audit_input["hashes"]["audit_campaign_lock_sha256"]
    )
    print("campaign_lock: exact JSON match and recorded SHA-256 match")

    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    usage = GENERATION / "usage.json"
    if usage.exists():
        required_records.append(usage)
    trace_root = GENERATION / "codex-trace"
    assert trace_root.is_dir() and not trace_root.is_symlink()
    for path in required_records:
        require_regular(path)
    print("required_records:", len(required_records), "regular and readable")

    hashes = audit_input["hashes"]
    direct_hashes = {
        LOCK: hashes["audit_campaign_lock_sha256"],
        REFERENCE / "canonical.py": hashes["canonical_sha256"],
        REFERENCE / "prompt.py": hashes["trusted_prompt_sha256"],
        REFERENCE / "py2mpy.py": hashes["trusted_translator_sha256"],
        CANDIDATE / "prompt.py": hashes["candidate_prompt_sha256"],
        CANDIDATE / "py2mpy.py": hashes["candidate_translator_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        GENERATION / "invocation.json": hashes["stage1_invocation_sha256"],
        GENERATION / "metrics.json": hashes["generation_metrics_sha256"],
        GENERATION / "codex-last.txt": hashes["generation_codex_last_sha256"],
        GENERATION / "codex-output.log": hashes["generation_codex_output_sha256"],
        GENERATION / "prompt.txt": hashes["generation_prompt_sha256"],
    }
    if usage.exists():
        direct_hashes[usage] = hashes["generation_usage_sha256"]
    for path, expected in direct_hashes.items():
        actual = sha256_file(path)
        assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
        print("sha256", actual, path)

    for path in [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        usage,
    ]:
        if path.exists():
            json.loads(path.read_text())
    print("structured JSON records: parse successfully")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    usage_doc = json.loads(usage.read_text())
    trace_files = [
        path for rel, kind, path in tree_entries(trace_root)
        if kind == "file" and path.suffix == ".jsonl"
    ]
    assert trace_files, "no structured trace JSONL"
    trace_relative = trace_files[0].relative_to(GENERATION).as_posix()
    expected_trace_file_hash = result["outputs"]["evidence"][trace_relative]
    assert invocation["outputs"]["evidence"][trace_relative] == expected_trace_file_hash
    assert sha256_file(trace_files[0]) == expected_trace_file_hash
    assert (
        pipeline_tree_sha256(trace_root)
        == usage_doc["source_trace_sha256"]
    )
    trace_lines = 0
    session_ids: set[str] = set()
    task_complete = 0
    for trace_file in trace_files:
        for line_number, line in enumerate(trace_file.read_text().splitlines(), 1):
            event = json.loads(line)
            trace_lines += 1
            if event.get("type") == "session_meta":
                session_ids.add(event["payload"]["id"])
            if (
                event.get("type") == "event_msg"
                and event.get("payload", {}).get("type") == "task_complete"
            ):
                task_complete += 1
    assert session_ids == {invocation["session_id"]}
    assert task_complete == 1
    print(
        "trace:",
        len(trace_files),
        "file(s),",
        trace_lines,
        "valid JSONL events, session",
        next(iter(session_ids)),
    )

    semantics_trusted = REFERENCE / "reference-semantics"
    semantics_candidate = CANDIDATE / "reference-semantics"
    assert semantics_trusted.is_dir(), "trusted supplied semantics missing"
    compare_trees(semantics_trusted, semantics_candidate)
    semantics_digest = pipeline_tree_sha256(semantics_trusted)
    assert semantics_digest == hashes["trusted_reference_semantics_manifest_sha256"]
    assert pipeline_tree_sha256(semantics_candidate) == semantics_digest
    print("supplied_semantics_tree:", semantics_digest, "exact recursive match")

    assert (REFERENCE / "prompt.py").read_bytes() == (CANDIDATE / "prompt.py").read_bytes()
    assert (REFERENCE / "py2mpy.py").read_bytes() == (CANDIDATE / "py2mpy.py").read_bytes()
    print("candidate_prompt_and_translator: byte-identical to trusted inputs")

    candidate_digest = pipeline_tree_sha256(CANDIDATE)
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    assert candidate_digest == invocation["retained_workspace_sha256"]
    print("candidate_tree_pipeline_sha256:", candidate_digest)

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for relative in required_candidate:
        require_regular(CANDIDATE / relative)
    print("required_candidate_artifacts: present as regular files")

    print("all_stage1_integrity_checks: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"INTEGRITY_FAILURE: {error}", file=sys.stderr)
        raise
