#!/usr/bin/env python3
import collections
import hashlib
import json
import os
import pathlib
import stat
import sys


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root_path: pathlib.Path) -> str:
    """Independent implementation of the launcher tree-digest format."""
    digest = hashlib.sha256()
    entries = []
    pending = [root_path]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            info = path.lstat()
            relative = path.relative_to(root_path).as_posix()
            if stat.S_ISDIR(info.st_mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            info = path.lstat()
            digest.update(info.st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def describe(path: pathlib.Path) -> str:
    try:
        info = path.lstat()
    except OSError as err:
        return f"MISSING/UNREADABLE {path}: {err}"
    if stat.S_ISREG(info.st_mode):
        kind = "regular"
    elif stat.S_ISDIR(info.st_mode):
        kind = "directory"
    elif stat.S_ISLNK(info.st_mode):
        kind = "symlink"
    else:
        kind = f"special-mode-{stat.S_IFMT(info.st_mode):o}"
    return f"{kind} mode={stat.S_IMODE(info.st_mode):03o} size={info.st_size} {path}"


def require_regular(paths):
    ok = True
    for path in paths:
        print(describe(path))
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode):
                ok = False
        except OSError:
            ok = False
    return ok


root = pathlib.Path("/")
audit_path = root / "audit-input.json"
lock_path = root / "audit-campaign-lock.json"
with audit_path.open(encoding="utf-8") as stream:
    audit = json.load(stream)
with lock_path.open(encoding="utf-8") as stream:
    lock = json.load(stream)

print("record_layout:", audit.get("record_layout"))
print("semantics_mode:", audit.get("semantics_mode"))
print("campaign_block_exact_match:", audit.get("audit_campaign") == lock)
actual_lock_hash = sha256(lock_path)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock_sha256:", actual_lock_hash)
print("campaign_lock_hash_match:", actual_lock_hash == expected_lock_hash)

required = [
    audit_path,
    lock_path,
    root / "run.json",
    root / "task.json",
    root / "generation-result.json",
    root / "reference/canonical.py",
    root / "reference/prompt.py",
    root / "reference/py2mpy.py",
    root / "generation-evidence/invocation.json",
    root / "generation-evidence/metrics.json",
    root / "generation-evidence/runtime-metrics.json",
    root / "generation-evidence/usage.json",
    root / "generation-evidence/codex-last.txt",
    root / "generation-evidence/codex-output.log",
    root / "generation-evidence/prompt.txt",
]
print("required_records_regular:", require_regular(required))

checks = {
    "audit_campaign_lock_sha256": lock_path,
    "candidate_prompt_sha256": root / "candidate/prompt.py",
    "candidate_translator_sha256": root / "candidate/py2mpy.py",
    "canonical_sha256": root / "reference/canonical.py",
    "generation_codex_last_sha256": root / "generation-evidence/codex-last.txt",
    "generation_codex_output_sha256": root / "generation-evidence/codex-output.log",
    "generation_metrics_sha256": root / "generation-evidence/metrics.json",
    "generation_prompt_sha256": root / "generation-evidence/prompt.txt",
    "generation_runtime_metrics_sha256": root / "generation-evidence/runtime-metrics.json",
    "generation_usage_sha256": root / "generation-evidence/usage.json",
    "run_manifest_sha256": root / "run.json",
    "stage1_invocation_sha256": root / "generation-evidence/invocation.json",
    "stage1_result_sha256": root / "generation-result.json",
    "task_manifest_sha256": root / "task.json",
    "trusted_prompt_sha256": root / "reference/prompt.py",
    "trusted_translator_sha256": root / "reference/py2mpy.py",
}
all_hashes_match = True
for key, path in checks.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    matched = actual == expected
    all_hashes_match &= matched
    print(f"{key}: match={matched} actual={actual} expected={expected}")
print("all_direct_recorded_hashes_match:", all_hashes_match)

with (root / "generation-result.json").open(encoding="utf-8") as stream:
    result = json.load(stream)
with (root / "generation-evidence/usage.json").open(encoding="utf-8") as stream:
    usage = json.load(stream)
tree_checks = {
    "candidate_pipeline_workspace_sha256": (
        root / "candidate",
        result["outputs"]["workspace_sha256"],
    ),
    "candidate_reference_semantics_manifest_sha256": (
        root / "candidate/reference-semantics",
        audit["manifest"]["inputs"]["reference_semantics_sha256"],
    ),
    "trusted_reference_semantics_manifest_sha256": (
        root / "reference/reference-semantics",
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    "generation_source_trace_sha256": (
        root / "generation-evidence/codex-trace",
        usage["source_trace_sha256"],
    ),
}
all_tree_hashes_match = True
for key, (path, expected) in tree_checks.items():
    actual = sha256_tree(path)
    matched = actual == expected
    all_tree_hashes_match &= matched
    print(f"{key}: match={matched} actual={actual} expected={expected}")
print("all_recorded_tree_hashes_match:", all_tree_hashes_match)

with (root / "task.json").open(encoding="utf-8") as stream:
    task = json.load(stream)
audit_task_projection = dict(audit["manifest"])
audit_only_task_fields = {
    key: audit_task_projection.pop(key)
    for key in sorted(set(audit_task_projection) - set(task))
}
print("task_manifest_matches_audit_projection:", task == audit_task_projection)
print("audit_synthesized_manifest_fields_not_in_task_record:", audit_only_task_fields)

result_files_match = True
for relative, expected in result["outputs"]["evidence"].items():
    path = root / "generation-evidence" / relative
    actual = sha256(path)
    matched = actual == expected
    result_files_match &= matched
    print(f"generation_result_file {relative}: match={matched} actual={actual} expected={expected}")
print("all_generation_result_file_hashes_match:", result_files_match)

trace_root = root / "generation-evidence/codex-trace"
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
print("trace_file_count:", len(trace_files))
for path in trace_files:
    print(f"trace_file_sha256 {path.relative_to(trace_root)} {sha256(path)}")

json_records = [
    root / "audit-input.json",
    root / "audit-campaign-lock.json",
    root / "run.json",
    root / "task.json",
    root / "generation-result.json",
    root / "generation-evidence/invocation.json",
    root / "generation-evidence/metrics.json",
    root / "generation-evidence/runtime-metrics.json",
    root / "generation-evidence/usage.json",
]
json_ok = True
for path in json_records:
    try:
        with path.open(encoding="utf-8") as stream:
            json.load(stream)
        print("json_parse_ok:", path)
    except Exception as err:
        json_ok = False
        print("json_parse_failed:", path, repr(err))
print("all_json_records_parse:", json_ok)

trace_ok = True
trace_lines = 0
top_types = collections.Counter()
payload_types = collections.Counter()
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except Exception as err:
                trace_ok = False
                print("trace_parse_failed:", path, line_number, repr(err))
                continue
            top_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
print("trace_jsonl_parse_ok:", trace_ok)
print("trace_line_count:", trace_lines)
print("trace_top_level_types:", dict(sorted(top_types.items())))
print("trace_payload_types:", dict(sorted(payload_types.items())))

print("candidate_tree_symlinks_and_specials:")
candidate_root = root / "candidate"
special_count = 0
for path in sorted(candidate_root.rglob("*")):
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
        special_count += 1
        print(describe(path))
print("candidate_special_entry_count:", special_count)

reference_root = root / "reference/reference-semantics"
print("trusted_reference_semantics_present:", reference_root.is_dir())
print("candidate_reference_semantics_present:", (candidate_root / "reference-semantics").is_dir())

proof_artifacts = [
    candidate_root / "solution.py",
    candidate_root / "solution.mpy",
    candidate_root / "verification.k",
    candidate_root / "spec.k",
    candidate_root / "prove.sh",
    candidate_root / "PROOF.md",
]
print("required_candidate_proof_artifacts_regular:", require_regular(proof_artifacts))

if not (
    all_hashes_match
    and all_tree_hashes_match
    and result_files_match
    and trace_ok
    and json_ok
):
    sys.exit(1)
