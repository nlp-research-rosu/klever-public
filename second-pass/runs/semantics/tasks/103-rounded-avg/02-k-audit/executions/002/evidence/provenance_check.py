#!/usr/bin/env python3
"""Independent Stage-1 manifest, hash, type, and supplied-tree checks."""

from pathlib import Path
import hashlib
import json
import os
import stat


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path):
    pending = [root]
    entries = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")
    return sorted(entries)


def sha_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path):
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"not a real regular file: {path}")


audit = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text(encoding="utf-8"))

print("record_layout=" + audit["record_layout"])
print("semantics_mode=" + audit["semantics_mode"])
if audit["record_layout"] != "legacy-selected-stage1":
    raise RuntimeError("unexpected record layout")
if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
    raise RuntimeError("unexpected semantics mode")

lock_sha = sha_file(Path("/audit-campaign-lock.json"))
print("campaign_lock_sha256=" + lock_sha)
print("campaign_block_equal=" + str(lock == audit["audit_campaign"]))
if lock_sha != audit["hashes"]["audit_campaign_lock_sha256"]:
    raise RuntimeError("campaign lock hash mismatch")
if lock != audit["audit_campaign"]:
    raise RuntimeError("campaign block mismatch")

required = [
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
for path in required:
    require_regular(path)
print("required_records_regular=" + str(len(required)))

hash_checks = [
    ("/run.json", "run_manifest_sha256"),
    ("/task.json", "task_manifest_sha256"),
    ("/generation-result.json", "stage1_result_sha256"),
    ("/generation-evidence/invocation.json", "stage1_invocation_sha256"),
    ("/generation-evidence/metrics.json", "generation_metrics_sha256"),
    ("/generation-evidence/codex-last.txt", "generation_codex_last_sha256"),
    ("/generation-evidence/codex-output.log", "generation_codex_output_sha256"),
    ("/generation-evidence/prompt.txt", "generation_prompt_sha256"),
    ("/generation-evidence/usage.json", "generation_usage_sha256"),
    ("/reference/canonical.py", "canonical_sha256"),
    ("/reference/prompt.py", "trusted_prompt_sha256"),
    ("/reference/py2mpy.py", "trusted_translator_sha256"),
]
for path_text, key in hash_checks:
    actual = sha_file(Path(path_text))
    expected = audit["hashes"][key]
    print(f"hash_match {path_text}={actual == expected} sha256={actual}")
    if actual != expected:
        raise RuntimeError(f"hash mismatch: {path_text}")

trace_root = Path("/generation-evidence/codex-trace")
trace_files = [path for _, kind, path in tree_entries(trace_root) if kind == "file"]
print("trace_regular_files=" + str(len(trace_files)))
for path in trace_files:
    relative = path.relative_to(trace_root).as_posix()
    expected = result["outputs"]["evidence"]["codex-trace/" + relative]
    actual = sha_file(path)
    print(f"trace_file_hash_match {relative}={actual == expected} sha256={actual}")
    if actual != expected:
        raise RuntimeError("trace file hash mismatch")
trace_tree = sha_tree(trace_root)
print("trace_tree_sha256=" + trace_tree)
print("trace_tree_matches_usage=" + str(trace_tree == usage["source_trace_sha256"]))
if trace_tree != usage["source_trace_sha256"]:
    raise RuntimeError("trace tree mismatch")

candidate_tree = sha_tree(Path("/candidate"))
print("candidate_tree_sha256=" + candidate_tree)
print(
    "candidate_matches_retained_workspace="
    + str(candidate_tree == invocation["retained_workspace_sha256"])
)
if candidate_tree != invocation["retained_workspace_sha256"]:
    raise RuntimeError("candidate retained-workspace mismatch")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
trusted_entries = tree_entries(trusted_semantics)
candidate_entries = tree_entries(candidate_semantics)
trusted_manifest = sha_tree(trusted_semantics)
candidate_manifest = sha_tree(candidate_semantics)
print("trusted_semantics_manifest_sha256=" + trusted_manifest)
print("candidate_semantics_manifest_sha256=" + candidate_manifest)
print("semantics_entry_lists_equal=" + str(
    [(r, k) for r, k, _ in trusted_entries]
    == [(r, k) for r, k, _ in candidate_entries]
))
if trusted_manifest != audit["hashes"]["trusted_reference_semantics_manifest_sha256"]:
    raise RuntimeError("trusted semantics manifest mismatch")
if trusted_manifest != candidate_manifest:
    raise RuntimeError("semantics manifest mismatch")
for (relative, kind, trusted), (_, _, candidate) in zip(
    trusted_entries, candidate_entries, strict=True
):
    if kind == "file" and sha_file(trusted) != sha_file(candidate):
        raise RuntimeError(f"semantics content mismatch: {relative}")
print("semantics_recursive_content_equal=True")

for candidate_path, trusted_path in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    require_regular(candidate_path)
    if sha_file(candidate_path) != sha_file(trusted_path):
        raise RuntimeError(f"candidate input mismatch: {candidate_path}")
print("candidate_prompt_translator_equal=True")
print("stage1_integrity=PASS")
