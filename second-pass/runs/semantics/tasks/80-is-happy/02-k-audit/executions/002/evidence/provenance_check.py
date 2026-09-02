#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink forbidden: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        assert not path.is_symlink(), f"symlink forbidden: {path}"
        if path.is_dir():
            entries[relative] = ("directory", None)
        elif path.is_file():
            entries[relative] = ("file", sha256(path))
        else:
            raise AssertionError(f"unexpected entry type: {path}")
    return entries


def manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        entries, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert audit["audit_campaign"] == lock
    assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    embedded_manifest = dict(audit["manifest"])
    assert embedded_manifest.pop("config") == audit["config"]
    assert embedded_manifest == json.loads(Path("/task.json").read_text())
    assert sha256(Path("/task.json")) == audit["hashes"]["manifest_sha256"]
    for _, mounted in audit["container_paths"].items():
        path = Path(mounted)
        assert path.exists(), f"launcher-declared mount absent: {path}"
        assert not path.is_symlink(), f"launcher-declared mount is symlink: {path}"

    required = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required.append(usage)
    trace_root = Path("/generation-evidence/codex-trace")
    assert trace_root.is_dir() and not trace_root.is_symlink()
    trace_files = sorted(trace_root.rglob("*"))
    assert trace_files, "empty structured trace"
    required.extend(path for path in trace_files if path.is_file())
    for path in required:
        require_regular(path)

    declared_file_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for filename, field in declared_file_hashes.items():
        path = Path(filename)
        if path.exists():
            actual = sha256(path)
            expected = audit["hashes"][field]
            assert actual == expected, (filename, actual, expected)
            print(f"HASH OK {actual} {filename}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    assert trusted_semantics == candidate_semantics
    print(
        "SEMANTICS TREE OK",
        len(trusted_semantics),
        manifest_digest(trusted_semantics),
    )

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in proof_artifacts:
        require_regular(Path("/candidate") / name)
    candidate_entries = tree_entries(Path("/candidate"))
    print(
        "CANDIDATE TREE LOCALLY HASHED",
        len(candidate_entries),
        manifest_digest(candidate_entries),
        "launcher_recorded_digest=",
        audit["hashes"]["candidate_tree_sha256"],
    )
    for relative, (kind, digest_value) in candidate_entries.items():
        if kind == "file":
            print(f"CANDIDATE FILE {digest_value} {relative}")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    for record in (result, invocation):
        for relative, expected in record["outputs"]["evidence"].items():
            path = Path("/generation-evidence") / relative
            require_regular(path)
            actual = sha256(path)
            assert actual == expected, (path, actual, expected)
            print(f"GENERATION HASH OK {actual} {path}")

    trace_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    total_lines = 0
    for path in sorted(p for p in trace_files if p.is_file()):
        with path.open() as stream:
            for line in stream:
                event = json.loads(line)
                total_lines += 1
                trace_counts[str(event.get("type"))] += 1
                payload = event.get("payload") or {}
                payload_counts[str(payload.get("type"))] += 1
    assert total_lines > 0
    print("TRACE JSON OK", total_lines, dict(trace_counts), dict(payload_counts))

    # Read and characterize the complete unstructured log, rather than relying
    # on the generation report's final lines.
    log_text = Path("/generation-evidence/codex-output.log").read_text(
        errors="replace"
    )
    print(
        "CODEX LOG READ OK",
        len(log_text.encode()),
        len(log_text.splitlines()),
        {
            "#Top": log_text.count("#Top"),
            "WarnStuckClaimState": log_text.count("WarnStuckClaimState"),
            "[Error]": log_text.count("[Error]"),
            "KPROVE_PASSED": log_text.count("KPROVE_PASSED"),
        },
    )
    print("ALL REQUIRED PROVENANCE CHECKS PASSED")


if __name__ == "__main__":
    main()
