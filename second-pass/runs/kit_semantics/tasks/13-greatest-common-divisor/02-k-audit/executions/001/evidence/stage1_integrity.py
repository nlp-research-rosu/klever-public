#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree_pipeline(root: Path) -> str:
    """Reimplement pipeline_contract.sha256_tree without importing the harness."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
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
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        return [f"missing/unreadable required regular file {path}: {error}"]
    if not stat.S_ISREG(mode):
        issues.append(f"required path is not a real regular file: {path}")
    if not os.access(path, os.R_OK):
        issues.append(f"required file is not readable: {path}")
    return issues


def require_real_dir(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        return [f"missing/unreadable required directory {path}: {error}"]
    if not stat.S_ISDIR(mode):
        issues.append(f"required path is not a real directory: {path}")
    if not os.access(path, os.R_OK | os.X_OK):
        issues.append(f"required directory is not readable/searchable: {path}")
    return issues


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, names, files in os.walk(root, followlinks=False):
        names.sort()
        files.sort()
        directory_path = Path(directory)
        for name in names + files:
            path = directory_path / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            else:
                result[relative] = ("unsupported", None)
    return result


def main() -> int:
    issues: list[str] = []
    for path in (AUDIT_INPUT, LOCK):
        issues.extend(require_regular(path))
    if issues:
        print("\n".join(issues))
        return 2

    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit_input.get('record_layout')}")
    print(f"semantics_mode={audit_input.get('semantics_mode')}")

    if audit_input.get("record_layout") != "pipeline-v3":
        issues.append("record layout is not pipeline-v3")
    if audit_input.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        issues.append("rendered semantics mode is not SUPPLIED_SEMANTICS")
    if lock != audit_input.get("audit_campaign"):
        issues.append("campaign lock JSON does not exactly match audit_campaign")
    actual_lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit_input["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256={actual_lock_hash}")
    if actual_lock_hash != expected_lock_hash:
        issues.append("campaign lock hash mismatch")

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
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]
    for path in required_files:
        issues.extend(require_regular(path))
    for path in required_dirs:
        issues.extend(require_real_dir(path))

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    if not trace_regular:
        issues.append("structured trace contains no regular files")
    for path in trace_files:
        mode = path.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            issues.append(f"structured trace has linked/unsupported entry: {path}")

    expected_hashes = {
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
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
    }
    for raw_path, key in expected_hashes.items():
        path = Path(raw_path)
        issues.extend(require_regular(path))
        if path.exists() and path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            expected = audit_input["hashes"][key]
            print(f"{key} actual={actual} expected={expected}")
            if actual != expected:
                issues.append(f"hash mismatch for {path}")

    trace_digest = sha256_tree_pipeline(trace_root)
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    expected_trace = usage["source_trace_sha256"]
    print(f"generation trace pipeline hash actual={trace_digest} expected={expected_trace}")
    print(
        "launcher alternate generation_codex_trace_sha256="
        f"{audit_input['hashes']['generation_codex_trace_sha256']}"
    )
    if trace_digest != expected_trace:
        issues.append("generation trace tree hash mismatch")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        issues.extend(require_regular(path))
        if path.exists() and path.is_file() and not path.is_symlink():
            actual = sha256_file(path)
            print(f"generation_result evidence {relative} actual={actual} expected={expected}")
            if actual != expected:
                issues.append(f"generation-result evidence hash mismatch: {relative}")

    workspace_digest = sha256_tree_pipeline(Path("/candidate"))
    expected_workspace = generation_result["outputs"]["workspace_sha256"]
    print(f"candidate pipeline tree hash actual={workspace_digest} expected={expected_workspace}")
    print(
        "launcher alternate candidate_tree_sha256="
        f"{audit_input['hashes']['candidate_tree_sha256']}"
    )
    if workspace_digest != expected_workspace:
        issues.append("candidate workspace differs from recorded generation output")

    candidate_prompt = Path("/candidate/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    if candidate_prompt.read_bytes() != Path("/reference/prompt.py").read_bytes():
        issues.append("candidate prompt differs from trusted prompt")
    if candidate_translator.read_bytes() != Path("/reference/py2mpy.py").read_bytes():
        issues.append("candidate translator differs from trusted translator")

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    candidate_bad_types = {
        path: data for path, data in candidate_semantics.items()
        if data[0] not in {"directory", "file"}
    }
    trusted_bad_types = {
        path: data for path, data in trusted_semantics.items()
        if data[0] not in {"directory", "file"}
    }
    if candidate_bad_types:
        issues.append(f"candidate supplied semantics has bad entry types: {candidate_bad_types}")
    if trusted_bad_types:
        issues.append(f"trusted supplied semantics has bad entry types: {trusted_bad_types}")
    if candidate_semantics != trusted_semantics:
        candidate_only = sorted(set(candidate_semantics) - set(trusted_semantics))
        trusted_only = sorted(set(trusted_semantics) - set(candidate_semantics))
        changed = sorted(
            path for path in set(candidate_semantics) & set(trusted_semantics)
            if candidate_semantics[path] != trusted_semantics[path]
        )
        issues.append(
            "supplied semantics mismatch: "
            f"candidate_only={candidate_only}, trusted_only={trusted_only}, changed={changed}"
        )
    print(f"supplied semantics entries={len(candidate_semantics)} exact_match={candidate_semantics == trusted_semantics}")
    for relative, (kind, digest) in sorted(candidate_semantics.items()):
        if kind == "file":
            print(f"semantics file {digest} {relative}")

    trace_type_counts: collections.Counter[str] = collections.Counter()
    trace_payload_types: collections.Counter[str] = collections.Counter()
    parsed_lines = 0
    for path in trace_regular:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    record = json.loads(line)
                except ValueError as error:
                    issues.append(f"invalid trace JSON {path}:{line_number}: {error}")
                    continue
                parsed_lines += 1
                trace_type_counts[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    trace_payload_types[str(payload.get("type"))] += 1
    print(f"trace_files={len(trace_regular)} parsed_jsonl_records={parsed_lines}")
    print(f"trace_record_types={dict(sorted(trace_type_counts.items()))}")
    print(f"trace_payload_types={dict(sorted(trace_payload_types.items()))}")

    print("ISSUES")
    if issues:
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("- none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
