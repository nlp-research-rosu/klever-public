#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """The pipeline-v3 tree algorithm in pipeline_contract.py."""
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
                raise AssertionError(f"unsupported/symlinked tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        answer: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                answer[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                answer[relative] = ("file", sha256_file(path))
            else:
                answer[relative] = ("UNSUPPORTED", None)
        return answer

    left_entries = entries(left)
    right_entries = entries(right)
    assert left_entries == right_entries, "supplied-semantics trees differ"
    print(f"supplied_semantics_entries={len(left_entries)} identical=true")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    print("record_layout=pipeline-v3 semantics_mode=SUPPLIED_SEMANTICS")

    paths = {
        "audit_campaign_lock": Path("/audit-campaign-lock.json"),
        "run_manifest": Path("/run.json"),
        "task_manifest": Path("/task.json"),
        "stage1_result": Path("/generation-result.json"),
        "generation_manifest": Path("/generation-evidence/invocation.json"),
        "generation_metrics": Path("/generation-evidence/metrics.json"),
        "generation_runtime_metrics": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage": Path("/generation-evidence/usage.json"),
        "generation_last": Path("/generation-evidence/codex-last.txt"),
        "generation_output": Path("/generation-evidence/codex-output.log"),
        "generation_prompt": Path("/generation-evidence/prompt.txt"),
        "canonical": Path("/reference/canonical.py"),
        "trusted_prompt": Path("/reference/prompt.py"),
        "translator": Path("/reference/py2mpy.py"),
        "candidate_prompt": Path("/candidate/prompt.py"),
        "candidate_translator": Path("/candidate/py2mpy.py"),
    }
    for path in paths.values():
        require_regular(path)
    for path in (
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ):
        require_directory(path)
    print("required_mount_types=all_real_files_or_directories")

    recorded = audit["hashes"]
    hash_expectations = {
        "audit_campaign_lock": "audit_campaign_lock_sha256",
        "run_manifest": "run_manifest_sha256",
        "task_manifest": "task_manifest_sha256",
        "stage1_result": "stage1_result_sha256",
        "generation_manifest": "stage1_invocation_sha256",
        "generation_metrics": "generation_metrics_sha256",
        "generation_runtime_metrics": "generation_runtime_metrics_sha256",
        "generation_usage": "generation_usage_sha256",
        "generation_last": "generation_codex_last_sha256",
        "generation_output": "generation_codex_output_sha256",
        "generation_prompt": "generation_prompt_sha256",
        "canonical": "canonical_sha256",
        "trusted_prompt": "trusted_prompt_sha256",
        "translator": "trusted_translator_sha256",
        "candidate_prompt": "candidate_prompt_sha256",
        "candidate_translator": "candidate_translator_sha256",
    }
    for label, hash_key in hash_expectations.items():
        actual = sha256_file(paths[label])
        expected = recorded[hash_key]
        assert actual == expected, (label, actual, expected)
        print(f"{label}_sha256={actual} matches_record=true")

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    assert lock == audit["audit_campaign"]
    print("campaign_lock_matches_campaign_block=true")

    result = json.loads(paths["stage1_result"].read_text())
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (relative, actual, expected)
        print(f"generation_evidence_sha256 {relative} {actual} matches=true")

    trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
    usage = json.loads(paths["generation_usage"].read_text())
    assert trace_tree == usage["source_trace_sha256"]
    print(f"generation_trace_tree_sha256={trace_tree} matches_usage=true")

    candidate_tree = sha256_tree(Path("/candidate"))
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    print(
        f"candidate_pipeline_tree_sha256={candidate_tree} "
        "matches_generation_result=true"
    )
    # The audit pack also records a transport-level digest under
    # candidate_tree_sha256. It is a different digest scheme from pipeline-v3's
    # sha256_tree, so it is printed rather than compared as if interchangeable.
    print(
        "audit_pack_candidate_tree_sha256="
        f"{recorded['candidate_tree_sha256']} digest_scheme=transport"
    )

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    compare_trees(candidate_semantics, trusted_semantics)
    semantics_tree = sha256_tree(trusted_semantics)
    assert semantics_tree == recorded[
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert semantics_tree == audit["manifest"]["inputs"][
        "reference_semantics_sha256"
    ]
    print(
        f"trusted_semantics_pipeline_tree_sha256={semantics_tree} "
        "matches_manifest=true"
    )

    assert paths["candidate_prompt"].read_bytes() == paths[
        "trusted_prompt"
    ].read_bytes()
    assert paths["candidate_translator"].read_bytes() == paths[
        "translator"
    ].read_bytes()
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")

    invocation = json.loads(paths["generation_manifest"].read_text())
    metrics = json.loads(paths["generation_metrics"].read_text())
    runtime = json.loads(paths["generation_runtime_metrics"].read_text())
    assert invocation["status"] == metrics["status"] == "SUCCEEDED"
    assert invocation["exit_code"] == metrics["exit_code"] == 0
    assert runtime["final_exit_code"] == runtime["harness_exit_code"] == 0
    print("generation_status_records_consistent=true")
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
