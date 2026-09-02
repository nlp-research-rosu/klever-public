#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
REFERENCE = Path("/reference")
CANDIDATE = Path("/candidate")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        raise AssertionError(f"missing required artifact: {path}")
    assert stat.S_ISREG(mode), f"required artifact is not a regular file: {path}"
    assert os.access(path, os.R_OK), f"required artifact is unreadable: {path}"


def check_hash(path: Path, expected: str, label: str) -> None:
    require_regular(path)
    actual = sha256(path)
    status = "OK" if actual == expected else "MISMATCH"
    print(f"{status} {label}: {path} sha256={actual} expected={expected}")
    assert actual == expected


def tree_manifest(root: Path) -> list[tuple[str, str, int]]:
    assert root.is_dir() and not root.is_symlink(), (
        f"tree missing, not a directory, or symlinked: {root}"
    )
    result: list[tuple[str, str, int]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), f"symlink forbidden in tree: {path}"
        if stat.S_ISDIR(mode):
            continue
        assert stat.S_ISREG(mode), f"non-regular tree entry: {path}"
        result.append((relative, sha256(path), path.stat().st_size))
    return result


def tree_layout(root: Path) -> list[tuple[str, str]]:
    """Return every relative entry and exact regular-file/directory type."""
    assert root.is_dir() and not root.is_symlink(), (
        f"tree missing, not a directory, or symlinked: {root}"
    )
    result: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        assert not stat.S_ISLNK(mode), f"symlink forbidden in tree: {path}"
        if stat.S_ISDIR(mode):
            kind = "directory"
        elif stat.S_ISREG(mode):
            kind = "regular-file"
        else:
            raise AssertionError(f"non-regular/non-directory tree entry: {path}")
        result.append((relative, kind))
    return result


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(LOCK)
    data = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    assert data["record_layout"] == "legacy-selected-stage1"
    assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == data["audit_campaign"], "campaign lock JSON does not match audit block"
    check_hash(
        LOCK,
        data["hashes"]["audit_campaign_lock_sha256"],
        "campaign lock",
    )

    expected_container_paths = {
        "audit_campaign_lock": Path("/audit-campaign-lock.json"),
        "candidate": Path("/candidate"),
        "canonical": Path("/reference/canonical.py"),
        "generation_last": Path("/generation-evidence/codex-last.txt"),
        "generation_manifest": Path("/generation-evidence/invocation.json"),
        "generation_metrics": Path("/generation-evidence/metrics.json"),
        "generation_output": Path("/generation-evidence/codex-output.log"),
        "generation_root": Path("/generation-evidence"),
        "generation_trace": Path("/generation-evidence/codex-trace"),
        "run_manifest": Path("/run.json"),
        "stage1_result": Path("/generation-result.json"),
        "task_manifest": Path("/task.json"),
        "translator": Path("/reference/py2mpy.py"),
        "trusted_prompt": Path("/reference/prompt.py"),
    }
    for key, expected in expected_container_paths.items():
        declared = Path(data["container_paths"][key])
        assert declared == expected, f"unexpected container path for {key}: {declared}"
        assert declared.exists(), f"launcher-declared provenance mount missing: {declared}"
        print(f"OK container_paths[{key}]={declared}")

    hashes = data["hashes"]
    declared_files = [
        (Path("/reference/canonical.py"), hashes["canonical_sha256"], "canonical"),
        (Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"], "trusted prompt"),
        (Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"], "trusted translator"),
        (Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"], "candidate prompt"),
        (Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"], "candidate translator"),
        (Path("/run.json"), hashes["run_manifest_sha256"], "run manifest"),
        (Path("/task.json"), hashes["task_manifest_sha256"], "task manifest"),
        (Path("/generation-result.json"), hashes["stage1_result_sha256"], "stage1 result"),
        (GENERATION / "invocation.json", hashes["stage1_invocation_sha256"], "invocation"),
        (GENERATION / "metrics.json", hashes["generation_metrics_sha256"], "metrics"),
        (GENERATION / "usage.json", hashes["generation_usage_sha256"], "usage"),
        (GENERATION / "prompt.txt", hashes["generation_prompt_sha256"], "generation prompt"),
        (GENERATION / "codex-last.txt", hashes["generation_codex_last_sha256"], "codex last"),
        (GENERATION / "codex-output.log", hashes["generation_codex_output_sha256"], "codex output"),
    ]
    for path, expected, label in declared_files:
        check_hash(path, expected, label)

    required_layout_files = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    for path in required_layout_files:
        require_regular(path)
    if (GENERATION / "usage.json").exists():
        require_regular(GENERATION / "usage.json")
    print("OK all required legacy-selected-stage1 records are readable regular files")

    invocation = json.loads((GENERATION / "invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    output_hashes = invocation["outputs"]["evidence"]
    assert output_hashes == result["outputs"]["evidence"]
    for relative, expected in sorted(output_hashes.items()):
        check_hash(GENERATION / relative, expected, f"generation evidence {relative}")

    trace_entries = sorted((GENERATION / "codex-trace").rglob("*"))
    assert all(
        (path.is_dir() or path.is_file()) and not path.is_symlink()
        for path in trace_entries
    ), "structured trace contains a symlink or non-file/non-directory entry"
    trace_files = [path for path in trace_entries if path.is_file()]
    assert trace_files, "structured trace is empty"
    assert len(trace_files) == 1, f"unexpected trace file count: {len(trace_files)}"
    type_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    line_count = 0
    final_messages: list[str] = []
    with trace_files[0].open() as stream:
        for line_count, line in enumerate(stream, start=1):
            event = json.loads(line)
            event_type = str(event.get("type", "<missing>"))
            type_counts[event_type] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_counts[payload_type] += 1
                if event_type == "response_item":
                    response_types[payload_type] += 1
                if payload_type in {"agent_message", "message"}:
                    message = payload.get("message")
                    if isinstance(message, str):
                        final_messages.append(message)
    print(f"OK structured trace parsed: {trace_files[0]} lines={line_count}")
    print(f"trace top-level type counts={dict(sorted(type_counts.items()))}")
    print(f"trace payload type counts={dict(sorted(payload_counts.items()))}")
    print(f"trace response-item type counts={dict(sorted(response_types.items()))}")
    if final_messages:
        print(f"trace last textual message={final_messages[-1][-500:]!r}")

    trusted_tree = tree_manifest(REFERENCE / "reference-semantics")
    candidate_tree = tree_manifest(CANDIDATE / "reference-semantics")
    trusted_layout = tree_layout(REFERENCE / "reference-semantics")
    candidate_layout = tree_layout(CANDIDATE / "reference-semantics")
    assert candidate_layout == trusted_layout, (
        "candidate supplied-semantics entry paths/types differ"
    )
    assert candidate_tree == trusted_tree, "candidate supplied-semantics tree differs"
    manifest_bytes = json.dumps(
        trusted_tree, ensure_ascii=True, separators=(",", ":")
    ).encode()
    independent_tree_hash = hashlib.sha256(manifest_bytes).hexdigest()
    print(
        "OK supplied-semantics recursive identity: "
        f"entries={len(trusted_layout)} files={len(trusted_tree)} "
        f"independent_manifest_sha256={independent_tree_hash}"
    )
    for relative, digest, size in trusted_tree:
        print(f"TREE {relative} size={size} sha256={digest}")

    candidate_entries = tree_manifest(CANDIDATE)
    print(
        "candidate independent recursive manifest: "
        f"regular_files={len(candidate_entries)} "
        f"sha256={hashlib.sha256(json.dumps(candidate_entries, separators=(',', ':')).encode()).hexdigest()}"
    )

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for relative in required_candidate:
        require_regular(CANDIDATE / relative)
        print(f"OK required candidate artifact {relative}")

    assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()
    assert (GENERATION / "prompt.txt").read_bytes() != b"", "generation prompt is empty"
    print("OK candidate prompt and translator are byte-identical to trusted mounts")
    print("STAGE1_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"STAGE1_INTEGRITY_FAILURE: {type(error).__name__}: {error}", file=sys.stderr)
        raise
