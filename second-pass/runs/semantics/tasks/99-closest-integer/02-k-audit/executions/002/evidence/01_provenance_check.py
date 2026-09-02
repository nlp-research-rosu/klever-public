#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlink not permitted: {path}"


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    result: list[tuple[str, str, str]] = []
    for base, directories, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in sorted(directories + files):
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode):
                result.append(("symlink", rel, os.readlink(path)))
            elif stat.S_ISDIR(info.st_mode):
                result.append(("directory", rel, ""))
            elif stat.S_ISREG(info.st_mode):
                result.append(("file", rel, sha256(path)))
            else:
                result.append(("other", rel, oct(info.st_mode)))
    return sorted(result)


def manifest_digest(entries: list[tuple[str, str, str]]) -> str:
    serialized = json.dumps(entries, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


data = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())

print(f"record_layout={data['record_layout']}")
print(f"semantics_mode={data['semantics_mode']}")
assert data["record_layout"] == "legacy-selected-stage1"
assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert lock == data["audit_campaign"], "campaign lock differs from audit campaign block"
assert sha256(LOCK) == data["hashes"]["audit_campaign_lock_sha256"]
print("campaign_lock_match=true")
print(f"audit_campaign_lock_sha256={sha256(LOCK)}")

required = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/usage.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
required += sorted(Path("/generation-evidence/codex-trace").rglob("*"))
required += [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/spec.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/prove.sh"),
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
]
for path in required:
    if path.is_dir():
        assert not path.is_symlink(), f"symlinked directory: {path}"
    else:
        require_regular(path)
print(f"required_artifact_count={len(required)}")
print("required_artifacts_regular_and_readable=true")

expected_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
for name, field in expected_hashes.items():
    actual = sha256(Path(name))
    expected = data["hashes"][field]
    print(f"hash {name} {actual} expected={expected} match={actual == expected}")
    assert actual == expected

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert trace_files, "structured trace is empty"
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
declared_trace = {
    key: value
    for key, value in invocation["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
assert len(trace_files) == len(declared_trace)
event_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
call_names: Counter[str] = Counter()
line_count = 0
for trace in trace_files:
    relative = "codex-trace/" + trace.relative_to(
        "/generation-evidence/codex-trace"
    ).as_posix()
    actual = sha256(trace)
    assert declared_trace[relative] == actual
    with trace.open() as stream:
        for line in stream:
            event = json.loads(line)
            line_count += 1
            event_counts[event.get("type", "<missing>")] += 1
            payload = event.get("payload", {})
            if isinstance(payload, dict):
                payload_counts[payload.get("type", "<missing>")] += 1
                if (
                    event.get("type") == "response_item"
                    and payload.get("type") == "function_call"
                ):
                    call_names[payload.get("name", "<missing>")] += 1
print(f"trace_file_count={len(trace_files)}")
print(f"trace_line_count={line_count}")
print(f"trace_event_types={dict(sorted(event_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_counts.items()))}")
print(f"trace_function_calls={dict(sorted(call_names.items()))}")

trusted = tree_manifest(Path("/reference/reference-semantics"))
candidate = tree_manifest(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_entry_count={len(trusted)}")
print(f"candidate_semantics_entry_count={len(candidate)}")
print(f"trusted_semantics_manifest_digest={manifest_digest(trusted)}")
print(f"candidate_semantics_manifest_digest={manifest_digest(candidate)}")
assert all(kind in {"file", "directory"} for kind, _, _ in trusted)
assert all(kind in {"file", "directory"} for kind, _, _ in candidate)
assert trusted == candidate, "candidate supplied-semantics tree differs from trusted tree"
print("reference_semantics_recursive_identity=true")

assert sha256(Path("/candidate/prompt.py")) == sha256(Path("/reference/prompt.py"))
assert sha256(Path("/candidate/py2mpy.py")) == sha256(Path("/reference/py2mpy.py"))
print("candidate_prompt_identity=true")
print("candidate_translator_identity=true")

candidate_tree = tree_manifest(Path("/candidate"))
print(f"candidate_tree_entry_count={len(candidate_tree)}")
print(f"candidate_tree_reviewer_manifest_digest={manifest_digest(candidate_tree)}")
print(
    "candidate_tree_launcher_digest="
    + data["hashes"]["candidate_tree_sha256"]
    + " (launcher algorithm is not declared; recorded without equating algorithms)"
)
for kind, relative, digest in candidate_tree:
    if kind == "file":
        print(f"candidate_file_sha256 {relative} {digest}")

usage = json.loads(Path("/generation-evidence/usage.json").read_text())
retained_trace_sha = sha256(trace_files[0]) if len(trace_files) == 1 else "<tree>"
print(f"usage_claimed_source_trace_sha256={usage.get('source_trace_sha256')}")
print(f"retained_trace_file_sha256={retained_trace_sha}")
print(
    "usage_source_trace_claim_matches_retained="
    + str(usage.get("source_trace_sha256") == retained_trace_sha).lower()
)
print("PROVENANCE_CHECK=PASS")
