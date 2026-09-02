#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checker."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_plain_file(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_plain_dir(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    assert path.is_dir(), f"not a directory: {path}"
    next(path.iterdir(), None)


def tree_records(root: Path) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        stat_result = path.lstat()
        if os.path.islink(path):
            kind = "symlink"
            value = os.readlink(path)
        elif path.is_dir():
            kind = "dir"
            value = ""
        elif path.is_file():
            kind = "file"
            value = sha256_file(path)
        else:
            kind = f"other:{stat_result.st_mode:o}"
            value = ""
        records.append((kind, rel, value))
    return records


def auditor_tree_digest(records: list[tuple[str, str, str]]) -> str:
    digest = hashlib.sha256()
    for kind, rel, value in records:
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def main() -> None:
    require_plain_file(AUDIT_INPUT)
    require_plain_file(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for path in required_files:
        require_plain_file(path)
    for path in required_dirs:
        require_plain_dir(path)

    hashes = audit["hashes"]
    expected_file_hashes = {
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): hashes["stage1_invocation_sha256"],
        Path("/generation-evidence/metrics.json"): hashes["generation_metrics_sha256"],
        Path("/generation-evidence/runtime-metrics.json"):
            hashes["generation_runtime_metrics_sha256"],
        Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
        Path("/generation-evidence/codex-last.txt"):
            hashes["generation_codex_last_sha256"],
        Path("/generation-evidence/codex-output.log"):
            hashes["generation_codex_output_sha256"],
        Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
        Path("/reference/canonical.py"): hashes["canonical_sha256"],
        Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
    }
    for path, expected in expected_file_hashes.items():
        require_plain_file(path)
        actual = sha256_file(path)
        assert actual == expected, f"hash mismatch: {path}: {actual} != {expected}"
        print(f"OK sha256 {actual} {path}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = generation_result["outputs"]["evidence"]
    generation_root = Path("/generation-evidence")
    for rel, expected in sorted(evidence_hashes.items()):
        path = generation_root / rel
        require_plain_file(path)
        actual = sha256_file(path)
        assert actual == expected, f"generation evidence mismatch: {rel}"
        print(f"OK generation-result sha256 {actual} {path}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert trace_files, "no structured trace JSONL"
    trace_lines = 0
    for path in trace_files:
        require_plain_file(path)
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                json.loads(line)
                trace_lines += 1
        print(f"OK trace JSONL {path} lines={line_number} sha256={sha256_file(path)}")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("OK candidate prompt is byte-identical to trusted prompt")
    print("OK candidate translator is byte-identical to trusted translator")

    candidate_records = tree_records(Path("/candidate/reference-semantics"))
    trusted_records = tree_records(Path("/reference/reference-semantics"))
    assert candidate_records == trusted_records, "supplied-semantics recursive mismatch"
    assert all(kind != "symlink" for kind, _, _ in candidate_records)
    assert all(not kind.startswith("other:") for kind, _, _ in candidate_records)
    print(
        "OK supplied-semantics trees identical "
        f"entries={len(candidate_records)} "
        f"auditor_digest={auditor_tree_digest(candidate_records)}"
    )
    print(f"OK campaign block equality and lock hash {sha256_file(LOCK)}")
    print(f"OK structured trace parsed records={trace_lines}")
    print("STAGE1_INTEGRITY_OK")


if __name__ == "__main__":
    main()
