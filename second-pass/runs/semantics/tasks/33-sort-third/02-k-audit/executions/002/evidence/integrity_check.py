#!/usr/bin/env python3
"""Independent integrity checks for audit stage 1.

This script deliberately recomputes file and pipeline tree digests from the
mounted container paths.  Host provenance paths in audit-input.json are not
used.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
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
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    data = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    assert data["record_layout"] == "legacy-selected-stage1"
    assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert data["audit_campaign"] == lock
    require_regular(Path("/audit-prompt.md"))
    assert file_digest(Path("/audit-prompt.md")) == lock["audit_prompt_sha256"]

    required = [
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

    trace_root = Path("/generation-evidence/codex-trace")
    candidate_root = Path("/candidate")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    for root in (trace_root, candidate_root, trusted_semantics, candidate_semantics):
        tree_entries(root)

    hashes = data["hashes"]
    file_expectations = {
        Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in file_expectations.items():
        actual = file_digest(path)
        assert actual == hashes[key], (path, actual, hashes[key])
        print(f"OK {key} {actual} {path}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()

    trusted_entries = tree_entries(trusted_semantics)
    candidate_entries = tree_entries(candidate_semantics)
    trusted_shape = [(relative, kind) for relative, kind, _ in trusted_entries]
    candidate_shape = [(relative, kind) for relative, kind, _ in candidate_entries]
    assert candidate_shape == trusted_shape
    for (relative, kind, candidate_path), (_, _, trusted_path) in zip(
        candidate_entries, trusted_entries, strict=True
    ):
        if kind == "file":
            assert candidate_path.read_bytes() == trusted_path.read_bytes(), relative

    # These are the independently reconstructed legacy pipeline digests.  They
    # match the stage-1 workspace and trace-source records.
    candidate_digest = pipeline_tree_digest(candidate_root)
    trace_digest = pipeline_tree_digest(trace_root)
    semantics_digest = pipeline_tree_digest(trusted_semantics)
    assert candidate_digest == json.loads(
        Path("/generation-result.json").read_text()
    )["outputs"]["workspace_sha256"]
    assert trace_digest == json.loads(
        Path("/generation-evidence/usage.json").read_text()
    )["source_trace_sha256"]
    assert semantics_digest == hashes["trusted_reference_semantics_manifest_sha256"]

    trace_files = [entry for entry in tree_entries(trace_root) if entry[1] == "file"]
    assert len(trace_files) == 1
    trace_file_hash = file_digest(trace_files[0][2])
    expected_trace_hash = next(
        value
        for key, value in json.loads(
            Path("/generation-result.json").read_text()
        )["outputs"]["evidence"].items()
        if key.startswith("codex-trace/")
    )
    assert trace_file_hash == expected_trace_hash

    print(f"OK campaign block exact match; lock sha256={file_digest(LOCK)}")
    print(f"OK candidate pipeline tree sha256={candidate_digest}")
    print(f"OK trace pipeline tree sha256={trace_digest}")
    print(f"OK supplied semantics pipeline tree sha256={semantics_digest}")
    print(f"OK supplied semantics exact recursive identity; entries={len(trusted_entries)}")
    print("INTEGRITY CHECKS PASSED")


if __name__ == "__main__":
    main()
