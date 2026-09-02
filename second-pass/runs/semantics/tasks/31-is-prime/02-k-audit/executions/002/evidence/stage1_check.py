#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    rows: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            rows.append(("symlink", rel, os.readlink(path)))
        elif path.is_dir():
            rows.append(("dir", rel, ""))
        elif path.is_file():
            rows.append(("file", rel, sha256_file(path)))
        else:
            rows.append(("other", rel, ""))
    encoded = "".join("\t".join(row) + "\n" for row in rows).encode()
    return rows, hashlib.sha256(encoded).hexdigest()


def compare_trees(left: Path, right: Path) -> list[str]:
    left_rows, _ = tree_manifest(left)
    right_rows, _ = tree_manifest(right)
    left_map = {(kind, rel): value for kind, rel, value in left_rows}
    right_map = {(kind, rel): value for kind, rel, value in right_rows}
    differences: list[str] = []
    for key in sorted(left_map.keys() | right_map.keys()):
        if key not in left_map:
            differences.append(f"only trusted: {key}")
        elif key not in right_map:
            differences.append(f"only candidate: {key}")
        elif left_map[key] != right_map[key]:
            differences.append(
                f"changed {key}: candidate={left_map[key]} trusted={right_map[key]}"
            )
    return differences


def print_hash_check(
    label: str, path: Path, expected: str | None, failures: list[str]
) -> None:
    if not path.is_file() or path.is_symlink():
        print(f"HASH {label}: invalid regular-file mount {path}")
        failures.append(label)
        return
    actual = sha256_file(path)
    status = "MATCH" if expected == actual else "MISMATCH"
    print(f"HASH {label}: {status} actual={actual} expected={expected} path={path}")
    if status != "MATCH":
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    record = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())

    print(f"record_layout={record.get('record_layout')}")
    print(f"semantics_mode={record.get('semantics_mode')}")
    print(f"input_provenance={record.get('manifest', {}).get('input_provenance')}")
    lock_equal = lock == record.get("audit_campaign")
    print(f"campaign_block_semantic_match={lock_equal}")
    if not lock_equal:
        failures.append("campaign block")

    hashes = record["hashes"]
    direct_checks = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        (
            "candidate_prompt",
            Path("/candidate/prompt.py"),
            hashes["candidate_prompt_sha256"],
        ),
        (
            "trusted_prompt",
            Path("/reference/prompt.py"),
            hashes["trusted_prompt_sha256"],
        ),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            hashes["candidate_translator_sha256"],
        ),
        (
            "trusted_translator",
            Path("/reference/py2mpy.py"),
            hashes["trusted_translator_sha256"],
        ),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        (
            "generation_result",
            Path("/generation-result.json"),
            hashes["stage1_result_sha256"],
        ),
        (
            "generation_invocation",
            Path("/generation-evidence/invocation.json"),
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_last",
            Path("/generation-evidence/codex-last.txt"),
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            Path("/generation-evidence/codex-output.log"),
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
    ]
    for label, path, expected in direct_checks:
        print_hash_check(label, path, expected, failures)

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    declared_evidence = result["outputs"]["evidence"]
    invocation_evidence = invocation["outputs"]["evidence"]
    for rel, expected in sorted(declared_evidence.items()):
        path = Path("/generation-evidence") / rel
        print_hash_check(f"result.outputs.evidence/{rel}", path, expected, failures)
        if invocation_evidence.get(rel) != expected:
            print(
                f"INVOCATION EVIDENCE MISMATCH {rel}: "
                f"{invocation_evidence.get(rel)} != {expected}"
            )
            failures.append(f"invocation evidence {rel}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required:
        ok = path.exists() and os.access(path, os.R_OK) and not path.is_symlink()
        print(f"REQUIRED {path}: {'OK' if ok else 'BAD'}")
        if not ok:
            failures.append(f"required {path}")
    usage = Path("/generation-evidence/usage.json")
    print(f"OPTIONAL_PRESENT {usage}: {usage.is_file() and not usage.is_symlink()}")
    runtime = Path("/generation-evidence/runtime-metrics.json")
    print(
        "LEGACY_RUNTIME_METRICS_NOT_REQUIRED "
        f"{runtime}: present={runtime.exists()}"
    )

    for left, right, label in [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
    ]:
        same = left.read_bytes() == right.read_bytes()
        print(f"BYTE_COMPARE {label}: {'IDENTICAL' if same else 'DIFFERENT'}")
        if not same:
            failures.append(f"byte compare {label}")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    sem_differences = compare_trees(candidate_sem, trusted_sem)
    candidate_rows, candidate_aggregate = tree_manifest(candidate_sem)
    trusted_rows, trusted_aggregate = tree_manifest(trusted_sem)
    print(
        f"SEMANTICS entries candidate={len(candidate_rows)} trusted={len(trusted_rows)} "
        f"reviewer_aggregate_candidate={candidate_aggregate} "
        f"reviewer_aggregate_trusted={trusted_aggregate}"
    )
    print(f"SEMANTICS_RECURSIVE_COMPARE differences={len(sem_differences)}")
    for difference in sem_differences:
        print(f"  {difference}")
    if sem_differences:
        failures.append("supplied semantics recursive comparison")

    protected_roots = [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]
    for root in protected_roots:
        symlinks = [p for p in root.rglob("*") if p.is_symlink()]
        print(f"SYMLINK_SCAN {root}: count={len(symlinks)}")
        for path in symlinks:
            print(f"  {path} -> {os.readlink(path)}")
        if symlinks:
            failures.append(f"symlink scan {root}")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    print(f"TRACE files={len(trace_files)}")
    type_counts: collections.Counter[str] = collections.Counter()
    payload_type_counts: collections.Counter[str] = collections.Counter()
    for trace in trace_files:
        lines = 0
        parse_errors = 0
        final_messages: list[str] = []
        for lines, raw in enumerate(trace.read_text().splitlines(), start=1):
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as err:
                parse_errors += 1
                print(f"TRACE_PARSE_ERROR {trace}:{lines}: {err}")
                continue
            type_counts[str(obj.get("type"))] += 1
            payload = obj.get("payload")
            if isinstance(payload, dict):
                payload_type_counts[str(payload.get("type"))] += 1
                if payload.get("type") in {"agent_message", "assistant_message"}:
                    message = payload.get("message") or payload.get("text")
                    if isinstance(message, str):
                        final_messages.append(message)
        print(
            f"TRACE_FILE {trace} sha256={sha256_file(trace)} "
            f"lines={lines} parse_errors={parse_errors}"
        )
        if parse_errors:
            failures.append(f"trace parse {trace}")
        for message in final_messages[-2:]:
            print(f"TRACE_AGENT_MESSAGE {message[:500]!r}")
    print(f"TRACE_TOP_LEVEL_TYPES {dict(sorted(type_counts.items()))}")
    print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_type_counts.items()))}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
