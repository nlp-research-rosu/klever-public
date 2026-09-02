#!/usr/bin/env python3
"""Independent mounted-input and pipeline-v3 provenance checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement pipeline_contract.sha256_tree without importing harness code."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
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


def require_real(path: Path, want_dir: bool) -> None:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        raise AssertionError(f"symlinked required path: {path}")
    if want_dir and not stat.S_ISDIR(mode):
        raise AssertionError(f"required directory mistyped: {path}")
    if not want_dir and not stat.S_ISREG(mode):
        raise AssertionError(f"required file mistyped: {path}")


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise AssertionError(f"symlink in semantics tree: {path}")
        if stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(path))
        else:
            raise AssertionError(f"unsupported entry in semantics tree: {path}")
    return result


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise AssertionError(
            f"{label} hash mismatch: expected={expected} actual={actual}"
        )
    print(f"PASS hash {label} {actual}")


def main() -> None:
    require_real(AUDIT_INPUT, False)
    require_real(LOCK, False)
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    print("PASS audit campaign block equals mounted campaign lock")

    hashes = audit["hashes"]
    check_hash("audit-campaign-lock", LOCK, hashes["audit_campaign_lock_sha256"])

    required_files = {
        "run-manifest": Path("/run.json"),
        "task-manifest": Path("/task.json"),
        "stage1-result": Path("/generation-result.json"),
        "stage1-invocation": Path("/generation-evidence/invocation.json"),
        "generation-metrics": Path("/generation-evidence/metrics.json"),
        "runtime-metrics": Path("/generation-evidence/runtime-metrics.json"),
        "usage": Path("/generation-evidence/usage.json"),
        "codex-last": Path("/generation-evidence/codex-last.txt"),
        "codex-output": Path("/generation-evidence/codex-output.log"),
        "generation-prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path("/reference/canonical.py"),
        "trusted-prompt": Path("/reference/prompt.py"),
        "trusted-translator": Path("/reference/py2mpy.py"),
        "candidate-prompt": Path("/candidate/prompt.py"),
        "candidate-translator": Path("/candidate/py2mpy.py"),
    }
    for path in required_files.values():
        require_real(path, False)
    for path in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ):
        require_real(path, True)
    print("PASS all pipeline-v3 records and launcher-declared mounts are real")

    recorded_file_hashes = {
        "run-manifest": "run_manifest_sha256",
        "task-manifest": "task_manifest_sha256",
        "stage1-result": "stage1_result_sha256",
        "stage1-invocation": "stage1_invocation_sha256",
        "generation-metrics": "generation_metrics_sha256",
        "runtime-metrics": "generation_runtime_metrics_sha256",
        "usage": "generation_usage_sha256",
        "codex-last": "generation_codex_last_sha256",
        "codex-output": "generation_codex_output_sha256",
        "generation-prompt": "generation_prompt_sha256",
        "canonical": "canonical_sha256",
        "trusted-prompt": "trusted_prompt_sha256",
        "trusted-translator": "trusted_translator_sha256",
        "candidate-prompt": "candidate_prompt_sha256",
        "candidate-translator": "candidate_translator_sha256",
    }
    for label, key in recorded_file_hashes.items():
        check_hash(label, required_files[label], hashes[key])

    run = json.loads(required_files["run-manifest"].read_text())
    task = json.loads(required_files["task-manifest"].read_text())
    result = json.loads(required_files["stage1-result"].read_text())
    invocation = json.loads(required_files["stage1-invocation"].read_text())
    metrics = json.loads(required_files["generation-metrics"].read_text())
    runtime = json.loads(required_files["runtime-metrics"].read_text())
    usage = json.loads(required_files["usage"].read_text())
    assert run["config"] == audit["config"]
    assert all(audit["manifest"][key] == value for key, value in task.items())
    assert audit["manifest"]["config"] == audit["config"]
    assert task["problem_id"] == audit["problem_id"] == "17-parse-music"
    assert task["condition"]["name"] == audit["condition"] == "kit-semantics"
    assert result["status"] == invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert result["outputs"]["workspace_sha256"] == invocation["outputs"][
        "workspace_sha256"
    ]
    assert runtime["harness_exit_code"] == runtime["model_exit_code"] == 0
    assert not runtime["oom_killed"] and not runtime["timeout_marker"]
    assert usage["status"] == "COMPLETE"
    print("PASS pipeline-v3 JSON records are mutually consistent")

    result_evidence = result["outputs"]["evidence"]
    evidence_paths = {
        "codex-last.txt": Path("/generation-evidence/codex-last.txt"),
        "codex-output.log": Path("/generation-evidence/codex-output.log"),
        "prompt.txt": Path("/generation-evidence/prompt.txt"),
        "runtime-metrics.json": Path("/generation-evidence/runtime-metrics.json"),
        "usage.json": Path("/generation-evidence/usage.json"),
    }
    for relative, path in evidence_paths.items():
        check_hash(f"result-output:{relative}", path, result_evidence[relative])
    trace_items = {
        key: value
        for key, value in result_evidence.items()
        if key.startswith("codex-trace/")
    }
    assert trace_items
    for relative, expected in sorted(trace_items.items()):
        path = Path("/generation-evidence") / relative
        require_real(path, False)
        check_hash(f"result-output:{relative}", path, expected)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    assert [p.relative_to(Path("/generation-evidence")).as_posix() for p in trace_files] == sorted(
        trace_items
    )
    line_count = 0
    type_counts: dict[str, int] = {}
    for trace in trace_files:
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                assert isinstance(record, dict) and "type" in record
                line_count += 1
                type_counts[record["type"]] = type_counts.get(record["type"], 0) + 1
    print(f"PASS structured trace parses: lines={line_count} types={type_counts}")

    candidate_prompt = required_files["candidate-prompt"].read_bytes()
    trusted_prompt = required_files["trusted-prompt"].read_bytes()
    candidate_translator = required_files["candidate-translator"].read_bytes()
    trusted_translator = required_files["trusted-translator"].read_bytes()
    assert candidate_prompt == trusted_prompt
    assert candidate_translator == trusted_translator
    print("PASS candidate prompt and translator are byte-identical to trusted mounts")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_entries = tree_entries(trusted_semantics)
    candidate_entries = tree_entries(candidate_semantics)
    assert candidate_entries == trusted_entries
    trusted_tree_hash = pipeline_tree_hash(trusted_semantics)
    candidate_tree_hash = pipeline_tree_hash(candidate_semantics)
    assert candidate_tree_hash == trusted_tree_hash
    assert trusted_tree_hash == task["inputs"]["reference_semantics_sha256"]
    assert trusted_tree_hash == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    print(
        "PASS supplied semantics trees have identical entries/types/bytes "
        f"files={sum(kind == 'file' for kind, _ in trusted_entries.values())} "
        f"tree_sha256={trusted_tree_hash}"
    )

    candidate_workspace_hash = pipeline_tree_hash(Path("/candidate"))
    trace_tree_hash = pipeline_tree_hash(trace_root)
    assert candidate_workspace_hash == result["outputs"]["workspace_sha256"]
    assert trace_tree_hash == usage["source_trace_sha256"]
    print(f"PASS candidate pipeline tree hash {candidate_workspace_hash}")
    print(f"PASS trace pipeline tree hash {trace_tree_hash}")
    print("OVERALL PASS")


if __name__ == "__main__":
    main()
