#!/usr/bin/env bash
set -uo pipefail

python3 - <<'PY'
import collections
import hashlib
import json
import os
from pathlib import Path

audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit = json.loads(audit_path.read_text())
lock = json.loads(lock_path.read_text())

print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("problem_id:", audit["problem_id"])
print("campaign_block_equals_lock:", audit["audit_campaign"] == lock)
print("campaign_lock_sha256:", hashlib.sha256(lock_path.read_bytes()).hexdigest())
print("campaign_lock_expected:", audit["hashes"]["audit_campaign_lock_sha256"])

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/codex-trace",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/reference/reference-semantics",
    "/candidate",
]
print("required_records:")
for raw in required:
    p = Path(raw)
    kind = "symlink" if p.is_symlink() else "dir" if p.is_dir() else "file" if p.is_file() else "missing-or-other"
    print(f"  {raw}: {kind}, readable={os.access(p, os.R_OK)}")

hash_targets = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
print("recorded_file_hash_checks:")
for raw, key in hash_targets.items():
    p = Path(raw)
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    expected = audit["hashes"][key]
    print(f"  {raw}: match={actual == expected} actual={actual} expected={expected}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [p for p in trace_files if p.is_file()]
print("trace_files:", [str(p) for p in trace_files])
result = json.loads(Path("/generation-result.json").read_text())
declared_trace = {
    k: v for k, v in result["outputs"]["evidence"].items()
    if k.startswith("codex-trace/")
}
for p in trace_files:
    rel = "codex-trace/" + str(p.relative_to("/generation-evidence/codex-trace"))
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    expected = declared_trace.get(rel)
    print(f"  trace {rel}: match={actual == expected} actual={actual} expected={expected}")

event_types = collections.Counter()
payload_types = collections.Counter()
json_lines = 0
for p in trace_files:
    with p.open() as stream:
        for json_lines, line in enumerate(stream, json_lines + 1):
            item = json.loads(line)
            event_types[item.get("type")] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[payload.get("type")] += 1
print("trace_json_lines:", json_lines)
print("trace_event_types:", dict(sorted(event_types.items(), key=lambda kv: str(kv[0]))))
print("trace_payload_types:", dict(sorted(payload_types.items(), key=lambda kv: str(kv[0]))))

def inventory(root):
    root = Path(root)
    entries = {}
    for p in sorted(root.rglob("*")):
        rel = str(p.relative_to(root))
        if p.is_symlink():
            entries[rel] = ("symlink", os.readlink(p))
        elif p.is_dir():
            entries[rel] = ("dir", None)
        elif p.is_file():
            entries[rel] = ("file", hashlib.sha256(p.read_bytes()).hexdigest())
        else:
            entries[rel] = ("other", None)
    return entries

trusted_semantics = inventory("/reference/reference-semantics")
candidate_semantics = inventory("/candidate/reference-semantics")
print("semantics_entry_sets_equal:", trusted_semantics.keys() == candidate_semantics.keys())
print("semantics_entries_exact:", trusted_semantics == candidate_semantics)
print("trusted_semantics_entries:", len(trusted_semantics))
print("candidate_semantics_entries:", len(candidate_semantics))
print("candidate_semantics_symlinks:", [k for k, v in candidate_semantics.items() if v[0] == "symlink"])
for rel in sorted(set(trusted_semantics) | set(candidate_semantics)):
    if trusted_semantics.get(rel) != candidate_semantics.get(rel):
        print("  semantics_difference:", rel, trusted_semantics.get(rel), candidate_semantics.get(rel))

candidate_all = inventory("/candidate")
print("candidate_all_entries:", len(candidate_all))
print("candidate_all_symlinks:", [k for k, v in candidate_all.items() if v[0] == "symlink"])
manifest_lines = []
for rel, (kind, digest) in sorted(candidate_all.items()):
    manifest_lines.append(f"{kind}\t{rel}\t{digest or ''}\n")
independent_tree_digest = hashlib.sha256("".join(manifest_lines).encode()).hexdigest()
print("candidate_independent_manifest_sha256:", independent_tree_digest)
print("launcher_candidate_tree_sha256_claim:", audit["hashes"]["candidate_tree_sha256"])

print("prompt_bytes_equal:", Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes())
print("translator_bytes_equal:", Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes())
print("declared_integrity_fields:", audit["integrity"])
PY
