#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def tree_entries(root: Path):
    entries = {}
    for base, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()
        base_path = Path(base)
        for name in dirnames + filenames:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            record = {
                "kind": entry_kind,
                "mode": stat.S_IMODE(path.lstat().st_mode),
                "size": path.lstat().st_size,
            }
            if entry_kind == "file":
                record["sha256"] = sha256(path)
            elif entry_kind == "symlink":
                record["target"] = os.readlink(path)
            entries[rel] = record
    return entries


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement pipeline_contract.sha256_tree independently."""
    digest = hashlib.sha256()
    entries = tree_entries(root)
    for relative, record in sorted(entries.items()):
        encoded = relative.encode("utf-8")
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        kind_label = (
            "directory"
            if record["kind"] == "dir"
            else "file"
            if record["kind"] == "file"
            else record["kind"]
        )
        digest.update(kind_label.encode("utf-8") + b"\0")
        if record["kind"] == "file":
            path = root / relative
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def check_regular(path: Path, label: str, failures: list[str]) -> None:
    try:
        entry_kind = kind(path)
    except (FileNotFoundError, PermissionError) as err:
        failures.append(f"{label}: unavailable: {err}")
        print(f"FAIL {label}: unavailable: {err}")
        return
    if entry_kind != "file":
        failures.append(f"{label}: expected regular file, got {entry_kind}")
        print(f"FAIL {label}: expected regular file, got {entry_kind}")
        return
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        failures.append(f"{label}: unreadable: {err}")
        print(f"FAIL {label}: unreadable: {err}")
        return
    print(f"OK   {label}: regular readable file {path}")


def main() -> int:
    failures: list[str] = []
    audit = load_json(AUDIT_INPUT)

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "legacy-selected-stage1":
        failures.append("unexpected record layout")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")

    required_files = {
        "audit input": AUDIT_INPUT,
        "campaign lock": Path("/audit-campaign-lock.json"),
        "run manifest": Path("/run.json"),
        "task manifest": Path("/task.json"),
        "stage1 result": Path("/generation-result.json"),
        "generation invocation": Path("/generation-evidence/invocation.json"),
        "generation metrics": Path("/generation-evidence/metrics.json"),
        "generation last": Path("/generation-evidence/codex-last.txt"),
        "generation output": Path("/generation-evidence/codex-output.log"),
        "generation prompt": Path("/generation-evidence/prompt.txt"),
    }
    for label, path in required_files.items():
        check_regular(path, label, failures)

    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir() or trace_root.is_symlink():
        failures.append("structured trace root is missing, unreadable, or symlinked")
    trace_files = sorted(trace_root.rglob("*.jsonl")) if trace_root.is_dir() else []
    if not trace_files:
        failures.append("structured trace contains no JSONL record")
    for index, path in enumerate(trace_files, start=1):
        check_regular(path, f"trace file {index}", failures)

    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        check_regular(usage, "generation usage (present, optional for layout)", failures)
    print(
        "INFO runtime-metrics.json absent; historical runtime metrics are not "
        "required for legacy-selected-stage1"
        if not Path("/generation-evidence/runtime-metrics.json").exists()
        else "INFO runtime-metrics.json present"
    )

    for key, mounted in sorted(audit["container_paths"].items()):
        path = Path(mounted)
        if not path.exists():
            failures.append(f"launcher-declared container path missing: {key}={path}")
            print(f"FAIL container_paths.{key}: missing {path}")
        elif path.is_symlink():
            failures.append(f"launcher-declared container path is symlinked: {key}={path}")
            print(f"FAIL container_paths.{key}: symlink {path}")
        elif not os.access(path, os.R_OK):
            failures.append(f"launcher-declared container path unreadable: {key}={path}")
            print(f"FAIL container_paths.{key}: unreadable {path}")
        else:
            print(f"OK   container_paths.{key}: {kind(path)} {path}")

    lock = load_json(Path("/audit-campaign-lock.json"))
    if lock == audit["audit_campaign"]:
        print("OK   campaign lock JSON exactly equals audit_input.audit_campaign")
    else:
        failures.append("campaign lock JSON differs from audit campaign block")
        print("FAIL campaign lock JSON differs from audit_input.audit_campaign")

    task = load_json(Path("/task.json"))
    embedded_manifest = dict(audit["manifest"])
    normalized_config = embedded_manifest.pop("config", None)
    if task == embedded_manifest and normalized_config == audit.get("manifest_config"):
        print(
            "OK   task manifest equals audit_input.manifest after removing the "
            "launcher-added config field, which equals manifest_config"
        )
    else:
        failures.append("task manifest differs materially from embedded manifest")
        print("FAIL task manifest differs materially from audit_input.manifest")

    recorded_file_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
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
    for hash_key, path in recorded_file_hashes.items():
        expected = audit["hashes"].get(hash_key)
        if expected is None:
            failures.append(f"recorded hash missing: {hash_key}")
            print(f"FAIL {hash_key}: absent from audit input")
            continue
        actual = sha256(path)
        if actual == expected:
            print(f"OK   {hash_key}: {actual}")
        else:
            failures.append(f"hash mismatch: {hash_key}")
            print(f"FAIL {hash_key}: expected={expected} actual={actual}")

    result_for_tree = load_json(Path("/generation-result.json"))
    invocation_for_tree = load_json(Path("/generation-evidence/invocation.json"))
    usage_for_tree = load_json(Path("/generation-evidence/usage.json"))
    recorded_tree_hashes = [
        (
            "candidate pipeline tree",
            Path("/candidate"),
            result_for_tree["outputs"]["workspace_sha256"],
        ),
        (
            "candidate reference-semantics pipeline tree",
            Path("/candidate/reference-semantics"),
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "trusted reference-semantics pipeline tree",
            Path("/reference/reference-semantics"),
            audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
        ),
        (
            "generation trace pipeline tree",
            Path("/generation-evidence/codex-trace"),
            usage_for_tree["source_trace_sha256"],
        ),
    ]
    for label, path, expected in recorded_tree_hashes:
        actual = pipeline_tree_sha256(path)
        if actual == expected:
            print(f"OK   {label}: {actual}")
        else:
            failures.append(f"tree hash mismatch: {label}")
            print(f"FAIL {label}: expected={expected} actual={actual}")
    candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
    candidate_pipeline_claims = {
        "generation-result outputs.workspace_sha256": result_for_tree["outputs"][
            "workspace_sha256"
        ],
        "invocation inputs.workspace_sha256": invocation_for_tree["inputs"][
            "workspace_sha256"
        ],
        "invocation outputs.workspace_sha256": invocation_for_tree["outputs"][
            "workspace_sha256"
        ],
        "invocation retained_workspace_sha256": invocation_for_tree[
            "retained_workspace_sha256"
        ],
    }
    for label, expected in candidate_pipeline_claims.items():
        if candidate_pipeline_hash == expected:
            print(f"OK   candidate tree matches {label}: {expected}")
        else:
            failures.append(f"candidate tree differs from {label}")
            print(
                f"FAIL candidate tree differs from {label}: "
                f"expected={expected} actual={candidate_pipeline_hash}"
            )
    print(
        "INFO launcher secure aggregate hashes recorded in audit input: "
        f"candidate={audit['hashes']['candidate_tree_sha256']} "
        "candidate-semantics="
        f"{audit['hashes']['candidate_reference_semantics_sha256']} "
        "trusted-semantics="
        f"{audit['hashes']['trusted_reference_semantics_sha256']} "
        f"trace={audit['hashes']['generation_codex_trace_sha256']}"
    )

    result = load_json(Path("/generation-result.json"))
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        if not path.is_file() or path.is_symlink():
            failures.append(f"generation-result evidence entry invalid: {rel}")
            print(f"FAIL generation-result evidence {rel}: missing/non-file/symlink")
            continue
        actual = sha256(path)
        if actual == expected:
            print(f"OK   generation-result evidence {rel}: {actual}")
        else:
            failures.append(f"generation-result evidence hash mismatch: {rel}")
            print(
                f"FAIL generation-result evidence {rel}: "
                f"expected={expected} actual={actual}"
            )

    byte_pairs = [
        (
            "candidate prompt versus trusted prompt",
            Path("/candidate/prompt.py"),
            Path("/reference/prompt.py"),
        ),
        (
            "candidate translator versus trusted translator",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
        ),
    ]
    for label, candidate, trusted in byte_pairs:
        if candidate.read_bytes() == trusted.read_bytes():
            print(f"OK   {label}: byte-identical")
        else:
            failures.append(f"{label}: bytes differ")
            print(f"FAIL {label}: bytes differ")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted supplied-semantics tree absent or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate supplied-semantics tree absent or symlinked")

    trusted_entries = tree_entries(trusted_semantics)
    candidate_entries = tree_entries(candidate_semantics)
    all_paths = sorted(set(trusted_entries) | set(candidate_entries))
    semantics_differences = []
    for rel in all_paths:
        trusted_record = trusted_entries.get(rel)
        candidate_record = candidate_entries.get(rel)
        if trusted_record != candidate_record:
            semantics_differences.append((rel, trusted_record, candidate_record))
    for rel, record in sorted(trusted_entries.items()):
        digest = record.get("sha256", "-")
        print(
            f"SEMANTICS_ENTRY {record['kind']} mode={record['mode']:04o} "
            f"size={record['size']} sha256={digest} path={rel}"
        )
    if semantics_differences:
        failures.append("candidate supplied-semantics tree differs from trusted tree")
        for rel, trusted_record, candidate_record in semantics_differences:
            print(
                f"FAIL semantics path={rel} trusted={trusted_record!r} "
                f"candidate={candidate_record!r}"
            )
    else:
        print(
            "OK   candidate reference-semantics recursively matches trusted tree "
            f"for all {len(trusted_entries)} entries, including types and modes"
        )

    candidate_entries_all = tree_entries(Path("/candidate"))
    non_regular = [
        (rel, rec["kind"])
        for rel, rec in candidate_entries_all.items()
        if rec["kind"] not in {"file", "dir"}
    ]
    if non_regular:
        failures.append("candidate contains symlink or other special entry")
        for rel, entry_kind in non_regular:
            print(f"FAIL candidate special entry: {entry_kind} {rel}")
    else:
        print(
            "OK   candidate tree contains only regular files and directories "
            f"({len(candidate_entries_all)} non-root entries)"
        )

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
