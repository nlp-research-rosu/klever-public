#!/usr/bin/env python3
"""Independent launcher/provenance checks for the audit record."""

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


def sha256_tree(root: Path) -> str:
    """Pipeline-v3 tree hash, independently implemented from its record format."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
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
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"not a real regular file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_tree(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise ValueError(f"not a real directory: {path}")
    sha256_tree(path)


def compare_trees(left: Path, right: Path) -> list[str]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                mode = child.stat(follow_symlinks=False).st_mode
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    result[relative] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[relative] = ("file", sha256_file(path))
                elif stat.S_ISLNK(mode):
                    result[relative] = ("symlink", os.readlink(path))
                else:
                    result[relative] = ("unsupported", None)
        return result

    li = inventory(left)
    ri = inventory(right)
    mismatches = []
    for name in sorted(set(li) | set(ri)):
        if li.get(name) != ri.get(name):
            mismatches.append(f"{name}: candidate={li.get(name)!r} trusted={ri.get(name)!r}")
    return mismatches


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    paths = document["container_paths"]
    hashes = document["hashes"]

    print(f"record_layout={document['record_layout']}")
    print(f"semantics_mode={document['semantics_mode']}")
    print(f"problem_id={document['problem_id']}")

    required_files = {
        "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
        "canonical": Path(paths["canonical"]),
        "translator": Path(paths["translator"]),
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_manifest": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "runtime_metrics": Path(paths["generation_root"]) / "runtime-metrics.json",
        "usage": Path(paths["generation_root"]) / "usage.json",
    }
    for label, path in required_files.items():
        require_regular(path)
        print(f"required_file {label} OK {path} sha256={sha256_file(path)}")

    required_trees = {
        "candidate": Path(paths["candidate"]),
        "generation_trace": Path(paths["generation_trace"]),
        "trusted_reference_semantics": Path("/reference/reference-semantics"),
        "candidate_reference_semantics": Path(paths["candidate"]) / "reference-semantics",
    }
    for label, path in required_trees.items():
        require_tree(path)
        print(f"required_tree {label} OK {path} pipeline_sha256={sha256_tree(path)}")

    expected_file_hashes = {
        required_files["audit_campaign_lock"]: hashes["audit_campaign_lock_sha256"],
        required_files["canonical"]: hashes["canonical_sha256"],
        required_files["translator"]: hashes["trusted_translator_sha256"],
        required_files["trusted_prompt"]: hashes["trusted_prompt_sha256"],
        required_files["run_manifest"]: hashes["run_manifest_sha256"],
        required_files["task_manifest"]: hashes["task_manifest_sha256"],
        required_files["stage1_result"]: hashes["stage1_result_sha256"],
        required_files["generation_manifest"]: hashes["stage1_invocation_sha256"],
        required_files["generation_metrics"]: hashes["generation_metrics_sha256"],
        required_files["generation_last"]: hashes["generation_codex_last_sha256"],
        required_files["generation_output"]: hashes["generation_codex_output_sha256"],
        required_files["generation_prompt"]: hashes["generation_prompt_sha256"],
        required_files["runtime_metrics"]: hashes["generation_runtime_metrics_sha256"],
        required_files["usage"]: hashes["generation_usage_sha256"],
    }
    failures: list[str] = []
    for path, expected in expected_file_hashes.items():
        actual = sha256_file(path)
        status = "MATCH" if actual == expected else "MISMATCH"
        print(f"recorded_hash {status} {path} expected={expected} actual={actual}")
        if status != "MATCH":
            failures.append(f"hash mismatch: {path}")

    lock = json.loads(required_files["audit_campaign_lock"].read_text(encoding="utf-8"))
    lock_match = lock == document["audit_campaign"]
    print(f"campaign_block_exact_match={lock_match}")
    if not lock_match:
        failures.append("campaign lock content differs from audit_campaign block")

    trace_hash = sha256_tree(required_trees["generation_trace"])
    usage = json.loads(required_files["usage"].read_text(encoding="utf-8"))
    print(
        "trace_tree_matches_usage_source_trace="
        f"{trace_hash == usage['source_trace_sha256']} "
        f"expected={usage['source_trace_sha256']} actual={trace_hash}"
    )
    if trace_hash != usage["source_trace_sha256"]:
        failures.append("generation trace differs from usage source trace hash")

    generation_result = json.loads(
        required_files["stage1_result"].read_text(encoding="utf-8")
    )
    evidence_hashes = generation_result["outputs"]["evidence"]
    generation_root = Path(paths["generation_root"])
    for relative, expected in sorted(evidence_hashes.items()):
        artifact = generation_root / relative
        require_regular(artifact)
        actual = sha256_file(artifact)
        status = "MATCH" if actual == expected else "MISMATCH"
        print(
            f"generation_result_evidence_hash {status} {artifact} "
            f"expected={expected} actual={actual}"
        )
        if status != "MATCH":
            failures.append(f"generation-result evidence hash mismatch: {artifact}")

    task_hash = sha256_file(required_files["task_manifest"])
    print(f"manifest_is_task_manifest={task_hash == hashes['manifest_sha256']}")

    stage1 = generation_result
    candidate_tree_hash = sha256_tree(required_trees["candidate"])
    stage1_workspace_hash = stage1["outputs"]["workspace_sha256"]
    print(
        "candidate_matches_stage1_workspace="
        f"{candidate_tree_hash == stage1_workspace_hash} "
        f"expected={stage1_workspace_hash} actual={candidate_tree_hash}"
    )
    if candidate_tree_hash != stage1_workspace_hash:
        failures.append("candidate mount differs from generation-result workspace")

    trusted_tree_hash = sha256_tree(required_trees["trusted_reference_semantics"])
    candidate_semantics_hash = sha256_tree(required_trees["candidate_reference_semantics"])
    expected_semantics_manifest = hashes["trusted_reference_semantics_manifest_sha256"]
    print(
        "trusted_semantics_manifest_hash_match="
        f"{trusted_tree_hash == expected_semantics_manifest} "
        f"expected={expected_semantics_manifest} actual={trusted_tree_hash}"
    )
    if trusted_tree_hash != expected_semantics_manifest:
        failures.append("trusted semantics tree differs from recorded manifest hash")

    semantics_mismatches = compare_trees(
        required_trees["candidate_reference_semantics"],
        required_trees["trusted_reference_semantics"],
    )
    print(f"semantics_recursive_mismatch_count={len(semantics_mismatches)}")
    for mismatch in semantics_mismatches:
        print(f"semantics_mismatch {mismatch}")
    if semantics_mismatches:
        failures.append("candidate supplied-semantics tree differs from trusted tree")
    if candidate_semantics_hash != trusted_tree_hash:
        failures.append("candidate and trusted semantics tree hashes differ")

    candidate_prompt = Path(paths["candidate"]) / "prompt.py"
    candidate_translator = Path(paths["candidate"]) / "py2mpy.py"
    for candidate_path, trusted_path, label in (
        (candidate_prompt, required_files["trusted_prompt"], "prompt"),
        (candidate_translator, required_files["translator"], "translator"),
    ):
        require_regular(candidate_path)
        equal = candidate_path.read_bytes() == trusted_path.read_bytes()
        print(f"candidate_{label}_byte_identity={equal}")
        if not equal:
            failures.append(f"candidate {label} differs from trusted mount")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
