#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import stat
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


def pipeline_tree_hash(root: pathlib.Path) -> str:
    """Reimplement the mounted pipeline's length-delimited tree hash."""
    mode = root.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, pathlib.Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = pathlib.Path(child.path)
            child_mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(child_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(child_mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
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


def require_regular(path: pathlib.Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"not a real regular file: {path}")


def assert_equal(label: str, actual: object, expected: object) -> None:
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{label}: {status}")
    def bounded(value: object) -> str:
        if isinstance(value, bytes):
            return f"<{len(value)} bytes sha256={hashlib.sha256(value).hexdigest()}>"
        rendered = repr(value)
        return rendered if len(rendered) <= 500 else rendered[:497] + "..."

    print(f"  actual:   {bounded(actual)}")
    print(f"  expected: {bounded(expected)}")
    if actual != expected:
        raise AssertionError(label)


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    print("record_layout:", audit["record_layout"])
    print("semantics_mode:", audit["semantics_mode"])
    assert_equal("campaign block equals lock", audit["audit_campaign"], lock)
    assert_equal(
        "campaign lock sha256",
        sha256_file(LOCK),
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

    if audit["record_layout"] != "legacy-selected-stage1":
        raise AssertionError("unexpected record layout")
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        raise AssertionError("unexpected semantics mode")
    if pathlib.Path("/reference/reference-semantics").exists() or pathlib.Path(
        "/reference/reference-semantics"
    ).is_symlink():
        raise AssertionError("forbidden supplied semantics mount exists")
    print("generated-semantics boundary: OK (no reference semantics mounted)")

    required = {
        "run_manifest_sha256": pathlib.Path("/run.json"),
        "task_manifest_sha256": pathlib.Path("/task.json"),
        "stage1_result_sha256": pathlib.Path("/generation-result.json"),
        "stage1_invocation_sha256": pathlib.Path(
            "/generation-evidence/invocation.json"
        ),
        "generation_metrics_sha256": pathlib.Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_usage_sha256": pathlib.Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": pathlib.Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": pathlib.Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": pathlib.Path(
            "/generation-evidence/prompt.txt"
        ),
        "canonical_sha256": pathlib.Path("/reference/canonical.py"),
        "trusted_prompt_sha256": pathlib.Path("/reference/prompt.py"),
        "trusted_translator_sha256": pathlib.Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": pathlib.Path("/candidate/prompt.py"),
        "candidate_translator_sha256": pathlib.Path("/candidate/py2mpy.py"),
    }
    for hash_key, path in required.items():
        require_regular(path)
        assert_equal(hash_key, sha256_file(path), audit["hashes"][hash_key])

    assert_equal(
        "candidate prompt byte identity",
        pathlib.Path("/candidate/prompt.py").read_bytes(),
        pathlib.Path("/reference/prompt.py").read_bytes(),
    )
    assert_equal(
        "candidate translator byte identity",
        pathlib.Path("/candidate/py2mpy.py").read_bytes(),
        pathlib.Path("/reference/py2mpy.py").read_bytes(),
    )

    for root in (
        pathlib.Path("/candidate"),
        pathlib.Path("/generation-evidence"),
        pathlib.Path("/generation-evidence/codex-trace"),
    ):
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise AssertionError(f"mistyped or linked entry: {path}")
        print(f"real files/directories only: OK ({root})")

    candidate_hash = pipeline_tree_hash(pathlib.Path("/candidate"))
    invocation = json.loads(
        pathlib.Path("/generation-evidence/invocation.json").read_text()
    )
    result = json.loads(pathlib.Path("/generation-result.json").read_text())
    assert_equal(
        "candidate pipeline tree hash vs invocation retained workspace",
        candidate_hash,
        invocation["retained_workspace_sha256"],
    )
    assert_equal(
        "candidate pipeline tree hash vs generation result workspace",
        candidate_hash,
        result["outputs"]["workspace_sha256"],
    )

    trace_root = pathlib.Path("/generation-evidence/codex-trace")
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    assert_equal("structured trace file count", len(trace_files), 1)
    trace_rel = trace_files[0].relative_to(
        pathlib.Path("/generation-evidence")
    ).as_posix()
    trace_file_hash = sha256_file(trace_files[0])
    assert_equal(
        "trace file hash vs invocation",
        trace_file_hash,
        invocation["outputs"]["evidence"][trace_rel],
    )
    assert_equal(
        "trace file hash vs generation result",
        trace_file_hash,
        result["outputs"]["evidence"][trace_rel],
    )
    usage = json.loads(pathlib.Path("/generation-evidence/usage.json").read_text())
    assert_equal(
        "trace pipeline tree hash vs usage",
        pipeline_tree_hash(trace_root),
        usage["source_trace_sha256"],
    )

    counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    line_count = 0
    with trace_files[0].open() as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            payload_counts[str(payload.get("type") if isinstance(payload, dict) else None)] += 1
    print("trace JSONL parse: OK")
    print("trace line count:", line_count)
    print("trace top-level types:", dict(counts))
    print("trace payload types:", dict(payload_counts))

    run = json.loads(pathlib.Path("/run.json").read_text())
    task = json.loads(pathlib.Path("/task.json").read_text())
    metrics = json.loads(pathlib.Path("/generation-evidence/metrics.json").read_text())
    assert_equal("problem id", task["problem_id"], audit["problem_id"])
    embedded_manifest = dict(audit["manifest"])
    embedded_config = embedded_manifest.pop("config")
    assert_equal(
        "task manifest block (excluding launcher-added config)",
        task,
        embedded_manifest,
    )
    assert_equal("embedded manifest config", embedded_config, audit["config"])
    assert_equal("run config", run["config"], audit["config"])
    assert_equal("generation status", result["status"], "SUCCEEDED")
    assert_equal("invocation status", invocation["status"], "SUCCEEDED")
    assert_equal("metrics status", metrics["status"], "SUCCEEDED")
    print("STAGE1_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"STAGE1_INTEGRITY_ERROR: {type(error).__name__}: {error}")
        raise
