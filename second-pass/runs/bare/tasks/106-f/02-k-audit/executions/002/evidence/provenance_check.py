#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit records."""

from __future__ import annotations

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


def pipeline_sha256_tree(root: Path) -> str:
    """Reproduce tools.pipeline_contract.sha256_tree without importing it."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"tree root is not a real directory: {root}")
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
    if not stat.S_ISREG(mode):
        raise ValueError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise ValueError(f"not a real directory: {path}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_structural_match={audit['audit_campaign'] == lock}")

    declared_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    actual_lock_hash = sha256_file(Path("/audit-campaign-lock.json"))
    print(f"audit_campaign_lock declared={declared_lock_hash} actual={actual_lock_hash}")

    required_files = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)
        print(f"regular_file {path} sha256={sha256_file(path)}")

    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference"),
    ]
    for path in required_directories:
        require_directory(path)
        print(f"real_directory {path}")

    for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root)
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                kind = "directory"
            elif stat.S_ISREG(mode):
                kind = f"file sha256={sha256_file(path)}"
            else:
                raise ValueError(f"linked or unsupported entry: {path}")
            print(f"tree_entry {root} {relative} {kind}")

    candidate_tree = pipeline_sha256_tree(Path("/candidate"))
    trace_tree = pipeline_sha256_tree(Path("/generation-evidence/codex-trace"))
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    usage_doc = json.loads(usage.read_text(encoding="utf-8"))
    print(f"pipeline_candidate_tree_actual={candidate_tree}")
    print(
        "pipeline_candidate_tree_generation_result="
        f"{result['outputs']['workspace_sha256']}"
    )
    print(
        "pipeline_candidate_tree_invocation="
        f"{invocation['outputs']['workspace_sha256']}"
    )
    print(f"pipeline_trace_tree_actual={trace_tree}")
    print(f"pipeline_trace_tree_usage={usage_doc['source_trace_sha256']}")
    print(
        "launcher_candidate_tree_record="
        f"{audit['hashes']['candidate_tree_sha256']}"
    )
    print(
        "launcher_trace_tree_record="
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )

    hash_paths = {
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
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    }
    mismatches = 0
    for key, path in hash_paths.items():
        declared = audit["hashes"][key]
        actual = sha256_file(path)
        matches = declared == actual
        mismatches += not matches
        print(f"declared_hash {key} matches={matches} declared={declared} actual={actual}")

    prompt_matches = (
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes()
    )
    translator_matches = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    reference_semantics_present = Path("/reference/reference-semantics").exists()
    print(f"candidate_prompt_matches_trusted={prompt_matches}")
    print(f"candidate_translator_matches_trusted={translator_matches}")
    print(f"reference_semantics_present={reference_semantics_present}")

    failures = [
        audit["record_layout"] != "legacy-selected-stage1",
        audit["semantics_mode"] != "GENERATED_SEMANTICS",
        audit["audit_campaign"] != lock,
        declared_lock_hash != actual_lock_hash,
        mismatches != 0,
        candidate_tree != result["outputs"]["workspace_sha256"],
        candidate_tree != invocation["outputs"]["workspace_sha256"],
        trace_tree != usage_doc["source_trace_sha256"],
        not prompt_matches,
        not translator_matches,
        reference_semantics_present,
    ]
    status = 1 if any(failures) else 0
    print(f"PROVENANCE_CHECK_STATUS={status}")
    return status


if __name__ == "__main__":
    sys.exit(main())
