#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_digest(root: Path) -> str:
    """Reproduce the pipeline-v2 length-delimited tree manifest digest."""
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
                raise AssertionError(f"unsupported or linked entry: {path}")
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    def collect(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", digest_file(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_entries = collect(left)
    right_entries = collect(right)
    assert left_entries == right_entries, "candidate/reference semantics differ"
    print(f"SEMANTICS_ENTRY_COUNT: {len(left_entries)}")
    print("SEMANTICS_RECURSIVE_IDENTITY: PASS")


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit["audit_campaign"]
    assert digest_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("CAMPAIGN_BLOCK_AND_HASH: PASS")

    paths = audit["container_paths"]
    required_files = [
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
        Path(paths["generation_root"]) / "usage.json",
    ]
    for path in required_files:
        require_regular(path)
    require_directory(Path(paths["generation_trace"]))
    trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
    trace_regular = []
    for path in trace_files:
        mode = path.lstat().st_mode
        assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), (
            f"linked/unsupported trace entry: {path}"
        )
        if stat.S_ISREG(mode):
            trace_regular.append(path)
    assert trace_regular, "structured trace has no regular records"
    print(f"REQUIRED_RECORDS_AND_TRACE: PASS ({len(trace_regular)} trace file)")

    expected_files = {
        Path(paths["run_manifest"]): "run_manifest_sha256",
        Path(paths["task_manifest"]): "task_manifest_sha256",
        Path(paths["stage1_result"]): "stage1_result_sha256",
        Path(paths["generation_manifest"]): "stage1_invocation_sha256",
        Path(paths["generation_metrics"]): "generation_metrics_sha256",
        Path(paths["generation_last"]): "generation_codex_last_sha256",
        Path(paths["generation_output"]): "generation_codex_output_sha256",
        Path(paths["generation_root"]) / "prompt.txt": "generation_prompt_sha256",
        Path(paths["generation_root"]) / "usage.json": "generation_usage_sha256",
        Path(paths["canonical"]): "canonical_sha256",
        Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
        Path(paths["translator"]): "trusted_translator_sha256",
    }
    for path, key in expected_files.items():
        require_regular(path)
        actual = digest_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, f"{key}: {actual} != {expected}"
        print(f"HASH_OK {key} {actual}")

    candidate = Path(paths["candidate"])
    require_directory(candidate)
    require_regular(candidate / "prompt.py")
    require_regular(candidate / "py2mpy.py")
    assert (candidate / "prompt.py").read_bytes() == Path(
        paths["trusted_prompt"]
    ).read_bytes()
    assert (candidate / "py2mpy.py").read_bytes() == Path(
        paths["translator"]
    ).read_bytes()
    print("CANDIDATE_PROMPT_TRANSLATOR_IDENTITY: PASS")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    require_directory(trusted_semantics)
    require_directory(candidate_semantics)
    compare_trees(candidate_semantics, trusted_semantics)
    candidate_manifest = manifest_digest(candidate_semantics)
    trusted_manifest = manifest_digest(trusted_semantics)
    expected_manifest = audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert candidate_manifest == trusted_manifest == expected_manifest
    print(f"SEMANTICS_MANIFEST_HASH_OK {trusted_manifest}")

    result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    candidate_manifest = manifest_digest(candidate)
    assert (
        candidate_manifest
        == result["outputs"]["workspace_sha256"]
        == invocation["retained_workspace_sha256"]
    )
    print(f"CANDIDATE_WORKSPACE_MANIFEST_HASH_OK {candidate_manifest}")
    for source_name, document in (("result", result), ("invocation", invocation)):
        for relative, expected in document["outputs"]["evidence"].items():
            path = Path(paths["generation_root"]) / relative
            require_regular(path)
            actual = digest_file(path)
            assert actual == expected, (
                f"{source_name} evidence hash mismatch: {relative}"
            )
        print(f"{source_name.upper()}_EVIDENCE_HASHES: PASS")

    trace_manifest = manifest_digest(Path(paths["generation_trace"]))
    usage = json.loads(
        (Path(paths["generation_root"]) / "usage.json").read_text()
    )
    assert trace_manifest == usage["source_trace_sha256"]
    print(f"TRACE_MANIFEST_HASH_OK {trace_manifest}")

    # Parse every JSON and JSONL record, including the entire structured trace.
    json_paths = [
        AUDIT_INPUT,
        LOCK,
        *required_files[:5],
        required_files[-1],
        Path(paths["generation_root"]) / "legacy-metrics.json",
        Path(paths["generation_root"]) / "legacy-run-input.json",
    ]
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    trace_records = 0
    for path in trace_regular:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                json.loads(line)
                trace_records += 1
    print(f"STRUCTURED_RECORD_PARSE: PASS ({trace_records} trace records)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, KeyError) as error:
        print(f"PROVENANCE_CHECK_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
