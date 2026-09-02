#!/usr/bin/env python3
"""Independent read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reproduce the pipeline-v2 tree digest recorded by generation metadata."""
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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
    with path.open("rb") as stream:
        stream.read(1)


def main() -> None:
    audit = json.loads(AUDIT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    lock = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(AUDIT)
    require_regular(lock)
    lock_doc = json.loads(lock.read_text())
    assert lock_doc == audit["audit_campaign"]
    assert sha256_file(lock) == audit["hashes"]["audit_campaign_lock_sha256"]

    required_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    for path, key in required_hashes.items():
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, (path, actual, expected)
        print(f"OK sha256 {path} {actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    assert not Path("/reference/reference-semantics").exists()
    print("OK generated-semantics boundary: no reference semantics mounted")

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [p for p in trace_files if p.is_file()]
    assert len(trace_files) == 1
    trace_rel = trace_files[0].relative_to("/generation-evidence").as_posix()
    trace_file_hash = sha256_file(trace_files[0])
    assert invocation["outputs"]["evidence"][trace_rel] == trace_file_hash
    assert result["outputs"]["evidence"][trace_rel] == trace_file_hash
    trace_rows = [
        json.loads(line) for line in trace_files[0].read_text().splitlines()
    ]
    assert len(trace_rows) == 248
    assert trace_rows[0]["type"] == "session_meta"
    assert trace_rows[-1]["payload"]["type"] == "task_complete"
    print(f"OK structured trace parsed rows={len(trace_rows)} file_sha256={trace_file_hash}")

    candidate_tree = pipeline_tree_hash(Path("/candidate"))
    trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    assert candidate_tree == invocation["retained_workspace_sha256"]
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert trace_tree == usage["source_trace_sha256"]
    print(f"OK pipeline candidate tree {candidate_tree}")
    print(f"OK pipeline trace tree {trace_tree}")

    symlinks = [
        p
        for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference"))
        for p in root.rglob("*")
        if p.is_symlink()
    ]
    assert not symlinks, symlinks
    print("OK no symlinked entries in candidate, generation evidence, or reference")
    print("STAGE1_INTEGRITY=PASS")


if __name__ == "__main__":
    main()
