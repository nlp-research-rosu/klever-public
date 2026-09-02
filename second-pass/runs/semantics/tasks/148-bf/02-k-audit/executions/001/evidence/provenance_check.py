#!/usr/bin/env python3
"""Independent integrity checks for the mounted 148-bf audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
EVIDENCE = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a directory: {path}"
    assert not path.is_symlink(), f"symlinked required directory: {path}"


def tree_records(root: Path) -> list[tuple[str, str, int, str]]:
    """Return a deterministic reviewer-defined manifest for a tree."""
    require_directory(root)
    records: list[tuple[str, str, int, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        assert not path.is_symlink(), f"symlink in tree: {path}"
        if stat.S_ISDIR(mode):
            records.append(("d", relative, 0, "-"))
        elif stat.S_ISREG(mode):
            records.append(("f", relative, path.stat().st_size, sha256(path)))
        else:
            raise AssertionError(f"unexpected tree entry type: {path}")
    return records


def manifest_digest(records: list[tuple[str, str, int, str]]) -> str:
    encoded = "".join(
        f"{kind}\t{name}\t{size}\t{digest}\n"
        for kind, name, size, digest in records
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def compare_trees(left: Path, right: Path) -> None:
    left_records = tree_records(left)
    right_records = tree_records(right)
    assert left_records == right_records, f"tree mismatch: {left} != {right}"
    print(
        "reference_semantics_reviewer_manifest_sha256="
        f"{manifest_digest(left_records)} entries={len(left_records)}"
    )


def check_recorded_hash(path: Path, expected: str, label: str) -> None:
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"{label} hash mismatch: {actual} != {expected}"
    print(f"{label}_sha256={actual}")


def main() -> None:
    require_regular(AUDIT)
    require_regular(LOCK)
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert lock == audit["audit_campaign"], "campaign lock block mismatch"
    check_recorded_hash(
        LOCK, audit["hashes"]["audit_campaign_lock_sha256"], "campaign_lock"
    )

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        EVIDENCE / "invocation.json",
        EVIDENCE / "metrics.json",
        EVIDENCE / "runtime-metrics.json",
        EVIDENCE / "usage.json",
        EVIDENCE / "codex-last.txt",
        EVIDENCE / "codex-output.log",
        EVIDENCE / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
        CANDIDATE / "prompt.py",
        CANDIDATE / "py2mpy.py",
        CANDIDATE / "solution.py",
        CANDIDATE / "solution.mpy",
        CANDIDATE / "verification.k",
        CANDIDATE / "spec.k",
        CANDIDATE / "prove.sh",
    ]
    for path in required_files:
        require_regular(path)
    for path in [
        EVIDENCE,
        EVIDENCE / "codex-trace",
        CANDIDATE,
        CANDIDATE / "reference-semantics",
        REFERENCE,
        REFERENCE / "reference-semantics",
    ]:
        require_directory(path)

    hashes = audit["hashes"]
    direct_hashes = {
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "stage1_invocation": EVIDENCE / "invocation.json",
        "generation_metrics": EVIDENCE / "metrics.json",
        "generation_runtime_metrics": EVIDENCE / "runtime-metrics.json",
        "generation_usage": EVIDENCE / "usage.json",
        "generation_codex_last": EVIDENCE / "codex-last.txt",
        "generation_codex_output": EVIDENCE / "codex-output.log",
        "generation_prompt": EVIDENCE / "prompt.txt",
        "canonical": REFERENCE / "canonical.py",
        "trusted_prompt": REFERENCE / "prompt.py",
        "trusted_translator": REFERENCE / "py2mpy.py",
        "candidate_prompt": CANDIDATE / "prompt.py",
        "candidate_translator": CANDIDATE / "py2mpy.py",
    }
    for label, path in direct_hashes.items():
        check_recorded_hash(path, hashes[f"{label}_sha256"], label)

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    compare_trees(
        CANDIDATE / "reference-semantics", REFERENCE / "reference-semantics"
    )

    task = json.loads(Path("/task.json").read_text())
    run = json.loads(Path("/run.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads((EVIDENCE / "invocation.json").read_text())
    embedded_task = dict(audit["manifest"])
    embedded_task.pop("config", None)
    assert task == embedded_task, "task manifest differs from embedded manifest"
    assert run["run_id"] == audit["run_id"]
    assert run["condition"]["name"] == audit["condition"]
    assert task["problem_id"] == audit["problem_id"]
    assert result["invocation"] == invocation["name"]
    assert result["session_id"] == invocation["session_id"]
    assert result["status"] == invocation["status"] == "SUCCEEDED"
    assert result["outputs"] == invocation["outputs"]

    for relative, expected in result["outputs"]["evidence"].items():
        check_recorded_hash(EVIDENCE / relative, expected, f"result_{relative}")

    trace_files = sorted((EVIDENCE / "codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files, "structured trace tree is empty"
    for path in trace_files:
        require_regular(path)

    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    parsed_lines = 0
    for trace_path in trace_files:
        with trace_path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                assert {"timestamp", "type", "payload"} <= record.keys(), (
                    trace_path,
                    line_number,
                )
                parsed_lines += 1
                event_types[record["type"]] += 1
                payload = record["payload"]
                if isinstance(payload, dict) and "type" in payload:
                    payload_types[str(payload["type"])] += 1
    print(f"trace_files={len(trace_files)} trace_json_lines={parsed_lines}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(
        "trace_reviewer_manifest_sha256="
        f"{manifest_digest(tree_records(EVIDENCE / 'codex-trace'))}"
    )

    candidate_records = tree_records(CANDIDATE)
    print(
        "candidate_reviewer_manifest_sha256="
        f"{manifest_digest(candidate_records)} entries={len(candidate_records)}"
    )
    print("INTEGRITY_CHECKS=PASS")


if __name__ == "__main__":
    main()
