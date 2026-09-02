#!/usr/bin/env python3
"""Independent pipeline-v3 provenance and mount-integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def type_name(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{mode:o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        names = sorted(dirs + files)
        for name in names:
            path = Path(parent) / name
            rel = path.relative_to(root).as_posix()
            kind = type_name(path)
            payload = sha256(path) if kind == "file" else (
                os.readlink(path) if kind == "symlink" else None
            )
            result[rel] = (kind, payload)
    return result


def tree_manifest_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for rel, (kind, payload) in sorted(tree_entries(root).items()):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        if payload is not None:
            digest.update(payload.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def check_regular(path: Path) -> bool:
    return (
        path.exists()
        and not path.is_symlink()
        and path.is_file()
        and os.access(path, os.R_OK)
    )


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    failures: list[str] = []

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("declared layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("declared semantics mode is not SUPPLIED_SEMANTICS")

    lock_equal = audit.get("audit_campaign") == lock
    print(f"campaign_block_equals_lock={lock_equal}")
    if not lock_equal:
        failures.append("campaign lock content differs from audit-input campaign block")

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
    ]
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if not trace_files:
        failures.append("structured trace has no JSONL file")
    required.extend(trace_files)
    for path in required:
        ok = check_regular(path)
        print(f"required_regular_readable {path}={ok}")
        if not ok:
            failures.append(f"required record/mount is absent, unreadable, or non-regular: {path}")

    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for path in required_dirs:
        ok = (
            path.exists()
            and not path.is_symlink()
            and path.is_dir()
            and os.access(path, os.R_OK)
        )
        print(f"required_directory {path}={ok}")
        if not ok:
            failures.append(f"required directory absent, unreadable, or mistyped: {path}")

    expected_hashes = {
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
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    recorded = audit["hashes"]
    for path_text, hash_key in expected_hashes.items():
        path = Path(path_text)
        if check_regular(path):
            actual = sha256(path)
            expected = recorded[hash_key]
            ok = actual == expected
            print(f"hash {path} actual={actual} recorded={expected} match={ok}")
            if not ok:
                failures.append(f"hash mismatch: {path}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    result_evidence = generation_result["outputs"]["evidence"]
    for path in trace_files:
        rel = path.relative_to(Path("/generation-evidence")).as_posix()
        expected = result_evidence.get(rel)
        actual = sha256(path)
        ok = actual == expected
        print(f"trace_hash {rel} actual={actual} recorded={expected} match={ok}")
        if not ok:
            failures.append(f"trace hash mismatch or missing recorded hash: {rel}")

    byte_pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]
    for candidate, trusted, label in byte_pairs:
        equal = candidate.read_bytes() == trusted.read_bytes()
        print(f"{label}_byte_identity={equal}")
        if not equal:
            failures.append(f"candidate {label} differs from trusted mount")

    candidate_required = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification-base.k"),
        Path("/candidate/verification.k"),
        Path("/candidate/loop-spec.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    candidate_defects = []
    for path in candidate_required:
        ok = check_regular(path)
        print(f"candidate_required_regular {path}={ok}")
        if not ok:
            candidate_defects.append(
                f"required candidate proof artifact absent or non-regular: {path}"
            )
    print(f"candidate_tree_manifest_sha256={tree_manifest_sha256(Path('/candidate'))}")
    candidate_tree_symlinks = [
        rel for rel, (kind, _) in tree_entries(Path("/candidate")).items()
        if kind == "symlink"
    ]
    print(f"candidate_tree_symlinks={candidate_tree_symlinks}")

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    print(
        "candidate_semantics_manifest_sha256="
        + tree_manifest_sha256(Path("/candidate/reference-semantics"))
    )
    print(
        "trusted_semantics_manifest_sha256="
        + tree_manifest_sha256(Path("/reference/reference-semantics"))
    )
    semantics_equal = candidate_semantics == trusted_semantics
    print(f"semantics_recursive_type_and_byte_identity={semantics_equal}")
    if not semantics_equal:
        candidate_only = sorted(candidate_semantics.keys() - trusted_semantics.keys())
        trusted_only = sorted(trusted_semantics.keys() - candidate_semantics.keys())
        changed = sorted(
            rel for rel in candidate_semantics.keys() & trusted_semantics.keys()
            if candidate_semantics[rel] != trusted_semantics[rel]
        )
        print(f"candidate_only_entries={candidate_only}")
        print(f"trusted_only_entries={trusted_only}")
        print(f"changed_or_mistyped_entries={changed}")
        failures.append("candidate supplied-semantics tree differs from trusted tree")
    symlinks = [
        rel for rel, (kind, _) in candidate_semantics.items() if kind == "symlink"
    ]
    print(f"candidate_semantics_symlinks={symlinks}")
    if symlinks:
        failures.append("candidate supplied-semantics tree contains symlinks")

    trace_type_counts: collections.Counter[str] = collections.Counter()
    payload_type_counts: collections.Counter[str] = collections.Counter()
    function_counts: collections.Counter[str] = collections.Counter()
    malformed = 0
    total_lines = 0
    for path in trace_files:
        with path.open() as stream:
            for line in stream:
                total_lines += 1
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    malformed += 1
                    continue
                trace_type_counts[str(obj.get("type"))] += 1
                payload = obj.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type"))] += 1
                    if payload.get("type") == "function_call":
                        function_counts[str(payload.get("name"))] += 1
    print(f"trace_jsonl_files={len(trace_files)}")
    print(f"trace_total_lines={total_lines}")
    print(f"trace_malformed_json_lines={malformed}")
    print(f"trace_record_type_counts={dict(sorted(trace_type_counts.items()))}")
    print(f"trace_payload_type_counts={dict(sorted(payload_type_counts.items()))}")
    print(f"trace_function_counts={dict(sorted(function_counts.items()))}")
    if malformed:
        failures.append("structured trace contains malformed JSONL")

    print("FAILURES:")
    for failure in failures:
        print(f"- {failure}")
    print("CANDIDATE_DEFECTS:")
    for defect in candidate_defects:
        print(f"- {defect}")
    print(f"INFRASTRUCTURE_INTEGRITY={'PASS' if not failures else 'FAIL'}")
    print(f"CANDIDATE_REQUIRED_ARTIFACTS={'PASS' if not candidate_defects else 'FAIL'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
