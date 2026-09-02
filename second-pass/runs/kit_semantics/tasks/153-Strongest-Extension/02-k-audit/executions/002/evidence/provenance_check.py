#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reviewer_tree_manifest(root: Path):
    entries = []
    for path in sorted([root, *root.rglob("*")], key=lambda item: str(item.relative_to(root))):
        relative = "." if path == root else path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            detail = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            detail = ""
        elif stat.S_ISREG(mode):
            kind = "file"
            detail = sha256(path)
        else:
            kind = "other"
            detail = oct(mode)
        entries.append((relative, kind, detail))
    encoded = "\n".join("\t".join(entry) for entry in entries).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


audit_input_path = Path("/audit-input.json")
campaign_lock_path = Path("/audit-campaign-lock.json")
audit_input = json.loads(audit_input_path.read_text())
campaign_lock = json.loads(campaign_lock_path.read_text())

print("record_layout:", audit_input["record_layout"])
print("problem:", audit_input["problem_id"])
print("generation_condition:", audit_input["condition"])
print("semantics_mode:", audit_input["semantics_mode"])
assert audit_input["record_layout"] == "pipeline-v3"
assert audit_input["problem_id"] == "153-Strongest-Extension"
assert audit_input["condition"] == "kit-semantics"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is True

print("campaign_lock_equal:", campaign_lock == audit_input["audit_campaign"])
assert campaign_lock == audit_input["audit_campaign"]
campaign_hash = sha256(campaign_lock_path)
print("campaign_lock_sha256:", campaign_hash)
print("campaign_lock_expected:", audit_input["hashes"]["audit_campaign_lock_sha256"])
assert campaign_hash == audit_input["hashes"]["audit_campaign_lock_sha256"]

required_records = [
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
]
for path in required_records:
    assert path.is_file() and os.access(path, os.R_OK), path
    print("required_record:", path, sha256(path))

hash_path_map = {
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
}
for key, path in hash_path_map.items():
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    print("recorded_hash:", key, "actual=", actual, "expected=", expected)
    assert actual == expected

generation_result = json.loads(Path("/generation-result.json").read_text())
trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert len(trace_files) == 1
trace_file = trace_files[0]
trace_hash = sha256(trace_file)
trace_relative = trace_file.relative_to("/generation-evidence").as_posix()
trace_expected = generation_result["outputs"]["evidence"][trace_relative]
print("trace_file:", trace_file)
print("trace_sha256:", trace_hash)
print("trace_expected:", trace_expected)
assert trace_hash == trace_expected

trace_counts = Counter()
trace_lines = 0
with trace_file.open() as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        trace_lines += 1
        trace_counts[record["type"]] += 1
print("trace_json_lines:", trace_lines)
print("trace_record_types:", dict(sorted(trace_counts.items())))

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical: true")
print("candidate_translator_byte_identical: true")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
assert trusted_semantics.is_dir()
assert candidate_semantics.is_dir()
trusted_entries, trusted_digest = reviewer_tree_manifest(trusted_semantics)
candidate_entries, candidate_digest = reviewer_tree_manifest(candidate_semantics)
print("trusted_semantics_reviewer_manifest_sha256:", trusted_digest)
print("candidate_semantics_reviewer_manifest_sha256:", candidate_digest)
print("semantics_entry_count:", len(trusted_entries))
print("semantics_direct_tree_identical:", trusted_entries == candidate_entries)
assert trusted_entries == candidate_entries
assert all(kind != "symlink" for _, kind, _ in trusted_entries)
assert all(kind != "symlink" for _, kind, _ in candidate_entries)

for root in [Path("/candidate"), Path("/reference"), Path("/generation-evidence")]:
    symlinks = [str(path) for path in root.rglob("*") if path.is_symlink()]
    print("symlinks_under:", root, symlinks)
    assert not symlinks

candidate_entries_all, candidate_digest_all = reviewer_tree_manifest(Path("/candidate"))
trace_entries_all, trace_digest_all = reviewer_tree_manifest(Path("/generation-evidence/codex-trace"))
print("candidate_reviewer_manifest_sha256:", candidate_digest_all)
print("candidate_reviewer_entry_count:", len(candidate_entries_all))
print("trace_reviewer_manifest_sha256:", trace_digest_all)
print("launcher_recorded_aggregate_hashes:", json.dumps({
    key: value
    for key, value in audit_input["hashes"].items()
    if "tree" in key or "trace" in key or "reference_semantics" in key
}, sort_keys=True))

candidate_required = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "connection-spec.k",
    "outer-connection-spec.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for relative in candidate_required:
    path = Path("/candidate") / relative
    assert path.is_file() and not path.is_symlink(), path
    print("candidate_proof_artifact:", relative, sha256(path))

print("PROVENANCE_CHECK: OK")
