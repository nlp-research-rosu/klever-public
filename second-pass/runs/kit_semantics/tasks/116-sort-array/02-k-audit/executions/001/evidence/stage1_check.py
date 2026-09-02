#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def kind(path: Path) -> str:
    mode = os.lstat(path).st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    actual = sha256_file(path)
    matches = expected is None or actual == expected
    print(
        f"HASH {label}: actual={actual} expected={expected or 'UNRECORDED'} "
        f"match={matches}"
    )
    return matches


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        entry_kind = kind(path)
        if entry_kind == "regular":
            result[rel] = (entry_kind, sha256_file(path))
        elif entry_kind == "symlink":
            result[rel] = (entry_kind, os.readlink(path))
        else:
            result[rel] = (entry_kind, None)
    return result


def compare_trees(left: Path, right: Path) -> bool:
    left_manifest = tree_manifest(left)
    right_manifest = tree_manifest(right)
    all_names = sorted(set(left_manifest) | set(right_manifest))
    differences = 0
    symlinks = 0
    for name in all_names:
        left_entry = left_manifest.get(name)
        right_entry = right_manifest.get(name)
        if (left_entry and left_entry[0] == "symlink") or (
            right_entry and right_entry[0] == "symlink"
        ):
            symlinks += 1
        if left_entry != right_entry:
            differences += 1
            print(f"TREE_DIFF {name}: candidate={left_entry} trusted={right_entry}")
    regular_files = sum(1 for value in left_manifest.values() if value[0] == "regular")
    directories = sum(1 for value in left_manifest.values() if value[0] == "directory")
    print(
        "TREE_COMPARE reference-semantics: "
        f"candidate_entries={len(left_manifest)} trusted_entries={len(right_manifest)} "
        f"candidate_files={regular_files} candidate_dirs={directories} "
        f"symlink_entries={symlinks} differences={differences}"
    )
    return differences == 0 and symlinks == 0


