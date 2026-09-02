#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_records(root: Path) -> dict[str, tuple[str, str | None]]:
    records: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        names = sorted(dirs + files)
        for name in names:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            path_kind = kind(path)
            payload = sha256(path) if path_kind == "file" else None
            if path_kind == "symlink":
                payload = os.readlink(path)
            records[rel] = (path_kind, payload)
        dirs[:] = [name for name in dirs if not (base_path / name).is_symlink()]
    return records


def digest_records(records: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def check_regular(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing: {path}")
        return
    if kind(path) != "file":
        failures.append(f"not a regular file: {path} ({kind(path)})")
        return
    try:
        with path.open("rb") as handle:
            handle.read(1)
    except OSError as err:
        failures.append(f"unreadable: {path}: {err}")


def check_hash(
    label: str,
    path: Path,
    expected: str,
    failures: list[str],
) -> None:
    actual = sha256(path)
    outcome = "MATCH" if actual == expected else "MISMATCH"
    print(f"HASH {label}: {outcome} actual={actual} expected={expected}")
    if outcome != "MATCH":
        failures.append(f"hash mismatch: {label} ({path})")


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("record_layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("semantics_mode is not SUPPLIED_SEMANTICS")

    if lock == audit.get("audit_campaign"):
        print("CAMPAIGN BLOCK: MATCH")
    else:
        print("CAMPAIGN BLOCK: MISMATCH")
        failures.append("campaign lock JSON differs from audit_campaign block")

    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    check_hash("audit_campaign_lock", LOCK, expected_lock_hash, failures)

    mounts = audit["container_paths"]
    for label, raw_path in sorted(mounts.items()):
        path = Path(raw_path)
        if not path.exists():
            failures.append(f"declared mount missing: {label}={path}")
            print(f"MOUNT {label}: MISSING {path}")
        else:
            print(f"MOUNT {label}: {kind(path)} {path}")
            if path.is_symlink():
                failures.append(f"declared mount is symlink: {label}={path}")

    required = [
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
    ]
    for path in required:
        check_regular(path, failures)

    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        failures.append("structured trace root missing, mistyped, or symlinked")
    trace_records = tree_records(trace_root) if trace_root.is_dir() else {}
    trace_files = [
        rel for rel, (entry_kind, _) in trace_records.items() if entry_kind == "file"
    ]
    trace_bad = [
        rel
        for rel, (entry_kind, _) in trace_records.items()
        if entry_kind not in {"file", "dir"}
    ]
    print(f"TRACE regular_files={len(trace_files)} nonregular_entries={trace_bad}")
    if not trace_files:
        failures.append("structured trace contains no regular files")
    if trace_bad:
        failures.append("structured trace contains non-file/non-directory entries")

    hashes = audit["hashes"]
    direct_hashes = {
        "canonical": (Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        "candidate_prompt": (
            Path("/candidate/prompt.py"),
            hashes["candidate_prompt_sha256"],
        ),
        "trusted_prompt": (
            Path("/reference/prompt.py"),
            hashes["trusted_prompt_sha256"],
        ),
        "candidate_translator": (
            Path("/candidate/py2mpy.py"),
            hashes["candidate_translator_sha256"],
        ),
        "trusted_translator": (
            Path("/reference/py2mpy.py"),
            hashes["trusted_translator_sha256"],
        ),
        "run_manifest": (Path("/run.json"), hashes["run_manifest_sha256"]),
        "task_manifest": (Path("/task.json"), hashes["task_manifest_sha256"]),
        "manifest": (Path("/task.json"), hashes["manifest_sha256"]),
        "stage1_result": (
            Path("/generation-result.json"),
            hashes["stage1_result_sha256"],
        ),
        "stage1_invocation": (
            Path("/generation-evidence/invocation.json"),
            hashes["stage1_invocation_sha256"],
        ),
        "generation_metrics": (
            Path("/generation-evidence/metrics.json"),
            hashes["generation_metrics_sha256"],
        ),
        "generation_runtime_metrics": (
            Path("/generation-evidence/runtime-metrics.json"),
            hashes["generation_runtime_metrics_sha256"],
        ),
        "generation_usage": (
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        "generation_last": (
            Path("/generation-evidence/codex-last.txt"),
            hashes["generation_codex_last_sha256"],
        ),
        "generation_output": (
            Path("/generation-evidence/codex-output.log"),
            hashes["generation_codex_output_sha256"],
        ),
        "generation_prompt": (
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
    }
    for label, (path, expected) in direct_hashes.items():
        check_hash(label, path, expected, failures)

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for rel, expected in invocation["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / rel
        check_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            check_hash(f"invocation:{rel}", path, expected, failures)

    comparisons = [
        (
            "prompt candidate-versus-trusted",
            Path("/candidate/prompt.py"),
            Path("/reference/prompt.py"),
        ),
        (
            "translator candidate-versus-trusted",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
        ),
    ]
    for label, left, right in comparisons:
        matches = left.read_bytes() == right.read_bytes()
        print(f"BYTE COMPARISON {label}: {'MATCH' if matches else 'MISMATCH'}")
        if not matches:
            failures.append(f"byte mismatch: {label}")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted supplied semantics missing, mistyped, or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate supplied semantics missing, mistyped, or symlinked")
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        candidate_records = tree_records(candidate_semantics)
        trusted_records = tree_records(trusted_semantics)
        print(
            "TREE candidate/reference-semantics "
            f"entries={len(candidate_records)} "
            f"review_digest={digest_records(candidate_records)}"
        )
        print(
            "TREE reference/reference-semantics "
            f"entries={len(trusted_records)} "
            f"review_digest={digest_records(trusted_records)}"
        )
        missing = sorted(set(trusted_records) - set(candidate_records))
        additional = sorted(set(candidate_records) - set(trusted_records))
        changed = sorted(
            rel
            for rel in set(candidate_records) & set(trusted_records)
            if candidate_records[rel] != trusted_records[rel]
        )
        print(
            "SEMANTICS COMPARISON "
            f"missing={missing} additional={additional} changed={changed}"
        )
        if missing or additional or changed:
            failures.append("candidate supplied-semantics tree differs from trusted")
        symlinks = sorted(
            rel
            for rel, (entry_kind, _) in candidate_records.items()
            if entry_kind == "symlink"
        )
        print(f"CANDIDATE SEMANTICS SYMLINKS: {symlinks}")
        if symlinks:
            failures.append("candidate supplied-semantics tree contains symlinks")

    print(f"FAILURE COUNT: {len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
