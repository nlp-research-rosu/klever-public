#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

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


def tree_manifest(root: Path) -> tuple[list[str], str]:
    records: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            records.append(f"L\t{rel}\t{os.readlink(path)}")
        elif stat.S_ISDIR(mode):
            records.append(f"D\t{rel}")
        elif stat.S_ISREG(mode):
            records.append(f"F\t{rel}\t{path.stat().st_size}\t{sha256_file(path)}")
        else:
            records.append(f"O\t{rel}\t{stat.S_IFMT(mode):o}")
    encoded = ("\n".join(records) + "\n").encode()
    return records, hashlib.sha256(encoded).hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Independently reproduce the pipeline-v3 length-delimited tree digest."""
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            entries.append((rel, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((rel, "file", path))
        else:
            raise ValueError(f"unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"MISSING {path}")
    elif path.is_symlink():
        failures.append(f"SYMLINK {path} -> {os.readlink(path)}")
    elif not path.is_file():
        failures.append(f"NOT_REGULAR {path}")


def main() -> int:
    data = json.loads(AUDIT_INPUT.read_text())
    recorded = data["hashes"]
    failures: list[str] = []

    required = [
        Path("/audit-input.json"),
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
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
        Path("/candidate/PROOF.md"),
    ]
    for path in required:
        require_regular(path, failures)

    required_dirs = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_dirs:
        if not path.exists():
            failures.append(f"MISSING {path}")
        elif path.is_symlink():
            failures.append(f"SYMLINK {path} -> {os.readlink(path)}")
        elif not path.is_dir():
            failures.append(f"NOT_DIRECTORY {path}")

    print(f"record_layout={data.get('record_layout')}")
    print(f"semantics_mode={data.get('semantics_mode')}")
    print(f"mount_reference_semantics={data.get('mount_reference_semantics')}")

    campaign_lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    campaign_equal = campaign_lock == data.get("audit_campaign")
    print(f"campaign_block_equal={campaign_equal}")
    if not campaign_equal:
        failures.append("campaign lock JSON does not equal audit_campaign block")

    direct_hashes = {
        "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "task_manifest_sha256": Path("/task.json"),
        "manifest_sha256": Path("/task.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
    }
    for key, path in direct_hashes.items():
        if not path.is_file():
            continue
        actual = sha256_file(path)
        expected = recorded.get(key)
        verdict = actual == expected
        print(f"HASH {key} actual={actual} expected={expected} match={verdict}")
        if not verdict:
            failures.append(f"hash mismatch: {key}")

    identity_pairs = [
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
    ]
    for left, right in identity_pairs:
        same = left.is_file() and right.is_file() and left.read_bytes() == right.read_bytes()
        print(f"BYTE_IDENTITY {left} {right} same={same}")
        if not same:
            failures.append(f"byte mismatch: {left} vs {right}")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    candidate_records, candidate_review_hash = tree_manifest(candidate_sem)
    trusted_records, trusted_review_hash = tree_manifest(trusted_sem)
    print(
        "SEMANTICS_TREE "
        f"candidate_entries={len(candidate_records)} trusted_entries={len(trusted_records)} "
        f"candidate_review_sha256={candidate_review_hash} "
        f"trusted_review_sha256={trusted_review_hash} "
        f"exact={candidate_records == trusted_records}"
    )
    if candidate_records != trusted_records:
        failures.append("candidate reference-semantics differs from trusted tree")
        for record in sorted(set(candidate_records) ^ set(trusted_records)):
            print(f"SEMANTICS_DIFF {record}")

    candidate_all_records, candidate_all_review_hash = tree_manifest(Path("/candidate"))
    candidate_files = sum(record.startswith("F\t") for record in candidate_all_records)
    candidate_dirs = sum(record.startswith("D\t") for record in candidate_all_records)
    candidate_bytes = sum(
        int(record.split("\t", 4)[2])
        for record in candidate_all_records
        if record.startswith("F\t")
    )
    print(
        "CANDIDATE_TREE "
        f"entries={len(candidate_all_records)} files={candidate_files} "
        f"dirs={candidate_dirs} bytes={candidate_bytes} "
        f"reviewer_manifest_sha256={candidate_all_review_hash} "
        f"launcher_recorded_sha256={recorded.get('candidate_tree_sha256')}"
    )
    generation_result = json.loads(Path("/generation-result.json").read_text())
    candidate_pipeline_hash = pipeline_tree_sha256(Path("/candidate"))
    expected_workspace_hash = generation_result["outputs"]["workspace_sha256"]
    print(
        "PIPELINE_TREE /candidate "
        f"actual={candidate_pipeline_hash} expected={expected_workspace_hash} "
        f"match={candidate_pipeline_hash == expected_workspace_hash}"
    )
    if candidate_pipeline_hash != expected_workspace_hash:
        failures.append("candidate tree differs from generation-result workspace")

    task = json.loads(Path("/task.json").read_text())
    expected_semantics_manifest = task["inputs"]["reference_semantics_sha256"]
    for semantics_root in [candidate_sem, trusted_sem]:
        actual = pipeline_tree_sha256(semantics_root)
        same = actual == expected_semantics_manifest
        print(
            f"PIPELINE_TREE {semantics_root} actual={actual} "
            f"expected={expected_semantics_manifest} match={same}"
        )
        if not same:
            failures.append(f"semantics manifest tree mismatch: {semantics_root}")

    trace_records, trace_review_hash = tree_manifest(Path("/generation-evidence/codex-trace"))
    print(
        f"TRACE_TREE entries={len(trace_records)} reviewer_manifest_sha256={trace_review_hash}"
    )
    for record in trace_records:
        print(f"TRACE_ENTRY {record}")
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    trace_pipeline_hash = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
    expected_trace_hash = usage["source_trace_sha256"]
    print(
        "PIPELINE_TREE /generation-evidence/codex-trace "
        f"actual={trace_pipeline_hash} expected={expected_trace_hash} "
        f"match={trace_pipeline_hash == expected_trace_hash}"
    )
    if trace_pipeline_hash != expected_trace_hash:
        failures.append("generation trace tree differs from usage source hash")

    for root in [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ]:
        special = []
        for path in root.rglob("*"):
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                special.append(path)
        print(f"SPECIAL_ENTRIES {root} count={len(special)}")
        for path in special:
            print(f"SPECIAL {path}")
        if special:
            failures.append(f"symlink/special entries below {root}")

    result = generation_result
    evidence_hashes = result["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for rel, expected in sorted(evidence_hashes.items()):
        path = evidence_root / rel
        require_regular(path, failures)
        if path.is_file():
            actual = sha256_file(path)
            same = actual == expected
            print(f"RESULT_EVIDENCE {rel} actual={actual} expected={expected} match={same}")
            if not same:
                failures.append(f"generation-result evidence hash mismatch: {rel}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
