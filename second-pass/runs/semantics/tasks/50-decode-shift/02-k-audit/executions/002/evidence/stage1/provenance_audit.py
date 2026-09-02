#!/usr/bin/env python3
"""Independently validate mounted audit records and consume the full trace."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def real_file(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode) and not path.is_symlink()


def real_dir(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISDIR(mode) and not path.is_symlink()


def tree_manifest(root: Path) -> list[tuple[str, str, str]]:
    records: list[tuple[str, str, str]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                records.append(("directory", rel, ""))
                pending.append(path)
            elif stat.S_ISREG(mode):
                records.append(("file", rel, sha256(path)))
            elif stat.S_ISLNK(mode):
                records.append(("symlink", rel, os.readlink(path)))
            else:
                records.append((f"special:{stat.S_IFMT(mode):o}", rel, ""))
    return sorted(records)


def manifest_digest(records: list[tuple[str, str, str]]) -> str:
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

required_files = [
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
required_dirs = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference/reference-semantics"),
]

for path in required_files:
    assert real_file(path), f"required regular file missing/mistyped/linked: {path}"
for path in required_dirs:
    assert real_dir(path), f"required real directory missing/mistyped/linked: {path}"

campaign = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
assert campaign == audit["audit_campaign"]

hash_pairs = {
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
for raw_path, key in hash_pairs.items():
    path = Path(raw_path)
    assert real_file(path), f"recorded input is not a real file: {path}"
    observed = sha256(path)
    expected = audit["hashes"][key]
    assert observed == expected, f"hash mismatch {path}: {observed} != {expected}"

generation_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
declared_evidence = generation_result["outputs"]["evidence"]
for relative, expected in sorted(declared_evidence.items()):
    path = Path("/generation-evidence") / relative
    assert real_file(path), f"generation-result evidence missing/mistyped: {path}"
    observed = sha256(path)
    assert observed == expected, f"generation-result hash mismatch {path}"

parsed_json_records = {}
for path in [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    *sorted(Path("/generation-evidence").glob("*.json")),
]:
    parsed_json_records[str(path)] = json.loads(path.read_text(encoding="utf-8"))

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()

candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
assert candidate_semantics == trusted_semantics
assert all(kind in {"file", "directory"} for kind, _, _ in candidate_semantics)

# Consume and validate every structured trace line, rather than trusting its claims.
event_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
assert trace_regular
trace_manifest = tree_manifest(Path("/generation-evidence/codex-trace"))
assert all(kind in {"file", "directory"} for kind, _, _ in trace_manifest)
trace_lines = 0
for path in trace_regular:
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            item = json.loads(line)
            assert isinstance(item, dict), (path, number)
            event_counts[str(item.get("type"))] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_counts[str(payload.get("type"))] += 1
            trace_lines += 1

# Consume all bytes of the two large prose/log records.
log_sizes = {}
for path in (
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/codex-last.txt"),
):
    data = path.read_bytes()
    log_sizes[str(path)] = len(data)

print("layout=legacy-selected-stage1")
print("semantics_mode=SUPPLIED_SEMANTICS")
print(f"campaign_lock_match=true sha256={sha256(Path('/audit-campaign-lock.json'))}")
print(f"required_files={len(required_files)} required_dirs={len(required_dirs)}")
print(f"recorded_file_hashes_verified={len(hash_pairs)}")
print(f"generation_result_output_hashes_verified={len(declared_evidence)}")
print(f"json_records_parsed={len(parsed_json_records)}")
print(
    "semantics_tree_equal=true "
    f"entries={len(candidate_semantics)} "
    f"independent_manifest_sha256={manifest_digest(candidate_semantics)}"
)
print(
    "candidate_tree "
    f"entries={len(tree_manifest(Path('/candidate')))} "
    f"independent_manifest_sha256={manifest_digest(tree_manifest(Path('/candidate')))}"
)
print(
    "trace_tree "
    f"files={len(trace_regular)} lines={trace_lines} "
    f"independent_manifest_sha256={manifest_digest(trace_manifest)}"
)
print(f"trace_event_counts={json.dumps(event_counts, sort_keys=True)}")
print(f"trace_payload_counts={json.dumps(payload_counts, sort_keys=True)}")
print(f"fully_consumed_log_sizes={json.dumps(log_sizes, sort_keys=True)}")
print("prompt_byte_identity=true translator_byte_identity=true")
print("PROVENANCE_AUDIT_OK")
