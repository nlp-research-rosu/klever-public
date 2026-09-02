#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script treats launcher JSON as data.  It hashes mounted files directly,
parses the complete JSONL trace, and recursively compares the candidate's
supplied-semantics copy with the trusted mounted tree without following links.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE_ROOT = Path("/generation-evidence/codex-trace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def artifact_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"other(mode={oct(mode)})"


def check_regular(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing required artifact: {path}")
        return
    if path.is_symlink():
        failures.append(f"required artifact is symlinked: {path}")
        return
    if not path.is_file():
        failures.append(
            f"required artifact is mistyped: {path} ({artifact_kind(path)})"
        )
        return
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        failures.append(f"required artifact is unreadable: {path}: {err}")


def tree_entries(root: Path) -> dict[str, tuple[str, int, str | None]]:
    entries: dict[str, tuple[str, int, str | None]] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        current_path = Path(current)
        for name in dirnames + filenames:
            path = current_path / name
            rel = str(path.relative_to(root))
            kind = artifact_kind(path)
            mode = stat.S_IMODE(path.lstat().st_mode)
            digest = sha256(path) if kind == "file" else None
            entries[rel] = (kind, mode, digest)
            if kind == "symlink":
                # os.walk lists symlinked directories in dirnames, but
                # followlinks=False guarantees that this script never follows them.
                continue
    return entries


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    if audit.get("record_layout") != "legacy-selected-stage1":
        failures.append("unexpected record layout for this audit")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected rendered semantics mode")

    lock_equal = audit.get("audit_campaign") == lock
    print(f"campaign_lock_structural_equality={lock_equal}")
    if not lock_equal:
        failures.append("campaign lock differs from audit_input.audit_campaign")

    lock_hash = sha256(LOCK)
    expected_lock_hash = audit.get("hashes", {}).get("audit_campaign_lock_sha256")
    print(f"campaign_lock_sha256={lock_hash}")
    print(f"campaign_lock_hash_matches={lock_hash == expected_lock_hash}")
    if lock_hash != expected_lock_hash:
        failures.append("campaign lock hash mismatch")

    required = [
        Path("/audit-input.json"),
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
    ]
    for path in required:
        check_regular(path, failures)

    for name, raw_path in sorted(audit.get("container_paths", {}).items()):
        path = Path(raw_path)
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        symlink = path.is_symlink()
        print(
            f"container_path {name}: path={path} exists={exists} "
            f"readable={readable} symlink={symlink} kind="
            f"{artifact_kind(path) if exists or symlink else 'missing'}"
        )
        if not exists:
            failures.append(f"launcher-declared container path missing: {name}={path}")
        elif not readable:
            failures.append(
                f"launcher-declared container path unreadable: {name}={path}"
            )
        elif symlink:
            failures.append(
                f"launcher-declared container path is symlinked: {name}={path}"
            )

    direct_hashes = {
        "audit_campaign_lock_sha256": LOCK,
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    declared_hashes = audit.get("hashes", {})
    for field, path in direct_hashes.items():
        actual = sha256(path)
        expected = declared_hashes.get(field)
        matched = actual == expected
        print(
            f"declared_hash {field}: actual={actual} expected={expected} "
            f"matches={matched}"
        )
        if not matched:
            failures.append(f"declared hash mismatch for {field}: {path}")

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    for rel, expected in sorted(
        invocation.get("outputs", {}).get("evidence", {}).items()
    ):
        path = Path("/generation-evidence") / rel
        check_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            actual = sha256(path)
            matched = actual == expected
            print(
                f"invocation_output {rel}: actual={actual} expected={expected} "
                f"matches={matched}"
            )
            if not matched:
                failures.append(f"invocation output hash mismatch: {path}")

    trace_files = sorted(TRACE_ROOT.rglob("*"))
    trace_regular = [
        path for path in trace_files if path.is_file() and not path.is_symlink()
    ]
    trace_symlinks = [path for path in trace_files if path.is_symlink()]
    print(f"trace_regular_file_count={len(trace_regular)}")
    print(f"trace_symlink_count={len(trace_symlinks)}")
    if not trace_regular:
        failures.append("structured trace contains no regular files")
    if trace_symlinks:
        failures.extend(f"structured trace has symlink: {p}" for p in trace_symlinks)

    trace_types: Counter[str] = Counter()
    trace_lines = 0
    trace_invalid = 0
    for path in trace_regular:
        print(f"trace_file {path.relative_to(TRACE_ROOT)} sha256={sha256(path)}")
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as err:
                    trace_invalid += 1
                    failures.append(f"invalid trace JSON: {path}:{line_number}: {err}")
                    continue
                trace_types[str(record.get("type", "<missing>"))] += 1
    print(f"trace_line_count={trace_lines}")
    print(f"trace_invalid_json_count={trace_invalid}")
    print(f"trace_top_level_types={dict(sorted(trace_types.items()))}")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted reference-semantics mount is absent or mistyped")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate reference-semantics is absent or mistyped")
    if (
        trusted_semantics.is_dir()
        and not trusted_semantics.is_symlink()
        and candidate_semantics.is_dir()
        and not candidate_semantics.is_symlink()
    ):
        candidate_entries = tree_entries(candidate_semantics)
        trusted_entries = tree_entries(trusted_semantics)
        print(f"candidate_semantics_entry_count={len(candidate_entries)}")
        print(f"trusted_semantics_entry_count={len(trusted_entries)}")
        all_rel = sorted(set(candidate_entries) | set(trusted_entries))
        for rel in all_rel:
            left = candidate_entries.get(rel)
            right = trusted_entries.get(rel)
            if left != right:
                failures.append(
                    f"reference-semantics entry mismatch: {rel}: "
                    f"candidate={left}, trusted={right}"
                )
        print(
            "reference_semantics_recursive_byte_and_type_match="
            f"{candidate_entries == trusted_entries}"
        )

    for candidate_path, trusted_path, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
            "translator",
        ),
    ]:
        equal = candidate_path.read_bytes() == trusted_path.read_bytes()
        print(f"candidate_{label}_byte_match={equal}")
        if not equal:
            failures.append(f"candidate {label} differs from trusted mount")

    print(f"runtime_metrics_present={Path('/generation-evidence/runtime-metrics.json').exists()}")
    print("runtime_metrics_required_for_layout=False")
    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
