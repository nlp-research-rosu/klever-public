#!/usr/bin/env python3
"""Read-only integrity verifier for the launcher-owned audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path
import sys


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing required path: {path}")
    elif path.is_symlink():
        errors.append(f"required path is symlinked: {path}")
    elif not path.is_file():
        errors.append(f"required path is not a regular file: {path}")


def main() -> int:
    errors: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    paths = {name: Path(value) for name, value in audit["container_paths"].items()}
    lock_path = paths["audit_campaign_lock"]
    lock = json.loads(lock_path.read_text())

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"problem_id={audit['problem_id']}")
    print(f"campaign_block_exact_match={audit['audit_campaign'] == lock}")
    if audit["audit_campaign"] != lock:
        errors.append("audit_campaign block does not equal campaign lock")

    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    actual_lock_hash = digest(lock_path)
    print(f"audit_campaign_lock expected={expected_lock_hash} actual={actual_lock_hash}")
    if expected_lock_hash != actual_lock_hash:
        errors.append("campaign lock hash mismatch")

    common_required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    if audit["record_layout"] == "pipeline-v3":
        common_required.extend(
            [
                Path("/generation-evidence/runtime-metrics.json"),
                Path("/generation-evidence/usage.json"),
            ]
        )
    elif audit["record_layout"] == "legacy-selected-stage1":
        usage = Path("/generation-evidence/usage.json")
        if usage.exists():
            common_required.append(usage)
    elif audit["record_layout"] == "legacy":
        common_required = [
            Path("/generation-evidence/run-input.json"),
            Path("/generation-evidence/metrics.json"),
            Path("/generation-evidence/codex-last.txt"),
            Path("/generation-evidence/codex-output.log"),
        ]
    else:
        errors.append(f"unknown record layout: {audit['record_layout']}")

    common_required.extend(
        [
            paths["candidate"] / "prompt.py",
            paths["candidate"] / "py2mpy.py",
            paths["trusted_prompt"],
            paths["translator"],
            paths["canonical"],
        ]
    )
    for path in common_required:
        check_regular(path, errors)

    trace_root = paths["generation_trace"]
    if not trace_root.exists() or trace_root.is_symlink() or not trace_root.is_dir():
        errors.append(f"invalid structured trace directory: {trace_root}")
        trace_files: list[Path] = []
    else:
        trace_files = sorted(trace_root.rglob("*.jsonl"))
        if not trace_files:
            errors.append("structured trace contains no JSONL record")
        for path in trace_files:
            check_regular(path, errors)

    candidate_root = paths["candidate"]
    reference_root = paths["trusted_prompt"].parent
    for root in [candidate_root, reference_root, paths["generation_root"]]:
        links = [path for path in root.rglob("*") if path.is_symlink()]
        print(f"symlinks_under_{root}={len(links)}")
        for path in links:
            errors.append(f"symlinked mounted artifact: {path}")

    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        errors.append("unexpected semantics mode for this audit")
    trusted_semantics = reference_root / "reference-semantics"
    print(f"trusted_reference_semantics_exists={trusted_semantics.exists()}")
    if trusted_semantics.exists():
        errors.append("GENERATED_SEMANTICS contradicts mounted trusted semantics")

    candidate_prompt = candidate_root / "prompt.py"
    candidate_translator = candidate_root / "py2mpy.py"
    comparisons = [
        ("candidate_prompt", candidate_prompt, paths["trusted_prompt"]),
        ("candidate_translator", candidate_translator, paths["translator"]),
    ]
    for name, candidate, trusted in comparisons:
        same = candidate.read_bytes() == trusted.read_bytes()
        print(f"{name}_byte_identity={same}")
        if not same:
            errors.append(f"{name} differs from trusted mount")

    recorded_hashes = {
        Path("/run.json"): audit["hashes"]["run_manifest_sha256"],
        Path("/task.json"): audit["hashes"]["task_manifest_sha256"],
        Path("/generation-result.json"): audit["hashes"]["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): audit["hashes"][
            "stage1_invocation_sha256"
        ],
        Path("/generation-evidence/metrics.json"): audit["hashes"][
            "generation_metrics_sha256"
        ],
        Path("/generation-evidence/codex-last.txt"): audit["hashes"][
            "generation_codex_last_sha256"
        ],
        Path("/generation-evidence/codex-output.log"): audit["hashes"][
            "generation_codex_output_sha256"
        ],
        Path("/generation-evidence/prompt.txt"): audit["hashes"][
            "generation_prompt_sha256"
        ],
        candidate_prompt: audit["hashes"]["candidate_prompt_sha256"],
        candidate_translator: audit["hashes"]["candidate_translator_sha256"],
        paths["trusted_prompt"]: audit["hashes"]["trusted_prompt_sha256"],
        paths["translator"]: audit["hashes"]["trusted_translator_sha256"],
        paths["canonical"]: audit["hashes"]["canonical_sha256"],
    }
    usage_path = Path("/generation-evidence/usage.json")
    if usage_path.exists():
        recorded_hashes[usage_path] = audit["hashes"]["generation_usage_sha256"]

    for path, expected in recorded_hashes.items():
        if not path.is_file():
            continue
        actual = digest(path)
        matches = actual == expected
        print(f"hash {path}: expected={expected} actual={actual} match={matches}")
        if not matches:
            errors.append(f"recorded hash mismatch: {path}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    evidence_hashes = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(evidence_hashes.items()):
        path = Path("/generation-evidence") / relative
        check_regular(path, errors)
        if path.is_file():
            actual = digest(path)
            matches = actual == expected
            print(
                f"generation-result evidence {relative}: "
                f"expected={expected} actual={actual} match={matches}"
            )
            if not matches:
                errors.append(f"generation-result evidence hash mismatch: {relative}")

    candidate_files = sorted(path for path in candidate_root.rglob("*") if path.is_file())
    print("independent_candidate_file_hashes:")
    for path in candidate_files:
        print(
            f"  {path.relative_to(candidate_root).as_posix()} "
            f"{digest(path)} mode={oct(path.stat().st_mode & 0o7777)} size={path.stat().st_size}"
        )

    trace_counts: collections.Counter[str] = collections.Counter()
    payload_counts: collections.Counter[str] = collections.Counter()
    trace_lines = 0
    call_names: list[str] = []
    tool_statuses: list[str] = []
    for trace in trace_files:
        print(f"trace_file={trace} sha256={digest(trace)}")
        with trace.open() as stream:
            for line_number, line in enumerate(stream, start=1):
                trace_lines += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as err:
                    errors.append(f"malformed trace JSON {trace}:{line_number}: {err}")
                    continue
                event_type = str(event.get("type"))
                trace_counts[event_type] += 1
                payload = event.get("payload", {})
                payload_type = str(payload.get("type"))
                payload_counts[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    call_names.append(
                        f"{line_number}:{payload.get('name')}:{payload.get('arguments')}"
                    )
                if payload_type in {"function_call_output", "custom_tool_call_output"}:
                    rendered = json.dumps(payload, sort_keys=True)
                    for marker in ["exit_code", "timed_out", "duration_ms"]:
                        if marker in rendered:
                            tool_statuses.append(
                                f"{line_number}:{marker}:{rendered[-600:]}"
                            )

    print(f"trace_valid_json_lines={trace_lines}")
    print(f"trace_event_counts={dict(sorted(trace_counts.items()))}")
    print(f"trace_payload_counts={dict(sorted(payload_counts.items()))}")
    print("trace_tool_calls:")
    for item in call_names:
        print(f"  {item}")
    print("trace_tool_status_excerpts:")
    for item in tool_statuses:
        print(f"  {item}")

    print(f"error_count={len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
