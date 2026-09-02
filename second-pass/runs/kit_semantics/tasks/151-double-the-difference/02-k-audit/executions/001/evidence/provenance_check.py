#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def regular_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise RuntimeError(f"symlinked entry: {root}/{rel} -> {os.readlink(path)}")
        if path.is_file():
            result[rel] = sha256_file(path)
        elif not path.is_dir():
            raise RuntimeError(f"non-file/non-directory entry: {root}/{rel}")
    return result


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    expected = audit["hashes"]
    paths = audit["container_paths"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    if audit["record_layout"] != "pipeline-v3":
        print("ERROR: unexpected record layout")
        return 1
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        print("ERROR: unexpected semantics mode")
        return 1

    lock_path = Path(paths["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    lock_equal = lock == audit["audit_campaign"]
    print(f"campaign_lock_exact_match={lock_equal}")
    if not lock_equal:
        return 1

    checks = {
        "audit_campaign_lock_sha256": lock_path,
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
    }

    ok = True
    for key, path in checks.items():
        if not path.is_file() or path.is_symlink():
            print(f"{key}: ERROR missing, mistyped, or symlinked: {path}")
            ok = False
            continue
        actual = sha256_file(path)
        match = actual == expected[key]
        print(f"{key}: {actual} match={match} path={path}")
        ok &= match

    candidate = Path(paths["candidate"])
    prompt_match = (candidate / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes()
    translator_match = (candidate / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes()
    print(f"candidate_prompt_byte_match={prompt_match}")
    print(f"candidate_translator_byte_match={translator_match}")
    ok &= prompt_match and translator_match

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if not trusted_semantics.is_dir():
        print("ERROR: trusted supplied semantics mount is absent")
        return 1
    trusted_tree = regular_tree(trusted_semantics)
    candidate_tree = regular_tree(candidate_semantics)
    print(f"trusted_semantics_files={len(trusted_tree)}")
    print(f"candidate_semantics_files={len(candidate_tree)}")
    print(f"semantics_recursive_byte_match={trusted_tree == candidate_tree}")
    ok &= trusted_tree == candidate_tree
    for rel, digest in trusted_tree.items():
        print(f"semantics_file sha256={digest} path={rel}")

    trace_root = Path(paths["generation_trace"])
    trace_tree = regular_tree(trace_root)
    print(f"structured_trace_files={len(trace_tree)}")
    stage1_result = json.loads(Path(paths["stage1_result"]).read_text())
    recorded_trace = {
        key.removeprefix("codex-trace/"): value
        for key, value in stage1_result["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    }
    print(f"structured_trace_manifest_match={trace_tree == recorded_trace}")
    ok &= trace_tree == recorded_trace
    for rel, digest in trace_tree.items():
        print(f"trace_file sha256={digest} path={rel}")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for rel in required_candidate:
        path = candidate / rel
        good = path.is_file() and not path.is_symlink()
        print(f"required_candidate_artifact={rel} regular={good}")
        ok &= good
        if good:
            print(f"candidate_artifact sha256={sha256_file(path)} path={rel}")

    for root in (candidate, Path("/reference"), Path("/generation-evidence")):
        links = [p.as_posix() for p in root.rglob("*") if p.is_symlink()]
        print(f"symlinks_under={root} count={len(links)}")
        for link in links:
            print(f"  {link}")
        ok &= not links

    print(f"RESULT={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
