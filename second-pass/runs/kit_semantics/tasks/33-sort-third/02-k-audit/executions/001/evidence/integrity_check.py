#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys
from collections import Counter


AUDIT = pathlib.Path("/audit-input.json")
LOCK = pathlib.Path("/audit-campaign-lock.json")


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: pathlib.Path) -> tuple[str, int, int, int]:
    records: list[str] = []
    files = directories = symlinks = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            symlinks += 1
            records.append(f"L\0{relative}\0{os.readlink(path)}\n")
        elif path.is_dir():
            directories += 1
            records.append(f"D\0{relative}\n")
        elif path.is_file():
            files += 1
            records.append(f"F\0{relative}\0{sha256_file(path)}\n")
        else:
            records.append(f"O\0{relative}\0{path.stat().st_mode:o}\n")
    digest = hashlib.sha256("".join(records).encode()).hexdigest()
    return digest, files, directories, symlinks


def pipeline_tree_sha256(root: pathlib.Path) -> str:
    """Reimplement the pipeline-v3 length-prefixed tree digest."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, pathlib.Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = pathlib.Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise ValueError(f"linked tree entry: {path}")
            if path.is_dir():
                entries.append((relative, "directory", path))
                pending.append(path)
            elif path.is_file():
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"unsupported tree entry mode {mode:o}: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def compare_trees(left: pathlib.Path, right: pathlib.Path) -> list[str]:
    problems: list[str] = []
    left_paths = {
        path.relative_to(left).as_posix(): path for path in left.rglob("*")
    }
    right_paths = {
        path.relative_to(right).as_posix(): path for path in right.rglob("*")
    }
    for relative in sorted(left_paths.keys() | right_paths.keys()):
        lpath = left_paths.get(relative)
        rpath = right_paths.get(relative)
        if lpath is None:
            problems.append(f"missing candidate entry: {relative}")
            continue
        if rpath is None:
            problems.append(f"additional candidate entry: {relative}")
            continue
        ltype = (
            "symlink"
            if lpath.is_symlink()
            else "dir"
            if lpath.is_dir()
            else "file"
            if lpath.is_file()
            else "other"
        )
        rtype = (
            "symlink"
            if rpath.is_symlink()
            else "dir"
            if rpath.is_dir()
            else "file"
            if rpath.is_file()
            else "other"
        )
        if ltype != rtype:
            problems.append(
                f"type mismatch {relative}: candidate={ltype}, trusted={rtype}"
            )
        elif ltype == "symlink":
            problems.append(f"symlink entry forbidden: {relative}")
        elif ltype == "file" and sha256_file(lpath) != sha256_file(rpath):
            problems.append(f"content mismatch: {relative}")
    return problems


def regular_readable(path: pathlib.Path) -> bool:
    return (
        path.exists()
        and path.is_file()
        and not path.is_symlink()
        and os.access(path, os.R_OK)
    )


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("declared layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("declared semantics mode is not SUPPLIED_SEMANTICS")
    if lock != audit.get("audit_campaign"):
        failures.append("campaign lock content does not match audit_campaign block")
    print(f"campaign_block_exact_match={lock == audit.get('audit_campaign')}")

    required = [
        pathlib.Path("/audit-input.json"),
        pathlib.Path("/audit-campaign-lock.json"),
        pathlib.Path("/run.json"),
        pathlib.Path("/task.json"),
        pathlib.Path("/generation-result.json"),
        pathlib.Path("/generation-evidence/invocation.json"),
        pathlib.Path("/generation-evidence/metrics.json"),
        pathlib.Path("/generation-evidence/runtime-metrics.json"),
        pathlib.Path("/generation-evidence/usage.json"),
        pathlib.Path("/generation-evidence/codex-last.txt"),
        pathlib.Path("/generation-evidence/codex-output.log"),
        pathlib.Path("/generation-evidence/prompt.txt"),
        pathlib.Path("/reference/canonical.py"),
        pathlib.Path("/reference/prompt.py"),
        pathlib.Path("/reference/py2mpy.py"),
    ]
    for path in required:
        ok = regular_readable(path)
        print(f"required_regular_readable {path}: {ok}")
        if not ok:
            failures.append(f"missing, unreadable, non-regular, or symlinked: {path}")

    for key, raw_path in audit.get("container_paths", {}).items():
        path = pathlib.Path(raw_path)
        ok = path.exists() and not path.is_symlink() and os.access(path, os.R_OK)
        print(f"container_path {key} {path}: {ok}")
        if not ok:
            failures.append(f"launcher-declared mount unavailable: {key}={path}")

    direct_hashes = {
        "audit_campaign_lock_sha256": pathlib.Path("/audit-campaign-lock.json"),
        "canonical_sha256": pathlib.Path("/reference/canonical.py"),
        "trusted_prompt_sha256": pathlib.Path("/reference/prompt.py"),
        "candidate_prompt_sha256": pathlib.Path("/candidate/prompt.py"),
        "trusted_translator_sha256": pathlib.Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": pathlib.Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": pathlib.Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": pathlib.Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": pathlib.Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_prompt_sha256": pathlib.Path(
            "/generation-evidence/prompt.txt"
        ),
        "generation_runtime_metrics_sha256": pathlib.Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": pathlib.Path(
            "/generation-evidence/usage.json"
        ),
        "manifest_sha256": pathlib.Path("/task.json"),
        "run_manifest_sha256": pathlib.Path("/run.json"),
        "stage1_invocation_sha256": pathlib.Path(
            "/generation-evidence/invocation.json"
        ),
        "stage1_result_sha256": pathlib.Path("/generation-result.json"),
        "task_manifest_sha256": pathlib.Path("/task.json"),
    }
    for key, path in direct_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"].get(key)
        match = actual == expected
        print(f"recorded_hash {key}: match={match} actual={actual}")
        if not match:
            failures.append(f"recorded hash mismatch: {key}")

    if pathlib.Path("/candidate/prompt.py").read_bytes() != pathlib.Path(
        "/reference/prompt.py"
    ).read_bytes():
        failures.append("candidate prompt differs from trusted prompt")
    if pathlib.Path("/candidate/py2mpy.py").read_bytes() != pathlib.Path(
        "/reference/py2mpy.py"
    ).read_bytes():
        failures.append("candidate translator differs from trusted translator")
    print(
        "candidate_prompt_byte_equal_trusted="
        + str(
            pathlib.Path("/candidate/prompt.py").read_bytes()
            == pathlib.Path("/reference/prompt.py").read_bytes()
        )
    )
    print(
        "candidate_translator_byte_equal_trusted="
        + str(
            pathlib.Path("/candidate/py2mpy.py").read_bytes()
            == pathlib.Path("/reference/py2mpy.py").read_bytes()
        )
    )

    trusted_semantics = pathlib.Path("/reference/reference-semantics")
    candidate_semantics = pathlib.Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures.append("trusted supplied-semantics tree absent or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        failures.append("candidate supplied-semantics tree absent or symlinked")
    semantics_problems = compare_trees(candidate_semantics, trusted_semantics)
    print(f"semantics_recursive_problem_count={len(semantics_problems)}")
    for problem in semantics_problems:
        print(f"semantics_problem={problem}")
    failures.extend(semantics_problems)

    for name, root in [
        ("candidate", pathlib.Path("/candidate")),
        ("candidate_reference_semantics", candidate_semantics),
        ("trusted_reference_semantics", trusted_semantics),
        ("generation_trace", pathlib.Path("/generation-evidence/codex-trace")),
    ]:
        digest, files, directories, symlinks = tree_manifest(root)
        print(
            f"independent_tree_manifest {name}: sha256={digest} "
            f"files={files} dirs={directories} symlinks={symlinks}"
        )

    result = json.loads(pathlib.Path("/generation-result.json").read_text())
    task = json.loads(pathlib.Path("/task.json").read_text())
    usage = json.loads(pathlib.Path("/generation-evidence/usage.json").read_text())
    pipeline_tree_checks = [
        (
            "candidate_vs_generation_result_workspace",
            pathlib.Path("/candidate"),
            result["outputs"]["workspace_sha256"],
        ),
        (
            "trusted_semantics_vs_task_manifest",
            trusted_semantics,
            task["inputs"]["reference_semantics_sha256"],
        ),
        (
            "candidate_semantics_vs_task_manifest",
            candidate_semantics,
            task["inputs"]["reference_semantics_sha256"],
        ),
        (
            "trace_vs_usage_source_trace",
            pathlib.Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
        ),
    ]
    for name, root, expected in pipeline_tree_checks:
        actual = pipeline_tree_sha256(root)
        match = actual == expected
        print(
            f"pipeline_tree_hash {name}: match={match} "
            f"actual={actual} expected={expected}"
        )
        if not match:
            failures.append(f"pipeline tree hash mismatch: {name}")

    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = pathlib.Path("/generation-evidence") / relative
        ok = regular_readable(path)
        actual = sha256_file(path) if ok else "UNAVAILABLE"
        match = ok and actual == expected
        print(
            f"generation_result_evidence_hash {relative}: "
            f"match={match} actual={actual}"
        )
        if not match:
            failures.append(f"generation-result evidence mismatch: {relative}")

    trace_files = sorted(
        pathlib.Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    if not trace_files:
        failures.append("structured trace has no JSONL files")
    event_counts: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        if path.is_symlink() or not path.is_file():
            failures.append(f"invalid trace entry: {path}")
            continue
        with path.open(encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    failures.append(f"malformed trace line {path}:{number}: {err}")
                    continue
                event_counts[str(event.get("type", "<missing>"))] += 1
    print(f"trace_files={len(trace_files)} trace_lines={trace_lines}")
    print(f"trace_event_types={dict(sorted(event_counts.items()))}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE={failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
