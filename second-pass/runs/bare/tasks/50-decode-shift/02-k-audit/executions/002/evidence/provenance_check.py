#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

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


def sha256_tree(root: Path) -> str:
    """The pipeline-v2 tree digest used by generation invocation records."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"not a real directory: {root}")
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
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["problem_id"] == "50-decode-shift"
    assert audit["condition"] == "bare"

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
    # usage.json is optional for this legacy layout, but present and checked.
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)

    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_directories:
        require_directory(path)
    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/reference/reference-semantics").is_symlink()

    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    assert lock == audit["audit_campaign"]
    assert (
        sha256_file(Path("/audit-campaign-lock.json"))
        == audit["hashes"]["audit_campaign_lock_sha256"]
    )

    named_hashes = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
    }
    if usage.exists():
        named_hashes[str(usage)] = "generation_usage_sha256"
    for filename, key in named_hashes.items():
        actual = sha256_file(Path(filename))
        expected = audit["hashes"][key]
        assert actual == expected, (filename, actual, expected)

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    candidate_files = sorted(Path("/candidate").iterdir())
    for path in candidate_files:
        require_regular(path)

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    candidate_digest = sha256_tree(Path("/candidate"))
    assert candidate_digest == invocation["retained_workspace_sha256"]
    assert candidate_digest == invocation["outputs"]["workspace_sha256"]

    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    assert candidate_digest == result["outputs"]["workspace_sha256"]

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    assert len(trace_files) == 1
    trace_relative = trace_files[0].relative_to(trace_root).as_posix()
    trace_key = f"codex-trace/{trace_relative}"
    trace_file_hash = sha256_file(trace_files[0])
    assert trace_file_hash == result["outputs"]["evidence"][trace_key]
    assert trace_file_hash == invocation["outputs"]["evidence"][trace_key]

    trace_tree_hash = sha256_tree(trace_root)
    if usage.exists():
        usage_doc = json.loads(usage.read_text(encoding="utf-8"))
        assert trace_tree_hash == usage_doc["source_trace_sha256"]

    # Parse every structured-trace line and classify it. This both reads and
    # validates the entire required structured record.
    counts: Counter[str] = Counter()
    with trace_files[0].open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            counts[
                "/".join(
                    str(value)
                    for value in (
                        event.get("type", ""),
                        event.get("payload", {}).get("type", ""),
                        event.get("payload", {}).get("role", ""),
                    )
                )
            ] += 1
    assert line_number == 314

    # Read the complete unstructured records, not merely their heads/tails.
    log_bytes = Path("/generation-evidence/codex-output.log").read_bytes()
    last_bytes = Path("/generation-evidence/codex-last.txt").read_bytes()
    prompt_bytes = Path("/generation-evidence/prompt.txt").read_bytes()

    print("PROVENANCE_CHECK=PASS")
    print(f"record_layout={audit['record_layout']}")
    print(f"campaign_lock_sha256={sha256_file(Path('/audit-campaign-lock.json'))}")
    print(f"candidate_pipeline_tree_sha256={candidate_digest}")
    print(f"trace_file_sha256={trace_file_hash}")
    print(f"trace_pipeline_tree_sha256={trace_tree_hash}")
    print(f"trace_lines={line_number}")
    print(f"trace_event_counts={dict(sorted(counts.items()))}")
    print(f"codex_output_bytes_read={len(log_bytes)}")
    print(f"codex_last_bytes_read={len(last_bytes)}")
    print(f"generation_prompt_bytes_read={len(prompt_bytes)}")
    print("candidate_entries=" + ",".join(path.name for path in candidate_files))
    print("reference_semantics=ABSENT_AS_REQUIRED")


if __name__ == "__main__":
    main()
