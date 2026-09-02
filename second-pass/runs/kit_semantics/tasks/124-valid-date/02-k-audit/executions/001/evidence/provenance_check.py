#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        failures.append(f"unreadable/missing: {path}: {err}")
        return
    if stat.S_ISLNK(mode):
        failures.append(f"symlink where regular file required: {path}")
    elif not stat.S_ISREG(mode):
        failures.append(f"wrong type (not regular file): {path}")
    elif not os.access(path, os.R_OK):
        failures.append(f"not readable: {path}")


def require_directory(path: Path, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        failures.append(f"unreadable/missing: {path}: {err}")
        return
    if stat.S_ISLNK(mode):
        failures.append(f"symlink where directory required: {path}")
    elif not stat.S_ISDIR(mode):
        failures.append(f"wrong type (not directory): {path}")
    elif not os.access(path, os.R_OK | os.X_OK):
        failures.append(f"not readable/searchable: {path}")


def tree_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    entries: list[tuple[str, str, str | None]] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append((rel, "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append((rel, "directory", None))
        elif stat.S_ISREG(mode):
            entries.append((rel, "file", digest(path)))
        else:
            entries.append((rel, f"mode:{stat.S_IFMT(mode):o}", None))
    return entries


def manifest_digest(entries: list[tuple[str, str, str | None]]) -> str:
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    failures: list[str] = []
    require_regular(AUDIT_INPUT, failures)
    if failures:
        print("\n".join(failures))
        return 1

    audit = json.loads(AUDIT_INPUT.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("declared layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("rendered semantics mode is not SUPPLIED_SEMANTICS")

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path, failures)
    if lock_path.is_file():
        lock = json.loads(lock_path.read_text())
        if lock != audit.get("audit_campaign"):
            failures.append("campaign lock JSON differs from audit_campaign block")
        actual = digest(lock_path)
        expected = audit["hashes"]["audit_campaign_lock_sha256"]
        print(f"audit_campaign_lock_sha256={actual} expected={expected}")
        if actual != expected:
            failures.append("campaign lock hash mismatch")

    declared_directories = {
        "candidate",
        "generation_root",
        "generation_trace",
    }
    for name, raw_path in sorted(audit["container_paths"].items()):
        path = Path(raw_path)
        if name in declared_directories:
            require_directory(path, failures)
        else:
            require_regular(path, failures)
        print(f"container_path[{name}]={path}")

    required_pipeline_files = [
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
    ]
    for path in required_pipeline_files:
        require_regular(path, failures)

    recorded_hashes = {
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
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in recorded_hashes.items():
        require_regular(path, failures)
        if path.is_file():
            actual = digest(path)
            expected = audit["hashes"][key]
            print(f"{key}={actual} expected={expected}")
            if actual != expected:
                failures.append(f"hash mismatch for {path}")

    result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = result["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for relative, expected in sorted(evidence_hashes.items()):
        path = evidence_root / relative
        require_regular(path, failures)
        if path.is_file():
            actual = digest(path)
            print(f"generation_result[{relative}]={actual} expected={expected}")
            if actual != expected:
                failures.append(f"generation-result hash mismatch: {relative}")

    if digest(Path("/candidate/prompt.py")) != digest(Path("/reference/prompt.py")):
        failures.append("candidate prompt differs from trusted prompt")
    if digest(Path("/candidate/py2mpy.py")) != digest(Path("/reference/py2mpy.py")):
        failures.append("candidate translator differs from trusted translator")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    require_directory(trusted_semantics, failures)
    require_directory(candidate_semantics, failures)
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        trusted_entries = tree_manifest(trusted_semantics)
        candidate_entries = tree_manifest(candidate_semantics)
        print(f"trusted_semantics_entries={len(trusted_entries)}")
        print(f"candidate_semantics_entries={len(candidate_entries)}")
        print(f"trusted_semantics_auditor_manifest_sha256="
              f"{manifest_digest(trusted_entries)}")
        print(f"candidate_semantics_auditor_manifest_sha256="
              f"{manifest_digest(candidate_entries)}")
        if trusted_entries != candidate_entries:
            failures.append("candidate supplied-semantics tree differs by "
                            "path, type, symlink target, or bytes")
        if any(entry[1] == "symlink" for entry in candidate_entries):
            failures.append("candidate supplied-semantics tree contains symlinks")
        for rel, kind, item_digest in trusted_entries:
            if kind == "file":
                print(f"semantics_file {item_digest}  {rel}")

    proof_artifacts = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in proof_artifacts:
        require_regular(Path("/candidate") / name, failures)
    candidate_symlinks = [
        path.relative_to("/candidate").as_posix()
        for path in Path("/candidate").rglob("*")
        if path.is_symlink()
    ]
    print(f"candidate_symlinks={candidate_symlinks}")
    if candidate_symlinks:
        failures.append("candidate tree contains symlinks")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    if not trace_files:
        failures.append("structured trace directory contains no JSONL file")
    for trace in trace_files:
        type_counts: Counter[str] = Counter()
        payload_counts: Counter[str] = Counter()
        line_count = 0
        with trace.open() as stream:
            for line_count, line in enumerate(stream, 1):
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"malformed trace JSON at {trace}:{line_count}: {err}")
                    break
                type_counts[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
        print(f"trace={trace} lines={line_count} sha256={digest(trace)}")
        print(f"trace_top_types={dict(sorted(type_counts.items()))}")
        print(f"trace_payload_types={dict(sorted(payload_counts.items()))}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
