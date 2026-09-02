#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the retained-workspace hash, including names and node kinds."""
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
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


def require_regular(path: Path) -> None:
    assert path.is_file() and not path.is_symlink(), f"not a real regular file: {path}"


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    required = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
    ]
    for path in required:
        require_regular(path)

    trace = Path("/generation-evidence/codex-trace")
    candidate = Path("/candidate")
    assert trace.is_dir() and not trace.is_symlink()
    assert candidate.is_dir() and not candidate.is_symlink()
    forbidden = Path("/reference/reference-semantics")
    assert not forbidden.exists() and not forbidden.is_symlink()

    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    assert lock == audit["audit_campaign"]

    expected_files = {
        "/audit-campaign-lock.json": hashes["audit_campaign_lock_sha256"],
        "/reference/canonical.py": hashes["canonical_sha256"],
        "/reference/prompt.py": hashes["trusted_prompt_sha256"],
        "/reference/py2mpy.py": hashes["trusted_translator_sha256"],
        "/candidate/prompt.py": hashes["candidate_prompt_sha256"],
        "/candidate/py2mpy.py": hashes["candidate_translator_sha256"],
        "/run.json": hashes["run_manifest_sha256"],
        "/task.json": hashes["task_manifest_sha256"],
        "/generation-result.json": hashes["stage1_result_sha256"],
        "/generation-evidence/invocation.json": hashes["stage1_invocation_sha256"],
        "/generation-evidence/metrics.json": hashes["generation_metrics_sha256"],
        "/generation-evidence/codex-last.txt": hashes["generation_codex_last_sha256"],
        "/generation-evidence/codex-output.log": hashes["generation_codex_output_sha256"],
        "/generation-evidence/prompt.txt": hashes["generation_prompt_sha256"],
        "/generation-evidence/usage.json": hashes["generation_usage_sha256"],
    }
    for name, expected in expected_files.items():
        observed = sha256_file(Path(name))
        print(f"SHA256 {name} {observed}")
        assert observed == expected, (name, observed, expected)

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    candidate_hash = pipeline_tree_hash(candidate)
    trace_hash = pipeline_tree_hash(trace)
    print(f"PIPELINE_TREE_SHA256 /candidate {candidate_hash}")
    print(f"PIPELINE_TREE_SHA256 {trace} {trace_hash}")
    assert candidate_hash == invocation["retained_workspace_sha256"]
    assert candidate_hash == result["outputs"]["workspace_sha256"]
    assert trace_hash == json.loads(
        Path("/generation-evidence/usage.json").read_text()
    )["source_trace_sha256"]

    trace_files = sorted(trace.rglob("*.jsonl"))
    assert len(trace_files) == 1
    trace_rel = trace_files[0].relative_to(Path("/generation-evidence")).as_posix()
    trace_file_hash = sha256_file(trace_files[0])
    print(f"SHA256 /generation-evidence/{trace_rel} {trace_file_hash}")
    assert trace_file_hash == invocation["outputs"]["evidence"][trace_rel]
    line_count = 0
    with trace_files[0].open() as stream:
        for line_count, line in enumerate(stream, 1):
            json.loads(line)
    print(f"TRACE_JSONL_LINES {line_count}")

    for path in sorted(candidate.rglob("*")):
        kind = "DIR" if path.is_dir() else "FILE"
        if path.is_symlink():
            kind = "SYMLINK"
        suffix = f" {sha256_file(path)}" if kind == "FILE" else ""
        print(f"CANDIDATE_{kind} {path.relative_to(candidate)}{suffix}")
        assert kind != "SYMLINK"

    print("INTEGRITY_CHECK PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
