#!/usr/bin/env python3
"""Independent read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pipeline_sha256_tree(root: Path) -> str:
    """Reproduce the declared pipeline-v2 tree digest, including directories."""
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def report_hash(label: str, path: Path, expected: str | None = None) -> None:
    actual = sha256(path)
    state = "RECORDED-MATCH" if expected == actual else (
        "INDEPENDENT" if expected is None else "MISMATCH"
    )
    print(f"{state} {label} {actual} {path}")


def main() -> int:
    audit_input = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit_input["hashes"]

    print("record_layout", audit_input["record_layout"])
    print("semantics_mode", audit_input["semantics_mode"])
    print("campaign_block_equals_lock", audit_input["audit_campaign"] == lock)
    report_hash("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"])

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
    ]
    print("required_records_present", all(p.is_file() for p in required))
    print("required_records_non_symlink", all(not p.is_symlink() for p in required))

    direct_records = [
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        (
            "generation_invocation",
            GENERATION / "invocation.json",
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            GENERATION / "metrics.json",
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_usage",
            GENERATION / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_last",
            GENERATION / "codex-last.txt",
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            GENERATION / "codex-output.log",
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            GENERATION / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        ("canonical", REFERENCE / "canonical.py", hashes["canonical_sha256"]),
        ("trusted_prompt", REFERENCE / "prompt.py", hashes["trusted_prompt_sha256"]),
        (
            "trusted_translator",
            REFERENCE / "py2mpy.py",
            hashes["trusted_translator_sha256"],
        ),
    ]
    for label, path, expected in direct_records:
        report_hash(label, path, expected)

    print(
        "candidate_prompt_byte_equal",
        (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes(),
    )
    print(
        "candidate_translator_byte_equal",
        (CANDIDATE / "py2mpy.py").read_bytes()
        == (REFERENCE / "py2mpy.py").read_bytes(),
    )
    print(
        "trusted_reference_semantics_absent",
        not (REFERENCE / "reference-semantics").exists(),
    )

    candidate_entries = sorted(CANDIDATE.rglob("*"))
    print("candidate_has_symlinks", any(p.is_symlink() for p in candidate_entries))
    for path in candidate_entries:
        if path.is_file():
            report_hash(f"candidate/{path.relative_to(CANDIDATE)}", path)

    result = json.loads(Path("/generation-result.json").read_text())
    candidate_pipeline_hash = pipeline_sha256_tree(CANDIDATE)
    print(
        "candidate_pipeline_tree_hash_matches_stage1_workspace",
        candidate_pipeline_hash == result["outputs"]["workspace_sha256"],
        candidate_pipeline_hash,
    )
    evidence_ok = True
    for rel, expected in sorted(result["outputs"]["evidence"].items()):
        path = GENERATION / rel
        actual = sha256(path)
        matches = actual == expected
        evidence_ok &= matches
        print("stage1_evidence_file", rel, "MATCH" if matches else "MISMATCH", actual)
    print("all_stage1_evidence_hashes_match", evidence_ok)

    trace_files = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
    usage = json.loads((GENERATION / "usage.json").read_text())
    trace_pipeline_hash = pipeline_sha256_tree(GENERATION / "codex-trace")
    print(
        "trace_pipeline_tree_hash_matches_usage",
        trace_pipeline_hash == usage["source_trace_sha256"],
        trace_pipeline_hash,
    )
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    parsed_lines = 0
    session_ids: set[str] = set()
    last_event: dict | None = None
    for trace_file in trace_files:
        for line in trace_file.read_text().splitlines():
            event = json.loads(line)
            parsed_lines += 1
            event_types[event.get("type", "<missing>")] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type", "<missing>"))] += 1
                session_id = payload.get("session_id")
                if isinstance(session_id, str):
                    session_ids.add(session_id)
            last_event = event
    print("trace_files", len(trace_files))
    print("trace_json_lines_parsed", parsed_lines)
    print("trace_event_types", dict(sorted(event_types.items())))
    print("trace_payload_types", dict(sorted(payload_types.items())))
    print("trace_session_ids", sorted(session_ids))
    print("trace_last_event_type", None if last_event is None else last_event.get("type"))

    ok = (
        audit_input["record_layout"] == "legacy-selected-stage1"
        and audit_input["semantics_mode"] == "GENERATED_SEMANTICS"
        and audit_input["audit_campaign"] == lock
        and all(p.is_file() and not p.is_symlink() for p in required)
        and evidence_ok
        and not any(p.is_symlink() for p in candidate_entries)
        and not (REFERENCE / "reference-semantics").exists()
    )
    print("PROVENANCE_CHECK", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
