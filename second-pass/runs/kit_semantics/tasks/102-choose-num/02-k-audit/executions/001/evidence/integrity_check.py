#!/usr/bin/env python3
"""Independent provenance and mount-integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplementation of the pipeline-v3 length-delimited tree digest."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"not a real directory: {root}")
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required record is not a real regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def compare_trees(left: Path, right: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
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

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    assert left_inventory == right_inventory, "supplied semantics trees differ"
    print(f"semantics_entries={len(left_inventory)} byte_identical=true")


def main() -> None:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit_input = json.loads(AUDIT_INPUT.read_text())
    campaign_lock = json.loads(CAMPAIGN_LOCK.read_text())

    assert audit_input["record_layout"] == "pipeline-v3"
    assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit_input["audit_campaign"] == campaign_lock
    hashes = audit_input["hashes"]
    assert sha256_file(CAMPAIGN_LOCK) == hashes["audit_campaign_lock_sha256"]
    print("campaign_lock_content_match=true")
    print(f"audit_campaign_lock_sha256={sha256_file(CAMPAIGN_LOCK)}")

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
    ]
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files, "structured trace is empty"
    for path in required + trace_files:
        require_regular(path)
    print(f"required_pipeline_records={len(required)} trace_files={len(trace_files)} all_regular=true")

    direct_expectations = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in direct_expectations.items():
        require_regular(path)
        actual = sha256_file(path)
        assert actual == hashes[key], f"{key}: expected {hashes[key]}, got {actual}"
        print(f"{key}={actual} match=true")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    trace_rel = next(key for key in generation_result["outputs"]["evidence"] if key.startswith("codex-trace/"))
    trace_path = Path("/generation-evidence") / trace_rel
    trace_expected = generation_result["outputs"]["evidence"][trace_rel]
    assert sha256_file(trace_path) == trace_expected
    assert invocation["outputs"]["evidence"][trace_rel] == trace_expected
    print(f"structured_trace_file_sha256={trace_expected} match=true")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")

    compare_trees(Path("/candidate/reference-semantics"), Path("/reference/reference-semantics"))
    candidate_semantics_hash = pipeline_tree_sha256(Path("/candidate/reference-semantics"))
    trusted_semantics_hash = pipeline_tree_sha256(Path("/reference/reference-semantics"))
    assert candidate_semantics_hash == trusted_semantics_hash
    assert candidate_semantics_hash == hashes["trusted_reference_semantics_manifest_sha256"]
    print(f"supplied_semantics_pipeline_tree_sha256={candidate_semantics_hash} match=true")

    candidate_hash = pipeline_tree_sha256(Path("/candidate"))
    trace_hash = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    assert candidate_hash == generation_result["outputs"]["workspace_sha256"]
    assert trace_hash == json.loads(Path("/generation-evidence/usage.json").read_text())["source_trace_sha256"]
    print(f"candidate_pipeline_tree_sha256={candidate_hash} match_generation_result=true")
    print(f"trace_pipeline_tree_sha256={trace_hash} match_usage_record=true")
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
