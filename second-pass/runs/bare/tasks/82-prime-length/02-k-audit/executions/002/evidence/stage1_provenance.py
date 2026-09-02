#!/usr/bin/env python3
"""Independent read-only checks of launcher and mounted provenance records."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def report_file(label: str, path: Path, expected: str | None = None) -> bool:
    exists = path.exists()
    readable = os.access(path, os.R_OK)
    regular = path.is_file()
    symlink = path.is_symlink()
    actual = sha256(path) if readable and regular and not symlink else None
    matches = expected is None or actual == expected
    print(
        f"{label}: path={path} exists={exists} readable={readable} "
        f"regular={regular} symlink={symlink} sha256={actual} "
        f"expected={expected} matches={matches}"
    )
    return exists and readable and regular and not symlink and matches


def inventory(root: Path) -> bool:
    ok = True
    print(f"INVENTORY {root}")
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        mode = path.lstat().st_mode
        kind = (
            "symlink"
            if stat.S_ISLNK(mode)
            else "file"
            if stat.S_ISREG(mode)
            else "dir"
            if stat.S_ISDIR(mode)
            else "other"
        )
        rel = path.relative_to(root)
        digest = sha256(path) if kind == "file" else "-"
        target = os.readlink(path) if kind == "symlink" else "-"
        print(f"  {kind} {rel} sha256={digest} target={target}")
        if kind in {"symlink", "other"}:
            ok = False
    return ok


def pipeline_tree_sha256(root: Path) -> str:
    """Recompute the pipeline-v2 length-delimited workspace/tree digest."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise RuntimeError(f"unsupported tree entry {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            payload = path.read_bytes()
            digest.update(len(payload).to_bytes(8, "big"))
            digest.update(payload)
    return digest.hexdigest()


def main() -> int:
    ok = True
    data = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    hashes = data["hashes"]
    paths = {name: Path(value) for name, value in data["container_paths"].items()}

    print(f"record_layout={data['record_layout']}")
    print(f"semantics_mode={data['semantics_mode']}")
    print(f"problem_id={data['problem_id']} condition={data['condition']}")

    required = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": paths["audit_campaign_lock"],
        "run_manifest": paths["run_manifest"],
        "task_manifest": paths["task_manifest"],
        "stage1_result": paths["stage1_result"],
        "generation_manifest": paths["generation_manifest"],
        "generation_metrics": paths["generation_metrics"],
        "generation_last": paths["generation_last"],
        "generation_output": paths["generation_output"],
        "generation_prompt": paths["generation_root"] / "prompt.txt",
        "generation_trace": paths["generation_trace"],
        "trusted_prompt": paths["trusted_prompt"],
        "translator": paths["translator"],
        "canonical": paths["canonical"],
        "candidate": paths["candidate"],
    }
    for label, path in required.items():
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        symlink = path.is_symlink()
        print(
            f"required {label}: path={path} exists={exists} "
            f"readable={readable} symlink={symlink}"
        )
        ok &= exists and readable and not symlink

    expected_files = [
        ("campaign_lock", paths["audit_campaign_lock"], hashes["audit_campaign_lock_sha256"]),
        ("run", paths["run_manifest"], hashes["run_manifest_sha256"]),
        ("task", paths["task_manifest"], hashes["task_manifest_sha256"]),
        ("generation_result", paths["stage1_result"], hashes["stage1_result_sha256"]),
        ("invocation", paths["generation_manifest"], hashes["stage1_invocation_sha256"]),
        ("metrics", paths["generation_metrics"], hashes["generation_metrics_sha256"]),
        ("usage", paths["generation_root"] / "usage.json", hashes["generation_usage_sha256"]),
        ("codex_last", paths["generation_last"], hashes["generation_codex_last_sha256"]),
        ("codex_output", paths["generation_output"], hashes["generation_codex_output_sha256"]),
        ("generation_prompt", paths["generation_root"] / "prompt.txt", hashes["generation_prompt_sha256"]),
        ("canonical", paths["canonical"], hashes["canonical_sha256"]),
        ("trusted_prompt", paths["trusted_prompt"], hashes["trusted_prompt_sha256"]),
        ("candidate_prompt", paths["candidate"] / "prompt.py", hashes["candidate_prompt_sha256"]),
        ("trusted_translator", paths["translator"], hashes["trusted_translator_sha256"]),
        ("candidate_translator", paths["candidate"] / "py2mpy.py", hashes["candidate_translator_sha256"]),
    ]
    for label, path, expected in expected_files:
        ok &= report_file(label, path, expected)

    lock = json.loads(paths["audit_campaign_lock"].read_text(encoding="utf-8"))
    lock_matches = lock == data["audit_campaign"]
    print(f"campaign_lock_structurally_matches_audit_input={lock_matches}")
    ok &= lock_matches

    prompt_match = (paths["candidate"] / "prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
    translator_match = (paths["candidate"] / "py2mpy.py").read_bytes() == paths["translator"].read_bytes()
    print(f"candidate_prompt_byte_matches_trusted={prompt_match}")
    print(f"candidate_translator_byte_matches_trusted={translator_match}")
    ok &= prompt_match and translator_match

    reference_semantics = Path("/reference/reference-semantics")
    print(
        "generated_semantics_boundary: "
        f"reference_semantics_exists={reference_semantics.exists()} "
        f"mount_reference_semantics={data['mount_reference_semantics']}"
    )
    ok &= not reference_semantics.exists() and not data["mount_reference_semantics"]

    ok &= inventory(paths["candidate"])
    ok &= inventory(paths["generation_trace"])

    generation_result = json.loads(paths["stage1_result"].read_text(encoding="utf-8"))
    invocation = json.loads(paths["generation_manifest"].read_text(encoding="utf-8"))
    usage = json.loads((paths["generation_root"] / "usage.json").read_text(encoding="utf-8"))
    candidate_pipeline_hash = pipeline_tree_sha256(paths["candidate"])
    expected_workspace_hashes = {
        generation_result["outputs"]["workspace_sha256"],
        invocation["outputs"]["workspace_sha256"],
        invocation["retained_workspace_sha256"],
    }
    candidate_pipeline_match = expected_workspace_hashes == {candidate_pipeline_hash}
    print(
        f"candidate_pipeline_tree_sha256={candidate_pipeline_hash} "
        f"recorded_workspace_hashes={sorted(expected_workspace_hashes)} "
        f"matches={candidate_pipeline_match}"
    )
    ok &= candidate_pipeline_match

    trace_pipeline_hash = pipeline_tree_sha256(paths["generation_trace"])
    trace_pipeline_match = trace_pipeline_hash == usage["source_trace_sha256"]
    print(
        f"trace_pipeline_tree_sha256={trace_pipeline_hash} "
        f"usage_source_trace_sha256={usage['source_trace_sha256']} "
        f"matches={trace_pipeline_match}"
    )
    ok &= trace_pipeline_match

    trace_files = sorted(paths["generation_trace"].rglob("*.jsonl"))
    trace_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    for trace in trace_files:
        with trace.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                trace_lines += 1
                trace_counts[record.get("type", "<none>")] += 1
                payload = record.get("payload") or {}
                payload_counts[payload.get("type", "<none>")] += 1
        print(f"trace_file={trace} valid_json_lines={line_number} sha256={sha256(trace)}")
        relative = trace.relative_to(paths["generation_root"]).as_posix()
        expected_trace_file_hash = generation_result["outputs"]["evidence"].get(relative)
        trace_file_match = sha256(trace) == expected_trace_file_hash
        print(
            f"trace_file_recorded_sha256={expected_trace_file_hash} "
            f"matches={trace_file_match}"
        )
        ok &= trace_file_match
    print(f"trace_total_lines={trace_lines} trace_types={dict(trace_counts)}")
    print(f"trace_payload_types={dict(payload_counts)}")
    ok &= bool(trace_files) and trace_lines > 0

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
        "prompt.py",
        "py2mpy.py",
    ]
    for rel in required_candidate:
        path = paths["candidate"] / rel
        candidate_ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
        print(f"required_candidate_artifact {rel}: ok={candidate_ok}")
        ok &= candidate_ok

    print(f"OVERALL_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
