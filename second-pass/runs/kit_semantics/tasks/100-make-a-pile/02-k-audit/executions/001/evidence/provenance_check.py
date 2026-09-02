#!/usr/bin/env python3
"""Independent read-only provenance and supplied-semantics integrity checks."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import stat


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")
TRACE = GENERATION / "codex-trace/2026/07/25/rollout-2026-07-25T01-33-50-019f97fa-e51b-7f40-8ec8-a44ec18d3c23.jsonl"


def file_sha(path: Path) -> str:
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"


def tree_records(root: Path):
    records = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            records.append(("symlink", rel, info.st_mode & 0o7777, path.readlink().as_posix()))
        elif stat.S_ISDIR(info.st_mode):
            records.append(("dir", rel, info.st_mode & 0o7777, ""))
        elif stat.S_ISREG(info.st_mode):
            records.append(("file", rel, info.st_mode & 0o7777, file_sha(path)))
        else:
            records.append(("other", rel, info.st_mode & 0o7777, ""))
    return records


def tree_digest(records) -> str:
    h = sha256()
    for record in records:
        h.update(("\0".join(map(str, record)) + "\n").encode())
    return h.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the pipeline-v3 content-tree digest from mounted bytes."""
    h = sha256()
    entries = []
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            entries.append((rel, "directory", path))
        elif stat.S_ISREG(info.st_mode):
            entries.append((rel, "file", path))
        else:
            raise AssertionError(f"unsupported or linked entry: {path}")
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            h.update(path.stat().st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
    return h.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(CAMPAIGN_LOCK.read_text())

assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
assert file_sha(CAMPAIGN_LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]
assert (REFERENCE / "reference-semantics").is_dir()

required_files = [
    AUDIT_INPUT,
    CAMPAIGN_LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "runtime-metrics.json",
    GENERATION / "usage.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    TRACE,
    REFERENCE / "canonical.py",
    REFERENCE / "prompt.py",
    REFERENCE / "py2mpy.py",
]
for path in required_files:
    require_regular(path)

declared_hashes = {
    CAMPAIGN_LOCK: "audit_campaign_lock_sha256",
    REFERENCE / "canonical.py": "canonical_sha256",
    REFERENCE / "prompt.py": "trusted_prompt_sha256",
    REFERENCE / "py2mpy.py": "trusted_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
}
for path, key in declared_hashes.items():
    actual = file_sha(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{key}: {actual} != {expected}"

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GENERATION / "invocation.json").read_text())
for record in (result, invocation):
    evidence_hashes = record["outputs"]["evidence"]
    for rel, expected in evidence_hashes.items():
        path = GENERATION / rel
        require_regular(path)
        assert file_sha(path) == expected, f"generation evidence mismatch: {rel}"

assert (CANDIDATE / "prompt.py").read_bytes() == (REFERENCE / "prompt.py").read_bytes()
assert (CANDIDATE / "py2mpy.py").read_bytes() == (REFERENCE / "py2mpy.py").read_bytes()

trusted_semantics_records = tree_records(REFERENCE / "reference-semantics")
candidate_semantics_records = tree_records(CANDIDATE / "reference-semantics")
assert trusted_semantics_records == candidate_semantics_records
assert all(record[0] != "symlink" for record in trusted_semantics_records)

required_candidate = [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]
for rel in required_candidate:
    path = CANDIDATE / rel
    require_regular(path)
    assert path.stat().st_size > 0

trace_counts = Counter()
trace_payload_types = Counter()
trace_function_names = Counter()
with TRACE.open() as stream:
    for line_no, line in enumerate(stream, 1):
        event = json.loads(line)
        trace_counts[event["type"]] += 1
        payload = event.get("payload", {})
        if isinstance(payload, dict):
            trace_payload_types[payload.get("type", "<none>")] += 1
            if payload.get("type") == "function_call":
                trace_function_names[payload.get("name", "<none>")] += 1
assert line_no == 386

candidate_records = tree_records(CANDIDATE)
assert all(record[0] in {"dir", "file"} for record in candidate_records)

task = json.loads(Path("/task.json").read_text())
usage = json.loads((GENERATION / "usage.json").read_text())
candidate_pipeline_digest = pipeline_tree_digest(CANDIDATE)
semantics_pipeline_digest = pipeline_tree_digest(REFERENCE / "reference-semantics")
trace_pipeline_digest = pipeline_tree_digest(GENERATION / "codex-trace")
assert candidate_pipeline_digest == result["outputs"]["workspace_sha256"]
assert semantics_pipeline_digest == task["inputs"]["reference_semantics_sha256"]
assert trace_pipeline_digest == usage["source_trace_sha256"]

print("record_layout=pipeline-v3")
print("semantics_mode=SUPPLIED_SEMANTICS")
print("campaign_lock_exact_match=true")
print(f"required_regular_files={len(required_files)}")
print("all_declared_file_hashes_match=true")
print("generation_result_evidence_hashes_match=true")
print("generation_invocation_evidence_hashes_match=true")
print("candidate_prompt_matches_trusted=true")
print("candidate_translator_matches_trusted=true")
print("candidate_reference_semantics_exact_recursive_match=true")
print(f"reference_semantics_entries={len(trusted_semantics_records)}")
print(f"reference_semantics_review_tree_digest={tree_digest(trusted_semantics_records)}")
print(f"candidate_entries={len(candidate_records)}")
print(f"candidate_review_tree_digest={tree_digest(candidate_records)}")
print(f"candidate_pipeline_tree_digest={candidate_pipeline_digest}")
print(f"semantics_pipeline_tree_digest={semantics_pipeline_digest}")
print(f"trace_pipeline_tree_digest={trace_pipeline_digest}")
print("pipeline_tree_hashes_match_records=true")
print(f"trace_json_lines={line_no}")
print(f"trace_top_level_types={dict(sorted(trace_counts.items()))}")
print(f"trace_payload_types={dict(sorted(trace_payload_types.items()))}")
print(f"trace_function_calls={dict(sorted(trace_function_names.items()))}")
print("PROVENANCE_CHECK=PASS")
