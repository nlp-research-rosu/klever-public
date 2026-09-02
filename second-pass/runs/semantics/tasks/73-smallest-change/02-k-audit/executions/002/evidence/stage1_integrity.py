#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_manifest(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    rows: list[tuple[str, str, str]] = []
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        names = sorted(dirnames + filenames)
        for name in names:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            value = sha256_file(path) if kind == "file" else (
                os.readlink(path) if kind == "symlink" else ""
            )
            rows.append((rel, kind, value))
    encoded = json.dumps(rows, separators=(",", ":"), ensure_ascii=True).encode()
    return rows, hashlib.sha256(encoded).hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required record: {path}")
    elif entry_kind(path) != "file":
        errors.append(f"required record is not a regular file: {path} ({entry_kind(path)})")
    elif not os.access(path, os.R_OK):
        errors.append(f"required record is unreadable: {path}")


def compare_trees(left: Path, right: Path, errors: list[str]) -> dict[str, Any]:
    left_rows, left_digest = tree_manifest(left)
    right_rows, right_digest = tree_manifest(right)
    left_map = {row[0]: row[1:] for row in left_rows}
    right_map = {row[0]: row[1:] for row in right_rows}
    missing = sorted(set(left_map) - set(right_map))
    additional = sorted(set(right_map) - set(left_map))
    changed = sorted(
        rel for rel in set(left_map) & set(right_map) if left_map[rel] != right_map[rel]
    )
    symlinks = sorted(
        rel
        for rel, (kind, _) in right_map.items()
        if kind == "symlink"
    )
    if missing:
        errors.append(f"candidate semantics missing entries: {missing}")
    if additional:
        errors.append(f"candidate semantics additional entries: {additional}")
    if changed:
        errors.append(f"candidate semantics changed/mistyped entries: {changed}")
    if symlinks:
        errors.append(f"candidate semantics symlink entries: {symlinks}")
    return {
        "trusted_entries": len(left_rows),
        "candidate_entries": len(right_rows),
        "trusted_normalized_tree_sha256": left_digest,
        "candidate_normalized_tree_sha256": right_digest,
        "missing": missing,
        "additional": additional,
        "changed_or_mistyped": changed,
        "candidate_symlinks": symlinks,
    }


