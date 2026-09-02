#!/usr/bin/env python3
"""Independent audit-mount integrity checks for pipeline-v3 evidence."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T02-42-31-019f9839-c891-7582-ba7d-29d91c2aeab9.jsonl"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement tools.pipeline_contract.sha256_tree independently."""
    digest = hashlib.sha256()
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


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            mode = path.lstat().st_mode
            rel = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256_file(path))
            else:
                result[rel] = ("unsupported", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    assert left_entries == right_entries, "supplied semantics trees differ"
    assert all(kind != "unsupported" for kind, _ in left_entries.values())
    print(f"SEMANTICS_TREE_ENTRIES={len(left_entries)} BYTE_IDENTICAL=true")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert lock == audit["audit_campaign"]
    assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
    print("CAMPAIGN_LOCK_MATCH=true")

    required = [
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
        TRACE,
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required:
        require_regular(path)
    print(f"REQUIRED_REGULAR_FILES={len(required)}")

    hash_pairs = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"):
            "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"):
            "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"):
            "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    }
    for path, key in hash_pairs.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, f"{path}: {actual} != {expected}"
        print(f"SHA256_OK {path} {actual}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in generation_result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"{path}: {actual} != {expected}"
        print(f"GENERATION_SHA256_OK {relative} {actual}")

    assert (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    assert (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print("CANDIDATE_PROMPT_TRANSLATOR_MATCH=true")

    compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )

    candidate_tree = pipeline_tree_sha256(Path("/candidate"))
    semantics_tree = pipeline_tree_sha256(Path("/candidate/reference-semantics"))
    trusted_semantics_tree = pipeline_tree_sha256(
        Path("/reference/reference-semantics")
    )
    trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    assert candidate_tree == generation_result["outputs"]["workspace_sha256"]
    assert semantics_tree == trusted_semantics_tree
    assert semantics_tree == json.loads(Path("/task.json").read_text())["inputs"][
        "reference_semantics_sha256"
    ]
    assert trace_tree == json.loads(
        Path("/generation-evidence/usage.json").read_text()
    )["source_trace_sha256"]
    print(f"PIPELINE_TREE_SHA256 /candidate {candidate_tree}")
    print(f"PIPELINE_TREE_SHA256 supplied-semantics {semantics_tree}")
    print(f"PIPELINE_TREE_SHA256 codex-trace {trace_tree}")

    trace_lines = 0
    with TRACE.open() as stream:
        for trace_lines, line in enumerate(stream, 1):
            json.loads(line)
    assert trace_lines == 1220
    print(f"TRACE_JSON_LINES={trace_lines} ALL_VALID=true")
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
