#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path

AUDIT_PATH = Path("/audit-input.json")
with AUDIT_PATH.open("rb") as handle:
    audit_bytes = handle.read()
audit = json.loads(audit_bytes)

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
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

trace_root = Path(audit["container_paths"]["generation_trace"])
trace_files = sorted(trace_root.rglob("*")) if trace_root.exists() else []
trace_regular_files = [path for path in trace_files if path.is_file()]

print("record_layout:", audit.get("record_layout"))
print("semantics_mode:", audit.get("semantics_mode"))
print("required_record_types:")
infrastructure_ok = True
for path in required:
    try:
        info = path.lstat()
        regular = stat.S_ISREG(info.st_mode)
        symlink = stat.S_ISLNK(info.st_mode)
        readable = os.access(path, os.R_OK)
    except FileNotFoundError:
        regular = symlink = readable = False
    print(f"  {path}: regular={regular} symlink={symlink} readable={readable}")
    infrastructure_ok &= regular and not symlink and readable

print("trace_tree:")
if not trace_regular_files:
    infrastructure_ok = False
    print("  NO REGULAR TRACE FILES")
for path in trace_files:
    info = path.lstat()
    kind = (
        "symlink" if stat.S_ISLNK(info.st_mode)
        else "file" if stat.S_ISREG(info.st_mode)
        else "dir" if stat.S_ISDIR(info.st_mode)
        else "other"
    )
    print(f"  {kind} {path}")
    if kind == "symlink" or kind == "other":
        infrastructure_ok = False

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

checks = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
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

print("declared_file_hash_checks:")
hashes_ok = True
for key, path in checks.items():
    declared = audit["hashes"].get(key)
    actual = sha256(path) if path.is_file() else None
    match = declared == actual
    hashes_ok &= match
    print(f"  {key}: declared={declared} actual={actual} match={match}")

with Path("/audit-campaign-lock.json").open(encoding="utf-8") as handle:
    campaign_lock = json.load(handle)
campaign_match = campaign_lock == audit["audit_campaign"]
print("campaign_lock_equals_audit_campaign:", campaign_match)

with Path("/generation-result.json").open(encoding="utf-8") as handle:
    generation_result = json.load(handle)
with Path("/generation-evidence/invocation.json").open(encoding="utf-8") as handle:
    invocation = json.load(handle)

generation_output_checks_ok = True
print("generation_output_hash_checks:")
for relative, declared in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path) if path.is_file() else None
    match = declared == actual
    generation_output_checks_ok &= match
    print(f"  {relative}: declared={declared} actual={actual} match={match}")

invocation_output_checks_ok = True
print("invocation_output_hash_checks:")
for relative, declared in sorted(invocation["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path) if path.is_file() else None
    match = declared == actual
    invocation_output_checks_ok &= match
    print(f"  {relative}: declared={declared} actual={actual} match={match}")

print("trace_jsonl_parse:")
trace_ok = True
for path in trace_regular_files:
    event_types = Counter()
    payload_types = Counter()
    malformed = []
    line_count = 0
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line_count = line_number
            try:
                event = json.loads(line)
            except Exception as error:
                malformed.append((line_number, repr(error)))
                continue
            event_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
    ok = not malformed
    trace_ok &= ok
    print(
        f"  {path}: lines={line_count} sha256={sha256(path)} "
        f"malformed={malformed} event_types={dict(event_types)} "
        f"payload_types={dict(payload_types)}"
    )

print("independent_integrity_summary:")
print("  infrastructure_ok:", infrastructure_ok)
print("  declared_hashes_ok:", hashes_ok)
print("  campaign_match:", campaign_match)
print("  generation_result_evidence_hashes_ok:", generation_output_checks_ok)
print("  invocation_evidence_hashes_ok:", invocation_output_checks_ok)
print("  trace_parse_ok:", trace_ok)
