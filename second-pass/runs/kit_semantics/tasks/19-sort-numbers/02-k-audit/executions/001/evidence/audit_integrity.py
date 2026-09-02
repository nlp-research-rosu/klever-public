#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def stable_tree_digest(root: Path) -> str:
    """Reviewer-defined digest over entry type, relative path, and file bytes."""
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode()
        mode = os.lstat(path).st_mode
        if stat.S_ISDIR(mode):
            kind = b"d"
            payload = b""
        elif stat.S_ISREG(mode):
            kind = b"f"
            payload = path.read_bytes()
        elif stat.S_ISLNK(mode):
            kind = b"l"
            payload = os.readlink(path).encode()
        else:
            kind = b"?"
            payload = b""
        digest.update(kind + b"\0" + relative + b"\0")
        digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    try:
        mode = os.lstat(path).st_mode
    except OSError as err:
        failures.append(f"required artifact unavailable: {path}: {err}")
        return
    if not stat.S_ISREG(mode):
        failures.append(f"required artifact is not a regular file: {path}")
    if not os.access(path, os.R_OK):
        failures.append(f"required artifact is unreadable: {path}")


def compare_trees(left: Path, right: Path) -> list[str]:
    differences: list[str] = []
    left_entries = {
        path.relative_to(left).as_posix(): path for path in left.rglob("*")
    }
    right_entries = {
        path.relative_to(right).as_posix(): path for path in right.rglob("*")
    }
    for relative in sorted(left_entries.keys() | right_entries.keys()):
        lpath = left_entries.get(relative)
        rpath = right_entries.get(relative)
        if lpath is None:
            differences.append(f"missing from candidate semantics: {relative}")
            continue
        if rpath is None:
            differences.append(f"additional candidate semantics entry: {relative}")
            continue
        lmode = os.lstat(lpath).st_mode
        rmode = os.lstat(rpath).st_mode
        lkind = stat.S_IFMT(lmode)
        rkind = stat.S_IFMT(rmode)
        if stat.S_ISLNK(lmode):
            differences.append(f"symlink in candidate semantics: {relative}")
            continue
        if lkind != rkind:
            differences.append(f"entry-type mismatch: {relative}")
            continue
        if stat.S_ISREG(lmode) and lpath.read_bytes() != rpath.read_bytes():
            differences.append(f"changed candidate semantics file: {relative}")
    return differences


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("record layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("semantics mode is not SUPPLIED_SEMANTICS")
    if lock != audit.get("audit_campaign"):
        failures.append("campaign lock object differs from audit_input.audit_campaign")
    else:
        print("campaign_lock_object_match=true")

    required = [
        AUDIT_INPUT,
        LOCK,
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
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file() or path.is_symlink()]
    if not trace_files:
        failures.append("structured trace has no files")
    required.extend(trace_files)
    for path in required:
        require_regular(path, failures)

    hashes = audit["hashes"]
    direct_hashes = {
        LOCK: hashes["audit_campaign_lock_sha256"],
        Path("/candidate/prompt.py"): hashes["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): hashes["candidate_translator_sha256"],
        Path("/reference/canonical.py"): hashes["canonical_sha256"],
        Path("/generation-evidence/codex-last.txt"): hashes["generation_codex_last_sha256"],
        Path("/generation-evidence/codex-output.log"): hashes["generation_codex_output_sha256"],
        Path("/generation-evidence/metrics.json"): hashes["generation_metrics_sha256"],
        Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
        Path("/generation-evidence/runtime-metrics.json"): hashes[
            "generation_runtime_metrics_sha256"
        ],
        Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
        Path("/generation-evidence/invocation.json"): hashes["stage1_invocation_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/reference/prompt.py"): hashes["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): hashes["trusted_translator_sha256"],
    }
    for path, expected in direct_hashes.items():
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            match = actual == expected
            print(f"sha256 {path} {actual} expected={expected} match={str(match).lower()}")
            if not match:
                failures.append(f"digest mismatch: {path}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    evidence_hashes = generation_result["outputs"]["evidence"]
    invocation_hashes = invocation["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    if evidence_hashes != invocation_hashes:
        failures.append("generation-result and invocation evidence maps differ")
    for relative, expected in sorted(evidence_hashes.items()):
        path = evidence_root / relative
        require_regular(path, failures)
        if path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            match = actual == expected
            print(
                f"evidence_sha256 {relative} {actual} "
                f"expected={expected} match={str(match).lower()}"
            )
            if not match:
                failures.append(f"generation evidence digest mismatch: {relative}")

    byte_pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]
    for candidate, trusted, label in byte_pairs:
        match = candidate.read_bytes() == trusted.read_bytes()
        print(f"candidate_{label}_byte_match={str(match).lower()}")
        if not match:
            failures.append(f"candidate {label} differs from trusted mount")
        if candidate.is_symlink():
            failures.append(f"candidate {label} is symlinked")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if not trusted_semantics.is_dir():
        failures.append("trusted reference semantics missing in supplied-semantics mode")
    if not candidate_semantics.is_dir():
        failures.append("candidate reference semantics missing")
    if candidate_semantics.is_dir() and trusted_semantics.is_dir():
        differences = compare_trees(candidate_semantics, trusted_semantics)
        print(f"semantics_tree_difference_count={len(differences)}")
        for difference in differences:
            print(f"SEMANTICS_DIFFERENCE {difference}")
        failures.extend(differences)
        print(
            "reviewer_tree_sha256 candidate_semantics="
            + stable_tree_digest(candidate_semantics)
        )
        print(
            "reviewer_tree_sha256 trusted_semantics="
            + stable_tree_digest(trusted_semantics)
        )

    print(
        "reviewer_tree_sha256 generation_trace="
        + stable_tree_digest(Path("/generation-evidence/codex-trace"))
    )
    print("reviewer_tree_sha256 candidate=" + stable_tree_digest(Path("/candidate")))

    trace_event_counts: Counter[str] = Counter()
    trace_payload_counts: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"malformed trace JSON: {path}:{line_number}: {err}")
                    continue
                trace_event_counts[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    trace_payload_counts[str(payload.get("type"))] += 1
    print(f"trace_files={len(trace_files)} trace_lines={trace_lines}")
    print(f"trace_event_types={dict(sorted(trace_event_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(trace_payload_counts.items()))}")

    for path in [
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ]:
        data = path.read_bytes()
        print(f"record_read {path} bytes={len(data)} lines={data.count(bytes([10]))}")

    for failure in failures:
        print(f"FAILURE {failure}")
    print(f"integrity_failure_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
