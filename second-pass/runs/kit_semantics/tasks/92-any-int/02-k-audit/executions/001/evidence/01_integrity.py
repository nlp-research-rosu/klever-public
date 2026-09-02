#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_file(
    label: str, path: Path, expected_hash: str | None = None
) -> bool:
    if not path.is_file() or path.is_symlink():
        print(f"FAIL file {label}: path={path} regular={path.is_file()} symlink={path.is_symlink()}")
        return False
    actual_hash = sha256(path)
    matches = expected_hash is None or actual_hash == expected_hash
    print(
        f"{'PASS' if matches else 'FAIL'} file {label}: "
        f"path={path} sha256={actual_hash} expected={expected_hash}"
    )
    return matches


def tree_entries(root: Path) -> dict[str, tuple[str, int, str | None]]:
    entries: dict[str, tuple[str, int, str | None]] = {}
    for base, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        dirnames.sort()
        filenames.sort()
        for name in [*dirnames, *filenames]:
            path = Path(base) / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            mode = stat.S_IMODE(info.st_mode)
            if stat.S_ISLNK(info.st_mode):
                entries[rel] = ("symlink", mode, os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                entries[rel] = ("directory", mode, None)
            elif stat.S_ISREG(info.st_mode):
                entries[rel] = ("file", mode, sha256(path))
            else:
                entries[rel] = ("other", mode, None)
    return entries


def require_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def main() -> int:
    failures: list[str] = []
    audit = require_json(AUDIT_INPUT)
    lock = require_json(LOCK)
    if audit["audit_campaign"] == lock:
        print("PASS campaign block exactly equals /audit-campaign-lock.json")
    else:
        print("FAIL campaign block differs from /audit-campaign-lock.json")
        failures.append("campaign-block")

    hashes = audit["hashes"]
    checks = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        ("stage1_invocation", Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"]),
        ("generation_metrics", Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"]),
        ("generation_runtime_metrics", Path("/generation-evidence/runtime-metrics.json"), hashes["generation_runtime_metrics_sha256"]),
        ("generation_usage", Path("/generation-evidence/usage.json"), hashes["generation_usage_sha256"]),
        ("generation_prompt", Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"]),
        ("generation_last", Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"]),
        ("generation_output", Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"]),
    ]
    for label, path, expected in checks:
        if not check_file(label, path, expected):
            failures.append(label)

    required_layout_paths = [
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
    for path in required_layout_paths:
        try:
            path.read_bytes()
            print(f"PASS readable pipeline-v3 record: {path}")
        except OSError as err:
            print(f"FAIL unreadable pipeline-v3 record: {path}: {err}")
            failures.append(str(path))

    for path in required_layout_paths:
        if path.suffix == ".json":
            try:
                require_json(path)
                print(f"PASS valid JSON: {path}")
            except (OSError, UnicodeError, json.JSONDecodeError) as err:
                print(f"FAIL invalid JSON: {path}: {err}")
                failures.append(f"json:{path}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*"))
    regular_traces = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    bad_trace_entries = [path for path in trace_files if path.is_symlink() or (not path.is_file() and not path.is_dir())]
    if not regular_traces or bad_trace_entries:
        print(
            f"FAIL structured trace inventory: regular={len(regular_traces)} "
            f"bad={[str(path) for path in bad_trace_entries]}"
        )
        failures.append("trace-inventory")
    else:
        print(f"PASS structured trace inventory: regular_files={len(regular_traces)}")

    generation_result = require_json(Path("/generation-result.json"))
    declared_trace_hashes = {
        rel.removeprefix("codex-trace/"): value
        for rel, value in generation_result["outputs"]["evidence"].items()
        if rel.startswith("codex-trace/")
    }
    trace_event_types: Counter[str] = Counter()
    trace_lines = 0
    for path in regular_traces:
        rel = path.relative_to(trace_root).as_posix()
        actual = sha256(path)
        expected = declared_trace_hashes.get(rel)
        match = actual == expected
        print(
            f"{'PASS' if match else 'FAIL'} trace file: rel={rel} "
            f"sha256={actual} expected={expected}"
        )
        if not match:
            failures.append(f"trace-hash:{rel}")
        try:
            with path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    event = json.loads(line)
                    trace_lines += 1
                    trace_event_types[str(event.get("type", "<missing>"))] += 1
            print(f"PASS valid JSONL: {path} lines={line_number}")
        except (OSError, UnicodeError, json.JSONDecodeError) as err:
            print(f"FAIL invalid JSONL: {path}: {err}")
            failures.append(f"jsonl:{rel}")
    print(f"TRACE SUMMARY lines={trace_lines} top_level_types={dict(trace_event_types)}")

    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        print(f"FAIL rendered semantics mode: {audit['semantics_mode']}")
        failures.append("semantics-mode")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("FAIL trusted supplied semantics tree missing, mistyped, or symlinked")
        failures.append("trusted-semantics-root")
    trusted_entries = tree_entries(trusted_semantics)
    candidate_entries = tree_entries(candidate_semantics)
    semantic_equal = trusted_entries == candidate_entries
    print(
        f"{'PASS' if semantic_equal else 'FAIL'} supplied semantics recursive comparison: "
        f"trusted_entries={len(trusted_entries)} candidate_entries={len(candidate_entries)}"
    )
    for rel in sorted(set(trusted_entries) | set(candidate_entries)):
        if trusted_entries.get(rel) != candidate_entries.get(rel):
            print(
                f"SEMANTICS DIFF {rel}: trusted={trusted_entries.get(rel)} "
                f"candidate={candidate_entries.get(rel)}"
            )
    if not semantic_equal:
        failures.append("candidate-semantics")

    for candidate_path, trusted_path, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        same = candidate_path.read_bytes() == trusted_path.read_bytes()
        print(f"{'PASS' if same else 'FAIL'} candidate {label} byte identity")
        if not same:
            failures.append(label)

    candidate_entries_all = tree_entries(Path("/candidate"))
    bad_candidate_entries = [
        (rel, value) for rel, value in candidate_entries_all.items()
        if value[0] in {"symlink", "other"}
    ]
    print(
        f"{'PASS' if not bad_candidate_entries else 'FAIL'} candidate symlink/special-file scan: "
        f"entries={len(candidate_entries_all)} bad={bad_candidate_entries}"
    )
    if bad_candidate_entries:
        failures.append("candidate-special-entries")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
        "prompt.py",
        "py2mpy.py",
        "reference-semantics",
    ]
    for rel in required_candidate:
        path = Path("/candidate") / rel
        expected_dir = rel == "reference-semantics"
        valid = path.is_dir() if expected_dir else path.is_file()
        valid = valid and not path.is_symlink()
        print(f"{'PASS' if valid else 'FAIL'} required candidate artifact: {rel}")
        if not valid:
            failures.append(f"candidate:{rel}")

    print(f"FINAL failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
