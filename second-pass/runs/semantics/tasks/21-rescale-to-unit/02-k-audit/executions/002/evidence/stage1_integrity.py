#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
lock_path = Path("/audit-campaign-lock.json")
lock = json.loads(lock_path.read_text())
hashes = audit["hashes"]

checks: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str) -> None:
    checks.append((name, condition, detail))


check(
    "campaign block equals lock JSON",
    audit["audit_campaign"] == lock,
    f"campaign_id={lock.get('campaign_id')}",
)
check(
    "campaign lock SHA-256",
    sha256(lock_path) == hashes["audit_campaign_lock_sha256"],
    sha256(lock_path),
)
check(
    "declared record layout",
    audit["record_layout"] == "legacy-selected-stage1",
    audit["record_layout"],
)
check(
    "declared semantics mode",
    audit["semantics_mode"] == "SUPPLIED_SEMANTICS",
    audit["semantics_mode"],
)

required_regular = {
    "audit input": audit_path,
    "campaign lock": lock_path,
    "run manifest": Path("/run.json"),
    "task manifest": Path("/task.json"),
    "stage1 result": Path("/generation-result.json"),
    "invocation": Path("/generation-evidence/invocation.json"),
    "metrics": Path("/generation-evidence/metrics.json"),
    "codex last": Path("/generation-evidence/codex-last.txt"),
    "codex output": Path("/generation-evidence/codex-output.log"),
    "generation prompt": Path("/generation-evidence/prompt.txt"),
    "canonical": Path("/reference/canonical.py"),
    "trusted prompt": Path("/reference/prompt.py"),
    "translator": Path("/reference/py2mpy.py"),
    "candidate mount": Path("/candidate"),
    "trusted supplied semantics": Path("/reference/reference-semantics"),
}
for name, path in required_regular.items():
    expected = path.is_dir() if name in {
        "candidate mount",
        "trusted supplied semantics",
    } else path.is_file()
    check(
        f"required mount/record: {name}",
        expected and not path.is_symlink(),
        f"{path} ({'directory' if path.is_dir() else 'file' if path.is_file() else 'missing/wrong type'})",
    )

recorded_file_hashes = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, field in recorded_file_hashes.items():
    actual = sha256(path)
    check(f"recorded hash: {field}", actual == hashes[field], actual)

task = json.loads(Path("/task.json").read_text())
run = json.loads(Path("/run.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
check(
    "mounted task fields agree with embedded audit manifest",
    all(audit["manifest"].get(key) == value for key, value in task.items()),
    f"task schema={task.get('schema_version')} embedded extra keys={sorted(set(audit['manifest']) - set(task))}",
)
check(
    "run/task/audit condition alignment",
    run["condition"] == task["condition"] == audit["manifest"]["condition"],
    repr(run["condition"]),
)
check(
    "problem identifier alignment",
    task["problem_id"] == audit["problem_id"] == "21-rescale-to-unit",
    task["problem_id"],
)

generation_files = {
    "codex-last.txt": Path("/generation-evidence/codex-last.txt"),
    "codex-output.log": Path("/generation-evidence/codex-output.log"),
    "prompt.txt": Path("/generation-evidence/prompt.txt"),
    "usage.json": Path("/generation-evidence/usage.json"),
    "legacy-metrics.json": Path("/generation-evidence/legacy-metrics.json"),
    "legacy-run-input.json": Path("/generation-evidence/legacy-run-input.json"),
}
trace_root = Path("/generation-evidence/codex-trace")
for trace_file in sorted(trace_root.rglob("*")):
    if trace_file.is_file():
        generation_files[str(trace_file.relative_to(Path("/generation-evidence")))] = trace_file

for relative, path in generation_files.items():
    actual = sha256(path)
    result_expected = result["outputs"]["evidence"].get(relative)
    invocation_expected = invocation["outputs"]["evidence"].get(relative)
    check(
        f"generation-result evidence hash: {relative}",
        result_expected == actual,
        f"actual={actual} recorded={result_expected}",
    )
    check(
        f"invocation evidence hash: {relative}",
        invocation_expected == actual,
        f"actual={actual} recorded={invocation_expected}",
    )

for field, left, right in [
    ("candidate prompt", Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    ("candidate translator", Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    check(
        f"{field} byte identity",
        left.read_bytes() == right.read_bytes(),
        f"{sha256(left)} vs {sha256(right)}",
    )

for root_name, root in [
    ("candidate", Path("/candidate")),
    ("reference", Path("/reference")),
    ("generation trace", trace_root),
]:
    symlinks = [str(path) for path in root.rglob("*") if path.is_symlink()]
    check(f"{root_name} contains no symlinks", not symlinks, repr(symlinks))

candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")
candidate_entries = {
    str(path.relative_to(candidate_semantics)): (
        "dir" if path.is_dir() else "file" if path.is_file() else "other"
    )
    for path in candidate_semantics.rglob("*")
}
trusted_entries = {
    str(path.relative_to(trusted_semantics)): (
        "dir" if path.is_dir() else "file" if path.is_file() else "other"
    )
    for path in trusted_semantics.rglob("*")
}
check(
    "supplied semantics entry set and types",
    candidate_entries == trusted_entries,
    f"candidate={len(candidate_entries)} trusted={len(trusted_entries)}",
)
semantics_mismatches = []
for relative, kind in trusted_entries.items():
    if kind == "file":
        trusted_file = trusted_semantics / relative
        candidate_file = candidate_semantics / relative
        if not candidate_file.is_file() or sha256(candidate_file) != sha256(trusted_file):
            semantics_mismatches.append(relative)
check(
    "supplied semantics file bytes",
    not semantics_mismatches,
    repr(semantics_mismatches),
)

trace_files = [path for path in trace_root.rglob("*") if path.is_file()]
check(
    "structured trace present",
    bool(trace_files),
    repr([str(path.relative_to(trace_root)) for path in trace_files]),
)
for trace_file in trace_files:
    parsed = 0
    types: dict[str, int] = {}
    with trace_file.open() as stream:
        for line_no, line in enumerate(stream, 1):
            record = json.loads(line)
            parsed += 1
            record_type = str(record.get("type"))
            types[record_type] = types.get(record_type, 0) + 1
    check(
        f"structured trace parses: {trace_file.name}",
        parsed > 0,
        f"records={parsed} types={types}",
    )

failures = 0
for name, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'}: {name}: {detail}")
    failures += not passed
print(f"SUMMARY: checks={len(checks)} failures={failures}")
raise SystemExit(1 if failures else 0)
