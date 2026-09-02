#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

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


def regular_file(path: Path) -> bool:
    return stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink()


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {str(p.relative_to(left)): p for p in left.rglob("*")}
    right_entries = {str(p.relative_to(right)): p for p in right.rglob("*")}
    if left_entries.keys() != right_entries.keys():
        problems.append(
            f"entry-set mismatch: only-left={sorted(left_entries.keys() - right_entries.keys())}, "
            f"only-right={sorted(right_entries.keys() - left_entries.keys())}"
        )
    for rel in sorted(left_entries.keys() & right_entries.keys()):
        lpath, rpath = left_entries[rel], right_entries[rel]
        lmode, rmode = lpath.lstat().st_mode, rpath.lstat().st_mode
        ltype = stat.S_IFMT(lmode)
        rtype = stat.S_IFMT(rmode)
        if ltype != rtype:
            problems.append(f"type mismatch: {rel}")
        if lpath.is_symlink() or rpath.is_symlink():
            problems.append(f"symlink entry: {rel}")
        if stat.S_ISREG(lmode) and stat.S_ISREG(rmode):
            lhash, rhash = sha256(lpath), sha256(rpath)
            if lhash != rhash:
                problems.append(f"content mismatch: {rel}: {lhash} != {rhash}")
    return problems


def check_hash(label: str, path: Path, expected: str) -> bool:
    if not regular_file(path):
        print(f"FAIL {label}: absent, non-regular, or symlinked: {path}")
        return False
    actual = sha256(path)
    okay = actual == expected
    print(f"{'PASS' if okay else 'FAIL'} {label}: expected={expected} actual={actual} path={path}")
    return okay


def main() -> int:
    source = json.loads(AUDIT_INPUT.read_text())
    hashes = source["hashes"]
    failures = 0

    print(f"record_layout={source['record_layout']}")
    print(f"semantics_mode={source['semantics_mode']}")
    if source["record_layout"] != "legacy-selected-stage1":
        print("FAIL unexpected record layout")
        failures += 1
    if source["semantics_mode"] != "SUPPLIED_SEMANTICS":
        print("FAIL unexpected semantics mode")
        failures += 1

    lock_path = Path(source["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    if lock == source["audit_campaign"]:
        print("PASS campaign lock JSON equals audit-input audit_campaign block")
    else:
        print("FAIL campaign lock JSON differs from audit-input audit_campaign block")
        failures += 1

    direct_hashes = [
        ("audit campaign lock", lock_path, hashes["audit_campaign_lock_sha256"]),
        ("run manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1 result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        ("stage1 invocation", Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"]),
        ("generation metrics", Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"]),
        ("generation last", Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"]),
        ("generation output", Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"]),
        ("generation prompt", Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"]),
        ("generation usage", Path("/generation-evidence/usage.json"), hashes["generation_usage_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("candidate prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("trusted translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
    ]
    for label, path, expected in direct_hashes:
        failures += not check_hash(label, path, expected)

    for candidate, trusted, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        if candidate.read_bytes() == trusted.read_bytes():
            print(f"PASS candidate {label} is byte-identical to trusted {label}")
        else:
            print(f"FAIL candidate {label} differs from trusted {label}")
            failures += 1

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("FAIL supplied trusted reference semantics is absent or symlinked")
        failures += 1
    problems = compare_trees(candidate_semantics, trusted_semantics)
    if problems:
        for problem in problems:
            print(f"FAIL reference-semantics integrity: {problem}")
        failures += len(problems)
    else:
        entries = list(trusted_semantics.rglob("*"))
        print(
            "PASS candidate reference-semantics recursively matches trusted tree "
            f"({sum(p.is_dir() for p in entries)} directories, "
            f"{sum(p.is_file() for p in entries)} regular files, no symlinks)"
        )

    generation_result = json.loads(Path("/generation-result.json").read_text())
    declared = generation_result["outputs"]["evidence"]
    for relpath, expected in sorted(declared.items()):
        failures += not check_hash(
            f"generation-result evidence {relpath}",
            Path("/generation-evidence") / relpath,
            expected,
        )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    if not trace_files:
        print("FAIL no structured trace JSONL")
        failures += 1
    for trace_file in trace_files:
        counts: Counter[str] = Counter()
        line_count = 0
        with trace_file.open() as stream:
            for line_count, line in enumerate(stream, 1):
                event = json.loads(line)
                counts[str(event.get("type", "<missing>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    counts[f"payload:{payload.get('type', '<missing>')}"] += 1
        print(
            f"PASS parsed complete structured trace {trace_file.relative_to(trace_root)}: "
            f"lines={line_count}, event_counts={dict(sorted(counts.items()))}"
        )

    required_legacy_selected = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_legacy_selected:
        if not regular_file(path):
            print(f"FAIL required legacy-selected-stage1 record absent or invalid: {path}")
            failures += 1
    print(
        "INFO runtime-metrics.json is absent; it is not required for "
        "legacy-selected-stage1 historical records"
    )
    print(f"SUMMARY failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
