#!/usr/bin/env python3
"""Independent integrity check for the mounted legacy-selected-stage1 record."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha_tree(root: Path) -> str:
    """Content digest used by the pipeline generation manifests."""
    mode = root.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            child_mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(child_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(child_mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def regular(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise AssertionError(f"not a real regular file: {path}")


def real_directory(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"not a real directory: {path}")


def load_json(path: Path):
    regular(path)
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise AssertionError(f"JSON root is not an object: {path}")
    return value


def require_hash(path: Path, expected: str, label: str) -> None:
    regular(path)
    actual = sha_file(path)
    print(f"HASH {label} actual={actual} expected={expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch: {label}")


def main() -> int:
    audit = load_json(Path("/audit-input.json"))
    lock = load_json(Path("/audit-campaign-lock.json"))
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    print("campaign_block_equal=true")

    hashes = audit["hashes"]
    require_hash(
        Path("/audit-campaign-lock.json"),
        hashes["audit_campaign_lock_sha256"],
        "audit campaign lock",
    )

    required_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        regular(path)
        print(f"TYPE regular {path}")
    for path in required_directories:
        real_directory(path)
        print(f"TYPE directory {path}")

    usage_path = Path("/generation-evidence/usage.json")
    regular(usage_path)
    print("OPTIONAL-PRESENT usage.json inspected")
    if Path("/generation-evidence/runtime-metrics.json").exists():
        regular(Path("/generation-evidence/runtime-metrics.json"))
        print("OPTIONAL-PRESENT runtime-metrics.json inspected")
    else:
        print("EXPECTED-HISTORICAL-ABSENCE runtime-metrics.json")

    if Path("/reference/reference-semantics").exists():
        raise AssertionError("reference semantics unexpectedly mounted")
    print("GENERATED_SEMANTICS_BOUNDARY no reference-semantics mount")

    for root in (Path("/candidate"), Path("/generation-evidence")):
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise AssertionError(f"linked/unsupported mounted entry: {path}")
    print("TREE_TYPES candidate/generation contain only regular files/directories")

    require_hash(
        Path("/candidate/prompt.py"),
        hashes["candidate_prompt_sha256"],
        "candidate prompt",
    )
    require_hash(
        Path("/candidate/py2mpy.py"),
        hashes["candidate_translator_sha256"],
        "candidate translator",
    )
    require_hash(
        Path("/reference/canonical.py"),
        hashes["canonical_sha256"],
        "trusted canonical",
    )
    require_hash(
        Path("/reference/prompt.py"),
        hashes["trusted_prompt_sha256"],
        "trusted prompt",
    )
    require_hash(
        Path("/reference/py2mpy.py"),
        hashes["trusted_translator_sha256"],
        "trusted translator",
    )
    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("BYTE_COMPARE candidate prompt/translator match trusted mounts")

    fixed_hashes = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for path_text, key in fixed_hashes.items():
        require_hash(Path(path_text), hashes[key], key)

    run = load_json(Path("/run.json"))
    task = load_json(Path("/task.json"))
    result = load_json(Path("/generation-result.json"))
    invocation = load_json(Path("/generation-evidence/invocation.json"))
    metrics = load_json(Path("/generation-evidence/metrics.json"))
    usage = load_json(usage_path)
    assert all(audit["manifest"].get(key) == value for key, value in task.items())
    assert audit["manifest"]["config"] == audit["config"]
    assert task["problem_id"] == audit["problem_id"] == "31-is-prime"
    assert run["run_id"] == audit["run_id"]
    assert invocation["status"] == metrics["status"] == result["status"] == "SUCCEEDED"
    print("MANIFEST_LINKS run/task/invocation/metrics/result coherent")

    for relative, expected in result["outputs"]["evidence"].items():
        require_hash(
            Path("/generation-evidence") / relative,
            expected,
            f"generation-result evidence {relative}",
        )

    candidate_tree = sha_tree(Path("/candidate"))
    trace_tree = sha_tree(Path("/generation-evidence/codex-trace"))
    print(f"PIPELINE_TREE candidate={candidate_tree}")
    print(f"PIPELINE_TREE trace={trace_tree}")
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["retained_workspace_sha256"]
    assert trace_tree == usage["source_trace_sha256"]
    print("TREE_LINKS candidate matches retained generation workspace; trace matches usage")
    print(
        "LAUNCHER_RECORDED_AGGREGATES "
        f"candidate={hashes['candidate_tree_sha256']} "
        f"trace={hashes['generation_codex_trace_sha256']}"
    )

    trace_types: Counter[str] = Counter()
    trace_lines = 0
    for trace_path in sorted(Path("/generation-evidence/codex-trace").rglob("*")):
        if not trace_path.is_file():
            continue
        with trace_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                event = json.loads(line)
                trace_lines += 1
                trace_types[event.get("type", "(missing)")] += 1
    print(f"TRACE parsed_lines={trace_lines} outer_types={dict(trace_types)}")

    codex_output = Path("/generation-evidence/codex-output.log").read_text(
        encoding="utf-8"
    )
    codex_last = Path("/generation-evidence/codex-last.txt").read_text(
        encoding="utf-8"
    )
    generation_prompt = Path("/generation-evidence/prompt.txt").read_text(
        encoding="utf-8"
    )
    print(
        "RECORD_CONTENT "
        f"output_lines={len(codex_output.splitlines())} "
        f"output_top_count={codex_output.count('#Top')} "
        f"output_stuck_count={codex_output.count('WarnStuckClaimState')} "
        f"last_result_marker={('RESULT: KPROVE_PASSED' in codex_last)} "
        f"prompt_chars={len(generation_prompt)}"
    )
    print("PROVENANCE_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
