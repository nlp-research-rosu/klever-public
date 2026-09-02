#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/opt/humaneval/tools")
from pipeline_contract import sha256_tree  # type: ignore  # trusted launcher helper


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
REFERENCE = Path("/reference")
CANDIDATE = Path("/candidate")
GENERATION = Path("/generation-evidence")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def scan_unsafe(root: Path) -> list[str]:
    unsafe: list[str] = []
    for directory, directories, files in os.walk(root, followlinks=False):
        for name in directories + files:
            path = Path(directory, name)
            mode = path.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                unsafe.append(str(path))
    return unsafe


def check_hash(path: Path, expected: str) -> None:
    actual = file_sha256(path)
    print(f"sha256 {path}: {actual}")
    assert actual == expected, (path, expected, actual)


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["problem_id"] == "52-below-threshold"
    assert audit["condition"] == "bare"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["mount_reference_semantics"] is False

    require_regular(AUDIT)
    require_regular(LOCK)
    require_directory(CANDIDATE)
    require_directory(REFERENCE)
    require_directory(GENERATION)

    assert lock == audit["audit_campaign"]
    check_hash(LOCK, hashes["audit_campaign_lock_sha256"])
    print("campaign block equals campaign lock: yes")

    required_container_paths = {
        "audit_campaign_lock",
        "candidate",
        "canonical",
        "generation_last",
        "generation_manifest",
        "generation_metrics",
        "generation_output",
        "generation_root",
        "generation_trace",
        "run_manifest",
        "stage1_result",
        "task_manifest",
        "translator",
        "trusted_prompt",
    }
    assert set(paths) == required_container_paths
    for label, raw_path in sorted(paths.items()):
        path = Path(raw_path)
        if label in {"candidate", "generation_root", "generation_trace"}:
            require_directory(path)
        else:
            require_regular(path)
        print(f"container path {label}: {path} [safe type]")

    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        GENERATION / "usage.json",
    ]
    for path in required_records:
        require_regular(path)
        print(f"required legacy-selected-stage1 record: {path}")

    # Runtime metrics are historically absent for this legacy-selected-stage1
    # record and are not reconstructed.
    print(
        "runtime-metrics.json present:",
        (GENERATION / "runtime-metrics.json").exists(),
        "(not required for this layout)",
    )

    assert not (REFERENCE / "reference-semantics").exists()
    print("generated-semantics boundary: no /reference/reference-semantics")

    assert not scan_unsafe(CANDIDATE)
    assert not scan_unsafe(REFERENCE)
    assert not scan_unsafe(GENERATION)
    print("linked or unsupported mounted entries: none")

    check_hash(Path("/reference/canonical.py"), hashes["canonical_sha256"])
    check_hash(Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"])
    check_hash(Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"])
    check_hash(Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"])
    check_hash(Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"])
    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate prompt byte-identical to trusted prompt: yes")
    print("candidate translator byte-identical to trusted translator: yes")

    check_hash(Path("/run.json"), hashes["run_manifest_sha256"])
    check_hash(Path("/task.json"), hashes["task_manifest_sha256"])
    check_hash(Path("/generation-result.json"), hashes["stage1_result_sha256"])
    check_hash(GENERATION / "invocation.json", hashes["stage1_invocation_sha256"])
    check_hash(GENERATION / "metrics.json", hashes["generation_metrics_sha256"])
    check_hash(GENERATION / "usage.json", hashes["generation_usage_sha256"])
    check_hash(GENERATION / "codex-last.txt", hashes["generation_codex_last_sha256"])
    check_hash(
        GENERATION / "codex-output.log", hashes["generation_codex_output_sha256"]
    )
    check_hash(GENERATION / "prompt.txt", hashes["generation_prompt_sha256"])

    task = json.loads(Path("/task.json").read_text())
    invocation = json.loads((GENERATION / "invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads((GENERATION / "usage.json").read_text())
    # The audit record enriches the exact task manifest with the run config.
    manifest = audit["manifest"]
    assert manifest["config"] == audit["config"]
    assert {key: manifest[key] for key in task} == task
    assert task["inputs"]["problem_prompt_sha256"] == hashes["trusted_prompt_sha256"]
    assert task["inputs"]["translator_sha256"] == hashes["trusted_translator_sha256"]
    assert (
        task["inputs"]["instruction_prompt_sha256"]
        == hashes["generation_prompt_sha256"]
    )
    assert invocation["outputs"] == result["outputs"]

    candidate_digest = sha256_tree(CANDIDATE)
    trace_digest = sha256_tree(GENERATION / "codex-trace")
    print(f"pipeline sha256_tree /candidate: {candidate_digest}")
    print(f"pipeline sha256_tree trace: {trace_digest}")
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    assert candidate_digest == invocation["retained_workspace_sha256"]
    assert trace_digest == usage["source_trace_sha256"]
    print("candidate tree matches retained Stage-1 workspace hash: yes")
    print("trace tree matches usage source-trace hash: yes")

    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        check_hash(GENERATION / relative, expected)

    print(
        "launcher candidate_tree_sha256 (separate launcher digest scheme):",
        hashes["candidate_tree_sha256"],
    )
    print(
        "launcher generation_codex_trace_sha256 (separate launcher digest scheme):",
        hashes["generation_codex_trace_sha256"],
    )
    print("PROVENANCE_CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
