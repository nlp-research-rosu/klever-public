#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(dirs + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            digest = sha256_file(path) if kind == "file" else None
            entries[rel] = (kind, digest)
    return entries


def independent_tree_hash(entries: dict[str, tuple[str, str | None]]) -> str:
    """Reviewer-defined deterministic hash over path, kind, and file digest."""
    digest = hashlib.sha256()
    for rel, (kind, file_digest) in sorted(entries.items()):
        row = f"{kind}\0{rel}\0{file_digest or ''}\n".encode()
        digest.update(row)
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"missing: {path}")
        return
    kind = entry_kind(path)
    if kind != "file":
        failures.append(f"expected regular file, got {kind}: {path}")
    elif not os.access(path, os.R_OK):
        failures.append(f"unreadable: {path}")


def compare_recorded(
    label: str,
    path: Path,
    expected: str,
    failures: list[str],
) -> None:
    require_regular(path, failures)
    if path.is_file() and not path.is_symlink():
        actual = sha256_file(path)
        status = "MATCH" if actual == expected else "MISMATCH"
        print(f"HASH {label} {status} expected={expected} actual={actual} path={path}")
        if actual != expected:
            failures.append(f"hash mismatch: {label}")


def main() -> int:
    failures: list[str] = []
    require_regular(AUDIT_INPUT, failures)
    data = json.loads(AUDIT_INPUT.read_text())
    print(
        "DECLARATION"
        f" record_layout={data.get('record_layout')}"
        f" semantics_mode={data.get('semantics_mode')}"
        f" problem_id={data.get('problem_id')}"
        f" condition={data.get('condition')}"
    )
    if data.get("record_layout") != "pipeline-v3":
        failures.append("record_layout is not pipeline-v3")
    if data.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("semantics_mode is not SUPPLIED_SEMANTICS")

    paths = {
        key: Path(value) for key, value in data["container_paths"].items()
    }
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
        paths["generation_root"] / "runtime-metrics.json",
        paths["generation_root"] / "usage.json",
        paths["generation_root"] / "prompt.txt",
    ]
    for path in required_files:
        require_regular(path, failures)

    candidate = paths["candidate"]
    reference_semantics = Path("/reference/reference-semantics")
    for directory in [
        candidate,
        paths["generation_root"],
        paths["generation_trace"],
        reference_semantics,
        candidate / "reference-semantics",
    ]:
        if not directory.exists():
            failures.append(f"missing directory: {directory}")
        elif entry_kind(directory) != "directory":
            failures.append(
                f"expected directory, got {entry_kind(directory)}: {directory}"
            )

    lock = json.loads(paths["audit_campaign_lock"].read_text())
    campaign_match = lock == data["audit_campaign"]
    print(f"CAMPAIGN_BLOCK exact_json_match={str(campaign_match).lower()}")
    if not campaign_match:
        failures.append("audit campaign lock does not equal audit_campaign block")

    hashes = data["hashes"]
    recorded_files = [
        (
            "audit_campaign_lock_sha256",
            paths["audit_campaign_lock"],
            hashes["audit_campaign_lock_sha256"],
        ),
        ("canonical_sha256", paths["canonical"], hashes["canonical_sha256"]),
        (
            "trusted_prompt_sha256",
            paths["trusted_prompt"],
            hashes["trusted_prompt_sha256"],
        ),
        (
            "candidate_prompt_sha256",
            candidate / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        (
            "trusted_translator_sha256",
            paths["translator"],
            hashes["trusted_translator_sha256"],
        ),
        (
            "candidate_translator_sha256",
            candidate / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
        (
            "run_manifest_sha256",
            paths["run_manifest"],
            hashes["run_manifest_sha256"],
        ),
        (
            "task_manifest_sha256",
            paths["task_manifest"],
            hashes["task_manifest_sha256"],
        ),
        (
            "stage1_result_sha256",
            paths["stage1_result"],
            hashes["stage1_result_sha256"],
        ),
        (
            "stage1_invocation_sha256",
            paths["generation_manifest"],
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics_sha256",
            paths["generation_metrics"],
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_runtime_metrics_sha256",
            paths["generation_root"] / "runtime-metrics.json",
            hashes["generation_runtime_metrics_sha256"],
        ),
        (
            "generation_usage_sha256",
            paths["generation_root"] / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_prompt_sha256",
            paths["generation_root"] / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        (
            "generation_codex_last_sha256",
            paths["generation_last"],
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_codex_output_sha256",
            paths["generation_output"],
            hashes["generation_codex_output_sha256"],
        ),
    ]
    for label, path, expected in recorded_files:
        compare_recorded(label, path, expected, failures)

    prompt_equal = (candidate / "prompt.py").read_bytes() == paths[
        "trusted_prompt"
    ].read_bytes()
    translator_equal = (candidate / "py2mpy.py").read_bytes() == paths[
        "translator"
    ].read_bytes()
    print(f"CANDIDATE_PROMPT byte_equal={str(prompt_equal).lower()}")
    print(f"CANDIDATE_TRANSLATOR byte_equal={str(translator_equal).lower()}")
    if not prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        failures.append("candidate translator differs from trusted translator")

    trusted_entries = tree_entries(reference_semantics)
    candidate_entries = tree_entries(candidate / "reference-semantics")
    exact_tree_match = trusted_entries == candidate_entries
    print(
        "REFERENCE_SEMANTICS"
        f" exact_recursive_match={str(exact_tree_match).lower()}"
        f" trusted_entries={len(trusted_entries)}"
        f" candidate_entries={len(candidate_entries)}"
        f" trusted_reviewer_hash={independent_tree_hash(trusted_entries)}"
        f" candidate_reviewer_hash={independent_tree_hash(candidate_entries)}"
    )
    if not exact_tree_match:
        all_paths = sorted(set(trusted_entries) | set(candidate_entries))
        for rel in all_paths:
            if trusted_entries.get(rel) != candidate_entries.get(rel):
                print(
                    f"REFERENCE_SEMANTICS_DIFF {rel}"
                    f" trusted={trusted_entries.get(rel)}"
                    f" candidate={candidate_entries.get(rel)}"
                )
        failures.append("candidate reference semantics differs recursively")

    candidate_all_entries = tree_entries(candidate)
    candidate_symlinks = [
        rel for rel, (kind, _) in candidate_all_entries.items() if kind == "symlink"
    ]
    candidate_other = [
        rel for rel, (kind, _) in candidate_all_entries.items() if kind == "other"
    ]
    print(
        "CANDIDATE_TREE"
        f" entries={len(candidate_all_entries)}"
        f" symlinks={len(candidate_symlinks)}"
        f" other_types={len(candidate_other)}"
        f" reviewer_hash={independent_tree_hash(candidate_all_entries)}"
        f" launcher_recorded_hash={hashes['candidate_tree_sha256']}"
    )
    if candidate_symlinks or candidate_other:
        print(f"CANDIDATE_BAD_TYPES symlinks={candidate_symlinks} other={candidate_other}")

    invocation = json.loads(paths["generation_manifest"].read_text())
    stage_result = json.loads(paths["stage1_result"].read_text())
    invocation_outputs = invocation["outputs"]["evidence"]
    result_outputs = stage_result["outputs"]["evidence"]
    evidence_records_match = invocation_outputs == result_outputs
    print(
        f"GENERATION_RECORDS invocation_result_evidence_match="
        f"{str(evidence_records_match).lower()}"
    )
    if not evidence_records_match:
        failures.append("invocation and generation result evidence maps differ")
    for rel, expected in sorted(invocation_outputs.items()):
        path = paths["generation_root"] / rel
        compare_recorded(f"invocation.outputs.evidence[{rel}]", path, expected, failures)

    trace_entries = tree_entries(paths["generation_trace"])
    trace_symlinks = [
        rel for rel, (kind, _) in trace_entries.items() if kind == "symlink"
    ]
    jsonl_files = sorted(
        path
        for path in paths["generation_trace"].rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    trace_lines = 0
    trace_json_errors = 0
    for path in jsonl_files:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                trace_lines += 1
                try:
                    json.loads(line)
                except json.JSONDecodeError as error:
                    trace_json_errors += 1
                    print(f"TRACE_JSON_ERROR {path}:{line_number}: {error}")
    print(
        "TRACE"
        f" files={len(jsonl_files)}"
        f" lines={trace_lines}"
        f" json_errors={trace_json_errors}"
        f" symlinks={len(trace_symlinks)}"
        f" reviewer_hash={independent_tree_hash(trace_entries)}"
        f" launcher_recorded_hash={hashes['generation_codex_trace_sha256']}"
    )
    if not jsonl_files:
        failures.append("structured trace has no files")
    if trace_json_errors:
        failures.append("structured trace contains malformed JSONL")
    if trace_symlinks:
        failures.append("structured trace contains symlinks")

    for json_path in [
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        paths["generation_root"] / "runtime-metrics.json",
        paths["generation_root"] / "usage.json",
    ]:
        try:
            json.loads(json_path.read_text())
            print(f"JSON_PARSE OK path={json_path}")
        except Exception as error:
            failures.append(f"unreadable/malformed JSON: {json_path}: {error}")

    print(f"RESULT failures={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