def main() -> int:
    audit = load_json(AUDIT_INPUT)
    paths = audit["container_paths"]
    hashes = audit["hashes"]
    print(
        f"DECLARATION record_layout={audit['record_layout']} "
        f"semantics_mode={audit['semantics_mode']} "
        f"problem_id={audit['problem_id']} condition={audit['condition']}"
    )

    required_files = {
        "audit_input": AUDIT_INPUT,
        "campaign_lock": Path(paths["audit_campaign_lock"]),
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_invocation": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path(paths["canonical"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "translator": Path(paths["translator"]),
        "candidate_prompt": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator": Path(paths["candidate"]) / "py2mpy.py",
    }
    required_dirs = {
        "candidate": Path(paths["candidate"]),
        "generation_root": Path(paths["generation_root"]),
        "generation_trace": Path(paths["generation_trace"]),
        "trusted_reference_semantics": Path("/reference/reference-semantics"),
        "candidate_reference_semantics": Path(paths["candidate"])
        / "reference-semantics",
    }

    ok = True
    for label, path in required_files.items():
        present = path.exists() or path.is_symlink()
        actual_kind = kind(path) if present else "missing"
        good = present and actual_kind == "regular" and os.access(path, os.R_OK)
        print(f"REQUIRED_FILE {label}: path={path} kind={actual_kind} readable={good}")
        ok &= good
    for label, path in required_dirs.items():
        present = path.exists() or path.is_symlink()
        actual_kind = kind(path) if present else "missing"
        good = present and actual_kind == "directory" and os.access(path, os.R_OK)
        print(f"REQUIRED_DIR {label}: path={path} kind={actual_kind} readable={good}")
        ok &= good

    campaign_path = Path(paths["audit_campaign_lock"])
    campaign = load_json(campaign_path)
    campaign_equal = campaign == audit["audit_campaign"]
    print(f"CAMPAIGN_BLOCK_MATCH={campaign_equal}")
    ok &= campaign_equal

    direct_hashes = [
        ("campaign_lock", campaign_path, hashes["audit_campaign_lock_sha256"]),
        ("run_manifest", Path(paths["run_manifest"]), hashes["run_manifest_sha256"]),
        ("task_manifest", Path(paths["task_manifest"]), hashes["task_manifest_sha256"]),
        ("stage1_result", Path(paths["stage1_result"]), hashes["stage1_result_sha256"]),
        (
            "generation_invocation",
            Path(paths["generation_manifest"]),
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            Path(paths["generation_metrics"]),
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_runtime_metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            hashes["generation_runtime_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_last",
            Path(paths["generation_last"]),
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            Path(paths["generation_output"]),
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
        ("canonical", Path(paths["canonical"]), hashes["canonical_sha256"]),
        ("trusted_prompt", Path(paths["trusted_prompt"]), hashes["trusted_prompt_sha256"]),
        ("translator", Path(paths["translator"]), hashes["trusted_translator_sha256"]),
        (
            "candidate_prompt",
            Path(paths["candidate"]) / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        (
            "candidate_translator",
            Path(paths["candidate"]) / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    ]
    for label, path, expected in direct_hashes:
        if path.is_file() and not path.is_symlink():
            ok &= report_hash(label, path, expected)

    trace_files = [
        path
        for path in Path(paths["generation_trace"]).rglob("*")
        if path.is_file() and not path.is_symlink()
    ]
    trace_symlinks = [
        path for path in Path(paths["generation_trace"]).rglob("*") if path.is_symlink()
    ]
    print(f"TRACE_FILES={len(trace_files)} TRACE_SYMLINKS={len(trace_symlinks)}")
    result_outputs = load_json(Path(paths["stage1_result"]))["outputs"]["evidence"]
    invocation_outputs = load_json(Path(paths["generation_manifest"]))["outputs"][
        "evidence"
    ]
    for trace in sorted(trace_files):
        rel = trace.relative_to(Path(paths["generation_root"])).as_posix()
        actual = sha256_file(trace)
        result_expected = result_outputs.get(rel)
        invocation_expected = invocation_outputs.get(rel)
        matches = actual == result_expected == invocation_expected
        print(
            f"TRACE_HASH {rel}: actual={actual} result={result_expected} "
            f"invocation={invocation_expected} match={matches}"
        )
        ok &= matches
    ok &= not trace_symlinks

    candidate_root = Path(paths["candidate"])
    candidate_noncompiled_symlinks = [
        path
        for path in candidate_root.rglob("*")
        if path.is_symlink()
        and "runtime-kompiled" not in path.parts
        and "verification-kompiled" not in path.parts
    ]
    print(f"CANDIDATE_SOURCE_SYMLINKS={len(candidate_noncompiled_symlinks)}")
    for path in candidate_noncompiled_symlinks:
        print(f"CANDIDATE_SOURCE_SYMLINK {path} -> {os.readlink(path)}")
    ok &= not candidate_noncompiled_symlinks

    prompt_same = (candidate_root / "prompt.py").read_bytes() == Path(
        paths["trusted_prompt"]
    ).read_bytes()
    translator_same = (candidate_root / "py2mpy.py").read_bytes() == Path(
        paths["translator"]
    ).read_bytes()
    print(f"CANDIDATE_PROMPT_BYTE_IDENTICAL={prompt_same}")
    print(f"CANDIDATE_TRANSLATOR_BYTE_IDENTICAL={translator_same}")
    ok &= prompt_same and translator_same

    semantics_same = compare_trees(
        candidate_root / "reference-semantics", Path("/reference/reference-semantics")
    )
    print(f"SUPPLIED_SEMANTICS_RECURSIVE_IDENTICAL={semantics_same}")
    ok &= semantics_same

    run = load_json(Path(paths["run_manifest"]))
    task = load_json(Path(paths["task_manifest"]))
    result = load_json(Path(paths["stage1_result"]))
    invocation = load_json(Path(paths["generation_manifest"]))
    audit_manifest = dict(audit["manifest"])
    normalized_manifest_config = audit_manifest.pop("config", None)
    cross_checks = {
        "run_id": run["run_id"] == audit["run_id"],
        "run_config": run["config"] == audit["config"],
        "task_manifest_core": task == audit_manifest,
        "normalized_manifest_config": normalized_manifest_config == audit["config"],
        "task_problem": task["problem_id"] == audit["problem_id"],
        "task_condition": task["condition"]["name"] == audit["condition"],
        "result_invocation": result["invocation"] == invocation["name"],
        "result_session": result["session_id"] == invocation["session_id"],
        "result_stage": result["stage"] == invocation["stage"],
        "result_status": result["status"] == invocation["status"],
        "result_outputs": result["outputs"] == invocation["outputs"],
        "prompt_hash_chain": task["inputs"]["instruction_prompt_sha256"]
        == invocation["prompt_sha256"]
        == hashes["generation_prompt_sha256"],
        "problem_prompt_hash_chain": task["inputs"]["problem_prompt_sha256"]
        == hashes["trusted_prompt_sha256"],
        "translator_hash_chain": task["inputs"]["translator_sha256"]
        == hashes["trusted_translator_sha256"],
    }
    for name, value in cross_checks.items():
        print(f"CROSS_CHECK {name}={value}")
        ok &= value

    print(f"OVERALL_STAGE1_INTEGRITY={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
