#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode):
        raise AssertionError(f"required regular file has type {stat.filemode(metadata.st_mode)}: {path}")
    with path.open("rb"):
        pass
    print(f"REQUIRED_REGULAR_READABLE OK {path}")


def compare_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    outcome = "OK" if actual == expected else "MISMATCH"
    print(f"HASH {outcome} {label} expected={expected} actual={actual} path={path}")
    if outcome != "OK":
        raise AssertionError(f"hash mismatch for {label}")


def tree_manifest(root: Path) -> tuple[str, list[tuple[str, str, str | None]]]:
    """Hash an independently specified manifest of names, types, and file bytes."""
    records: list[tuple[str, str, str | None]] = []
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        if stat.S_ISREG(metadata.st_mode):
            kind = "file"
            content_hash = sha256_file(path)
        elif stat.S_ISDIR(metadata.st_mode):
            kind = "directory"
            content_hash = None
        elif stat.S_ISLNK(metadata.st_mode):
            kind = "symlink"
            content_hash = hashlib.sha256(os.readlink(path).encode()).hexdigest()
        else:
            kind = stat.filemode(metadata.st_mode)
            content_hash = None
        record = (relative, kind, content_hash)
        records.append(record)
        digest.update(json.dumps(record, separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest(), records


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = audit["container_paths"]
    expected_hashes = audit["hashes"]

    required = [
        Path("/audit-input.json"),
        Path(paths["audit_campaign_lock"]),
        Path(paths["run_manifest"]),
        Path(paths["task_manifest"]),
        Path(paths["stage1_result"]),
        Path(paths["generation_manifest"]),
        Path(paths["generation_metrics"]),
        Path(paths["generation_last"]),
        Path(paths["generation_output"]),
        Path(paths["generation_root"]) / "prompt.txt",
    ]
    usage = Path(paths["generation_root"]) / "usage.json"
    if usage.exists() or usage.is_symlink():
        required.append(usage)

    trace_root = Path(paths["generation_trace"])
    trace_files = sorted(trace_root.rglob("*"))
    regular_traces = [item for item in trace_files if item.is_file() and not item.is_symlink()]
    if not regular_traces:
        raise AssertionError("structured trace has no regular files")
    required.extend(regular_traces)
    for path in required:
        require_regular(path)

    if audit["record_layout"] != "legacy-selected-stage1":
        raise AssertionError(f"unexpected record layout: {audit['record_layout']}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError(f"unexpected semantics mode: {audit['semantics_mode']}")
    print("DECLARATION OK record_layout=legacy-selected-stage1 semantics_mode=SUPPLIED_SEMANTICS")

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    if lock != audit["audit_campaign"]:
        raise AssertionError("campaign lock JSON differs from audit_campaign block")
    print("CAMPAIGN_JSON_EQUAL OK")

    direct_hashes = {
        "audit_campaign_lock_sha256": Path(paths["audit_campaign_lock"]),
        "run_manifest_sha256": Path(paths["run_manifest"]),
        "task_manifest_sha256": Path(paths["task_manifest"]),
        "stage1_result_sha256": Path(paths["stage1_result"]),
        "stage1_invocation_sha256": Path(paths["generation_manifest"]),
        "generation_metrics_sha256": Path(paths["generation_metrics"]),
        "generation_codex_last_sha256": Path(paths["generation_last"]),
        "generation_codex_output_sha256": Path(paths["generation_output"]),
        "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
        "generation_usage_sha256": usage,
        "canonical_sha256": Path(paths["canonical"]),
        "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
        "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
        "trusted_translator_sha256": Path(paths["translator"]),
        "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
    }
    for label, path in direct_hashes.items():
        compare_hash(label, path, expected_hashes[label])

    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    stage_result = json.loads(Path(paths["stage1_result"]).read_text())
    for relative, expected in invocation["outputs"]["evidence"].items():
        evidence_path = Path(paths["generation_root"]) / relative
        require_regular(evidence_path)
        compare_hash(f"invocation.outputs.evidence[{relative}]", evidence_path, expected)
    for relative, expected in stage_result["outputs"]["evidence"].items():
        evidence_path = Path(paths["generation_root"]) / relative
        require_regular(evidence_path)
        compare_hash(f"stage-result.outputs.evidence[{relative}]", evidence_path, expected)

    trace_count = 0
    event_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_calls: collections.Counter[str] = collections.Counter()
    for trace in regular_traces:
        compare_hash(
            f"trace[{trace.relative_to(Path(paths['generation_root'])).as_posix()}]",
            trace,
            invocation["outputs"]["evidence"][trace.relative_to(Path(paths["generation_root"])).as_posix()],
        )
        with trace.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                trace_count += 1
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "function_call":
                        tool_calls[str(payload.get("name"))] += 1
    print(f"TRACE_JSON_VALID OK records={trace_count}")
    print(f"TRACE_EVENT_TYPES {dict(sorted(event_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(f"TRACE_TOOL_CALLS {dict(sorted(tool_calls.items()))}")

    candidate = Path(paths["candidate"])
    reference = Path("/reference")
    byte_pairs = [
        (candidate / "prompt.py", reference / "prompt.py"),
        (candidate / "py2mpy.py", reference / "py2mpy.py"),
    ]
    for left, right in byte_pairs:
        if left.read_bytes() != right.read_bytes():
            raise AssertionError(f"byte comparison failed: {left} != {right}")
        print(f"BYTE_IDENTICAL OK {left} {right}")

    trusted_semantics = reference / "reference-semantics"
    candidate_semantics = candidate / "reference-semantics"
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        raise AssertionError("trusted supplied semantics is absent, not a directory, or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        raise AssertionError("candidate supplied semantics is absent, not a directory, or symlinked")
    trusted_digest, trusted_records = tree_manifest(trusted_semantics)
    candidate_digest, candidate_records = tree_manifest(candidate_semantics)
    print(f"INDEPENDENT_TREE_MANIFEST trusted={trusted_digest} candidate={candidate_digest}")
    if trusted_records != candidate_records:
        trusted_set = set(trusted_records)
        candidate_set = set(candidate_records)
        print(f"ONLY_TRUSTED {sorted(trusted_set - candidate_set)}")
        print(f"ONLY_CANDIDATE {sorted(candidate_set - trusted_set)}")
        raise AssertionError("candidate reference-semantics differs recursively from trusted tree")
    if any(record[1] == "symlink" for record in candidate_records):
        raise AssertionError("candidate supplied semantics contains a symlink")
    print(f"SUPPLIED_SEMANTICS_RECURSIVE_IDENTITY OK entries={len(candidate_records)} symlinks=0")

    all_candidate_symlinks = [
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_symlink()
    ]
    print(f"CANDIDATE_SYMLINKS count={len(all_candidate_symlinks)} entries={all_candidate_symlinks}")
    candidate_digest, candidate_all_records = tree_manifest(candidate)
    print(
        "INDEPENDENT_CANDIDATE_TREE_MANIFEST "
        f"digest={candidate_digest} entries={len(candidate_all_records)} "
        f"launcher_recorded_digest={expected_hashes['candidate_tree_sha256']} "
        "algorithm=reviewer-json-lines-v1"
    )
    for artifact in [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]:
        artifact_path = candidate / artifact
        require_regular(artifact_path)
        print(f"CANDIDATE_ARTIFACT_HASH {sha256_file(artifact_path)} {artifact_path}")

    if not all(audit["integrity"].values()):
        raise AssertionError(f"launcher integrity field contains false: {audit['integrity']}")
    print(f"LAUNCHER_INTEGRITY_FIELDS all_true={audit['integrity']}")
    print("STAGE1_INTEGRITY_RESULT PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"STAGE1_INTEGRITY_RESULT FAIL error={error}", file=sys.stderr)
        raise
