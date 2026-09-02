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
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing: {path}")
        return
    if path.is_symlink():
        errors.append(f"symlink where regular file required: {path}")
        return
    if not path.is_file():
        errors.append(f"not a regular file: {path}")
        return
    try:
        path.read_bytes()
    except OSError as err:
        errors.append(f"unreadable: {path}: {err}")


def tree_manifest(root: Path) -> tuple[list[dict[str, object]], list[str]]:
    entries: list[dict[str, object]] = []
    invalid: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append({"path": rel, "type": "dir"})
        elif stat.S_ISREG(mode):
            entries.append(
                {
                    "path": rel,
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": digest_file(path),
                }
            )
        elif stat.S_ISLNK(mode):
            target = os.readlink(path)
            entries.append({"path": rel, "type": "symlink", "target": target})
            invalid.append(f"{path} -> {target}")
        else:
            entries.append({"path": rel, "type": "special", "mode": oct(mode)})
            invalid.append(f"{path} (mode {oct(mode)})")
    return entries, invalid


def manifest_digest(entries: list[dict[str, object]]) -> str:
    payload = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    infrastructure_errors: list[str] = []
    candidate_integrity_errors: list[str] = []

    require_regular(AUDIT_INPUT, infrastructure_errors)
    require_regular(CAMPAIGN_LOCK, infrastructure_errors)
    if infrastructure_errors:
        for item in infrastructure_errors:
            print(f"INFRA_ERROR: {item}")
        return 2

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    if audit.get("record_layout") != "legacy-selected-stage1":
        infrastructure_errors.append(
            f"unexpected record layout: {audit.get('record_layout')!r}"
        )
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        infrastructure_errors.append(
            f"unexpected semantics mode: {audit.get('semantics_mode')!r}"
        )

    lock_equal = audit.get("audit_campaign") == lock
    lock_hash = digest_file(CAMPAIGN_LOCK)
    expected_lock_hash = audit["hashes"].get("audit_campaign_lock_sha256")
    print(f"campaign_block_equal={lock_equal}")
    print(f"campaign_lock_sha256 actual={lock_hash} expected={expected_lock_hash}")
    if not lock_equal or lock_hash != expected_lock_hash:
        infrastructure_errors.append("campaign lock/block/hash mismatch")

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
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_records.append(usage)
    for path in required_records:
        require_regular(path, infrastructure_errors)

    print("container_paths:")
    for key, raw_path in sorted(audit["container_paths"].items()):
        path = Path(raw_path)
        status = (
            "symlink"
            if path.is_symlink()
            else "directory"
            if path.is_dir()
            else "regular"
            if path.is_file()
            else "missing-or-special"
        )
        print(f"  {key}: {path} [{status}]")
        if status == "missing-or-special":
            infrastructure_errors.append(f"declared mount absent/special: {key}={path}")
        elif status == "symlink":
            infrastructure_errors.append(f"declared mount is symlink: {key}={path}")

    direct_hashes = {
        "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    if usage.exists():
        direct_hashes["generation_usage_sha256"] = usage

    print("direct recorded hash checks:")
    for key, path in direct_hashes.items():
        require_regular(path, infrastructure_errors)
        if not path.is_file() or path.is_symlink():
            continue
        actual = digest_file(path)
        expected = audit["hashes"].get(key)
        matches = actual == expected
        print(f"  {key}: match={matches} actual={actual} expected={expected}")
        if not matches:
            infrastructure_errors.append(f"recorded hash mismatch: {key} ({path})")

    prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        candidate_integrity_errors.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        candidate_integrity_errors.append(
            "candidate translator differs from trusted translator"
        )

    candidate_root_entries, candidate_root_invalid = tree_manifest(Path("/candidate"))
    print(f"candidate_root_entries={len(candidate_root_entries)}")
    print(
        "candidate_root_independent_manifest_sha256="
        f"{manifest_digest(candidate_root_entries)}"
    )
    print(
        "launcher_recorded_candidate_tree_sha256="
        f"{audit['hashes'].get('candidate_tree_sha256')}"
    )
    print(f"candidate_root_invalid_entries={candidate_root_invalid}")
    if candidate_root_invalid:
        candidate_integrity_errors.append(
            f"candidate root contains symlink/special entries: {candidate_root_invalid}"
        )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        infrastructure_errors.append("trusted reference-semantics missing or symlinked")
        trusted_entries: list[dict[str, object]] = []
        trusted_invalid: list[str] = []
    else:
        trusted_entries, trusted_invalid = tree_manifest(trusted_semantics)
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        candidate_integrity_errors.append(
            "candidate reference-semantics missing or symlinked"
        )
        candidate_entries: list[dict[str, object]] = []
        candidate_invalid: list[str] = []
    else:
        candidate_entries, candidate_invalid = tree_manifest(candidate_semantics)

    print(f"trusted_semantics_entries={len(trusted_entries)}")
    print(f"candidate_semantics_entries={len(candidate_entries)}")
    print(f"trusted_semantics_invalid_entries={trusted_invalid}")
    print(f"candidate_semantics_invalid_entries={candidate_invalid}")
    print(f"semantics_manifest_equal={trusted_entries == candidate_entries}")
    print(f"trusted_semantics_independent_digest={manifest_digest(trusted_entries)}")
    print(f"candidate_semantics_independent_digest={manifest_digest(candidate_entries)}")
    if trusted_invalid:
        infrastructure_errors.append(
            f"trusted semantics contains symlink/special entries: {trusted_invalid}"
        )
    if candidate_invalid:
        candidate_integrity_errors.append(
            f"candidate semantics contains symlink/special entries: {candidate_invalid}"
        )
    if trusted_entries != candidate_entries:
        candidate_integrity_errors.append(
            "candidate semantics tree differs from trusted tree by path/type/size/hash"
        )

    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        infrastructure_errors.append("structured trace directory missing or symlinked")
    else:
        trace_files = sorted(trace_root.rglob("*"))
        trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
        trace_bad = [
            str(path)
            for path in trace_files
            if path.is_symlink() or (not path.is_file() and not path.is_dir())
        ]
        parsed_lines = 0
        for path in trace_regular:
            with path.open() as stream:
                for line_number, line in enumerate(stream, 1):
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as err:
                        infrastructure_errors.append(
                            f"malformed trace JSON {path}:{line_number}: {err}"
                        )
                    parsed_lines += 1
        print(f"trace_regular_files={len(trace_regular)}")
        print(f"trace_parsed_json_lines={parsed_lines}")
        print(f"trace_bad_entries={trace_bad}")
        if not trace_regular:
            infrastructure_errors.append("structured trace contains no regular files")
        if trace_bad:
            infrastructure_errors.append(f"structured trace has bad entries: {trace_bad}")

    generation_entries, generation_invalid = tree_manifest(
        Path("/generation-evidence")
    )
    print(f"generation_evidence_entries={len(generation_entries)}")
    print(
        "generation_evidence_independent_manifest_sha256="
        f"{manifest_digest(generation_entries)}"
    )
    print(f"generation_evidence_invalid_entries={generation_invalid}")
    if generation_invalid:
        infrastructure_errors.append(
            f"generation evidence contains symlink/special entries: {generation_invalid}"
        )

    records = {
        path.name: json.loads(path.read_text())
        for path in (
            Path("/run.json"),
            Path("/task.json"),
            Path("/generation-result.json"),
            Path("/generation-evidence/invocation.json"),
            Path("/generation-evidence/metrics.json"),
        )
    }
    if usage.exists():
        records[usage.name] = json.loads(usage.read_text())
    print("record_top_level_keys:")
    for name, record in sorted(records.items()):
        print(f"  {name}: {sorted(record.keys())}")

    task = records["task.json"]
    audit_manifest = audit.get("manifest", {})
    shared_manifest_keys = sorted(set(task) & set(audit_manifest))
    manifest_shared_equal = all(task[key] == audit_manifest[key] for key in shared_manifest_keys)
    print(f"task_and_audit_manifest_shared_keys={shared_manifest_keys}")
    print(f"task_and_audit_manifest_shared_values_equal={manifest_shared_equal}")
    if not manifest_shared_equal:
        infrastructure_errors.append(
            "/task.json disagrees with audit-input manifest on shared fields"
        )
    if task.get("condition", {}).get("name") != "semantics":
        infrastructure_errors.append("task condition is not semantics")
    if audit.get("problem_id") != "123-get-odd-collatz":
        infrastructure_errors.append("audit problem id mismatch")

    invocation_outputs = records["invocation.json"].get("outputs", {}).get("evidence", {})
    print("invocation evidence hash checks:")
    for relative_path, expected in sorted(invocation_outputs.items()):
        evidence_path = Path("/generation-evidence") / relative_path
        require_regular(evidence_path, infrastructure_errors)
        if evidence_path.is_file() and not evidence_path.is_symlink():
            actual = digest_file(evidence_path)
            matches = actual == expected
            print(
                f"  {relative_path}: match={matches} "
                f"actual={actual} expected={expected}"
            )
            if not matches:
                infrastructure_errors.append(
                    f"invocation evidence hash mismatch: {relative_path}"
                )

    proof_required = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
    ]
    candidate_missing = []
    for path in proof_required:
        if not path.is_file() or path.is_symlink():
            candidate_missing.append(str(path))
    print(f"candidate_required_proof_artifacts_missing_or_symlinked={candidate_missing}")

    print(f"candidate_integrity_error_count={len(candidate_integrity_errors)}")
    for item in candidate_integrity_errors:
        print(f"CANDIDATE_INTEGRITY_ERROR: {item}")
    print(f"infrastructure_error_count={len(infrastructure_errors)}")
    for item in infrastructure_errors:
        print(f"INFRA_ERROR: {item}")

    if infrastructure_errors:
        return 2
    if candidate_integrity_errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
