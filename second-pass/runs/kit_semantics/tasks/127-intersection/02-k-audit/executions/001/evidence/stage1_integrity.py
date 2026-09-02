#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a directory: {path}"


def tree_manifest(root: Path) -> tuple[list[tuple[str, str, str]], str]:
    entries: list[tuple[str, str, str]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        current = Path(dirpath)
        for name in dirnames + filenames:
            path = current / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries.append((relative, "symlink", os.readlink(path)))
            elif stat.S_ISDIR(mode):
                entries.append((relative, "directory", ""))
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", sha256(path)))
            else:
                entries.append((relative, "special", oct(mode)))
    encoded = "\n".join("\t".join(entry) for entry in entries).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == audit["audit_campaign"]
assert sha256(CAMPAIGN_LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
print("record_layout=pipeline-v3")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_lock_matches_audit_campaign=true")
print(f"audit_campaign_lock_sha256={sha256(CAMPAIGN_LOCK)}")

required_files = {
    "canonical": Path("/reference/canonical.py"),
    "trusted_prompt": Path("/reference/prompt.py"),
    "translator": Path("/reference/py2mpy.py"),
    "run_manifest": Path("/run.json"),
    "task_manifest": Path("/task.json"),
    "stage1_result": Path("/generation-result.json"),
    "generation_manifest": Path("/generation-evidence/invocation.json"),
    "generation_metrics": Path("/generation-evidence/metrics.json"),
    "generation_runtime_metrics": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage": Path("/generation-evidence/usage.json"),
    "generation_last": Path("/generation-evidence/codex-last.txt"),
    "generation_output": Path("/generation-evidence/codex-output.log"),
    "generation_prompt": Path("/generation-evidence/prompt.txt"),
}
for name, path in required_files.items():
    require_regular(path)
    print(f"required_file[{name}]={path} sha256={sha256(path)}")

for path in (
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
):
    require_directory(path)
    print(f"required_directory={path}")

recorded_hashes = {
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, field in recorded_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][field]
    assert actual == expected, f"{path}: expected {expected}, got {actual}"
    print(f"recorded_hash_match[{field}]=true")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("candidate_prompt_byte_identical_to_trusted=true")
print("candidate_translator_byte_identical_to_trusted=true")

trusted_entries, trusted_tree_digest = tree_manifest(Path("/reference/reference-semantics"))
candidate_entries, candidate_tree_digest = tree_manifest(Path("/candidate/reference-semantics"))
assert trusted_entries == candidate_entries
assert not any(kind == "symlink" for _, kind, _ in trusted_entries)
print(f"reference_semantics_entries={len(trusted_entries)}")
print(f"trusted_reference_semantics_independent_manifest_sha256={trusted_tree_digest}")
print(f"candidate_reference_semantics_independent_manifest_sha256={candidate_tree_digest}")
print("reference_semantics_exact_recursive_match=true")
for relative, kind, digest in trusted_entries:
    print(f"reference_entry={kind}\t{relative}\t{digest}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
regular_trace_files = []
for path in trace_files:
    mode = path.lstat().st_mode
    assert not stat.S_ISLNK(mode), f"symlinked trace entry: {path}"
    assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), f"special trace entry: {path}"
    if stat.S_ISREG(mode):
        regular_trace_files.append(path)
        print(f"trace_file={path} sha256={sha256(path)}")
assert regular_trace_files, "structured trace contains no regular files"

stage1_result = json.loads(Path("/generation-result.json").read_text())
for relative, expected in stage1_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"{relative}: expected {expected}, got {actual}"
    print(f"stage1_result_evidence_hash_match[{relative}]=true")

print("STAGE1_INTEGRITY_OK")
