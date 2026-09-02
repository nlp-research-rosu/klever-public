#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v2 length-delimited tree digest independently."""
    root = root.resolve(strict=True)
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
                raise AssertionError(f"linked/unsupported tree entry: {path}")
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists() or usage.is_symlink():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)

    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference"),
    ]
    for path in required_directories:
        require_directory(path)

    forbidden = Path("/reference/reference-semantics")
    assert not forbidden.exists() and not forbidden.is_symlink()

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    assert lock == audit["audit_campaign"]

    expected_files = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
    }
    hashes = audit["hashes"]
    for raw_path, key in expected_files.items():
        path = Path(raw_path)
        if path.exists():
            actual = sha256_file(path)
            assert actual == hashes[key], (raw_path, actual, hashes[key])
            print(f"FILE_HASH_OK {raw_path} {actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("CANDIDATE_PROMPT_BYTE_IDENTICAL")
    print("CANDIDATE_TRANSLATOR_BYTE_IDENTICAL")

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    recorded_tree = result["outputs"]["workspace_sha256"]
    actual_tree = safe_tree_sha256(Path("/candidate"))
    assert actual_tree == recorded_tree
    assert actual_tree == invocation["outputs"]["workspace_sha256"]
    assert actual_tree == invocation["retained_workspace_sha256"]
    print(f"CANDIDATE_SAFE_TREE_OK {actual_tree}")
    print(
        "AUDIT_INPUT_OPAQUE_CANDIDATE_TREE "
        f"{hashes['candidate_tree_sha256']}"
    )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_tree = safe_tree_sha256(trace_root)
    usage_doc = json.loads(usage.read_text())
    assert trace_tree == usage_doc["source_trace_sha256"]
    print(f"TRACE_SAFE_TREE_OK {trace_tree}")
    print(
        "AUDIT_INPUT_OPAQUE_TRACE_TREE "
        f"{hashes['generation_codex_trace_sha256']}"
    )

    evidence_hashes = result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (relative, actual, expected)
        print(f"RESULT_EVIDENCE_HASH_OK {relative} {actual}")

    trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
    event_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    line_count = 0
    for path in trace_files:
        require_regular(path)
        with path.open() as stream:
            for line_count, line in enumerate(stream, 1):
                event = json.loads(line)
                event_counts[event["type"]] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
    print(f"TRACE_JSON_LINES {line_count}")
    print(f"TRACE_EVENT_COUNTS {dict(sorted(event_counts.items()))}")
    print(f"TRACE_PAYLOAD_COUNTS {dict(sorted(payload_counts.items()))}")
    print("PROVENANCE_CHECK_COMPLETE")


if __name__ == "__main__":
    main()
