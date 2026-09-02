#!/usr/bin/env python3
"""Independent integrity checks for the launcher mounts and supplied semantics."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path: Path) -> str:
    info = path.lstat()
    if stat.S_ISREG(info.st_mode):
        kind = "regular"
    elif stat.S_ISDIR(info.st_mode):
        kind = "directory"
    elif stat.S_ISLNK(info.st_mode):
        kind = "symlink"
    else:
        kind = f"other(mode={oct(info.st_mode)})"
    return f"{kind}, readable={os.access(path, os.R_OK)}, size={info.st_size}"


def tree_entries(root: Path) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        names = sorted(dirnames + filenames)
        for name in names:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                entries[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                entries[rel] = ("directory", "")
            elif stat.S_ISREG(info.st_mode):
                entries[rel] = ("regular", sha256_file(path))
            else:
                entries[rel] = ("other", oct(info.st_mode))
    return entries


def reviewer_tree_digest(entries: dict[str, tuple[str, str]]) -> str:
    """Review-local deterministic digest; direct comparisons do not depend on it."""
    digest = hashlib.sha256()
    for rel, (kind, value) in sorted(entries.items()):
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def main() -> int:
    failures: list[str] = []
    if not AUDIT_INPUT.is_file():
        print("INFRASTRUCTURE FAILURE: /audit-input.json is absent or not regular")
        return 2
    audit = json.loads(AUDIT_INPUT.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    print(f"condition={audit.get('condition')}")

    required = [
        Path("/candidate"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/reference/reference-semantics"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation/invocation.json"),
        Path("/generation/metrics.json"),
        Path("/generation/runtime-metrics.json"),
        Path("/generation/usage.json"),
        Path("/generation/codex-last.txt"),
        Path("/generation/codex-output.log"),
        Path("/generation/prompt.txt"),
        Path("/generation/codex-trace"),
    ]
    print("REQUIRED MOUNT/RECORD TYPES")
    for path in required:
        try:
            print(f"{path}: {describe(path)}")
            if not os.access(path, os.R_OK):
                fail(f"unreadable required path: {path}", failures)
        except FileNotFoundError:
            fail(f"missing required path: {path}", failures)

    if audit.get("record_layout") != "pipeline-v3":
        fail("declared record layout is not pipeline-v3", failures)
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        fail("rendered semantics mode is not SUPPLIED_SEMANTICS", failures)

    file_hash_fields = {
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation/invocation.json": "stage1_invocation_sha256",
        "/generation/metrics.json": "generation_metrics_sha256",
        "/generation/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation/usage.json": "generation_usage_sha256",
        "/generation/codex-last.txt": "generation_codex_last_sha256",
        "/generation/codex-output.log": "generation_codex_output_sha256",
        "/generation/prompt.txt": "generation_prompt_sha256",
    }
    print("RECORDED FILE HASH CHECKS")
    for raw_path, field in file_hash_fields.items():
        path = Path(raw_path)
        if not path.is_file() or path.is_symlink():
            fail(f"required regular non-symlink file missing/mistyped: {path}", failures)
            continue
        actual = sha256_file(path)
        expected = audit["hashes"].get(field)
        status_text = "MATCH" if actual == expected else "MISMATCH"
        print(f"{path}: sha256={actual} recorded[{field}]={expected} {status_text}")
        if actual != expected:
            fail(f"recorded hash mismatch for {path}", failures)

    print("CANDIDATE TRUSTED-INPUT BYTE COMPARISONS")
    for candidate, trusted in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]:
        same = candidate.read_bytes() == trusted.read_bytes()
        print(f"{candidate} == {trusted}: {same}")
        if not same:
            fail(f"candidate protected input differs: {candidate}", failures)

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    print("SUPPLIED SEMANTICS RECURSIVE COMPARISON")
    print(f"candidate entry count={len(candidate_semantics)}")
    print(f"trusted entry count={len(trusted_semantics)}")
    print(f"candidate reviewer_tree_sha256={reviewer_tree_digest(candidate_semantics)}")
    print(f"trusted reviewer_tree_sha256={reviewer_tree_digest(trusted_semantics)}")
    for rel in sorted(candidate_semantics.keys() | trusted_semantics.keys()):
        candidate_entry = candidate_semantics.get(rel)
        trusted_entry = trusted_semantics.get(rel)
        if candidate_entry != trusted_entry:
            fail(
                f"reference semantics mismatch at {rel}: "
                f"candidate={candidate_entry}, trusted={trusted_entry}",
                failures,
            )
    candidate_symlinks = [
        rel for rel, (kind, _) in candidate_semantics.items() if kind == "symlink"
    ]
    print(f"candidate reference-semantics symlinks={candidate_symlinks}")
    if candidate_symlinks:
        fail("candidate reference semantics contains symlinks", failures)

    whole_candidate = tree_entries(Path("/candidate"))
    all_candidate_symlinks = [
        rel for rel, (kind, _) in whole_candidate.items() if kind == "symlink"
    ]
    print("CANDIDATE TREE SUMMARY")
    print(f"entry count={len(whole_candidate)}")
    print(f"reviewer_tree_sha256={reviewer_tree_digest(whole_candidate)}")
    print(f"symlinks={all_candidate_symlinks}")
    if all_candidate_symlinks:
        fail("candidate tree contains symlink entries", failures)

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    print("REQUIRED CANDIDATE PROOF ARTIFACT TYPES")
    for name in required_candidate:
        path = Path("/candidate") / name
        try:
            print(f"{path}: {describe(path)}")
            if not path.is_file() or path.is_symlink():
                fail(f"required candidate proof artifact is absent/mistyped: {path}", failures)
        except FileNotFoundError:
            fail(f"required candidate proof artifact missing: {path}", failures)

    generation_result = json.loads(Path("/generation-result.json").read_text())
    print("GENERATION EVIDENCE HASH CHECKS")
    evidence = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(evidence.items()):
        path = Path("/generation") / relative
        if not path.is_file() or path.is_symlink():
            fail(f"generation evidence missing/mistyped: {path}", failures)
            continue
        actual = sha256_file(path)
        status_text = "MATCH" if actual == expected else "MISMATCH"
        print(f"{path}: sha256={actual} result={expected} {status_text}")
        if actual != expected:
            fail(f"generation evidence hash mismatch: {path}", failures)

    trace_root = Path("/generation/codex-trace")
    trace_entries = tree_entries(trace_root)
    trace_files = [
        rel for rel, (kind, _) in trace_entries.items() if kind == "regular"
    ]
    print("STRUCTURED TRACE SUMMARY")
    print(f"regular files={trace_files}")
    print(f"reviewer_tree_sha256={reviewer_tree_digest(trace_entries)}")
    if not trace_files:
        fail("structured trace has no regular files", failures)
    for rel in trace_files:
        path = trace_root / rel
        line_count = 0
        with path.open("r", encoding="utf-8") as stream:
            for line_count, line in enumerate(stream, start=1):
                try:
                    json.loads(line)
                except json.JSONDecodeError as err:
                    fail(f"invalid JSONL {path}:{line_count}: {err}", failures)
        print(f"{path}: parsed_json_lines={line_count}")

    print(f"TOTAL_FAILURES={len(failures)}")
    for message in failures:
        print(f"FAILURE_SUMMARY: {message}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
