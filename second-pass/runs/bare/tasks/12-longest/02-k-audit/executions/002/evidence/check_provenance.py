#!/usr/bin/env python3
"""Independent checks of mounted audit records and declared SHA-256 values."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
import sys


AUDIT_INPUT = pathlib.Path("/audit-input.json")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report_file(label: str, path: pathlib.Path, expected: str | None) -> bool:
    if not path.exists() or not path.is_file() or path.is_symlink():
        print(f"{label}: BAD_TYPE_OR_MISSING path={path}")
        return False
    actual = sha(path)
    ok = expected is None or actual == expected
    print(
        f"{label}: {'OK' if ok else 'HASH_MISMATCH'} "
        f"path={path} sha256={actual} expected={expected}"
    )
    return ok


def inspect_tree(label: str, root: pathlib.Path) -> bool:
    ok = root.is_dir() and not root.is_symlink()
    print(f"{label}: root={root} root_ok={ok}")
    if not ok:
        return False
    entries: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        base = pathlib.Path(dirpath)
        for name in dirnames + filenames:
            path = base / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries.append(f"L {rel} -> {os.readlink(path)}")
                ok = False
            elif stat.S_ISDIR(mode):
                entries.append(f"D {rel}")
            elif stat.S_ISREG(mode):
                entries.append(
                    f"F {rel} mode={stat.S_IMODE(mode):04o} "
                    f"size={path.stat().st_size} sha256={sha(path)}"
                )
            else:
                entries.append(f"OTHER {rel} mode={mode:o}")
                ok = False
    for entry in entries:
        print(f"{label}_ENTRY: {entry}")
    manifest = ("\n".join(entries) + "\n").encode()
    print(f"{label}_INDEPENDENT_MANIFEST_SHA256={hashlib.sha256(manifest).hexdigest()}")
    return ok


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    hashes = data["hashes"]
    paths = {key: pathlib.Path(value) for key, value in data["container_paths"].items()}
    ok = True

    print(f"record_layout={data.get('record_layout')}")
    print(f"semantics_mode={data.get('semantics_mode')}")
    print(f"problem_id={data.get('problem_id')}")
    print(f"condition={data.get('condition')}")

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    campaign_equal = lock == data["audit_campaign"]
    print(f"campaign_lock_structural_match={campaign_equal}")
    ok &= campaign_equal

    checks = [
        ("audit_campaign_lock", paths["audit_campaign_lock"], hashes["audit_campaign_lock_sha256"]),
        ("run_manifest", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task_manifest", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("stage1_result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        ("generation_manifest", paths["generation_manifest"], hashes["stage1_invocation_sha256"]),
        ("generation_metrics", paths["generation_metrics"], hashes["generation_metrics_sha256"]),
        ("generation_last", paths["generation_last"], hashes["generation_codex_last_sha256"]),
        ("generation_output", paths["generation_output"], hashes["generation_codex_output_sha256"]),
        ("generation_prompt", paths["generation_root"] / "prompt.txt", hashes["generation_prompt_sha256"]),
        ("generation_usage", paths["generation_root"] / "usage.json", hashes["generation_usage_sha256"]),
        ("canonical", paths["canonical"], hashes["canonical_sha256"]),
        ("trusted_prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        ("trusted_translator", paths["translator"], hashes["trusted_translator_sha256"]),
        ("candidate_prompt", paths["candidate"] / "prompt.py", hashes["candidate_prompt_sha256"]),
        ("candidate_translator", paths["candidate"] / "py2mpy.py", hashes["candidate_translator_sha256"]),
    ]
    for args in checks:
        ok &= report_file(*args)

    trace_root = paths["generation_trace"]
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    print(f"trace_file_count={len(trace_files)}")
    for path in trace_files:
        print(f"TRACE_FILE path={path} sha256={sha(path)}")
    ok &= inspect_tree("candidate", paths["candidate"])
    ok &= inspect_tree("generation_trace", trace_root)

    trusted_semantics = pathlib.Path("/reference/reference-semantics")
    absent = not trusted_semantics.exists() and not trusted_semantics.is_symlink()
    print(f"generated_semantics_boundary_reference_tree_absent={absent}")
    ok &= absent

    candidate_prompt_equal = (
        (paths["candidate"] / "prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
    )
    candidate_translator_equal = (
        (paths["candidate"] / "py2mpy.py").read_bytes() == paths["translator"].read_bytes()
    )
    print(f"candidate_prompt_byte_identical={candidate_prompt_equal}")
    print(f"candidate_translator_byte_identical={candidate_translator_equal}")
    ok &= candidate_prompt_equal and candidate_translator_equal

    print(f"OVERALL={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
