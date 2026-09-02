#!/usr/bin/env python3
"""Independent launcher/provenance integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise AssertionError(f"not a regular file: {path}")
    if path.is_symlink():
        raise AssertionError(f"symlinked required file: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def tree_manifest(root: Path):
    records = []
    for path in sorted(root.rglob("*")):
        info = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(info.st_mode):
            raise AssertionError(f"symlink in tree: {path}")
        if stat.S_ISREG(info.st_mode):
            records.append(
                {
                    "path": relative,
                    "mode": stat.S_IMODE(info.st_mode),
                    "size": info.st_size,
                    "sha256": sha256(path),
                }
            )
        elif not stat.S_ISDIR(info.st_mode):
            raise AssertionError(f"special entry in tree: {path}")
    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return records, hashlib.sha256(encoded).hexdigest()


def check_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256(path)
    print(f"{label}: expected={expected} actual={actual} match={actual == expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch for {path}")


def main() -> int:
    audit_input_path = Path("/audit-input.json")
    campaign_lock_path = Path("/audit-campaign-lock.json")
    require_regular(audit_input_path)
    require_regular(campaign_lock_path)
    audit_input = json.loads(audit_input_path.read_text())
    campaign_lock = json.loads(campaign_lock_path.read_text())

    print(f"record_layout={audit_input['record_layout']}")
    print(f"semantics_mode={audit_input['semantics_mode']}")
    print(f"problem_id={audit_input['problem_id']}")
    print(f"condition={audit_input['condition']}")
    print(f"campaign_block_equal={audit_input['audit_campaign'] == campaign_lock}")
    if audit_input["audit_campaign"] != campaign_lock:
        raise AssertionError("campaign lock differs from audit campaign block")

    hashes = audit_input["hashes"]
    hash_checks = {
        "audit_campaign_lock_sha256": campaign_lock_path,
        "candidate_prompt_sha256": Path("/candidate/prompt.py"),
        "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
        "canonical_sha256": Path("/reference/canonical.py"),
        "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
        "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
        "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
        "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
        "generation_usage_sha256": Path("/generation-evidence/usage.json"),
        "run_manifest_sha256": Path("/run.json"),
        "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
        "stage1_result_sha256": Path("/generation-result.json"),
        "task_manifest_sha256": Path("/task.json"),
        "trusted_prompt_sha256": Path("/reference/prompt.py"),
        "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    }
    for label, path in hash_checks.items():
        require_regular(path)
        check_hash(label, path, hashes[label])

    check_hash("manifest_sha256", Path("/task.json"), hashes["manifest_sha256"])
    if Path("/reference/reference-semantics").exists() or Path(
        "/reference/reference-semantics"
    ).is_symlink():
        raise AssertionError("reference-semantics unexpectedly present")
    print("reference_semantics_absent=True")
    if hashes["trusted_reference_semantics_sha256"] is not None:
        raise AssertionError("trusted reference-semantics hash is non-null")
    if hashes["candidate_reference_semantics_sha256"] is not None:
        raise AssertionError("candidate reference-semantics hash is non-null")

    if Path("/candidate/prompt.py").read_bytes() != Path(
        "/reference/prompt.py"
    ).read_bytes():
        raise AssertionError("candidate prompt differs from trusted prompt")
    if Path("/candidate/py2mpy.py").read_bytes() != Path(
        "/reference/py2mpy.py"
    ).read_bytes():
        raise AssertionError("candidate translator differs from trusted translator")
    print("candidate_prompt_byte_equal=True")
    print("candidate_translator_byte_equal=True")

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
    for name in required_candidate:
        require_regular(Path("/candidate") / name)
    print(f"required_candidate_files={required_candidate!r}")

    required_generation = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/usage.json"),
    ]
    for path in required_generation:
        require_regular(path)
    print("legacy_selected_stage1_required_records_present=True")

    for label, raw_path in audit_input["container_paths"].items():
        path = Path(raw_path)
        if not path.exists():
            raise AssertionError(f"missing declared container path {label}: {path}")
        if path.is_symlink():
            raise AssertionError(f"symlinked declared container path {label}: {path}")
    print("all_declared_container_paths_present=True")

    trace_root = Path(audit_input["container_paths"]["generation_trace"])
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    stage1_result = json.loads(Path("/generation-result.json").read_text())
    output_hashes = stage1_result["outputs"]["evidence"]
    for path in trace_files:
        relative = path.relative_to(Path("/generation-evidence")).as_posix()
        require_regular(path)
        check_hash(f"trace_output[{relative}]", path, output_hashes[relative])

    trace_counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    parsed_trace_lines = 0
    final_messages = []
    for path in trace_files:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            record = json.loads(line)
            parsed_trace_lines += 1
            trace_counts[record.get("type")] += 1
            payload = record.get("payload") or {}
            payload_counts[payload.get("type")] += 1
            if payload.get("type") == "task_complete":
                final_messages.append(payload.get("last_agent_message"))
    print(f"trace_files={[str(path) for path in trace_files]!r}")
    print(f"parsed_trace_lines={parsed_trace_lines}")
    print(f"trace_record_types={dict(trace_counts)!r}")
    print(f"trace_payload_types={dict(payload_counts)!r}")
    print(f"trace_task_complete_messages={len(final_messages)}")

    codex_log = Path("/generation-evidence/codex-output.log").read_text(
        errors="replace"
    )
    print(f"codex_output_lines={len(codex_log.splitlines())}")
    print(f"codex_output_top_occurrences={codex_log.count('#Top')}")
    print(
        "codex_output_has_final_marker="
        f"{'RESULT: KPROVE_PASSED' in codex_log}"
    )

    for root in (
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
    ):
        records, manifest_hash = tree_manifest(root)
        print(
            f"audit_tree_manifest root={root} files={len(records)} "
            f"sha256={manifest_hash}"
        )
        for record in records:
            print(f"  {record}")

    print(f"launcher_candidate_tree_sha256={hashes['candidate_tree_sha256']}")
    print(
        "launcher_generation_trace_tree_sha256="
        f"{hashes['generation_codex_trace_sha256']}"
    )
    print("integrity_status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
