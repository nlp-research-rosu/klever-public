#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

The tree digest below is reviewer-defined: SHA-256 over sorted records of
relative path, entry type, mode, and (for regular files) content SHA-256.
It is recorded to make the exact mounted state independently reproducible;
recursive entry comparison, rather than agreement with an undocumented
launcher tree-hash algorithm, is the supplied-semantics integrity gate.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_records(root: Path) -> list[tuple[str, str, int, int, str]]:
    records: list[tuple[str, str, int, int, str]] = []
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        base = Path(current)
        for name in dirs + files:
            path = base / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            mode = stat.S_IMODE(info.st_mode)
            if stat.S_ISLNK(info.st_mode):
                kind = "symlink"
                value = os.readlink(path)
            elif stat.S_ISDIR(info.st_mode):
                kind = "dir"
                value = ""
            elif stat.S_ISREG(info.st_mode):
                kind = "file"
                value = file_sha256(path)
            else:
                kind = "other"
                value = ""
            records.append((rel, kind, mode, info.st_size, value))
    return records


def tree_digest(records: list[tuple[str, str, int, int, str]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(("\0".join(map(str, record)) + "\n").encode())
    return digest.hexdigest()


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    failures: list[str] = []

    print(f"audit-input sha256: {file_sha256(AUDIT_INPUT)}")
    actual_lock_hash = file_sha256(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign-lock sha256: {actual_lock_hash}")
    print(f"campaign-lock expected: {expected_lock_hash}")
    print(f"campaign object exact match: {lock == audit['audit_campaign']}")
    if actual_lock_hash != expected_lock_hash:
        failures.append("campaign-lock hash mismatch")
    if lock != audit["audit_campaign"]:
        failures.append("campaign object mismatch")

    mounted_hashes = {
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in mounted_hashes.items():
        expected = audit["hashes"][key]
        actual = file_sha256(path)
        ok = actual == expected
        print(f"{key}: {'MATCH' if ok else 'MISMATCH'} {actual} {path}")
        if not ok:
            failures.append(f"{key} mismatch")

    required_records = [
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
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_records:
        ok = path.exists() and os.access(path, os.R_OK)
        print(f"required readable: {ok} {path}")
        if not ok:
            failures.append(f"missing/unreadable required record {path}")

    candidate = entry_records(Path("/candidate/reference-semantics"))
    trusted = entry_records(Path("/reference/reference-semantics"))
    candidate_map = {record[0]: record[1:] for record in candidate}
    trusted_map = {record[0]: record[1:] for record in trusted}
    names = sorted(set(candidate_map) | set(trusted_map))
    differences = [
        (name, candidate_map.get(name), trusted_map.get(name))
        for name in names
        if candidate_map.get(name) != trusted_map.get(name)
    ]
    print(f"candidate semantics entries: {len(candidate)}")
    print(f"trusted semantics entries: {len(trusted)}")
    print(f"candidate semantics reviewer digest: {tree_digest(candidate)}")
    print(f"trusted semantics reviewer digest: {tree_digest(trusted)}")
    print(f"recursive semantics differences: {len(differences)}")
    for difference in differences:
        print(f"DIFFERENCE {difference!r}")
    if differences:
        failures.append("supplied-semantics recursive mismatch")

    candidate_tree = entry_records(Path("/candidate"))
    trace_tree = entry_records(Path("/generation-evidence/codex-trace"))
    print(f"candidate tree reviewer digest: {tree_digest(candidate_tree)}")
    print(f"candidate tree entries: {len(candidate_tree)}")
    print(f"generation trace reviewer digest: {tree_digest(trace_tree)}")
    print(f"generation trace entries: {len(trace_tree)}")
    unexpected_links = [
        f"/candidate/{record[0]}"
        for record in candidate_tree
        if record[1] == "symlink"
    ] + [
        f"/generation-evidence/codex-trace/{record[0]}"
        for record in trace_tree
        if record[1] == "symlink"
    ]
    print(f"symlinked candidate/trace entries: {len(unexpected_links)}")
    for link in unexpected_links:
        print(f"SYMLINK {link}")
    if unexpected_links:
        failures.append("unexpected symlink")

    print(f"FAILURE_COUNT: {len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
