#!/usr/bin/env python3
"""Independent integrity checks for the launcher mounts and supplied semantics."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independently implement the pipeline-v3 length-delimited tree digest."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def describe(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        return f"UNREADABLE:{err}"
    if stat.S_ISLNK(mode):
        return f"symlink->{os.readlink(path)}"
    if stat.S_ISREG(mode):
        return f"file:{path.stat().st_size}"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"other:{oct(mode)}"


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_entries = {
        p.relative_to(left).as_posix(): p for p in left.rglob("*")
    }
    right_entries = {
        p.relative_to(right).as_posix(): p for p in right.rglob("*")
    }
    for rel in sorted(left_entries.keys() | right_entries.keys()):
        lp = left_entries.get(rel)
        rp = right_entries.get(rel)
        if lp is None:
            problems.append(f"missing candidate entry: {rel}")
            continue
        if rp is None:
            problems.append(f"additional candidate entry: {rel}")
            continue
        lm = lp.lstat().st_mode
        rm = rp.lstat().st_mode
        lt = stat.S_IFMT(lm)
        rt = stat.S_IFMT(rm)
        if stat.S_ISLNK(lm) or stat.S_ISLNK(rm):
            problems.append(
                f"symlinked entry: {rel}: candidate={describe(lp)} trusted={describe(rp)}"
            )
        elif lt != rt:
            problems.append(
                f"type mismatch: {rel}: candidate={describe(lp)} trusted={describe(rp)}"
            )
        elif stat.S_ISREG(lm) and sha256(lp) != sha256(rp):
            problems.append(
                f"content mismatch: {rel}: candidate={sha256(lp)} trusted={sha256(rp)}"
            )
    return problems


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    failures: list[str] = []

    print(f"record_layout={data.get('record_layout')}")
    print(f"semantics_mode={data.get('semantics_mode')}")

    lock_path = Path(data["container_paths"]["audit_campaign_lock"])
    lock_bytes_hash = sha256(lock_path)
    lock_data = json.loads(lock_path.read_text())
    expected_lock_hash = data["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_lock_sha256={lock_bytes_hash}")
    print(f"campaign_lock_hash_recorded={expected_lock_hash}")
    print(f"campaign_block_object_equal={lock_data == data['audit_campaign']}")
    if lock_bytes_hash != expected_lock_hash:
        failures.append("campaign lock byte hash mismatch")
    if lock_data != data["audit_campaign"]:
        failures.append("campaign lock object differs from audit_campaign block")

    declared = {
        "audit_campaign_lock": "/audit-campaign-lock.json",
        "candidate": "/candidate",
        "canonical": "/reference/canonical.py",
        "generation_last": "/generation-evidence/codex-last.txt",
        "generation_manifest": "/generation-evidence/invocation.json",
        "generation_metrics": "/generation-evidence/metrics.json",
        "generation_output": "/generation-evidence/codex-output.log",
        "generation_root": "/generation-evidence",
        "generation_trace": "/generation-evidence/codex-trace",
        "run_manifest": "/run.json",
        "stage1_result": "/generation-result.json",
        "task_manifest": "/task.json",
        "translator": "/reference/py2mpy.py",
        "trusted_prompt": "/reference/prompt.py",
    }
    print("declared_container_paths:")
    for key, expected_path in declared.items():
        actual = data["container_paths"].get(key)
        status_text = describe(Path(actual)) if actual else "MISSING_KEY"
        print(f"  {key}: declared={actual!r} expected={expected_path!r} type={status_text}")
        if actual != expected_path or status_text.startswith(("UNREADABLE", "MISSING")):
            failures.append(f"bad declared mount {key}")

    required_pipeline = [
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
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    print("pipeline_v3_required_records:")
    for path in required_pipeline:
        type_text = describe(path)
        print(f"  {path}: {type_text}")
        if not path.is_file() or path.is_symlink():
            failures.append(f"missing, mistyped, or symlinked required record: {path}")
    print(f"  structured_trace_regular_files={sum(p.is_file() for p in trace_files)}")
    for path in trace_files:
        if path.is_symlink() or (not path.is_file() and not path.is_dir()):
            failures.append(f"mistyped or symlinked trace entry: {path}")
    if not any(p.is_file() for p in trace_files):
        failures.append("structured trace contains no regular files")

    hash_checks = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    print("recorded_file_hashes:")
    for raw_path, key in hash_checks.items():
        path = Path(raw_path)
        actual = sha256(path)
        expected = data["hashes"][key]
        ok = actual == expected
        print(f"  {raw_path}: {actual} expected={expected} ok={ok}")
        if not ok:
            failures.append(f"hash mismatch for {raw_path}")

    gen_result = json.loads(Path("/generation-result.json").read_text())
    output_hashes = gen_result["outputs"]["evidence"]
    output_paths = {
        "codex-last.txt": Path("/generation-evidence/codex-last.txt"),
        "codex-output.log": Path("/generation-evidence/codex-output.log"),
        "prompt.txt": Path("/generation-evidence/prompt.txt"),
        "runtime-metrics.json": Path("/generation-evidence/runtime-metrics.json"),
        "usage.json": Path("/generation-evidence/usage.json"),
    }
    trace_rel = next(k for k in output_hashes if k.startswith("codex-trace/"))
    output_paths[trace_rel] = Path("/generation-evidence") / trace_rel
    print("generation_result_output_hashes:")
    for key, path in output_paths.items():
        actual = sha256(path)
        expected = output_hashes[key]
        print(f"  {key}: {actual} expected={expected} ok={actual == expected}")
        if actual != expected:
            failures.append(f"generation-result output hash mismatch: {key}")

    task = json.loads(Path("/task.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    tree_checks = [
        (
            Path("/candidate"),
            gen_result["outputs"]["workspace_sha256"],
            "generation-result workspace_sha256",
        ),
        (
            Path("/reference/reference-semantics"),
            task["inputs"]["reference_semantics_sha256"],
            "task reference_semantics_sha256",
        ),
        (
            Path("/candidate/reference-semantics"),
            task["inputs"]["reference_semantics_sha256"],
            "task reference_semantics_sha256",
        ),
        (
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
            "usage source_trace_sha256",
        ),
    ]
    print("pipeline_v3_tree_hashes:")
    for path, expected, label in tree_checks:
        actual = pipeline_tree_sha256(path)
        print(f"  {path}: {actual} expected={expected} ({label}) ok={actual == expected}")
        if actual != expected:
            failures.append(f"pipeline-v3 tree hash mismatch: {path}")

    print("trusted_copy_checks:")
    for candidate_path, trusted_path in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]:
        ok = (
            candidate_path.is_file()
            and trusted_path.is_file()
            and not candidate_path.is_symlink()
            and not trusted_path.is_symlink()
            and candidate_path.read_bytes() == trusted_path.read_bytes()
        )
        print(f"  {candidate_path} == {trusted_path}: {ok}")
        if not ok:
            failures.append(f"trusted copy mismatch: {candidate_path}")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    if data.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("rendered semantics mode is not SUPPLIED_SEMANTICS")
    if not trusted_sem.is_dir() or trusted_sem.is_symlink():
        failures.append("trusted reference semantics absent, mistyped, or symlinked")
    sem_problems = compare_trees(candidate_sem, trusted_sem)
    print(f"supplied_semantics_tree_problem_count={len(sem_problems)}")
    for problem in sem_problems:
        print(f"  {problem}")
    failures.extend(sem_problems)

    all_roots = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]
    symlinks = sorted(
        str(p)
        for root in all_roots
        for p in root.rglob("*")
        if p.is_symlink()
    )
    print(f"all_input_symlink_count={len(symlinks)}")
    for path in symlinks:
        print(f"  {path}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
