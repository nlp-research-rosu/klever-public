#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required regular file is mistyped: {path}"
    assert not path.is_symlink(), f"required file is symlinked: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_manifest(root: Path):
    entries = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries.append(("symlink", relative, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append(("directory", relative, ""))
        elif stat.S_ISREG(mode):
            entries.append(("file", relative, sha256(path)))
        else:
            entries.append(("other", relative, oct(mode)))
    return entries


def manifest_digest(entries) -> str:
    encoded = json.dumps(
        entries, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

paths = audit["container_paths"]
required_pipeline_files = [
    Path(paths["run_manifest"]),
    Path(paths["task_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path("/generation-evidence/prompt.txt"),
]
for required in [AUDIT, LOCK, *required_pipeline_files]:
    require_regular(required)

required_directories = [
    Path(paths["candidate"]),
    Path(paths["generation_root"]),
    Path(paths["generation_trace"]),
    Path("/reference/reference-semantics"),
]
for required in required_directories:
    mode = required.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required directory is mistyped: {required}"
    assert not required.is_symlink(), f"required directory is symlinked: {required}"

recorded_file_hashes = {
    Path(paths["run_manifest"]): "run_manifest_sha256",
    Path(paths["task_manifest"]): "task_manifest_sha256",
    Path(paths["stage1_result"]): "stage1_result_sha256",
    Path(paths["generation_manifest"]): "stage1_invocation_sha256",
    Path(paths["generation_metrics"]): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"):
        "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path(paths["generation_last"]): "generation_codex_last_sha256",
    Path(paths["generation_output"]): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path(paths["canonical"]): "canonical_sha256",
    Path(paths["trusted_prompt"]): "trusted_prompt_sha256",
    Path(paths["translator"]): "trusted_translator_sha256",
    Path(paths["candidate"]) / "prompt.py": "candidate_prompt_sha256",
    Path(paths["candidate"]) / "py2mpy.py": "candidate_translator_sha256",
}
for path, key in recorded_file_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"hash mismatch for {path}: {actual} != {expected}"
    print(f"HASH OK {path} {actual}")

result = json.loads(Path(paths["stage1_result"]).read_text(encoding="utf-8"))
invocation = json.loads(
    Path(paths["generation_manifest"]).read_text(encoding="utf-8")
)
assert result["outputs"]["evidence"] == invocation["outputs"]["evidence"]
for relative, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path(paths["generation_root"]) / relative
    require_regular(path)
    actual = sha256(path)
    assert actual == expected, f"generation evidence hash mismatch: {path}"
    print(f"RESULT HASH OK {path} {actual}")

trace_files = sorted(Path(paths["generation_trace"]).rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert trace_files, "structured trace has no files"
trace_types = Counter()
trace_payload_types = Counter()
trace_lines = 0
for path in trace_files:
    require_regular(path)
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            trace_types[record.get("type")] += 1
            payload = record.get("payload", {})
            trace_payload_types[payload.get("type")] += 1
print(f"TRACE JSON OK files={len(trace_files)} lines={trace_lines}")
print(f"TRACE TYPES {dict(sorted(trace_types.items()))}")
print(f"TRACE PAYLOAD TYPES {dict(sorted(trace_payload_types.items(), key=str))}")

candidate = Path(paths["candidate"])
for relative in [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
    "prompt.py",
    "py2mpy.py",
]:
    require_regular(candidate / relative)

assert (candidate / "prompt.py").read_bytes() == Path(
    paths["trusted_prompt"]
).read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == Path(
    paths["translator"]
).read_bytes()

trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
candidate_semantics = tree_manifest(candidate / "reference-semantics")
assert trusted_semantics == candidate_semantics
assert all(entry[0] in {"file", "directory"} for entry in candidate_semantics)
print(
    "SEMANTICS TREE OK "
    f"entries={len(candidate_semantics)} "
    f"reviewer_digest={manifest_digest(candidate_semantics)}"
)
for kind, relative, digest in candidate_semantics:
    print(f"SEMANTICS {kind} {relative} {digest}")

all_candidate_entries = tree_manifest(candidate)
assert all(entry[0] != "symlink" for entry in all_candidate_entries)
print(
    "CANDIDATE TREE NO SYMLINKS "
    f"entries={len(all_candidate_entries)} "
    f"reviewer_digest={manifest_digest(all_candidate_entries)}"
)
print("CAMPAIGN LOCK MATCH")
print("PIPELINE-V3 REQUIRED RECORDS OK")
print("STAGE1 INTEGRITY PASS")
