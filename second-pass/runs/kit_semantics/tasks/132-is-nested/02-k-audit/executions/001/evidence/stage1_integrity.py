#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        return f"MISSING/UNREADABLE ({err})"
    if stat.S_ISREG(mode):
        return "regular file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return f"symlink -> {os.readlink(path)}"
    return f"special mode {oct(mode)}"


def compare_trees(left: Path, right: Path) -> list[str]:
    mismatches: list[str] = []

    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256(path))
            else:
                result[relative] = (f"special:{oct(mode)}", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    for relative in sorted(left_entries.keys() | right_entries.keys()):
        if relative not in left_entries:
            mismatches.append(f"missing candidate entry: {relative}")
        elif relative not in right_entries:
            mismatches.append(f"additional candidate entry: {relative}")
        elif left_entries[relative] != right_entries[relative]:
            mismatches.append(
                f"changed/mistyped entry: {relative}: "
                f"candidate={left_entries[relative]} trusted={right_entries[relative]}"
            )
    return mismatches


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    hashes = audit["hashes"]
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}

    print("audit-input parse: OK")
    print(f"record_layout: {audit['record_layout']}")
    print(f"semantics_mode: {audit['semantics_mode']}")
    print(f"problem_id: {audit['problem_id']}")
    print(f"condition: {audit['condition']}")

    lock_path = paths["audit_campaign_lock"]
    lock = json.loads(lock_path.read_text())
    print(f"campaign block equals lock JSON: {audit['audit_campaign'] == lock}")
    actual_lock_hash = sha256(lock_path)
    print(
        "campaign lock hash: "
        f"actual={actual_lock_hash} expected={hashes['audit_campaign_lock_sha256']} "
        f"match={actual_lock_hash == hashes['audit_campaign_lock_sha256']}"
    )

    required_pipeline_v3 = [
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
        Path("/generation-evidence/codex-trace"),
        paths["candidate"],
        paths["canonical"],
        paths["translator"],
        paths["trusted_prompt"],
        Path("/reference/reference-semantics"),
    ]
    print("required mounted records and inputs:")
    for path in required_pipeline_v3:
        print(f"  {path}: {describe(path)} readable={os.access(path, os.R_OK)}")

    direct_hashes = [
        (Path("/run.json"), "run_manifest_sha256"),
        (Path("/task.json"), "task_manifest_sha256"),
        (Path("/generation-result.json"), "stage1_result_sha256"),
        (Path("/generation-evidence/invocation.json"), "stage1_invocation_sha256"),
        (Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
        (
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
        (
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
        (paths["canonical"], "canonical_sha256"),
        (paths["translator"], "trusted_translator_sha256"),
        (paths["trusted_prompt"], "trusted_prompt_sha256"),
        (Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        (Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
    ]
    print("direct SHA-256 checks:")
    for path, key in direct_hashes:
        actual = sha256(path)
        expected = hashes[key]
        print(f"  {path}: {actual} expected={expected} match={actual == expected}")

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    expected_trace_files = invocation["outputs"]["evidence"]
    trace_root = Path("/generation-evidence")
    print("invocation-declared generation evidence:")
    for relative, expected in sorted(expected_trace_files.items()):
        path = trace_root / relative
        actual = sha256(path)
        print(f"  {relative}: {actual} expected={expected} match={actual == expected}")

    print("candidate prompt byte-identical to trusted:", end=" ")
    print(Path("/candidate/prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes())
    print("candidate translator byte-identical to trusted:", end=" ")
    print(Path("/candidate/py2mpy.py").read_bytes() == paths["translator"].read_bytes())

    semantic_mismatches = compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"supplied-semantics recursive mismatch count: {len(semantic_mismatches)}")
    for mismatch in semantic_mismatches:
        print(f"  {mismatch}")

    trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_symlinks = [path for path in trace_paths if path.is_symlink()]
    trace_files = [path for path in trace_paths if path.is_file()]
    print(f"structured trace files: {len(trace_files)}; symlinks: {len(trace_symlinks)}")
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    parsed_lines = 0
    for path in trace_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                parsed_lines += 1
                event_types[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
    print(f"structured trace JSON lines parsed: {parsed_lines}")
    print(f"structured trace top-level event types: {dict(sorted(event_types.items()))}")
    print(f"structured trace payload types: {dict(sorted(payload_types.items()))}")

    candidate_symlinks = [
        path for path in Path("/candidate").rglob("*") if path.is_symlink()
    ]
    reference_symlinks = [
        path for path in Path("/reference").rglob("*") if path.is_symlink()
    ]
    generation_symlinks = [
        path for path in Path("/generation-evidence").rglob("*") if path.is_symlink()
    ]
    print(
        "symlink counts: "
        f"candidate={len(candidate_symlinks)} "
        f"reference={len(reference_symlinks)} "
        f"generation-evidence={len(generation_symlinks)}"
    )
    for path in candidate_symlinks + reference_symlinks + generation_symlinks:
        print(f"  symlink: {path} -> {os.readlink(path)}")

    required_candidate = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    print("required candidate proof artifacts:")
    for relative in required_candidate:
        path = Path("/candidate") / relative
        print(f"  {relative}: {describe(path)} readable={os.access(path, os.R_OK)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
