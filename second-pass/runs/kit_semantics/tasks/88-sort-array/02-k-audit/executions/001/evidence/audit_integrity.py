#!/usr/bin/env python3
"""Independent integrity checks for the mounted pipeline-v3 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat


AUDIT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree digest."""
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
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
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"not a real regular file: {path}")


def compare_trees(left: Path, right: Path) -> tuple[int, str]:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", file_sha256(path))
            else:
                result[relative] = ("unsupported", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    if left_entries != right_entries:
        left_only = sorted(left_entries.keys() - right_entries.keys())
        right_only = sorted(right_entries.keys() - left_entries.keys())
        changed = sorted(
            key
            for key in left_entries.keys() & right_entries.keys()
            if left_entries[key] != right_entries[key]
        )
        raise AssertionError(
            f"tree mismatch: left_only={left_only}, right_only={right_only}, "
            f"changed={changed}"
        )
    return len(left_entries), pipeline_tree_sha256(left)


def main() -> None:
    document = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert document["record_layout"] == "pipeline-v3"
    assert document["semantics_mode"] == "SUPPLIED_SEMANTICS"

    required_files = [
        AUDIT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required_files:
        require_regular(path)

    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_directories:
        if not path.is_dir() or path.is_symlink():
            raise AssertionError(f"not a real directory: {path}")

    for root in required_directories:
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
                raise AssertionError(f"linked or unsupported entry: {path}")

    hashes = document["hashes"]
    named_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
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
        "/generation-evidence/runtime-metrics.json":
            "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log":
            "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for filename, key in named_hashes.items():
        actual = file_sha256(Path(filename))
        expected = hashes[key]
        assert actual == expected, (filename, expected, actual)
        print(f"FILE_HASH_OK {key} {actual} {filename}")

    campaign = json.loads(
        Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
    )
    assert campaign == document["audit_campaign"]
    print("CAMPAIGN_BLOCK_OK exact JSON object match")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    count, semantics_digest = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    assert semantics_digest == document["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    print(
        "SEMANTICS_TREE_OK "
        f"entries={count} pipeline_sha256={semantics_digest}"
    )

    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    evidence_hashes = generation_result["outputs"]["evidence"]
    assert evidence_hashes == invocation["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        actual = file_sha256(Path("/generation-evidence") / relative)
        assert actual == expected, (relative, expected, actual)
        print(f"GENERATION_RECORD_HASH_OK {actual} {relative}")

    candidate_digest = pipeline_tree_sha256(Path("/candidate"))
    expected_candidate = generation_result["outputs"]["workspace_sha256"]
    assert candidate_digest == expected_candidate
    print(f"CANDIDATE_PIPELINE_TREE_OK {candidate_digest}")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_digest = pipeline_tree_sha256(trace_root)
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert trace_digest == usage["source_trace_sha256"]
    trace_lines = 0
    for trace_file in sorted(trace_root.rglob("*.jsonl")):
        require_regular(trace_file)
        for line in trace_file.read_text(encoding="utf-8").splitlines():
            json.loads(line)
            trace_lines += 1
    print(
        f"TRACE_OK files={len(list(trace_root.rglob('*.jsonl')))} "
        f"lines={trace_lines} pipeline_sha256={trace_digest}"
    )

    print("INTEGRITY_RESULT PASS")


if __name__ == "__main__":
    main()
