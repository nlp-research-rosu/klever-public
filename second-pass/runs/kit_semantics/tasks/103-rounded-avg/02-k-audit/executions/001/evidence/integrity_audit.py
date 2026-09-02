#!/usr/bin/env python3
"""Independent mounted-input and supplied-semantics integrity checks."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory_tree(path: Path) -> tuple[str, list[str]]:
    """Hash a typed, relative-path-and-content inventory and report bad nodes."""
    digest = hashlib.sha256()
    bad: list[str] = []
    root_st = os.lstat(path)
    if not stat.S_ISDIR(root_st.st_mode) or stat.S_ISLNK(root_st.st_mode):
        return "", [f"root is not a real directory: {path}"]
    for current, dirs, files in os.walk(path, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        files.sort()
        for name in list(dirs):
            node = current_path / name
            node_st = os.lstat(node)
            rel = node.relative_to(path).as_posix()
            if stat.S_ISLNK(node_st.st_mode):
                bad.append(f"symlink directory: {rel} -> {os.readlink(node)}")
                dirs.remove(name)
            elif not stat.S_ISDIR(node_st.st_mode):
                bad.append(f"non-directory in dirs list: {rel}")
            else:
                digest.update(b"D\0" + rel.encode() + b"\0")
        for name in files:
            node = current_path / name
            node_st = os.lstat(node)
            rel = node.relative_to(path).as_posix()
            if stat.S_ISLNK(node_st.st_mode):
                bad.append(f"symlink file: {rel} -> {os.readlink(node)}")
                continue
            if not stat.S_ISREG(node_st.st_mode):
                bad.append(f"non-regular entry: {rel}")
                continue
            file_hash = sha256_file(node)
            digest.update(
                b"F\0"
                + rel.encode()
                + b"\0"
                + str(node_st.st_size).encode()
                + b"\0"
                + file_hash.encode()
                + b"\0"
            )
    return digest.hexdigest(), bad


def compare_trees(left: Path, right: Path) -> list[str]:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        found: dict[str, tuple[str, str | None]] = {}
        for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
            current_path = Path(current)
            dirs.sort()
            files.sort()
            for name in list(dirs):
                node = current_path / name
                rel = node.relative_to(root).as_posix()
                node_st = os.lstat(node)
                if stat.S_ISLNK(node_st.st_mode):
                    found[rel] = ("symlink", os.readlink(node))
                    dirs.remove(name)
                elif stat.S_ISDIR(node_st.st_mode):
                    found[rel] = ("dir", None)
                else:
                    found[rel] = ("other", None)
            for name in files:
                node = current_path / name
                rel = node.relative_to(root).as_posix()
                node_st = os.lstat(node)
                if stat.S_ISLNK(node_st.st_mode):
                    found[rel] = ("symlink", os.readlink(node))
                elif stat.S_ISREG(node_st.st_mode):
                    found[rel] = ("file", sha256_file(node))
                else:
                    found[rel] = ("other", None)
        return found

    l_entries = entries(left)
    r_entries = entries(right)
    differences: list[str] = []
    for rel in sorted(set(l_entries) | set(r_entries)):
        if rel not in l_entries:
            differences.append(f"missing from candidate: {rel} {r_entries[rel]}")
        elif rel not in r_entries:
            differences.append(f"additional in candidate: {rel} {l_entries[rel]}")
        elif l_entries[rel] != r_entries[rel]:
            differences.append(
                f"changed/mistyped: {rel} candidate={l_entries[rel]} trusted={r_entries[rel]}"
            )
    return differences


def require_regular(path: Path, failures: list[str]) -> None:
    try:
        node_st = os.lstat(path)
    except OSError as err:
        failures.append(f"absent/unreadable required file {path}: {err}")
        return
    if stat.S_ISLNK(node_st.st_mode) or not stat.S_ISREG(node_st.st_mode):
        failures.append(f"required file is not a real regular file: {path}")
        return
    try:
        with path.open("rb") as stream:
            stream.read(1)
    except OSError as err:
        failures.append(f"unreadable required file {path}: {err}")


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = audit["container_paths"]
    hashes = audit["hashes"]
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    print(f"campaign_json_equal={lock == audit['audit_campaign']}")
    if lock != audit["audit_campaign"]:
        failures.append("campaign lock JSON does not equal audit_input.audit_campaign")

    file_hash_checks = {
        lock_path: "audit_campaign_lock_sha256",
        Path(paths["canonical"]): "canonical_sha256",
        Path(paths["generation_last"]): "generation_codex_last_sha256",
        Path(paths["generation_manifest"]): "stage1_invocation_sha256",
        Path(paths["generation_metrics"]): "generation_metrics_sha256",
        Path(paths["generation_output"]): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path(paths["run_manifest"]): "run_manifest_sha256",
        Path(paths["stage1_result"]): "stage1_result_sha256",
        Path(paths["task_manifest"]): "task_manifest_sha256",
        Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
        Path(paths["translator"]): "trusted_translator_sha256",
        Path(paths["candidate"]) / "prompt.py": "candidate_prompt_sha256",
        Path(paths["candidate"]) / "py2mpy.py": "candidate_translator_sha256",
    }
    for path, key in file_hash_checks.items():
        require_regular(path, failures)
        if not path.is_file():
            continue
        actual = sha256_file(path)
        expected = hashes.get(key)
        match = actual == expected
        print(f"sha256 {path} actual={actual} recorded[{key}]={expected} match={match}")
        if not match:
            failures.append(f"recorded hash mismatch: {path} vs {key}")

    required_pipeline_v3 = [
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
    for path in required_pipeline_v3:
        require_regular(path, failures)

    trace_path = Path(paths["generation_trace"])
    trace_hash, trace_bad = inventory_tree(trace_path)
    print(f"reviewer_trace_inventory_sha256={trace_hash}")
    print(f"recorded_generation_trace_sha256={hashes.get('generation_codex_trace_sha256')}")
    for item in trace_bad:
        failures.append(f"trace integrity: {item}")

    candidate_root = Path(paths["candidate"])
    candidate_hash, candidate_bad = inventory_tree(candidate_root)
    print(f"reviewer_candidate_inventory_sha256={candidate_hash}")
    print(f"recorded_candidate_tree_sha256={hashes.get('candidate_tree_sha256')}")
    for item in candidate_bad:
        failures.append(f"candidate integrity: {item}")

    candidate_semantics = candidate_root / "reference-semantics"
    trusted_semantics = Path("/reference/reference-semantics")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("rendered mode is not SUPPLIED_SEMANTICS")
    if not trusted_semantics.is_dir():
        failures.append("trusted reference-semantics is absent in SUPPLIED_SEMANTICS mode")
    else:
        candidate_sem_hash, candidate_sem_bad = inventory_tree(candidate_semantics)
        trusted_sem_hash, trusted_sem_bad = inventory_tree(trusted_semantics)
        print(f"reviewer_candidate_semantics_inventory_sha256={candidate_sem_hash}")
        print(f"reviewer_trusted_semantics_inventory_sha256={trusted_sem_hash}")
        print(
            "recorded_candidate_semantics_sha256="
            f"{hashes.get('candidate_reference_semantics_sha256')}"
        )
        print(
            "recorded_trusted_semantics_sha256="
            f"{hashes.get('trusted_reference_semantics_sha256')}"
        )
        for item in candidate_sem_bad:
            failures.append(f"candidate semantics integrity: {item}")
        for item in trusted_sem_bad:
            failures.append(f"trusted semantics integrity: {item}")
        differences = compare_trees(candidate_semantics, trusted_semantics)
        print(f"semantics_tree_difference_count={len(differences)}")
        for difference in differences:
            failures.append(f"semantics difference: {difference}")

    exact_pairs = [
        (candidate_root / "prompt.py", Path(paths["trusted_prompt"]), "prompt"),
        (candidate_root / "py2mpy.py", Path(paths["translator"]), "translator"),
    ]
    for candidate_file, trusted_file, label in exact_pairs:
        same = (
            candidate_file.is_file()
            and trusted_file.is_file()
            and candidate_file.read_bytes() == trusted_file.read_bytes()
        )
        print(f"{label}_byte_equal={same}")
        if not same:
            failures.append(f"candidate {label} is not byte-identical to trusted input")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