def main() -> int:
    errors: list[str] = []
    for path in (AUDIT_INPUT, LOCK):
        require_regular(path, errors)
    if errors:
        print(json.dumps({"status": "INFRASTRUCTURE_BREACH", "errors": errors}, indent=2))
        return 2

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    if audit.get("audit_campaign") != lock:
        errors.append("audit campaign block does not structurally equal campaign lock")

    expected_lock_hash = audit.get("hashes", {}).get("audit_campaign_lock_sha256")
    actual_lock_hash = sha256_file(LOCK)
    if expected_lock_hash != actual_lock_hash:
        errors.append(
            f"campaign lock hash mismatch: expected {expected_lock_hash}, got {actual_lock_hash}"
        )

    layout = audit.get("record_layout")
    if layout != "legacy-selected-stage1":
        errors.append(f"unexpected record_layout for this audit: {layout!r}")

    container = audit.get("container_paths", {})
    required = [
        Path(container.get("run_manifest", "/missing-run-manifest")),
        Path(container.get("task_manifest", "/missing-task-manifest")),
        Path(container.get("stage1_result", "/missing-stage1-result")),
        Path(container.get("generation_manifest", "/missing-generation-manifest")),
        Path(container.get("generation_metrics", "/missing-generation-metrics")),
        Path(container.get("generation_last", "/missing-generation-last")),
        Path(container.get("generation_output", "/missing-generation-output")),
        Path(container.get("generation_root", "/missing-generation-root")) / "prompt.txt",
    ]
    usage = Path(container.get("generation_root", "/missing-generation-root")) / "usage.json"
    if usage.exists():
        required.append(usage)
    for path in required:
        require_regular(path, errors)

    trace_root = Path(container.get("generation_trace", "/missing-generation-trace"))
    if not trace_root.exists():
        errors.append(f"missing required structured trace: {trace_root}")
    elif entry_kind(trace_root) != "directory":
        errors.append(f"structured trace is not a directory: {trace_root}")
    elif not os.access(trace_root, os.R_OK):
        errors.append(f"structured trace is unreadable: {trace_root}")

    expected_hash_keys = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    direct_hashes: dict[str, dict[str, Any]] = {}
    for path, key in expected_hash_keys.items():
        if not path.exists() or entry_kind(path) != "file":
            continue
        actual = sha256_file(path)
        expected = audit.get("hashes", {}).get(key)
        match = actual == expected
        direct_hashes[str(path)] = {
            "expected_key": key,
            "expected": expected,
            "actual": actual,
            "match": match,
        }
        if not match:
            errors.append(f"hash mismatch for {path}: expected {expected}, got {actual}")

    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append(f"semantics mode mismatch: {audit.get('semantics_mode')!r}")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    for path, label in (
        (trusted_semantics, "trusted supplied semantics"),
        (candidate_semantics, "candidate supplied semantics"),
    ):
        if not path.exists():
            errors.append(f"missing {label}: {path}")
        elif entry_kind(path) != "directory":
            errors.append(f"{label} is not a directory: {path} ({entry_kind(path)})")
    semantics_comparison: dict[str, Any] = {}
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        semantics_comparison = compare_trees(trusted_semantics, candidate_semantics, errors)

    candidate_rows, candidate_normalized_digest = tree_manifest(Path("/candidate"))
    candidate_source_hashes = {
        row[0]: row[2]
        for row in candidate_rows
        if row[1] == "file"
        and (
            row[0].endswith(".k")
            or row[0].endswith(".mpy")
            or row[0].endswith(".py")
            or row[0].endswith(".sh")
        )
    }

    all_mount_roots = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference"),
        Path("/candidate"),
        Path("/generation-evidence"),
    ]
    mount_symlinks: list[str] = []
    for root in all_mount_roots:
        if entry_kind(root) == "symlink":
            mount_symlinks.append(str(root))
        elif root.is_dir():
            for current, dirnames, filenames in os.walk(root, followlinks=False):
                for name in dirnames + filenames:
                    path = Path(current) / name
                    if entry_kind(path) == "symlink":
                        mount_symlinks.append(str(path))

    task_manifest_match = False
    task_manifest_differences: dict[str, Any] = {}
    if Path("/task.json").is_file():
        task_record = json.loads(Path("/task.json").read_text())
        embedded_task = audit.get("manifest", {})
        task_manifest_match = task_record == embedded_task
        task_manifest_differences = {
            "only_in_task_record": sorted(set(task_record) - set(embedded_task)),
            "only_in_audit_envelope": sorted(set(embedded_task) - set(task_record)),
            "different_shared_keys": sorted(
                key
                for key in set(task_record) & set(embedded_task)
                if task_record[key] != embedded_task[key]
            ),
        }

    generation_result = (
        json.loads(Path("/generation-result.json").read_text())
        if Path("/generation-result.json").is_file()
        else {}
    )
    evidence_hashes = generation_result.get("outputs", {}).get("evidence", {})
    generation_evidence_checks: dict[str, Any] = {}
    generation_root = Path("/generation-evidence")
    for rel, expected in sorted(evidence_hashes.items()):
        path = generation_root / rel
        require_regular(path, errors)
        if path.is_file():
            actual = sha256_file(path)
            generation_evidence_checks[rel] = {
                "expected": expected,
                "actual": actual,
                "match": expected == actual,
            }
            if expected != actual:
                errors.append(
                    f"generation-result evidence hash mismatch for {rel}: "
                    f"expected {expected}, got {actual}"
                )

    # Fully consume and validate every structured-trace JSON line.
    trace_counts: Counter[str] = Counter()
    trace_files: list[dict[str, Any]] = []
    trace_parse_errors: list[str] = []
    if trace_root.is_dir():
        trace_paths = sorted(path for path in trace_root.rglob("*") if path.is_file())
        for path in trace_paths:
            line_count = 0
            with path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, 1):
                    line_count += 1
                    try:
                        record = json.loads(line)
                        trace_counts[str(record.get("type", "<missing>"))] += 1
                    except Exception as exc:
                        trace_parse_errors.append(f"{path}:{line_number}: {exc}")
            trace_files.append(
                {
                    "path": str(path.relative_to(trace_root)),
                    "bytes": path.stat().st_size,
                    "lines": line_count,
                    "sha256": sha256_file(path),
                }
            )
    if trace_parse_errors:
        errors.append(f"structured trace parse failures: {trace_parse_errors}")

    # Fully consume the large untrusted prose logs as bytes.
    consumed_logs: dict[str, Any] = {}
    for path in (
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ):
        if path.is_file():
            data = path.read_bytes()
            consumed_logs[str(path)] = {
                "bytes": len(data),
                "lines": data.count(b"\n"),
                "sha256": hashlib.sha256(data).hexdigest(),
            }

    result = {
        "status": "OK" if not errors else "INFRASTRUCTURE_BREACH",
        "record_layout": layout,
        "semantics_mode": audit.get("semantics_mode"),
        "campaign_structural_match": audit.get("audit_campaign") == lock,
        "campaign_hash_expected": expected_lock_hash,
        "campaign_hash_actual": actual_lock_hash,
        "task_manifest_structural_match": task_manifest_match,
        "task_manifest_top_level_differences": task_manifest_differences,
        "direct_hashes": direct_hashes,
        "semantics_comparison": semantics_comparison,
        "candidate_normalized_tree": {
            "entries": len(candidate_rows),
            "sha256": candidate_normalized_digest,
            "launcher_recorded_sha256": audit.get("hashes", {}).get("candidate_tree_sha256"),
            "note": "Independent normalized-manifest digest; the launcher tree digest uses its own encoding.",
        },
        "candidate_source_hashes": candidate_source_hashes,
        "all_mount_symlinks": sorted(mount_symlinks),
        "generation_result_evidence_hashes": generation_evidence_checks,
        "structured_trace_files": trace_files,
        "structured_trace_type_counts": dict(sorted(trace_counts.items())),
        "structured_trace_parse_errors": trace_parse_errors,
        "consumed_untrusted_logs": consumed_logs,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
