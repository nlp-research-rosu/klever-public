#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

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
    """Reimplement /opt/humaneval/tools/pipeline_contract.py:sha256_tree."""
    root_mode = root.stat(follow_symlinks=False).st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported entry: {path}")
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


def regular(path: Path) -> bool:
    return stat.S_ISREG(path.stat(follow_symlinks=False).st_mode)


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    expected = audit["hashes"]
    paths = {
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
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    }
    required = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
    ]
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    required.extend(path for path in trace_files if path.is_file())

    print("record_layout", audit["record_layout"])
    print("semantics_mode", audit["semantics_mode"])
    print("campaign_structural_match", audit["audit_campaign"] == lock)
    print("required_records")
    for path in required:
        print(path, "exists", path.exists(), "regular", regular(path))
    print("recorded_file_hashes")
    for key, path in paths.items():
        actual = sha256_file(path)
        print(key, "expected", expected[key], "actual", actual,
              "match", expected[key] == actual)

    trace = Path(
        "/generation-evidence/codex-trace/2026/07/22/"
        "rollout-2026-07-22T04-26-46-019f8926-2706-76c1-9838-b7b318fd85d9.jsonl"
    )
    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    trace_rel = trace.relative_to("/generation-evidence").as_posix()
    trace_file_hash = sha256_file(trace)
    print("trace_file_sha256", trace_file_hash)
    print(
        "trace_file_matches_generation_result",
        trace_file_hash == result["outputs"]["evidence"][trace_rel],
    )
    print(
        "trace_file_matches_invocation",
        trace_file_hash == invocation["outputs"]["evidence"][trace_rel],
    )
    print(
        "candidate_pipeline_tree_sha256",
        pipeline_tree_hash(Path("/candidate")),
    )
    print(
        "candidate_matches_stage1_workspace",
        pipeline_tree_hash(Path("/candidate"))
        == result["outputs"]["workspace_sha256"],
    )
    print(
        "trace_pipeline_tree_sha256",
        pipeline_tree_hash(Path("/generation-evidence/codex-trace")),
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    print(
        "trace_matches_usage_source_tree",
        pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
        == usage["source_trace_sha256"],
    )
    print(
        "candidate_prompt_byte_identical",
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
    )
    print(
        "candidate_translator_byte_identical",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
    )
    print(
        "generated_mode_reference_semantics_absent",
        not Path("/reference/reference-semantics").exists(),
    )
    symlinks = [
        str(path)
        for root in (Path("/candidate"), Path("/reference"),
                     Path("/generation-evidence"))
        for path in root.rglob("*")
        if path.is_symlink()
    ]
    print("symlinks", symlinks)


if __name__ == "__main__":
    main()
