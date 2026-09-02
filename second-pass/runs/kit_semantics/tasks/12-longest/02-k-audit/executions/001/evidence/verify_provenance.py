#!/usr/bin/env python3
"""Independent pipeline-v3 provenance and mount-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise AssertionError(f"linked or unsupported entry: {path}")
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


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require_regular(path: Path) -> None:
    assert stat.S_ISREG(path.lstat().st_mode), f"not a real regular file: {path}"


def main() -> None:
    audit = load("/audit-input.json")
    lock = load("/audit-campaign-lock.json")
    run = load("/run.json")
    task = load("/task.json")
    result = load("/generation-result.json")
    invocation = load("/generation-evidence/invocation.json")
    usage = load("/generation-evidence/usage.json")

    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert audit["audit_campaign"] == lock
    assert (
        sha256_file(Path("/audit-campaign-lock.json"))
        == audit["hashes"]["audit_campaign_lock_sha256"]
    )
    print("OK campaign block byte-hash and exact JSON equality")

    required = [
        "/audit-input.json",
        "/audit-campaign-lock.json",
        "/run.json",
        "/task.json",
        "/generation-result.json",
        "/generation-evidence/invocation.json",
        "/generation-evidence/metrics.json",
        "/generation-evidence/runtime-metrics.json",
        "/generation-evidence/usage.json",
        "/generation-evidence/codex-last.txt",
        "/generation-evidence/codex-output.log",
        "/generation-evidence/prompt.txt",
        "/reference/canonical.py",
        "/reference/prompt.py",
        "/reference/py2mpy.py",
        "/candidate/prompt.py",
        "/candidate/py2mpy.py",
    ]
    for name in required:
        require_regular(Path(name))
    for name in [
        "/candidate",
        "/candidate/reference-semantics",
        "/reference/reference-semantics",
        "/generation-evidence/codex-trace",
    ]:
        assert stat.S_ISDIR(Path(name).lstat().st_mode), f"not a real directory: {name}"
    print("OK all required pipeline-v3 records and declared mounts are real entries")

    direct_hashes = {
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for name, key in direct_hashes.items():
        actual = sha256_file(Path(name))
        assert actual == audit["hashes"][key], (name, actual, audit["hashes"][key])
    print(f"OK {len(direct_hashes)} launcher-recorded direct file hashes")

    for key, value in task.items():
        assert audit["manifest"][key] == value
    assert audit["manifest"]["config"] == audit["manifest_config"]
    assert run["run_id"] == audit["run_id"]
    assert result["status"] == invocation["status"] == "SUCCEEDED"
    assert result["session_id"] == invocation["session_id"]
    assert result["outputs"] == invocation["outputs"]
    print("OK task/run/result/invocation cross-record identity fields")

    candidate_tree = sha256_tree(Path("/candidate"))
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    print(f"OK candidate pipeline tree digest {candidate_tree}")

    trusted_semantics_tree = sha256_tree(Path("/reference/reference-semantics"))
    candidate_semantics_tree = sha256_tree(Path("/candidate/reference-semantics"))
    assert trusted_semantics_tree == candidate_semantics_tree
    assert (
        trusted_semantics_tree
        == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
    )
    assert trusted_semantics_tree == task["inputs"]["reference_semantics_sha256"]
    print(f"OK supplied-semantics pipeline tree digest {trusted_semantics_tree}")

    trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
    assert trace_tree == usage["source_trace_sha256"]
    print(f"OK structured-trace pipeline tree digest {trace_tree}")

    evidence_map = invocation["outputs"]["evidence"]
    for relative, expected in sorted(evidence_map.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (relative, actual, expected)
    print(f"OK {len(evidence_map)} invocation evidence hashes")

    assert sha256_file(Path("/candidate/prompt.py")) == sha256_file(
        Path("/reference/prompt.py")
    )
    assert sha256_file(Path("/candidate/py2mpy.py")) == sha256_file(
        Path("/reference/py2mpy.py")
    )
    assert sha256_file(Path("/generation-evidence/prompt.txt")) == task["inputs"][
        "instruction_prompt_sha256"
    ]
    print("OK trusted prompt, translator, and generation prompt bindings")


if __name__ == "__main__":
    main()
