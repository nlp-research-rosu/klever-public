#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    require_directory(root)
    pending = [root]
    result: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for item in os.scandir(directory):
            path = Path(item.path)
            mode = item.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(result)


def pipeline_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            content_size = path.stat(follow_symlinks=False).st_size
            digest.update(content_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    require_regular(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"JSON root is not an object: {path}")
    return value


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    outcome = "MATCH" if actual == expected else "MISMATCH"
    print(f"HASH {label} {outcome} expected={expected} actual={actual} path={path}")
    if actual != expected:
        raise AssertionError(f"hash mismatch: {label}")


def compare_trees(left: Path, right: Path) -> None:
    left_entries = tree_entries(left)
    right_entries = tree_entries(right)
    left_shape = [(relative, kind) for relative, kind, _ in left_entries]
    right_shape = [(relative, kind) for relative, kind, _ in right_entries]
    if left_shape != right_shape:
        missing = sorted(set(right_shape) - set(left_shape))
        additional = sorted(set(left_shape) - set(right_shape))
        raise AssertionError(
            f"semantics shape differs: missing={missing!r} additional={additional!r}"
        )
    files = 0
    for (relative, kind, left_path), (_, _, right_path) in zip(
        left_entries, right_entries, strict=True
    ):
        if kind == "file":
            files += 1
            left_hash = sha256_file(left_path)
            right_hash = sha256_file(right_path)
            if left_hash != right_hash:
                raise AssertionError(
                    f"semantics file differs: {relative} "
                    f"candidate={left_hash} trusted={right_hash}"
                )
    print(
        "SUPPLIED_SEMANTICS BYTE_IDENTICAL "
        f"entries={len(left_entries)} files={files} symlinks=0"
    )


def summarize_trace(root: Path) -> None:
    event_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    files = 0
    lines = 0
    last_events: collections.deque[str] = collections.deque(maxlen=12)
    for relative, kind, path in tree_entries(root):
        if kind != "file":
            continue
        files += 1
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                lines += 1
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise AssertionError(f"trace event is not an object: {path}:{line_number}")
                event_type = str(event.get("type"))
                event_counts[event_type] += 1
                payload = event.get("payload")
                payload_type = (
                    str(payload.get("type")) if isinstance(payload, dict) else "<none>"
                )
                payload_counts[payload_type] += 1
                last_events.append(
                    f"{relative}:{line_number} type={event_type} payload={payload_type}"
                )
    print(f"TRACE_PARSED files={files} lines={lines}")
    print(f"TRACE_EVENT_COUNTS {dict(sorted(event_counts.items()))}")
    print(f"TRACE_PAYLOAD_COUNTS {dict(sorted(payload_counts.items()))}")
    print("TRACE_LAST_EVENTS")
    for summary in last_events:
        print(summary)


def main() -> None:
    audit = load_object(AUDIT_INPUT)
    if audit.get("record_layout") != "pipeline-v3":
        raise AssertionError(f"unexpected record layout: {audit.get('record_layout')!r}")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode: {audit.get('semantics_mode')!r}")
    if audit.get("mount_reference_semantics") is not True:
        raise AssertionError("supplied semantics mount flag is not true")
    print("LAYOUT pipeline-v3")
    print("SEMANTICS_MODE SUPPLIED_SEMANTICS")

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
    ]
    for path in required_files:
        require_regular(path)
        print(f"REQUIRED_FILE OK {path}")
    for path in required_directories:
        require_directory(path)
        print(f"REQUIRED_DIRECTORY OK {path}")

    campaign = load_object(Path("/audit-campaign-lock.json"))
    if campaign != audit["audit_campaign"]:
        raise AssertionError("campaign lock does not equal audit_input.audit_campaign")
    print("CAMPAIGN_BLOCK EXACT_MATCH")

    hashes = audit["hashes"]
    direct_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for label, path in direct_hashes.items():
        check_hash(label, path, hashes[label])

    run = load_object(Path("/run.json"))
    task = load_object(Path("/task.json"))
    result = load_object(Path("/generation-result.json"))
    invocation = load_object(Path("/generation-evidence/invocation.json"))
    metrics = load_object(Path("/generation-evidence/metrics.json"))
    runtime = load_object(Path("/generation-evidence/runtime-metrics.json"))
    usage = load_object(Path("/generation-evidence/usage.json"))
    for document_name, document in (("run", run), ("task", task)):
        if document["condition"] != audit["manifest"]["condition"]:
            raise AssertionError(f"{document_name} condition differs")
    embedded_manifest = audit["manifest"]
    for field in ("schema_version", "condition", "current_stage", "inputs", "problem_id"):
        if task[field] != embedded_manifest[field]:
            raise AssertionError(f"task.json differs from embedded manifest field {field}")
    if embedded_manifest.get("config") != audit["config"]:
        raise AssertionError("embedded manifest config differs from audit config")
    if task["problem_id"] != audit["problem_id"]:
        raise AssertionError("problem id differs")
    if run["run_id"] != audit["run_id"]:
        raise AssertionError("run id differs")
    if result["status"] != "SUCCEEDED" or invocation["status"] != "SUCCEEDED":
        raise AssertionError("generation status is not SUCCEEDED")
    if metrics["exit_code"] != 0 or runtime["final_exit_code"] != 0:
        raise AssertionError("generation execution did not exit zero")
    if usage["status"] != "COMPLETE":
        raise AssertionError("usage record is incomplete")
    print("MANIFEST_LINKAGE CONSISTENT")

    candidate_tree = pipeline_tree_sha256(Path("/candidate"))
    expected_candidate_tree = result["outputs"]["workspace_sha256"]
    invocation_candidate_tree = invocation["outputs"]["workspace_sha256"]
    if candidate_tree != expected_candidate_tree or candidate_tree != invocation_candidate_tree:
        raise AssertionError(
            "candidate pipeline tree hash differs from generation records: "
            f"actual={candidate_tree} result={expected_candidate_tree} "
            f"invocation={invocation_candidate_tree}"
        )
    print(f"PIPELINE_TREE candidate MATCH {candidate_tree}")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_tree = pipeline_tree_sha256(trusted_semantics)
    candidate_semantics_tree = pipeline_tree_sha256(candidate_semantics)
    expected_semantics_tree = task["inputs"]["reference_semantics_sha256"]
    if (
        trusted_tree != expected_semantics_tree
        or candidate_semantics_tree != expected_semantics_tree
    ):
        raise AssertionError(
            "semantics pipeline tree hash mismatch: "
            f"trusted={trusted_tree} candidate={candidate_semantics_tree} "
            f"expected={expected_semantics_tree}"
        )
    print(f"PIPELINE_TREE supplied_semantics MATCH {trusted_tree}")
    compare_trees(candidate_semantics, trusted_semantics)

    if sha256_file(Path("/candidate/prompt.py")) != sha256_file(
        Path("/reference/prompt.py")
    ):
        raise AssertionError("candidate prompt differs from trusted prompt")
    if sha256_file(Path("/candidate/py2mpy.py")) != sha256_file(
        Path("/reference/py2mpy.py")
    ):
        raise AssertionError("candidate translator differs from trusted translator")
    print("CANDIDATE_PROMPT BYTE_IDENTICAL")
    print("CANDIDATE_TRANSLATOR BYTE_IDENTICAL")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_tree = pipeline_tree_sha256(trace_root)
    if trace_tree != usage["source_trace_sha256"]:
        raise AssertionError(
            f"trace tree mismatch: actual={trace_tree} usage={usage['source_trace_sha256']}"
        )
    print(f"PIPELINE_TREE generation_trace MATCH {trace_tree}")
    evidence_map = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_map.items()):
        path = Path("/generation-evidence") / relative
        check_hash(f"generation_result.outputs.evidence[{relative}]", path, expected)
    if evidence_map != invocation["outputs"]["evidence"]:
        raise AssertionError("result and invocation evidence maps differ")

    summarize_trace(trace_root)
    last = Path("/generation-evidence/codex-last.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    output = Path("/generation-evidence/codex-output.log").read_text(
        encoding="utf-8", errors="replace"
    )
    prompt = Path("/generation-evidence/prompt.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    print(
        "GENERATION_TEXT_READ "
        f"last_bytes={len(last.encode())} last_lines={len(last.splitlines())} "
        f"output_bytes={len(output.encode())} output_lines={len(output.splitlines())} "
        f"prompt_bytes={len(prompt.encode())} prompt_lines={len(prompt.splitlines())}"
    )
    print("GENERATION_LAST_BEGIN")
    print(last.rstrip())
    print("GENERATION_LAST_END")

    print("AUXILIARY_AUDIT_INPUT_DIRECTORY_DIGESTS")
    for label in (
        "candidate_tree_sha256",
        "candidate_reference_semantics_sha256",
        "trusted_reference_semantics_sha256",
        "generation_codex_trace_sha256",
    ):
        print(f"{label}={hashes[label]}")
    print("STAGE1_INTEGRITY PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"STAGE1_INTEGRITY FAIL {type(error).__name__}: {error}")
        raise
