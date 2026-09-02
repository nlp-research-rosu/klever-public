#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe_tree(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    """Return typed entries and a reviewer-defined deterministic manifest hash."""
    entries: list[tuple[str, str, str]] = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = Path(current) / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries.append(("symlink", rel, os.readlink(path)))
            elif stat.S_ISDIR(mode):
                entries.append(("dir", rel, ""))
            elif stat.S_ISREG(mode):
                entries.append(("file", rel, sha256_file(path)))
            else:
                entries.append(("other", rel, oct(mode)))
    payload = "".join(
        f"{kind}\0{rel}\0{value}\n" for kind, rel, value in entries
    ).encode()
    return entries, hashlib.sha256(payload).hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    left_entries, _ = describe_tree(left)
    right_entries, _ = describe_tree(right)
    left_map = {(kind, rel): value for kind, rel, value in left_entries}
    right_map = {(kind, rel): value for kind, rel, value in right_entries}
    issues: list[str] = []
    for key in sorted(left_map.keys() | right_map.keys()):
        if key not in left_map:
            issues.append(f"missing from candidate: {key}")
        elif key not in right_map:
            issues.append(f"additional in candidate: {key}")
        elif left_map[key] != right_map[key]:
            issues.append(
                f"changed entry {key}: candidate={left_map[key]} trusted={right_map[key]}"
            )
    # Detect type changes at equal relative paths, which the typed-key map exposes
    # as two add/remove findings but deserves an explicit message too.
    left_type = {rel: kind for kind, rel, _ in left_entries}
    right_type = {rel: kind for kind, rel, _ in right_entries}
    for rel in sorted(left_type.keys() & right_type.keys()):
        if left_type[rel] != right_type[rel]:
            issues.append(
                f"mistyped entry {rel}: candidate={left_type[rel]} trusted={right_type[rel]}"
            )
    return issues


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/provenance_check.py")
    print("CHECK: launcher-owned JSON readability")
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print("audit-input readable: yes")
    print("audit-campaign-lock readable: yes")
    actual_lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign lock sha256 actual={actual_lock_hash}")
    print(f"campaign lock sha256 expected={expected_lock_hash}")
    print(f"campaign lock hash match={actual_lock_hash == expected_lock_hash}")
    print(f"campaign block exact match={lock == audit['audit_campaign']}")
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/reference/reference-semantics"),
        Path("/candidate"),
    ]
    print("CHECK: required mounts and records")
    for path in required:
        readable = os.access(path, os.R_OK)
        print(f"{path}: exists={path.exists()} readable={readable} symlink={path.is_symlink()}")

    file_hash_checks = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    print("CHECK: independently recomputed file hashes")
    for path, key in file_hash_checks.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        print(f"{path}: actual={actual} expected={expected} match={actual == expected}")

    print("CHECK: trusted/candidate byte identity")
    for candidate, trusted in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]:
        print(f"{candidate} == {trusted}: {candidate.read_bytes() == trusted.read_bytes()}")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    c_entries, c_hash = describe_tree(candidate_sem)
    t_entries, t_hash = describe_tree(trusted_sem)
    sem_issues = compare_trees(candidate_sem, trusted_sem)
    print("CHECK: supplied semantics recursive integrity")
    print(f"candidate typed-manifest sha256={c_hash}")
    print(f"trusted typed-manifest sha256={t_hash}")
    print(f"candidate entry count={len(c_entries)} trusted entry count={len(t_entries)}")
    print(f"candidate symlinks={[rel for kind, rel, _ in c_entries if kind == 'symlink']}")
    print(f"trusted symlinks={[rel for kind, rel, _ in t_entries if kind == 'symlink']}")
    print(f"semantic tree issues={len(sem_issues)}")
    for issue in sem_issues:
        print(f"SEMANTICS ISSUE: {issue}")

    trace_files = sorted(
        p for p in Path("/generation-evidence/codex-trace").rglob("*") if p.is_file()
    )
    print("CHECK: structured trace full JSONL parse")
    for trace in trace_files:
        counts: collections.Counter[str] = collections.Counter()
        invalid: list[int] = []
        lines = 0
        for lines, raw_line in enumerate(trace.open("r", encoding="utf-8"), start=1):
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError:
                invalid.append(lines)
                continue
            counts[str(record.get("type", "<missing>"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                counts[f"payload:{payload.get('type', '<missing>')}"] += 1
        print(
            f"{trace}: sha256={sha256_file(trace)} lines={lines} "
            f"invalid_json_lines={invalid} event_counts={dict(sorted(counts.items()))}"
        )

    evidence_outputs = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )["outputs"]["evidence"]
    print("CHECK: invocation-declared generation evidence hashes")
    for relative, expected in sorted(evidence_outputs.items()):
        path = Path("/generation-evidence") / relative
        actual = sha256_file(path)
        print(f"{relative}: actual={actual} expected={expected} match={actual == expected}")


if __name__ == "__main__":
    main()
