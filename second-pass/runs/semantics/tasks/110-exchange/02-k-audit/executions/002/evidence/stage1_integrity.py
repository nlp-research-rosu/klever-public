#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
EVIDENCE = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_records(root: Path):
    records = {}
    for path in sorted([root, *root.rglob("*")]):
        relative = "." if path == root else path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind = "symlink"
            payload = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            kind = "directory"
            payload = ""
        elif stat.S_ISREG(info.st_mode):
            kind = "file"
            payload = sha256(path)
        else:
            kind = f"other:{stat.S_IFMT(info.st_mode):o}"
            payload = ""
        records[relative] = (kind, stat.S_IMODE(info.st_mode), payload)
    return records


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert sha256(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    EVIDENCE / "invocation.json",
    EVIDENCE / "metrics.json",
    EVIDENCE / "codex-last.txt",
    EVIDENCE / "codex-output.log",
    EVIDENCE / "prompt.txt",
    REFERENCE / "canonical.py",
    REFERENCE / "prompt.py",
    REFERENCE / "py2mpy.py",
]
for path in required:
    require_regular(path)

trace_root = EVIDENCE / "codex-trace"
trace_files = sorted(trace_root.rglob("*"))
assert trace_files, "structured trace is absent"
assert all(not path.is_symlink() for path in [trace_root, *trace_files])
trace_jsonl = [path for path in trace_files if path.is_file()]
assert trace_jsonl
trace_records = 0
for path in trace_jsonl:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            trace_records += 1

expected_hashes = {
    LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    EVIDENCE / "invocation.json": "stage1_invocation_sha256",
    EVIDENCE / "metrics.json": "generation_metrics_sha256",
    EVIDENCE / "codex-last.txt": "generation_codex_last_sha256",
    EVIDENCE / "codex-output.log": "generation_codex_output_sha256",
    EVIDENCE / "prompt.txt": "generation_prompt_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
}
if (EVIDENCE / "usage.json").exists():
    require_regular(EVIDENCE / "usage.json")
    expected_hashes[EVIDENCE / "usage.json"] = "generation_usage_sha256"

for path, key in expected_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{key}: expected {expected}, got {actual}"
    print(f"HASH_OK {key} {actual} {path}")

assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
trusted_records = tree_records(trusted_semantics)
candidate_records = tree_records(candidate_semantics)
assert candidate_records == trusted_records, "candidate supplied-semantics tree differs"
assert all(kind != "symlink" for kind, _, _ in trusted_records.values())

manifest = "\n".join(
    f"{relative}\t{kind}\t{mode:o}\t{payload}"
    for relative, (kind, mode, payload) in trusted_records.items()
)
manifest_sha = hashlib.sha256(manifest.encode()).hexdigest()

for artifact in ["solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"]:
    require_regular(CANDIDATE / artifact)

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((EVIDENCE / "invocation.json").read_text())
for relative, expected in generation_result["outputs"]["evidence"].items():
    mounted = EVIDENCE / relative
    require_regular(mounted)
    assert sha256(mounted) == expected, f"generation-result evidence mismatch: {relative}"
for relative, expected in invocation["outputs"]["evidence"].items():
    mounted = EVIDENCE / relative
    require_regular(mounted)
    assert sha256(mounted) == expected, f"invocation evidence mismatch: {relative}"

print(f"CAMPAIGN_EQUAL True lock_sha256={sha256(LOCK)}")
print(f"TRACE_JSON_FILES {len(trace_jsonl)} TRACE_RECORDS {trace_records}")
print(f"SEMANTICS_ENTRIES {len(trusted_records)} INDEPENDENT_MANIFEST_SHA256 {manifest_sha}")
print("SUPPLIED_SEMANTICS_RECURSIVE_IDENTITY True")
print("REQUIRED_CANDIDATE_ARTIFACTS_PRESENT True")
print("STAGE1_INTEGRITY PASS")
