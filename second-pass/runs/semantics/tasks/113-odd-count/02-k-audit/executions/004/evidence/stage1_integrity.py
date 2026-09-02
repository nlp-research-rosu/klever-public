#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This deliberately does not trust the launcher booleans.  It hashes mounted
regular files, validates the declared legacy-selected-stage1 record layout,
parses every structured-trace record, and compares the supplied-semantics
trees entry by entry without following symlinks.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check_regular(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        errors.append(f"missing/unreadable required artifact {path}: {err}")
        return
    if stat.S_ISLNK(mode):
        errors.append(f"required artifact is symlink: {path}")
    elif not stat.S_ISREG(mode):
        errors.append(f"required artifact is not a regular file: {path}")


def tree_records(root: Path) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            records.append(("symlink", rel, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            records.append(("dir", rel, ""))
        elif stat.S_ISREG(mode):
            records.append(("file", rel, digest(path)))
        else:
            records.append(("other", rel, oct(mode)))
    return records


def manifest_digest(records: list[tuple[str, str, str]]) -> str:
    h = hashlib.sha256()
    for kind, rel, value in records:
        h.update(f"{kind}\t{rel}\t{value}\n".encode())
    return h.hexdigest()


def main() -> int:
    errors: list[str] = []
    for required in (AUDIT_INPUT, LOCK):
        check_regular(required, errors)
    if errors:
        print("\n".join(errors))
        return 2

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"audit_input_sha256={digest(AUDIT_INPUT)}")
    print(f"audit_campaign_lock_sha256={digest(LOCK)}")
    print(
        "campaign_block_equal="
        f"{audit.get('audit_campaign') == lock}"
    )
    print(
        "campaign_hash_equal="
        f"{digest(LOCK) == audit.get('hashes', {}).get('audit_campaign_lock_sha256')}"
    )
    if audit.get("audit_campaign") != lock:
        errors.append("audit_campaign block differs from campaign lock")
    if digest(LOCK) != audit.get("hashes", {}).get("audit_campaign_lock_sha256"):
        errors.append("campaign lock hash differs from recorded hash")
    if audit.get("record_layout") != "legacy-selected-stage1":
        errors.append("unexpected record layout for this audit")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append("unexpected rendered semantics mode")

    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for record in required_records:
        check_regular(record, errors)
    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        errors.append("structured trace root missing, mistyped, or symlinked")

    direct_hashes = {
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
    hashes = audit.get("hashes", {})
    print("direct_hash_checks:")
    for name, key in direct_hashes.items():
        path = Path(name)
        if not path.exists() and key == "generation_usage_sha256":
            print(f"  OPTIONAL_ABSENT {name}")
            continue
        check_regular(path, errors)
        if not path.is_file():
            continue
        actual = digest(path)
        expected = hashes.get(key)
        match = actual == expected
        print(f"  {name}: {actual} expected={expected} match={match}")
        if not match:
            errors.append(f"hash mismatch: {name}")

    # Check all hashes recorded by both generation manifests for their evidence.
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    evidence_roots = (
        ("invocation", invocation.get("outputs", {}).get("evidence", {})),
        ("generation-result", result.get("outputs", {}).get("evidence", {})),
    )
    for source, mapping in evidence_roots:
        print(f"{source}_evidence_hash_checks:")
        for rel, expected in sorted(mapping.items()):
            path = Path("/generation-evidence") / rel
            check_regular(path, errors)
            if not path.is_file():
                continue
            actual = digest(path)
            match = actual == expected
            print(f"  {rel}: {actual} expected={expected} match={match}")
            if not match:
                errors.append(f"{source} evidence hash mismatch: {rel}")

    # Parse every trace line, not just the launcher-selected token event.
    trace_files = sorted(trace_root.rglob("*"))
    trace_regular = []
    trace_lines = 0
    for path in trace_files:
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            errors.append(f"symlink in structured trace: {path}")
        elif stat.S_ISREG(mode):
            trace_regular.append(path)
            with path.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    try:
                        json.loads(line)
                    except Exception as err:
                        errors.append(f"malformed trace JSON {path}:{line_number}: {err}")
                    trace_lines += 1
        elif not stat.S_ISDIR(mode):
            errors.append(f"mistyped structured trace entry: {path}")
    print(f"trace_regular_files={len(trace_regular)}")
    print(f"trace_json_lines_parsed={trace_lines}")

    # Exact supplied-semantics comparison, including type, path, and content.
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        errors.append("trusted supplied semantics absent, mistyped, or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        errors.append("candidate supplied semantics absent, mistyped, or symlinked")
    trusted_records = tree_records(trusted_semantics)
    candidate_records = tree_records(candidate_semantics)
    exact = trusted_records == candidate_records
    print(f"trusted_semantics_entries={len(trusted_records)}")
    print(f"candidate_semantics_entries={len(candidate_records)}")
    print(f"semantics_tree_exact={exact}")
    print(f"trusted_semantics_independent_manifest_sha256={manifest_digest(trusted_records)}")
    print(f"candidate_semantics_independent_manifest_sha256={manifest_digest(candidate_records)}")
    print(
        "recorded_trusted_semantics_tree_sha256="
        f"{hashes.get('trusted_reference_semantics_sha256')}"
    )
    print(
        "recorded_candidate_semantics_tree_sha256="
        f"{hashes.get('candidate_reference_semantics_sha256')}"
    )
    if not exact:
        errors.append("candidate semantics tree differs from trusted tree")

    candidate_tree_records = tree_records(Path("/candidate"))
    print(f"candidate_tree_entries={len(candidate_tree_records)}")
    print(
        "candidate_independent_manifest_sha256="
        f"{manifest_digest(candidate_tree_records)}"
    )
    print(f"recorded_candidate_tree_sha256={hashes.get('candidate_tree_sha256')}")
    for kind, rel, value in candidate_tree_records:
        if kind in ("symlink", "other"):
            errors.append(f"linked or unsupported candidate entry: {rel} ({kind})")
        if kind == "file":
            print(f"candidate_file_sha256 {rel} {value}")

    for candidate_artifact in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ):
        check_regular(Path("/candidate") / candidate_artifact, errors)

    print(f"integrity_error_count={len(errors)}")
    for err in errors:
        print(f"ERROR: {err}")
    print(f"integrity_check_exit={0 if not errors else 1}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
