#!/usr/bin/env python3
"""Reviewer-authored integrity checks for the mounted audit inputs."""

from __future__ import annotations

from collections import Counter
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise AssertionError(f"not a real directory: {path}")


def inspect_tree(root: Path) -> tuple[int, int]:
    require_directory(root)
    directories = 1
    files = 0
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in dirnames:
            path = base / name
            require_directory(path)
            directories += 1
        for name in filenames:
            path = base / name
            require_regular(path)
            files += 1
    return directories, files


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v2 length-prefixed tree digest."""
    require_directory(root)
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
                raise AssertionError(f"unsupported tree entry: {path}")
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


def main() -> int:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["mount_reference_semantics"] is False

    lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
    require_regular(lock_path)
    lock = json.loads(lock_path.read_text())
    assert lock == audit["audit_campaign"]

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required.append(Path("/generation-evidence/usage.json"))
    for path in required:
        require_regular(path)

    for key in ("candidate", "generation_root", "generation_trace"):
        require_directory(Path(audit["container_paths"][key]))
    for key in ("canonical", "translator", "trusted_prompt"):
        require_regular(Path(audit["container_paths"][key]))

    recorded = audit["hashes"]
    direct_hashes = {
        "audit_campaign_lock_sha256": lock_path,
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
    }
    if "generation_usage_sha256" in recorded:
        direct_hashes["generation_usage_sha256"] = Path(
            "/generation-evidence/usage.json"
        )
    for key, path in direct_hashes.items():
        actual = sha256_file(path)
        print(f"{key}: expected={recorded[key]} actual={actual}")
        assert actual == recorded[key]

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/candidate/reference-semantics").exists()

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        directories, files = inspect_tree(root)
        print(f"tree {root}: directories={directories} files={files} symlinks=0")

    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    result = json.loads(Path("/generation-result.json").read_text())
    candidate_digest = pipeline_tree_sha256(Path("/candidate"))
    print(f"candidate pipeline tree sha256={candidate_digest}")
    assert candidate_digest == invocation["retained_workspace_sha256"]
    assert candidate_digest == invocation["outputs"]["workspace_sha256"]
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    print(
        "launcher candidate snapshot sha256="
        + recorded["candidate_tree_sha256"]
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert trace_files
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    response_item_types: Counter[str] = Counter()
    tool_calls: Counter[str] = Counter()
    line_count = 0
    for path in trace_files:
        require_regular(path)
        with path.open() as stream:
            for line_count_in_file, line in enumerate(stream, 1):
                record = json.loads(line)
                line_count += 1
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if record.get("type") == "response_item":
                        response_item_types[str(payload.get("type"))] += 1
                        if payload.get("type") == "function_call":
                            tool_calls[str(payload.get("name"))] += 1
        print(
            f"trace {path}: lines={line_count_in_file} "
            f"sha256={sha256_file(path)}"
        )
    print(f"trace total JSON records={line_count}")
    print(f"top-level event types={dict(sorted(event_types.items()))}")
    print(f"payload types={dict(sorted(payload_types.items()))}")
    print(f"response item types={dict(sorted(response_item_types.items()))}")
    print(f"tool calls={dict(sorted(tool_calls.items()))}")
    trace_digest = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(f"trace pipeline tree sha256={trace_digest}")
    assert trace_digest == usage["source_trace_sha256"]
    print(
        "launcher trace snapshot sha256="
        + recorded["generation_codex_trace_sha256"]
    )
    print("PROVENANCE_CHECK_OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"PROVENANCE_CHECK_FAILED: {error}", file=sys.stderr)
        raise
