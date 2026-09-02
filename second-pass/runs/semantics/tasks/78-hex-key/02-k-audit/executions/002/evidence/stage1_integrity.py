#!/usr/bin/env python3
"""Independent integrity checks for the mounted legacy-selected-stage1 record."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({mode:o})"


def tree_manifest(root: Path) -> tuple[str, list[str]]:
    entries: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        entry_kind = kind(path)
        if entry_kind == "regular":
            entries.append(f"F\t{rel}\t{path.stat().st_size}\t{sha256(path)}")
        elif entry_kind == "symlink":
            entries.append(f"L\t{rel}\t{os.readlink(path)}")
        elif entry_kind == "directory":
            entries.append(f"D\t{rel}")
        else:
            entries.append(f"O\t{rel}\t{entry_kind}")
    body = ("\n".join(entries) + "\n").encode()
    return hashlib.sha256(body).hexdigest(), entries


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce the launcher pipeline's length-delimited tree digest."""
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
                raise ValueError(f"unsupported tree entry: {path}")
    for relative, entry_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_kind.encode() + b"\0")
        if entry_kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    _, left_entries = tree_manifest(left)
    _, right_entries = tree_manifest(right)
    return sorted(set(left_entries).symmetric_difference(right_entries))


def main() -> int:
    record = json.loads(AUDIT_INPUT.read_text())
    failures: list[str] = []

    print(f"audit-input type={kind(AUDIT_INPUT)} sha256={sha256(AUDIT_INPUT)}")
    print(f"record_layout={record.get('record_layout')}")
    print(f"semantics_mode={record.get('semantics_mode')}")
    if record.get("record_layout") != "legacy-selected-stage1":
        failures.append("unexpected record layout")
    if record.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("unexpected semantics mode")

    container_paths = record["container_paths"]
    for label, raw_path in sorted(container_paths.items()):
        path = Path(raw_path)
        exists = path.exists() or path.is_symlink()
        print(f"container_path {label}: {raw_path} exists={exists} kind={kind(path) if exists else 'missing'}")
        if not exists:
            failures.append(f"missing launcher-declared mount: {label}={raw_path}")

    required_regular = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
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
    if usage.exists() or usage.is_symlink():
        required_regular.append(usage)
    trace_root = Path("/generation-evidence/codex-trace")
    for path in required_regular:
        actual = kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"required_record {path}: {actual}")
        if actual != "regular":
            failures.append(f"required record is not a regular file: {path} ({actual})")
    if kind(trace_root) != "directory":
        failures.append(f"trace root is not a directory: {trace_root}")

    lock_path = Path("/audit-campaign-lock.json")
    lock = json.loads(lock_path.read_text())
    lock_equal = lock == record["audit_campaign"]
    lock_hash = sha256(lock_path)
    print(f"campaign_block_equal={lock_equal}")
    print(f"campaign_lock_sha256={lock_hash}")
    print(f"campaign_lock_recorded_sha256={record['hashes']['audit_campaign_lock_sha256']}")
    if not lock_equal:
        failures.append("campaign lock JSON does not equal audit_campaign block")
    if lock_hash != record["hashes"]["audit_campaign_lock_sha256"]:
        failures.append("campaign lock hash mismatch")

    hash_checks = {
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
    for raw_path, hash_key in hash_checks.items():
        path = Path(raw_path)
        if not path.exists():
            continue
        actual = sha256(path)
        expected = record["hashes"].get(hash_key)
        match = actual == expected
        print(f"hash {path}: actual={actual} recorded[{hash_key}]={expected} match={match}")
        if not match:
            failures.append(f"hash mismatch: {path}")

    candidate_required = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "prompt.py",
        "py2mpy.py",
    ]
    candidate_root = Path("/candidate")
    for rel in candidate_required:
        path = candidate_root / rel
        actual = kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"candidate_required {rel}: {actual}")
        if actual != "regular":
            failures.append(f"candidate proof artifact is not regular: {rel} ({actual})")

    candidate_semantics = candidate_root / "reference-semantics"
    trusted_semantics = Path("/reference/reference-semantics")
    if kind(trusted_semantics) != "directory":
        failures.append("trusted reference semantics absent or mistyped")
    differences = compare_trees(candidate_semantics, trusted_semantics)
    candidate_tree_hash, candidate_entries = tree_manifest(candidate_semantics)
    trusted_tree_hash, trusted_entries = tree_manifest(trusted_semantics)
    print(f"candidate_semantics_independent_manifest_sha256={candidate_tree_hash}")
    print(f"trusted_semantics_independent_manifest_sha256={trusted_tree_hash}")
    pipeline_candidate_hash = pipeline_tree_hash(candidate_root)
    pipeline_candidate_expected = result = json.loads(
        Path("/generation-result.json").read_text()
    )["outputs"]["workspace_sha256"]
    pipeline_semantics_hash = pipeline_tree_hash(trusted_semantics)
    pipeline_semantics_expected = record["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    pipeline_trace_hash = pipeline_tree_hash(trace_root)
    trace_expected = json.loads(usage.read_text())["source_trace_sha256"]
    print(
        "candidate_pipeline_tree_sha256="
        f"{pipeline_candidate_hash} expected_workspace_sha256="
        f"{pipeline_candidate_expected} match="
        f"{pipeline_candidate_hash == pipeline_candidate_expected}"
    )
    print(
        "trusted_semantics_pipeline_tree_sha256="
        f"{pipeline_semantics_hash} expected_manifest_sha256="
        f"{pipeline_semantics_expected} match="
        f"{pipeline_semantics_hash == pipeline_semantics_expected}"
    )
    print(
        "trace_pipeline_tree_sha256="
        f"{pipeline_trace_hash} expected_usage_source_trace_sha256="
        f"{trace_expected} match={pipeline_trace_hash == trace_expected}"
    )
    if pipeline_candidate_hash != pipeline_candidate_expected:
        failures.append("candidate tree does not match retained generation workspace hash")
    if pipeline_semantics_hash != pipeline_semantics_expected:
        failures.append("trusted semantics tree manifest hash mismatch")
    if pipeline_trace_hash != trace_expected:
        failures.append("trace tree does not match usage source trace hash")
    print(f"semantics_entry_count candidate={len(candidate_entries)} trusted={len(trusted_entries)}")
    print(f"semantics_trees_exact={not differences}")
    for difference in differences:
        print("SEMANTICS_DIFFERENCE " + difference)
    if differences:
        failures.append("candidate supplied-semantics tree differs from trusted tree")

    prompt_equal = (candidate_root / "prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    translator_equal = (candidate_root / "py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print(f"candidate_prompt_byte_equal={prompt_equal}")
    print(f"candidate_translator_byte_equal={translator_equal}")
    if not prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        failures.append("candidate translator differs from trusted translator")

    mounted_roots = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]
    symlinks: list[str] = []
    for root in mounted_roots:
        symlinks.extend(str(path) for path in root.rglob("*") if path.is_symlink())
    print(f"symlink_count={len(symlinks)}")
    for path in symlinks:
        print("SYMLINK " + path)
    if symlinks:
        failures.append("symlink found in audited mounted inputs")

    result = json.loads(Path("/generation-result.json").read_text())
    declared_outputs = result["outputs"]["evidence"]
    for rel, expected in sorted(declared_outputs.items()):
        path = Path("/generation-evidence") / rel
        actual_kind = kind(path) if path.exists() or path.is_symlink() else "missing"
        actual_hash = sha256(path) if actual_kind == "regular" else None
        match = actual_hash == expected
        print(f"declared_generation_output {rel}: kind={actual_kind} actual={actual_hash} expected={expected} match={match}")
        if not match:
            failures.append(f"generation-result evidence mismatch: {rel}")

    trace_files = sorted(trace_root.rglob("*.jsonl"))
    print(f"trace_jsonl_count={len(trace_files)}")
    event_types: Counter[str] = Counter()
    invalid_trace_lines = 0
    trace_lines = 0
    for path in trace_files:
        print(f"trace_file {path}: sha256={sha256(path)} size={path.stat().st_size}")
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                trace_lines += 1
                try:
                    event = json.loads(line)
                    event_types[str(event.get("type", "<missing>"))] += 1
                except json.JSONDecodeError:
                    invalid_trace_lines += 1
    print(f"trace_lines={trace_lines} invalid_json_lines={invalid_trace_lines}")
    print("trace_event_types=" + json.dumps(dict(sorted(event_types.items())), sort_keys=True))
    if not trace_files or invalid_trace_lines:
        failures.append("structured trace missing or malformed")

    print(f"failure_count={len(failures)}")
    for failure in failures:
        print("FAILURE " + failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
