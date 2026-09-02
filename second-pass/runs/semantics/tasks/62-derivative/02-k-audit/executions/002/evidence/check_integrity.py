#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path, failures: list[str]) -> None:
    try:
        info = path.lstat()
    except OSError as err:
        failures.append(f"missing/unreadable: {path}: {err}")
        return
    if stat.S_ISLNK(info.st_mode):
        failures.append(f"symlink forbidden: {path}")
    elif not stat.S_ISREG(info.st_mode):
        failures.append(f"not a regular file: {path}")
    if not os.access(path, os.R_OK):
        failures.append(f"unreadable: {path}")


def compare_trees(left: Path, right: Path, failures: list[str]) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(info.st_mode):
                result[rel] = ("dir", None)
            elif stat.S_ISREG(info.st_mode):
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
        return result

    lhs = entries(left)
    rhs = entries(right)
    if lhs != rhs:
        for rel in sorted(set(lhs) | set(rhs)):
            if lhs.get(rel) != rhs.get(rel):
                failures.append(
                    f"semantics mismatch {rel}: trusted={lhs.get(rel)!r}, "
                    f"candidate={rhs.get(rel)!r}"
                )
    if any(kind == "symlink" for kind, _ in rhs.values()):
        failures.append("candidate reference-semantics contains a symlink")
    print(f"trusted_semantics_entries={len(lhs)}")
    print(f"candidate_semantics_entries={len(rhs)}")
    print(f"semantics_recursive_identity={lhs == rhs}")


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)
with LOCK.open(encoding="utf-8") as stream:
    lock = json.load(stream)

failures: list[str] = []
print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"campaign_block_matches_lock={audit.get('audit_campaign') == lock}")
if audit.get("audit_campaign") != lock:
    failures.append("campaign lock JSON does not match audit_campaign block")

actual_lock_hash = sha256(LOCK)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock_sha256={actual_lock_hash}")
if actual_lock_hash != expected_lock_hash:
    failures.append("audit campaign lock hash mismatch")

if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
    failures.append("rendered semantics mode is not SUPPLIED_SEMANTICS")
if not Path("/reference/reference-semantics").is_dir():
    failures.append("trusted supplied semantics mount is absent")

required = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
if audit.get("record_layout") != "legacy-selected-stage1":
    failures.append("unexpected record layout for this audit script")

for raw_path, hash_key in required.items():
    path = Path(raw_path)
    require_regular(path, failures)
    if path.is_file() and not path.is_symlink():
        actual = sha256(path)
        expected = audit["hashes"][hash_key]
        print(f"{path.name}_sha256={actual} expected={expected} match={actual == expected}")
        if actual != expected:
            failures.append(f"recorded hash mismatch: {path}")

usage = Path("/generation-evidence/usage.json")
if usage.exists():
    require_regular(usage, failures)
    if usage.is_file() and not usage.is_symlink():
        actual = sha256(usage)
        expected = audit["hashes"].get("generation_usage_sha256")
        print(f"usage_sha256={actual} expected={expected} match={actual == expected}")
        if expected and actual != expected:
            failures.append("usage hash mismatch")

for raw_path in (
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/candidate/prompt.py",
    "/candidate/py2mpy.py",
):
    require_regular(Path(raw_path), failures)

artifact_hashes = {
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
for raw_path, hash_key in artifact_hashes.items():
    path = Path(raw_path)
    if path.is_file() and not path.is_symlink():
        actual = sha256(path)
        expected = audit["hashes"][hash_key]
        print(f"{raw_path}_sha256={actual} match={actual == expected}")
        if actual != expected:
            failures.append(f"input artifact hash mismatch: {raw_path}")

if (
    Path("/candidate/prompt.py").read_bytes()
    != Path("/reference/prompt.py").read_bytes()
):
    failures.append("candidate prompt differs from trusted prompt")
if (
    Path("/candidate/py2mpy.py").read_bytes()
    != Path("/reference/py2mpy.py").read_bytes()
):
    failures.append("candidate translator differs from trusted translator")

compare_trees(
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
    failures,
)

for name in ("solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"):
    require_regular(Path("/candidate") / name, failures)

with Path("/generation-result.json").open(encoding="utf-8") as stream:
    result = json.load(stream)
recorded_evidence = result["outputs"]["evidence"]
for rel, expected in sorted(recorded_evidence.items()):
    path = Path("/generation-evidence") / rel
    require_regular(path, failures)
    if path.is_file() and not path.is_symlink():
        actual = sha256(path)
        print(f"generation_evidence {rel} sha256={actual} match={actual == expected}")
        if actual != expected:
            failures.append(f"generation-result evidence hash mismatch: {rel}")

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
regular_trace_files = [
    path for path in trace_files if path.is_file() and not path.is_symlink()
]
if not regular_trace_files:
    failures.append("structured trace has no regular files")
if any(path.is_symlink() for path in trace_files):
    failures.append("structured trace contains symlinked entries")

line_count = 0
event_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
first_timestamp = None
last_timestamp = None
parse_errors: list[str] = []
for trace in regular_trace_files:
    with trace.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            line_count += 1
            try:
                event = json.loads(line)
            except Exception as err:
                parse_errors.append(f"{trace}:{number}: {err}")
                continue
            timestamp = event.get("timestamp")
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
            event_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "custom_tool_call":
                    tool_names[str(payload.get("name"))] += 1

print(f"trace_files={len(regular_trace_files)}")
print(f"trace_lines={line_count}")
print(f"trace_first_timestamp={first_timestamp}")
print(f"trace_last_timestamp={last_timestamp}")
print(f"trace_event_types={dict(event_types)}")
print(f"trace_payload_types={dict(payload_types)}")
print(f"trace_tool_names={dict(tool_names)}")
print(f"trace_parse_errors={len(parse_errors)}")
failures.extend(parse_errors)

print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
