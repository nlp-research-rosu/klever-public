#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Reimplement pipeline_contract.sha256_tree without importing launcher code."""
    if not stat.S_ISDIR(root.lstat().st_mode):
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


def require_kind(path: Path, expected: str) -> None:
    mode = path.lstat().st_mode
    actual = (
        "file"
        if stat.S_ISREG(mode)
        else "directory"
        if stat.S_ISDIR(mode)
        else "other"
    )
    if actual != expected:
        raise AssertionError(f"{path}: expected {expected}, observed {actual}")
    print(f"OK kind {expected}: {path}")


def compare_trees(left: Path, right: Path) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
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
                    result[relative] = ("file", file_hash(path))
                else:
                    result[relative] = ("unsupported", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    if left_entries != right_entries:
        missing = sorted(set(left_entries) - set(right_entries))
        additional = sorted(set(right_entries) - set(left_entries))
        changed = sorted(
            key
            for key in set(left_entries) & set(right_entries)
            if left_entries[key] != right_entries[key]
        )
        raise AssertionError(
            "tree mismatch: "
            f"missing={missing}, additional={additional}, changed={changed}"
        )
    print(f"OK exact typed tree equality: {left} == {right}")
    for relative in sorted(left_entries):
        kind, digest = left_entries[relative]
        suffix = f" sha256={digest}" if digest is not None else ""
        print(f"TREE {kind} {relative}{suffix}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["problem_id"] == "155-even-odd-count"
    print("OK layout/mode/problem: pipeline-v3 SUPPLIED_SEMANTICS 155-even-odd-count")

    required_files = [
        AUDIT_INPUT,
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
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_kind(path, "file")
    for path in required_directories:
        require_kind(path, "directory")

    for name, mounted in sorted(audit["container_paths"].items()):
        path = Path(mounted)
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
            f"container path {name} is linked or unsupported: {path}"
        )
        print(f"OK container_paths[{name}]={path}")

    campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
    assert campaign == audit["audit_campaign"]
    print("OK audit campaign lock object equals audit_input.audit_campaign")

    hashes = audit["hashes"]
    direct_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path(
            "/generation-evidence/codex-last.txt"
        ),
        "generation_codex_output_sha256": Path(
            "/generation-evidence/codex-output.log"
        ),
        "generation_metrics_sha256": Path(
            "/generation-evidence/metrics.json"
        ),
        "generation_prompt_sha256": Path(
            "/generation-evidence/prompt.txt"
        ),
        "generation_runtime_metrics_sha256": Path(
            "/generation-evidence/runtime-metrics.json"
        ),
        "generation_usage_sha256": Path(
            "/generation-evidence/usage.json"
        ),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "stage1_invocation_sha256": Path(
            "/generation-evidence/invocation.json"
        ),
    }
    for field, path in direct_hashes.items():
        observed = file_hash(path)
        expected = hashes[field]
        assert observed == expected, (
            f"hash mismatch {field}: expected {expected}, observed {observed}"
        )
        print(f"OK hash {field}={observed} path={path}")

    assert file_hash(Path("/candidate/prompt.py")) == file_hash(
        Path("/reference/prompt.py")
    )
    assert file_hash(Path("/candidate/py2mpy.py")) == file_hash(
        Path("/reference/py2mpy.py")
    )
    print("OK candidate prompt and translator are byte-identical to trusted mounts")

    compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    trusted_tree_hash = tree_hash(Path("/reference/reference-semantics"))
    candidate_semantics_hash = tree_hash(
        Path("/candidate/reference-semantics")
    )
    assert trusted_tree_hash == hashes[
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert trusted_tree_hash == audit["manifest"]["inputs"][
        "reference_semantics_sha256"
    ]
    assert candidate_semantics_hash == trusted_tree_hash
    print(f"OK independent supplied-semantics tree hash={trusted_tree_hash}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_hash = tree_hash(Path("/generation-evidence/codex-trace"))
    candidate_hash = tree_hash(Path("/candidate"))
    assert trace_hash == usage["source_trace_sha256"]
    assert candidate_hash == generation_result["outputs"]["workspace_sha256"]
    assert candidate_hash == invocation["outputs"]["workspace_sha256"]
    print(f"OK independent structured-trace tree hash={trace_hash}")
    print(f"OK independent candidate tree hash={candidate_hash}")

    evidence_hashes = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_kind(path, "file")
        observed = file_hash(path)
        assert observed == expected, (
            f"generation-result evidence hash mismatch for {relative}"
        )
        print(f"OK generation-result evidence hash {relative}={observed}")

    task_manifest = json.loads(Path("/task.json").read_text())
    embedded_manifest = audit["manifest"]
    for field in (
        "schema_version",
        "problem_id",
        "current_stage",
        "condition",
        "inputs",
    ):
        assert task_manifest[field] == embedded_manifest[field], (
            f"task manifest field differs from embedded manifest: {field}"
        )
    assert embedded_manifest["config"] == audit["manifest_config"]
    print(
        "OK task manifest core fields equal embedded audit-input manifest; "
        "embedded-only config equals manifest_config"
    )
    print("STAGE1_CHECKS=PASS")


if __name__ == "__main__":
    main()
