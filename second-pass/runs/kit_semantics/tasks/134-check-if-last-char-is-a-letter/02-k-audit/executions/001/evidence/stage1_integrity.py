#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dirnames + filenames):
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = os.lstat(path).st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = ("other", oct(mode))
    return result


def sha256_tree(root: Path) -> str:
    """Launcher-compatible digest over regular files and directories."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def raw_tree_digest(root: Path) -> str:
    """Audit-mount digest: relative path, short kind tag, and raw file bytes."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "d", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "f", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "f":
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"audit_input_type=regular:{AUDIT.is_file()} symlink:{AUDIT.is_symlink()}")
    print(f"campaign_lock_type=regular:{LOCK.is_file()} symlink:{LOCK.is_symlink()}")
    actual_lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256 expected={expected_lock_hash} actual={actual_lock_hash}")
    if actual_lock_hash != expected_lock_hash:
        failures.append("campaign lock hash mismatch")
    campaign_equal = audit["audit_campaign"] == lock
    print(f"campaign_json_matches={campaign_equal}")
    if not campaign_equal:
        failures.append("campaign JSON differs from audit-input")

    file_hash_checks = {
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
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for raw_path, key in file_hash_checks.items():
        path = Path(raw_path)
        if not path.is_file() or path.is_symlink():
            print(f"FILE_INVALID {raw_path} exists={path.exists()} symlink={path.is_symlink()}")
            failures.append(f"missing, mistyped, or symlinked required file {raw_path}")
            continue
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        print(f"sha256 {raw_path} expected={expected} actual={actual} match={actual == expected}")
        if actual != expected:
            failures.append(f"hash mismatch {raw_path}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    trace_bad = [
        str(path)
        for path in trace_root.rglob("*")
        if path.is_symlink() or (not path.is_file() and not path.is_dir())
    ]
    print(f"trace_file_count={len(trace_files)} trace_bad_entries={trace_bad}")
    if not trace_root.is_dir() or trace_root.is_symlink() or not trace_files or trace_bad:
        failures.append("structured trace missing, mistyped, empty, or symlinked")
    for path in trace_files:
        print(f"trace_file_sha256 {path} {sha256_file(path)}")

    launcher_tree_records = {
        "/candidate": "candidate_tree_sha256",
        "/candidate/reference-semantics": "candidate_reference_semantics_sha256",
        "/reference/reference-semantics": "trusted_reference_semantics_sha256",
        "/generation-evidence/codex-trace": "generation_codex_trace_sha256",
    }
    for raw_path, key in launcher_tree_records.items():
        path = Path(raw_path)
        expected = audit["hashes"][key]
        print(
            f"launcher_recorded_tree_sha256 {raw_path} recorded={expected} "
            "(launcher digest scheme is distinct from the pipeline manifest digest)"
        )

    generation_result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    pipeline_tree_checks = [
        (
            Path("/candidate"),
            generation_result["outputs"]["workspace_sha256"],
            "generation-result workspace",
        ),
        (
            Path("/candidate/reference-semantics"),
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
            "reference-semantics manifest",
        ),
        (
            Path("/reference/reference-semantics"),
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
            "trusted reference-semantics manifest",
        ),
        (
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
            "usage source trace",
        ),
    ]
    for path, expected, label in pipeline_tree_checks:
        actual = sha256_tree(path)
        print(
            f"pipeline_tree_sha256 {label} {path} expected={expected} "
            f"actual={actual} match={actual == expected}"
        )
        if actual != expected:
            failures.append(f"pipeline tree hash mismatch {label} {path}")

    trusted = inventory(Path("/reference/reference-semantics"))
    candidate = inventory(Path("/candidate/reference-semantics"))
    all_names = sorted(set(trusted) | set(candidate))
    semantics_diffs = [
        (name, trusted.get(name), candidate.get(name))
        for name in all_names
        if trusted.get(name) != candidate.get(name)
    ]
    trusted_bad = [name for name, value in trusted.items() if value[0] not in {"directory", "file"}]
    candidate_bad = [name for name, value in candidate.items() if value[0] not in {"directory", "file"}]
    print(
        "semantics_inventory "
        f"trusted_entries={len(trusted)} candidate_entries={len(candidate)} "
        f"diff_count={len(semantics_diffs)} "
        f"trusted_bad={trusted_bad} candidate_bad={candidate_bad}"
    )
    for diff in semantics_diffs:
        print(f"SEMANTICS_DIFF {diff!r}")
    if semantics_diffs or trusted_bad or candidate_bad:
        failures.append("candidate supplied-semantics tree differs from trusted tree")

    byte_pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]
    for left, right in byte_pairs:
        same = left.read_bytes() == right.read_bytes()
        print(f"byte_identity {left} {right} match={same}")
        if not same:
            failures.append(f"byte mismatch {left} vs {right}")

    declared = audit["container_paths"]
    for key, raw_path in sorted(declared.items()):
        path = Path(raw_path)
        valid = path.exists() and not path.is_symlink()
        print(
            f"declared_mount {key}={raw_path} "
            f"exists={path.exists()} symlink={path.is_symlink()} valid={valid}"
        )
        if not valid:
            failures.append(f"launcher-declared mount invalid: {key}={raw_path}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
