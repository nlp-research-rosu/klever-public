#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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


def tree_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    result = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            result.append((relative, "directory", None))
        elif stat.S_ISREG(mode):
            result.append((relative, "file", sha256_file(path)))
        elif stat.S_ISLNK(mode):
            result.append((relative, "symlink", os.readlink(path)))
        else:
            result.append((relative, "unsupported", None))
    return result


def main() -> None:
    document = json.loads(AUDIT_INPUT.read_text())
    hashes = document["hashes"]
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    print("record_layout", document["record_layout"])
    print("semantics_mode", document["semantics_mode"])
    print("campaign_exact_match", lock == document["audit_campaign"])

    files = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    for key, path in files.items():
        actual = sha256_file(path)
        print(key, actual, "MATCH" if actual == hashes[key] else "MISMATCH")

    candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
    print("semantics_manifest_exact_match", candidate_semantics == trusted_semantics)
    print("semantics_entries", len(candidate_semantics))
    print(
        "candidate_pipeline_tree_hash",
        pipeline_tree_hash(Path("/candidate")),
    )
    print(
        "candidate_semantics_pipeline_tree_hash",
        pipeline_tree_hash(Path("/candidate/reference-semantics")),
    )
    print(
        "trusted_semantics_pipeline_tree_hash",
        pipeline_tree_hash(Path("/reference/reference-semantics")),
    )
    print(
        "trace_pipeline_tree_hash",
        pipeline_tree_hash(Path("/generation-evidence/codex-trace")),
    )

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    candidate_tree_hash = pipeline_tree_hash(Path("/candidate"))
    print(
        "candidate_matches_generation_result",
        candidate_tree_hash == generation_result["outputs"]["workspace_sha256"],
    )
    print(
        "candidate_matches_invocation",
        candidate_tree_hash == invocation["outputs"]["workspace_sha256"],
    )

    trace_files = sorted(
        Path("/generation-evidence/codex-trace").rglob("*.jsonl")
    )
    for path in trace_files:
        rel = path.relative_to("/generation-evidence").as_posix()
        actual = sha256_file(path)
        expected = generation_result["outputs"]["evidence"].get(rel)
        print("trace_file", rel, actual, "MATCH" if actual == expected else "MISMATCH")


if __name__ == "__main__":
    main()
