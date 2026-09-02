#!/usr/bin/env python3
"""Independent mounted-input and supplied-semantics integrity audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            if entry_kind == "file":
                detail = sha256(path)
            elif entry_kind == "symlink":
                detail = os.readlink(path)
            else:
                detail = "-"
            entries[rel] = (entry_kind, detail)
    return entries


def tree_manifest_hash(entries: dict[str, tuple[str, str]]) -> str:
    payload = "".join(
        f"{name}\t{entry_kind}\t{detail}\n"
        for name, (entry_kind, detail) in sorted(entries.items())
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    expected = audit["hashes"]
    container_paths = audit["container_paths"]

    print("record_layout", audit["record_layout"])
    print("semantics_mode", audit["semantics_mode"])
    print("mount_reference_semantics", audit["mount_reference_semantics"])

    required = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": LOCK,
        "candidate": Path(container_paths["candidate"]),
        "canonical": Path(container_paths["canonical"]),
        "trusted_prompt": Path(container_paths["trusted_prompt"]),
        "translator": Path(container_paths["translator"]),
        "run_manifest": Path(container_paths["run_manifest"]),
        "task_manifest": Path(container_paths["task_manifest"]),
        "stage1_result": Path(container_paths["stage1_result"]),
        "generation_manifest": Path(container_paths["generation_manifest"]),
        "generation_metrics": Path(container_paths["generation_metrics"]),
        "generation_last": Path(container_paths["generation_last"]),
        "generation_output": Path(container_paths["generation_output"]),
        "generation_prompt": Path(container_paths["generation_root"]) / "prompt.txt",
        "generation_trace": Path(container_paths["generation_trace"]),
    }
    usage = Path(container_paths["generation_root"]) / "usage.json"
    if usage.exists():
        required["generation_usage"] = usage

    print("\nREQUIRED PATHS")
    missing = []
    for name, path in required.items():
        present = path.exists()
        readable = os.access(path, os.R_OK)
        print(name, kind(path) if present else "missing", readable, path)
        if not present or not readable:
            missing.append(name)

    print("\nRECORDED FILE HASH CHECKS")
    checks = {
        "audit_campaign_lock_sha256": LOCK,
        "canonical_sha256": Path(container_paths["canonical"]),
        "trusted_prompt_sha256": Path(container_paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(container_paths["translator"]),
        "candidate_prompt_sha256": Path(container_paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(container_paths["candidate"]) / "py2mpy.py",
        "run_manifest_sha256": Path(container_paths["run_manifest"]),
        "task_manifest_sha256": Path(container_paths["task_manifest"]),
        "stage1_result_sha256": Path(container_paths["stage1_result"]),
        "stage1_invocation_sha256": Path(container_paths["generation_manifest"]),
        "generation_metrics_sha256": Path(container_paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(container_paths["generation_last"]),
        "generation_codex_output_sha256": Path(container_paths["generation_output"]),
        "generation_prompt_sha256": Path(container_paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": usage,
    }
    hash_failures = []
    for key, path in checks.items():
        actual = sha256(path) if path.is_file() else "MISSING_OR_NOT_FILE"
        wanted = expected.get(key, "NO_RECORDED_HASH")
        matches = actual == wanted
        print(key, "MATCH" if matches else "MISMATCH", "actual", actual, "expected", wanted)
        if not matches:
            hash_failures.append(key)

    trace_files = sorted(
        path
        for path in Path(container_paths["generation_trace"]).rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    print("\nTRACE FILES")
    for path in trace_files:
        print(path.relative_to(container_paths["generation_trace"]), sha256(path), path.stat().st_size)

    print("\nCAMPAIGN")
    block_match = lock == audit["audit_campaign"]
    lock_hash_match = sha256(LOCK) == expected["audit_campaign_lock_sha256"]
    print("block_match", block_match)
    print("lock_hash_match", lock_hash_match)

    print("\nTRUSTED/CANDIDATE PROMPT+TRANSLATOR")
    candidate = Path(container_paths["candidate"])
    pairs = [
        (candidate / "prompt.py", Path(container_paths["trusted_prompt"])),
        (candidate / "py2mpy.py", Path(container_paths["translator"])),
    ]
    pair_failures = []
    for left, right in pairs:
        match = left.read_bytes() == right.read_bytes()
        print(left.name, "BYTE_IDENTICAL" if match else "DIFFERENT", sha256(left), sha256(right))
        if not match:
            pair_failures.append(left.name)

    print("\nSUPPLIED SEMANTICS TREE")
    candidate_root = candidate / "reference-semantics"
    trusted_root = Path("/reference/reference-semantics")
    candidate_entries = tree_entries(candidate_root)
    trusted_entries = tree_entries(trusted_root)
    all_names = sorted(set(candidate_entries) | set(trusted_entries))
    tree_failures = []
    for name in all_names:
        candidate_entry = candidate_entries.get(name)
        trusted_entry = trusted_entries.get(name)
        if candidate_entry != trusted_entry:
            tree_failures.append(name)
            print("DIFFERENCE", name, "candidate", candidate_entry, "trusted", trusted_entry)
    print("candidate_entry_count", len(candidate_entries))
    print("trusted_entry_count", len(trusted_entries))
    print("candidate_manifest_hash", tree_manifest_hash(candidate_entries))
    print("trusted_manifest_hash", tree_manifest_hash(trusted_entries))
    print("recorded_candidate_tree_hash", expected["candidate_reference_semantics_sha256"])
    print("recorded_trusted_tree_hash", expected["trusted_reference_semantics_sha256"])
    print("tree_comparison", "IDENTICAL" if not tree_failures else "DIFFERENT")
    print("candidate_symlinks", [name for name, value in candidate_entries.items() if value[0] == "symlink"])
    print("trusted_symlinks", [name for name, value in trusted_entries.items() if value[0] == "symlink"])

    failures = missing + hash_failures + pair_failures + tree_failures
    print("\nSUMMARY")
    print("failure_count", len(failures))
    print("status", "PASS" if not failures and block_match and lock_hash_match else "FAIL")
    return 0 if not failures and block_match and lock_hash_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
