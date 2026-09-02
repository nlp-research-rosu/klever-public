#!/usr/bin/env python3
"""Independent launcher-record, mount, hash, and supplied-semantics checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(root: Path) -> tuple[str, int, int, int]:
    """Reviewer-defined deterministic digest over paths, types, and file bytes."""
    digest = hashlib.sha256()
    files = directories = symlinks = 0
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirnames.sort()
        filenames.sort()
        for name in dirnames + filenames:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                kind = b"L"
                payload = os.readlink(path).encode()
                symlinks += 1
            elif path.is_dir():
                kind = b"D"
                payload = b""
                directories += 1
            elif path.is_file():
                kind = b"F"
                payload = bytes.fromhex(sha256(path))
                files += 1
            else:
                kind = b"?"
                payload = b""
            digest.update(kind + b"\0" + relative.encode() + b"\0" + payload + b"\0")
    return digest.hexdigest(), files, directories, symlinks


def require_regular(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing: {path}")
    elif path.is_symlink():
        failures.append(f"symlinked: {path}")
    elif not path.is_file():
        failures.append(f"mistyped non-file: {path}")
    elif not os.access(path, os.R_OK):
        failures.append(f"unreadable: {path}")


def compare_trees(left: Path, right: Path, failures: list[str]) -> None:
    left_entries = {
        p.relative_to(left).as_posix(): p for p in left.rglob("*")
    }
    right_entries = {
        p.relative_to(right).as_posix(): p for p in right.rglob("*")
    }
    if set(left_entries) != set(right_entries):
        failures.append(
            f"semantics entry-set mismatch: left-only={sorted(set(left_entries)-set(right_entries))}, "
            f"right-only={sorted(set(right_entries)-set(left_entries))}"
        )
    for relative in sorted(set(left_entries) & set(right_entries)):
        first, second = left_entries[relative], right_entries[relative]
        first_kind = (
            "symlink" if first.is_symlink() else "dir" if first.is_dir()
            else "file" if first.is_file() else "other"
        )
        second_kind = (
            "symlink" if second.is_symlink() else "dir" if second.is_dir()
            else "file" if second.is_file() else "other"
        )
        if first_kind != second_kind:
            failures.append(f"semantics type mismatch {relative}: {first_kind} != {second_kind}")
        elif first_kind == "symlink":
            failures.append(f"semantics symlink forbidden: {relative}")
        elif first_kind == "file" and sha256(first) != sha256(second):
            failures.append(f"semantics content mismatch: {relative}")


def main() -> int:
    failures: list[str] = []
    audit_input_path = Path("/audit-input.json")
    lock_path = Path("/audit-campaign-lock.json")
    require_regular(audit_input_path, failures)
    require_regular(lock_path, failures)
    audit_input = json.loads(audit_input_path.read_text())
    lock = json.loads(lock_path.read_text())

    if audit_input["record_layout"] != "pipeline-v3":
        failures.append(f"unexpected record layout: {audit_input['record_layout']}")
    if audit_input["semantics_mode"] != "SUPPLIED_SEMANTICS":
        failures.append(f"unexpected semantics mode: {audit_input['semantics_mode']}")
    if audit_input["audit_campaign"] != lock:
        failures.append("campaign-lock object differs from audit_campaign")

    paths = audit_input["container_paths"]
    for name, raw in sorted(paths.items()):
        path = Path(raw)
        if not path.exists():
            failures.append(f"launcher-declared mount missing: {name}={path}")
        elif not os.access(path, os.R_OK):
            failures.append(f"launcher-declared mount unreadable: {name}={path}")

    required_pipeline_files = [
        Path("/run.json"), Path("/task.json"), Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_pipeline_files:
        require_regular(path, failures)

    hash_checks = [
        (lock_path, "audit_campaign_lock_sha256"),
        (Path("/reference/canonical.py"), "canonical_sha256"),
        (Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        (Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        (Path("/run.json"), "run_manifest_sha256"),
        (Path("/task.json"), "task_manifest_sha256"),
        (Path("/generation-result.json"), "stage1_result_sha256"),
        (Path("/generation-evidence/invocation.json"), "stage1_invocation_sha256"),
        (Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
        (Path("/generation-evidence/runtime-metrics.json"), "generation_runtime_metrics_sha256"),
        (Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
        (Path("/generation-evidence/codex-last.txt"), "generation_codex_last_sha256"),
        (Path("/generation-evidence/codex-output.log"), "generation_codex_output_sha256"),
        (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
    ]
    checked_hashes = []
    for path, key in hash_checks:
        actual = sha256(path)
        expected = audit_input["hashes"][key]
        checked_hashes.append({"path": str(path), "actual": actual, "recorded": expected})
        if actual != expected:
            failures.append(f"hash mismatch {path}: {actual} != {expected}")

    trace_root = Path(paths["generation_trace"])
    trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
    declared_evidence = json.loads(Path("/generation-result.json").read_text())["outputs"]["evidence"]
    trace_records = []
    for trace_path in trace_files:
        relative = trace_path.relative_to(Path("/generation-evidence")).as_posix()
        actual = sha256(trace_path)
        expected = declared_evidence.get(relative)
        if expected is None:
            failures.append(f"undeclared structured trace file: {relative}")
        elif actual != expected:
            failures.append(f"trace hash mismatch: {relative}")
        json_types: collections.Counter[str] = collections.Counter()
        line_count = 0
        for line_count, line in enumerate(trace_path.read_text().splitlines(), 1):
            record = json.loads(line)
            json_types[record.get("type", "?")] += 1
        trace_records.append({
            "path": str(trace_path), "sha256": actual, "lines": line_count,
            "record_types": dict(json_types),
        })

    candidate = Path(paths["candidate"])
    for name in (
        "solution.py", "solution.mpy", "verification.k", "spec.k",
        "prove.sh", "PROOF.md", "prompt.py", "py2mpy.py",
    ):
        require_regular(candidate / name, failures)

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if not trusted_semantics.is_dir():
        failures.append("SUPPLIED_SEMANTICS trusted tree missing or mistyped")
    if not candidate_semantics.is_dir():
        failures.append("candidate reference-semantics missing or mistyped")
    compare_trees(trusted_semantics, candidate_semantics, failures)

    if sha256(Path("/reference/prompt.py")) != sha256(candidate / "prompt.py"):
        failures.append("candidate prompt differs from trusted prompt")
    if sha256(Path("/reference/py2mpy.py")) != sha256(candidate / "py2mpy.py"):
        failures.append("candidate translator differs from trusted translator")

    trusted_tree = tree_digest(trusted_semantics)
    candidate_semantics_tree = tree_digest(candidate_semantics)
    candidate_tree = tree_digest(candidate)
    if trusted_tree[0] != candidate_semantics_tree[0]:
        failures.append("reviewer-defined supplied-semantics tree digest mismatch")

    print(json.dumps({
        "record_layout": audit_input["record_layout"],
        "semantics_mode": audit_input["semantics_mode"],
        "campaign_object_equal": audit_input["audit_campaign"] == lock,
        "checked_hashes": checked_hashes,
        "trace_records": trace_records,
        "trusted_semantics_tree_digest": trusted_tree,
        "candidate_semantics_tree_digest": candidate_semantics_tree,
        "candidate_full_tree_independent_digest": candidate_tree,
        "candidate_prompt_byte_equal": sha256(Path("/reference/prompt.py"))
        == sha256(candidate / "prompt.py"),
        "candidate_translator_byte_equal": sha256(Path("/reference/py2mpy.py"))
        == sha256(candidate / "py2mpy.py"),
        "failure_count": len(failures),
        "failures": failures,
    }, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
