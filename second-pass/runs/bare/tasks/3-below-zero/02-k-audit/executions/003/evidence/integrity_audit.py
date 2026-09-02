#!/usr/bin/env python3
"""Independent mounted-input integrity audit for HumanEval/3."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplement the pipeline-v2 content/tree digest (no imported helper)."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
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
        raise ValueError(f"required regular file is missing or mistyped: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise ValueError(f"required real directory is missing or mistyped: {path}")


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    result = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label}: {result} expected={expected} actual={actual} path={path}")
    if actual != expected:
        raise ValueError(f"hash mismatch for {label}")


def main() -> None:
    require_regular(AUDIT_INPUT)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    if audit["record_layout"] != "legacy-selected-stage1":
        raise ValueError(f"unexpected record layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        raise ValueError(f"unexpected semantics mode: {audit['semantics_mode']}")

    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    required_files = [
        AUDIT_INPUT,
        paths["audit_campaign_lock"],
        paths["canonical"],
        paths["trusted_prompt"],
        paths["translator"],
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_last"],
        paths["generation_output"],
        paths["generation_root"] / "prompt.txt",
    ]
    usage = paths["generation_root"] / "usage.json"
    if usage.exists() or usage.is_symlink():
        required_files.append(usage)
    for path in required_files:
        require_regular(path)

    required_directories = [
        paths["candidate"],
        paths["generation_root"],
        paths["generation_trace"],
    ]
    for path in required_directories:
        require_directory(path)

    reference_semantics = Path("/reference/reference-semantics")
    if reference_semantics.exists() or reference_semantics.is_symlink():
        raise ValueError(
            "GENERATED_SEMANTICS breach: /reference/reference-semantics exists"
        )
    print("reference-semantics: correctly absent")

    campaign_lock = json.loads(
        paths["audit_campaign_lock"].read_text(encoding="utf-8")
    )
    if campaign_lock != audit["audit_campaign"]:
        raise ValueError("campaign lock does not equal audit campaign block")
    print("campaign block: exact JSON-object match")

    hashes = audit["hashes"]
    file_checks = {
        "audit_campaign_lock_sha256": paths["audit_campaign_lock"],
        "canonical_sha256": paths["canonical"],
        "trusted_prompt_sha256": paths["trusted_prompt"],
        "trusted_translator_sha256": paths["translator"],
        "candidate_prompt_sha256": paths["candidate"] / "prompt.py",
        "candidate_translator_sha256": paths["candidate"] / "py2mpy.py",
        "run_manifest_sha256": paths["run_manifest"],
        "task_manifest_sha256": paths["task_manifest"],
        "stage1_result_sha256": paths["stage1_result"],
        "stage1_invocation_sha256": paths["generation_manifest"],
        "generation_metrics_sha256": paths["generation_metrics"],
        "generation_codex_last_sha256": paths["generation_last"],
        "generation_codex_output_sha256": paths["generation_output"],
        "generation_prompt_sha256": paths["generation_root"] / "prompt.txt",
        "generation_usage_sha256": usage,
    }
    for key, path in file_checks.items():
        expected = hashes.get(key)
        if expected is not None:
            check_hash(key, path, expected)

    if (paths["candidate"] / "prompt.py").read_bytes() != paths[
        "trusted_prompt"
    ].read_bytes():
        raise ValueError("candidate prompt differs from trusted prompt")
    if (paths["candidate"] / "py2mpy.py").read_bytes() != paths[
        "translator"
    ].read_bytes():
        raise ValueError("candidate translator differs from trusted translator")
    print("candidate prompt/translator: byte-identical to trusted mounts")

    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file()]
    trace_links = [path for path in trace_files if path.is_symlink()]
    if trace_links:
        raise ValueError(f"trace contains symlinks: {trace_links}")
    generation_result = json.loads(
        paths["stage1_result"].read_text(encoding="utf-8")
    )
    evidence_hashes = generation_result["outputs"]["evidence"]
    for path in trace_regular:
        relative = path.relative_to(paths["generation_root"]).as_posix()
        if relative not in evidence_hashes:
            raise ValueError(f"unrecorded trace file: {relative}")
        check_hash(
            f"generation-result:{relative}", path, evidence_hashes[relative]
        )

    candidate_digest = pipeline_tree_digest(paths["candidate"])
    trace_digest = pipeline_tree_digest(paths["generation_trace"])
    expected_workspace = generation_result["outputs"]["workspace_sha256"]
    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    if candidate_digest != expected_workspace:
        raise ValueError("candidate tree differs from generation-result workspace")
    if candidate_digest != invocation["retained_workspace_sha256"]:
        raise ValueError("candidate tree differs from retained invocation workspace")
    usage_doc = json.loads(usage.read_text(encoding="utf-8"))
    if trace_digest != usage_doc["source_trace_sha256"]:
        raise ValueError("trace tree differs from usage source trace")
    print(
        "candidate pipeline tree digest: MATCH "
        f"expected={expected_workspace} actual={candidate_digest}"
    )
    print(
        "trace pipeline tree digest: MATCH "
        f"expected={usage_doc['source_trace_sha256']} actual={trace_digest}"
    )

    # The audit manifest also records launcher-specific tree hashes without
    # declaring their serialization. Preserve them explicitly; content is
    # independently pinned above by the pipeline digest and per-file hashes.
    print(
        "launcher candidate_tree_sha256 (serialization not declared): "
        f"{hashes['candidate_tree_sha256']}"
    )
    print(
        "launcher generation_codex_trace_sha256 "
        f"(serialization not declared): {hashes['generation_codex_trace_sha256']}"
    )

    integrity = audit["integrity"]
    expected_integrity = {
        "candidate_prompt_matches_trusted": True,
        "candidate_reference_semantics_matches_trusted": None,
        "candidate_translator_matches_trusted": True,
        "manifest_prompt_hash_matches_trusted": True,
        "manifest_reference_semantics_hash_matches_trusted": None,
        "manifest_translator_hash_matches_trusted": True,
    }
    if integrity != expected_integrity:
        raise ValueError(f"unexpected integrity block: {integrity}")
    print("declared integrity block: consistent with independent checks")

    for json_path in (
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        usage,
    ):
        document = json.loads(json_path.read_text(encoding="utf-8"))
        print(f"parsed JSON object: {json_path} keys={sorted(document)}")

    prompt_hash = sha256_file(paths["generation_root"] / "prompt.txt")
    task = json.loads(paths["task_manifest"].read_text(encoding="utf-8"))
    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    result = json.loads(paths["stage1_result"].read_text(encoding="utf-8"))
    if task["inputs"]["instruction_prompt_sha256"] != prompt_hash:
        raise ValueError("task instruction prompt hash mismatch")
    if invocation["prompt_sha256"] != prompt_hash:
        raise ValueError("invocation prompt hash mismatch")
    if result["outputs"]["evidence"]["prompt.txt"] != prompt_hash:
        raise ValueError("result prompt hash mismatch")
    print("generation prompt provenance chain: MATCH")

    print("INTEGRITY_AUDIT: PASS")


if __name__ == "__main__":
    main()
