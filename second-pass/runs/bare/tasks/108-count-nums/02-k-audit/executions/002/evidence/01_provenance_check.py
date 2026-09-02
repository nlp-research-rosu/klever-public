#!/usr/bin/env python3
"""Independent launcher/mount integrity checks for this audit."""

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


def pipeline_tree_sha256(root: Path) -> str:
    """Independent reimplementation of pipeline-v2's length-delimited digest."""
    root_mode = os.lstat(root).st_mode
    if not stat.S_ISDIR(root_mode) or stat.S_ISLNK(root_mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
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
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = os.lstat(path).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = os.lstat(path).st_mode
    assert stat.S_ISREG(mode) and not stat.S_ISLNK(mode), path
    with path.open("rb") as stream:
        stream.read(1)


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    assert audit_input["record_layout"] == "legacy-selected-stage1"
    assert audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
    paths = {key: Path(value) for key, value in audit_input["container_paths"].items()}

    required = [
        paths["audit_campaign_lock"],
        paths["candidate"],
        paths["canonical"],
        paths["generation_last"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_output"],
        paths["generation_root"],
        paths["generation_trace"],
        paths["run_manifest"],
        paths["stage1_result"],
        paths["task_manifest"],
        paths["translator"],
        paths["trusted_prompt"],
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required:
        mode = os.lstat(path).st_mode
        if path.is_dir():
            assert stat.S_ISDIR(mode) and not stat.S_ISLNK(mode), path
        else:
            require_regular(path)
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        require_regular(usage)

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    assert lock == audit_input["audit_campaign"]
    assert (
        sha256_file(paths["audit_campaign_lock"])
        == audit_input["hashes"]["audit_campaign_lock_sha256"]
    )

    simple_hashes = {
        paths["canonical"]: "canonical_sha256",
        paths["generation_last"]: "generation_codex_last_sha256",
        paths["generation_metrics"]: "generation_metrics_sha256",
        paths["generation_output"]: "generation_codex_output_sha256",
        paths["generation_manifest"]: "stage1_invocation_sha256",
        paths["run_manifest"]: "run_manifest_sha256",
        paths["stage1_result"]: "stage1_result_sha256",
        paths["task_manifest"]: "task_manifest_sha256",
        paths["translator"]: "trusted_translator_sha256",
        paths["trusted_prompt"]: "trusted_prompt_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    if usage.exists():
        simple_hashes[usage] = "generation_usage_sha256"
    for path, field in simple_hashes.items():
        actual = sha256_file(path)
        expected = audit_input["hashes"][field]
        print(f"FILE_HASH {path} actual={actual} expected={expected}")
        assert actual == expected

    candidate = paths["candidate"]
    for root, directories, files in os.walk(candidate, followlinks=False):
        for name in directories + files:
            path = Path(root) / name
            mode = os.lstat(path).st_mode
            assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), path
            assert not stat.S_ISLNK(mode), path
    assert (candidate / "prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == paths["translator"].read_bytes()
    assert not Path("/reference/reference-semantics").exists()
    assert not (candidate / "reference-semantics").exists()

    result = json.loads(paths["stage1_result"].read_text())
    invocation = json.loads(paths["generation_manifest"].read_text())
    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files
    trace_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    trace_lines = 0
    for path in trace_files:
        require_regular(path)
        relative = path.relative_to(paths["generation_root"]).as_posix()
        actual = sha256_file(path)
        print(f"TRACE_FILE_HASH {relative} {actual}")
        assert result["outputs"]["evidence"][relative] == actual
        assert invocation["outputs"]["evidence"][relative] == actual
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                event = json.loads(line)
                trace_lines += 1
                trace_types[event.get("type", "<none>")] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[payload.get("type", "<none>")] += 1

    candidate_tree = pipeline_tree_sha256(candidate)
    trace_tree = pipeline_tree_sha256(paths["generation_trace"])
    print(f"PIPELINE_TREE /candidate {candidate_tree}")
    print(f"PIPELINE_TREE /generation-evidence/codex-trace {trace_tree}")
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["retained_workspace_sha256"]
    if usage.exists():
        usage_doc = json.loads(usage.read_text())
        assert trace_tree == usage_doc["source_trace_sha256"]

    print(f"TRACE_LINES {trace_lines}")
    print(f"TRACE_TYPES {dict(sorted(trace_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print("CAMPAIGN_LOCK_MATCH true")
    print("CANDIDATE_PROMPT_MATCH true")
    print("CANDIDATE_TRANSLATOR_MATCH true")
    print("GENERATED_SEMANTICS_BOUNDARY_OK true")
    print("PROVENANCE_CHECKS_OK true")


if __name__ == "__main__":
    main()
