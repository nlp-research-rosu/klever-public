#!/usr/bin/env python3
"""Independently validate the mounted audit records and their recorded hashes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    """Reproduce the length-delimited launcher tree digest."""
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f"tree root is not a real directory: {path}")
    entries: list[tuple[str, str, Path]] = []
    pending = [path]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {child_path}")
    digest = hashlib.sha256()
    for relative, kind, child_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = child_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with child_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def real_file(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and os.access(path, os.R_OK)


def report_check(name: str, actual: object, expected: object) -> bool:
    matches = actual == expected
    print(
        json.dumps(
            {"check": name, "actual": actual, "expected": expected, "match": matches},
            sort_keys=True,
        )
    )
    return matches


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    hashes = document["hashes"]
    paths = document["container_paths"]
    failures = 0

    if not report_check("record_layout", document["record_layout"], "legacy-selected-stage1"):
        failures += 1
    if not report_check("semantics_mode", document["semantics_mode"], "GENERATED_SEMANTICS"):
        failures += 1
    if not report_check("campaign_block_equals_lock", document["audit_campaign"], lock):
        failures += 1
    if not report_check(
        "campaign_lock_sha256", file_digest(CAMPAIGN_LOCK), hashes["audit_campaign_lock_sha256"]
    ):
        failures += 1

    required = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": CAMPAIGN_LOCK,
        "run": Path(paths["run_manifest"]),
        "task": Path(paths["task_manifest"]),
        "generation_result": Path(paths["stage1_result"]),
        "invocation": Path(paths["generation_manifest"]),
        "metrics": Path(paths["generation_metrics"]),
        "codex_last": Path(paths["generation_last"]),
        "codex_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
    }
    for name, path in required.items():
        if not report_check(f"regular_readable:{name}", real_file(path), True):
            failures += 1

    trace_root = Path(paths["generation_trace"])
    roots = {
        "candidate": Path(paths["candidate"]),
        "generation_root": Path(paths["generation_root"]),
        "trace_root": trace_root,
        "reference_root": Path(paths["canonical"]).parent,
    }
    for name, root in roots.items():
        try:
            digest = tree_digest(root)
            print(json.dumps({"tree": name, "path": str(root), "sha256": digest}))
        except Exception as error:
            print(json.dumps({"tree": name, "path": str(root), "error": str(error)}))
            failures += 1

    file_hash_checks = {
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
        "canonical_sha256": Path(paths["canonical"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "trusted_translator_sha256": Path(paths["translator"]),
    }
    usage_path = Path(paths["generation_root"]) / "usage.json"
    if usage_path.exists():
        file_hash_checks["generation_usage_sha256"] = usage_path
    for key, path in file_hash_checks.items():
        actual = file_digest(path)
        if not report_check(key, actual, hashes[key]):
            failures += 1

    candidate_pipeline_digest = tree_digest(Path(paths["candidate"]))
    if not report_check(
        "candidate_pipeline_tree_sha256",
        candidate_pipeline_digest,
        invocation["retained_workspace_sha256"],
    ):
        failures += 1
    trace_pipeline_digest = tree_digest(trace_root)
    if not report_check(
        "trace_pipeline_tree_sha256",
        trace_pipeline_digest,
        usage["source_trace_sha256"],
    ):
        failures += 1
    print(
        json.dumps(
            {
                "note": "audit-input tree fields use an unspecified launcher digest scheme",
                "recorded_candidate_tree_sha256": hashes["candidate_tree_sha256"],
                "recorded_generation_codex_trace_sha256": hashes[
                    "generation_codex_trace_sha256"
                ],
                "independent_pipeline_candidate_sha256": candidate_pipeline_digest,
                "independent_pipeline_trace_sha256": trace_pipeline_digest,
            },
            sort_keys=True,
        )
    )
    if not report_check(
        "candidate_prompt_byte_identity",
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes(),
        True,
    ):
        failures += 1
    if not report_check(
        "candidate_translator_byte_identity",
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes(),
        True,
    ):
        failures += 1
    if not report_check(
        "trusted_reference_semantics_absent",
        not (Path(paths["canonical"]).parent / "reference-semantics").exists(),
        True,
    ):
        failures += 1
    if not report_check(
        "candidate_reference_semantics_absent",
        not (Path(paths["candidate"]) / "reference-semantics").exists(),
        True,
    ):
        failures += 1

    print(json.dumps({"integrity_failures": failures}))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
