#!/usr/bin/env python3
"""Independently verify launcher records and mounted provenance."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independent implementation of the recorded pipeline tree format."""
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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

    digest = hashlib.sha256()
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    lock = json.loads(lock_path.read_text())
    assert audit["audit_campaign"] == lock
    assert file_sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("campaign lock: structural and hash match")

    required = {
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    }
    for hash_key, path in required.items():
        require_regular(path)
        actual = file_sha256(path)
        expected = audit["hashes"][hash_key]
        assert actual == expected, (path, actual, expected)
        print(f"{path}: {actual} MATCH")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("candidate prompt and translator: byte-identical to trusted inputs")

    assert not Path("/reference/reference-semantics").exists()
    assert audit["hashes"]["trusted_reference_semantics_sha256"] is None
    assert audit["hashes"]["candidate_reference_semantics_sha256"] is None
    print("generated-semantics boundary: no reference semantics present")

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_digest = pipeline_tree_sha256(Path("/candidate"))
    trace_digest = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    assert candidate_digest == invocation["retained_workspace_sha256"]
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    assert trace_digest == usage["source_trace_sha256"]
    print(f"candidate pipeline tree: {candidate_digest} MATCH")
    print(f"trace pipeline tree: {trace_digest} MATCH")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert len(trace_files) == 1
    trace_rel = trace_files[0].relative_to("/generation-evidence").as_posix()
    trace_file_digest = file_sha256(trace_files[0])
    assert (
        trace_file_digest
        == invocation["outputs"]["evidence"][trace_rel]
        == result["outputs"]["evidence"][trace_rel]
    )
    print(f"trace file: {trace_file_digest} MATCH")

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        links = [path for path in root.rglob("*") if path.is_symlink()]
        assert not links, links
    print("mounted candidate/reference/generation trees: no symlinks")

    # runtime-metrics.json was not historically recorded for this declared layout.
    assert not Path("/generation-evidence/runtime-metrics.json").exists()
    print("legacy-selected-stage1 expected absence: runtime-metrics.json")
    print("PROVENANCE_CHECKS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
