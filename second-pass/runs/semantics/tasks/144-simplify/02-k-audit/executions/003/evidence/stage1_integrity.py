#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        names = sorted(dirnames + filenames)
        for name in names:
            path = current / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            value: str | None = None
            if kind == "file":
                value = sha256(path)
            elif kind == "symlink":
                value = os.readlink(path)
            result[rel] = (kind, value)
    return result


def tree_manifest_digest(entries: dict[str, tuple[str, str | None]]) -> str:
    digest = hashlib.sha256()
    for rel, (kind, value) in sorted(entries.items()):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        if value is not None:
            digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def manifest_tree_digest(root: Path) -> str:
    """Pipeline manifest digest: typed paths, file lengths, and raw bytes."""
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


def show_json_equality(left: Any, right: Any) -> bool:
    return left == right


def main() -> int:
    problems: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    lock_equal = show_json_equality(audit.get("audit_campaign"), lock)
    print(f"campaign_block_equals_lock={lock_equal}")
    if not lock_equal:
        problems.append("campaign lock JSON differs from audit_campaign block")

    actual_lock_hash = sha256(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_campaign_lock sha256 actual={actual_lock_hash} expected={expected_lock_hash}")
    if actual_lock_hash != expected_lock_hash:
        problems.append("campaign lock SHA-256 mismatch")

    required_layout = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required_layout.append(Path("/generation-evidence/usage.json"))

    for key, mounted in sorted(audit["container_paths"].items()):
        path = Path(mounted)
        present = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if present or path.is_symlink() else "missing"
        print(f"container_path {key}: path={path} present={present} readable={readable} kind={kind}")
        if not present or not readable:
            problems.append(f"launcher-declared mount missing/unreadable: {key}={path}")

    for path in required_layout:
        present = path.exists()
        readable = os.access(path, os.R_OK)
        kind = entry_kind(path) if present or path.is_symlink() else "missing"
        print(f"layout_required path={path} present={present} readable={readable} kind={kind}")
        if not present or not readable:
            problems.append(f"required record missing/unreadable: {path}")

    direct_hashes = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    }
    for path, key in direct_hashes.items():
        expected = audit["hashes"].get(key)
        if not path.is_file():
            print(f"direct_hash path={path} actual=ABSENT expected={expected}")
            if expected is not None:
                problems.append(f"hash-declared file absent: {path}")
            continue
        actual = sha256(path)
        ok = expected == actual
        print(f"direct_hash path={path} actual={actual} expected={expected} match={ok}")
        if expected is not None and not ok:
            problems.append(f"SHA-256 mismatch: {path}")

    comparisons = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "candidate prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "candidate translator"),
    ]
    for candidate, trusted, label in comparisons:
        exact = candidate.read_bytes() == trusted.read_bytes()
        print(f"byte_identity {label}: {exact}")
        if not exact:
            problems.append(f"{label} differs from trusted mount")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    print(f"trusted_reference_semantics_present={trusted_semantics.is_dir()}")
    if not trusted_semantics.is_dir():
        problems.append("SUPPLIED_SEMANTICS trusted tree absent")
    if not candidate_semantics.is_dir():
        problems.append("candidate reference-semantics tree absent")
    else:
        trusted_entries = tree_entries(trusted_semantics)
        candidate_entries = tree_entries(candidate_semantics)
        all_rel = sorted(set(trusted_entries) | set(candidate_entries))
        diffs = []
        for rel in all_rel:
            if trusted_entries.get(rel) != candidate_entries.get(rel):
                diffs.append((rel, trusted_entries.get(rel), candidate_entries.get(rel)))
        trusted_symlinks = [rel for rel, value in trusted_entries.items() if value[0] == "symlink"]
        candidate_symlinks = [rel for rel, value in candidate_entries.items() if value[0] == "symlink"]
        print(f"trusted_semantics_entries={len(trusted_entries)} candidate_semantics_entries={len(candidate_entries)}")
        print(f"trusted_semantics_symlinks={trusted_symlinks}")
        print(f"candidate_semantics_symlinks={candidate_symlinks}")
        print(f"reference_semantics_recursive_differences={len(diffs)}")
        for diff in diffs:
            print(f"reference_semantics_diff={diff!r}")
        if diffs or trusted_symlinks or candidate_symlinks:
            problems.append("candidate supplied-semantics tree is not an exact regular-file/directory copy")
        trusted_digest = tree_manifest_digest(trusted_entries)
        candidate_digest = tree_manifest_digest(candidate_entries)
        print(f"reviewer_tree_digest trusted_reference_semantics={trusted_digest}")
        print(f"reviewer_tree_digest candidate_reference_semantics={candidate_digest}")
        expected_manifest_digest = audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
        trusted_manifest_digest = manifest_tree_digest(trusted_semantics)
        candidate_manifest_digest = manifest_tree_digest(candidate_semantics)
        print(
            "manifest_tree_digest trusted_reference_semantics="
            f"{trusted_manifest_digest} expected={expected_manifest_digest} "
            f"match={trusted_manifest_digest == expected_manifest_digest}"
        )
        print(
            "manifest_tree_digest candidate_reference_semantics="
            f"{candidate_manifest_digest} expected={expected_manifest_digest} "
            f"match={candidate_manifest_digest == expected_manifest_digest}"
        )
        if trusted_manifest_digest != expected_manifest_digest:
            problems.append("trusted supplied-semantics manifest digest mismatch")
        if candidate_manifest_digest != expected_manifest_digest:
            problems.append("candidate supplied-semantics manifest digest mismatch")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = tree_entries(trace_root)
    jsonl_files = sorted(trace_root.rglob("*.jsonl"))
    trace_lines = 0
    for path in jsonl_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                json.loads(line)
                trace_lines += 1
    print(f"structured_trace_jsonl_files={len(jsonl_files)} parsed_json_lines={trace_lines}")
    print(f"reviewer_tree_digest generation_trace={tree_manifest_digest(trace_entries)}")

    candidate_entries = tree_entries(Path("/candidate"))
    candidate_symlinks = [rel for rel, value in candidate_entries.items() if value[0] == "symlink"]
    print(f"candidate_entries={len(candidate_entries)} candidate_symlinks={candidate_symlinks}")
    print(f"reviewer_tree_digest candidate={tree_manifest_digest(candidate_entries)}")
    if candidate_symlinks:
        problems.append("candidate contains symlinked entries")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    candidate_manifest_digest = manifest_tree_digest(Path("/candidate"))
    expected_candidate_manifest_digest = generation_result["outputs"]["workspace_sha256"]
    print(
        f"manifest_tree_digest candidate={candidate_manifest_digest} "
        f"expected={expected_candidate_manifest_digest} "
        f"match={candidate_manifest_digest == expected_candidate_manifest_digest}"
    )
    if candidate_manifest_digest != expected_candidate_manifest_digest:
        problems.append("candidate workspace manifest digest mismatch")

    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_manifest_digest = manifest_tree_digest(trace_root)
    expected_trace_manifest_digest = usage["source_trace_sha256"]
    print(
        f"manifest_tree_digest generation_trace={trace_manifest_digest} "
        f"expected={expected_trace_manifest_digest} "
        f"match={trace_manifest_digest == expected_trace_manifest_digest}"
    )
    if trace_manifest_digest != expected_trace_manifest_digest:
        problems.append("generation trace manifest digest mismatch")

    for rel, expected in sorted(generation_result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / rel
        actual = sha256(path) if path.is_file() else "ABSENT"
        match = actual == expected
        print(f"generation_result_evidence path={path} actual={actual} expected={expected} match={match}")
        if not match:
            problems.append(f"generation-result evidence hash mismatch: {path}")

    task = json.loads(Path("/task.json").read_text())
    audit_manifest = audit.get("manifest", {})
    task_is_exact_subset = all(audit_manifest.get(key) == value for key, value in task.items())
    audit_only_keys = sorted(set(audit_manifest) - set(task))
    task_only_keys = sorted(set(task) - set(audit_manifest))
    print(f"task_json_is_exact_subset_of_audit_manifest={task_is_exact_subset}")
    print(f"audit_manifest_only_top_level_keys={audit_only_keys}")
    print(f"task_json_only_top_level_keys={task_only_keys}")
    if not task_is_exact_subset or task_only_keys:
        problems.append("task.json conflicts with audit-input manifest block")

    print(f"PROBLEM_COUNT={len(problems)}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
