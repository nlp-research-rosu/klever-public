#!/usr/bin/env python3
"""Independent read-only provenance and record-layout checks for this audit."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes:
    # Reading through one function makes the full-file read explicit.
    return path.read_bytes()


def load_json(path: Path):
    return json.loads(read_bytes(path))


def tree_manifest(root: Path) -> tuple[str, list[str], list[str]]:
    """Return an auditor-defined content manifest digest, entries, and symlinks.

    Encoding per sorted entry:
      D NUL relative-path LF
      F NUL relative-path NUL sha256(file-bytes) LF
      L NUL relative-path NUL link-target LF
    """
    records: list[bytes] = []
    display: list[str] = []
    symlinks: list[str] = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            target = os.readlink(path)
            records.append(b"L\0" + rel.encode() + b"\0" + target.encode() + b"\n")
            display.append(f"L {rel} -> {target}")
            symlinks.append(rel)
        elif stat.S_ISDIR(mode):
            records.append(b"D\0" + rel.encode() + b"\n")
            display.append(f"D {rel}")
        elif stat.S_ISREG(mode):
            digest = sha256_bytes(read_bytes(path))
            records.append(b"F\0" + rel.encode() + b"\0" + digest.encode() + b"\n")
            display.append(f"F {rel} {digest}")
        else:
            records.append(b"O\0" + rel.encode() + b"\n")
            display.append(f"O {rel}")
    return sha256_bytes(b"".join(records)), display, symlinks


def main() -> int:
    failures: list[str] = []
    audit = load_json(AUDIT_INPUT)
    lock = load_json(CAMPAIGN_LOCK)
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"problem_id={audit.get('problem_id')}")

    campaign_equal = audit.get("audit_campaign") == lock
    lock_hash = sha256_bytes(read_bytes(CAMPAIGN_LOCK))
    lock_expected = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_object_equal={campaign_equal}")
    print(f"campaign_lock_sha256={lock_hash}")
    print(f"campaign_lock_recorded={lock_expected}")
    if not campaign_equal or lock_hash != lock_expected:
        failures.append("campaign lock mismatch")

    declared = audit["container_paths"]
    for name, raw in sorted(declared.items()):
        path = Path(raw)
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        symlink = path.is_symlink()
        print(
            f"declared_mount {name}: path={path} exists={exists} "
            f"readable={readable} symlink={symlink}"
        )
        if not exists or not readable:
            failures.append(f"declared mount unavailable: {name}")

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        required.append(usage)
    trace_root = Path("/generation-evidence/codex-trace")
    if not trace_root.is_dir():
        failures.append("structured trace directory missing")

    recorded_file_hashes = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    hashes = audit["hashes"]
    for path in required:
        exists = path.exists()
        readable = os.access(path, os.R_OK)
        symlink = path.is_symlink()
        print(f"required_record {path}: exists={exists} readable={readable} symlink={symlink}")
        if not exists or not readable:
            failures.append(f"required record unavailable: {path}")
    for path, key in recorded_file_hashes.items():
        if not path.exists():
            failures.append(f"hashed input missing: {path}")
            continue
        digest = sha256_bytes(read_bytes(path))
        expected = hashes.get(key)
        matches = digest == expected
        print(f"hash {path}: actual={digest} recorded={expected} matches={matches}")
        if expected is not None and not matches:
            failures.append(f"hash mismatch: {path}")

    # Parse the structured records, which also guarantees complete reads.
    for path in [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
    ] + ([usage] if usage.exists() else []):
        obj = load_json(path)
        print(f"json_parse {path}: ok type={type(obj).__name__} keys={sorted(obj)}")

    result = load_json(Path("/generation-result.json"))
    output_hashes = result.get("outputs", {}).get("evidence", {})
    for rel, expected in sorted(output_hashes.items()):
        path = Path("/generation-evidence") / rel
        if not path.exists():
            failures.append(f"generation-result output missing: {rel}")
            print(f"generation_result_output {rel}: missing")
            continue
        digest = sha256_bytes(read_bytes(path))
        print(
            f"generation_result_output {rel}: actual={digest} "
            f"recorded={expected} matches={digest == expected}"
        )
        if digest != expected:
            failures.append(f"generation-result output hash mismatch: {rel}")

    trace_files = sorted(trace_root.rglob("*")) if trace_root.exists() else []
    trace_files = [p for p in trace_files if p.is_file()]
    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    roles: Counter[str] = Counter()
    trace_lines = 0
    trace_bytes = 0
    tool_calls: list[str] = []
    for path in trace_files:
        raw = read_bytes(path)
        trace_bytes += len(raw)
        for lineno, line in enumerate(raw.splitlines(), 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except Exception as err:
                failures.append(f"trace JSON parse failure: {path}:{lineno}: {err}")
                continue
            event_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "message":
                    roles[str(payload.get("role"))] += 1
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name"))
                    args = str(payload.get("arguments") or payload.get("input") or "")
                    tool_calls.append(f"{name} {args[:500]}")
    print(f"trace_files={len(trace_files)} trace_lines={trace_lines} trace_bytes={trace_bytes}")
    print(f"trace_event_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_message_roles={dict(sorted(roles.items()))}")
    print(f"trace_tool_call_count={len(tool_calls)}")
    for idx, call in enumerate(tool_calls, 1):
        print(f"trace_tool_call[{idx}]={call}")

    output_text = read_bytes(Path("/generation-evidence/codex-output.log"))
    print(
        "generation_output_full_read="
        f"bytes:{len(output_text)} lines:{len(output_text.splitlines())} "
        f"sha256:{sha256_bytes(output_text)}"
    )
    for needle in [
        b"KPROVE_PASSED",
        b"#Top",
        b"WarnStuckClaimState",
        b"kompile",
        b"kprove",
        b"krun",
    ]:
        print(f"generation_output_occurrences {needle.decode()}={output_text.count(needle)}")

    candidate_prompt = read_bytes(Path("/candidate/prompt.py"))
    trusted_prompt = read_bytes(Path("/reference/prompt.py"))
    candidate_translator = read_bytes(Path("/candidate/py2mpy.py"))
    trusted_translator = read_bytes(Path("/reference/py2mpy.py"))
    print(f"candidate_prompt_byte_equal={candidate_prompt == trusted_prompt}")
    print(f"candidate_translator_byte_equal={candidate_translator == trusted_translator}")
    if candidate_prompt != trusted_prompt:
        failures.append("candidate prompt differs from trusted prompt")
    if candidate_translator != trusted_translator:
        failures.append("candidate translator differs from trusted translator")

    candidate_sem = Path("/candidate/reference-semantics")
    trusted_sem = Path("/reference/reference-semantics")
    if audit.get("semantics_mode") == "SUPPLIED_SEMANTICS" and not trusted_sem.is_dir():
        failures.append("trusted supplied semantics absent")
    candidate_digest, candidate_entries, candidate_links = tree_manifest(candidate_sem)
    trusted_digest, trusted_entries, trusted_links = tree_manifest(trusted_sem)
    print(f"auditor_manifest candidate_reference_semantics={candidate_digest}")
    print(f"auditor_manifest trusted_reference_semantics={trusted_digest}")
    print(f"reference_semantics_manifests_equal={candidate_entries == trusted_entries}")
    print(f"candidate_reference_semantics_symlinks={candidate_links}")
    print(f"trusted_reference_semantics_symlinks={trusted_links}")
    print("trusted_reference_semantics_entries_begin")
    for entry in trusted_entries:
        print(entry)
    print("trusted_reference_semantics_entries_end")
    if candidate_entries != trusted_entries:
        failures.append("candidate supplied semantics differs from trusted tree")
    if candidate_links or trusted_links:
        failures.append("symlink in supplied semantics")

    candidate_digest, candidate_entries, candidate_links = tree_manifest(Path("/candidate"))
    print(f"auditor_manifest candidate_tree={candidate_digest}")
    print(f"candidate_tree_symlinks={candidate_links}")
    print(f"candidate_tree_entry_count={len(candidate_entries)}")
    trace_digest, _, trace_links = tree_manifest(trace_root)
    print(f"auditor_manifest generation_trace_tree={trace_digest}")
    print(f"generation_trace_symlinks={trace_links}")
    if trace_links:
        failures.append("symlink in structured trace")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE={failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
