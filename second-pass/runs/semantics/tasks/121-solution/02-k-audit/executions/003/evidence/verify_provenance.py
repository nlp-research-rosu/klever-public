#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

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
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked required file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def tree_records(root: Path) -> list[tuple[str, str, str | None]]:
    records: list[tuple[str, str, str | None]] = []
    for path in sorted([root, *root.rglob("*")]):
        relative = "." if path == root else path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            kind = "directory"
            value = None
        elif stat.S_ISREG(info.st_mode):
            kind = "file"
            value = sha256(path)
        else:
            kind = f"mode-{stat.S_IFMT(info.st_mode):o}"
            value = None
        records.append((relative, kind, value))
    return records


def record_digest(records: list[tuple[str, str, str | None]]) -> str:
    encoded = json.dumps(
        records, ensure_ascii=False, separators=(",", ":"), sort_keys=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

lock_path = Path(audit["container_paths"]["audit_campaign_lock"])
require_regular(AUDIT_INPUT)
require_regular(lock_path)
lock = json.loads(lock_path.read_text())
print("campaign_block_equals_lock:", audit["audit_campaign"] == lock)
print("campaign_lock_sha256:", sha256(lock_path))
assert audit["audit_campaign"] == lock
assert sha256(lock_path) == audit["hashes"]["audit_campaign_lock_sha256"]

required = {
    "run_manifest": Path("/run.json"),
    "task_manifest": Path("/task.json"),
    "stage1_result": Path("/generation-result.json"),
    "invocation": Path("/generation-evidence/invocation.json"),
    "metrics": Path("/generation-evidence/metrics.json"),
    "usage": Path("/generation-evidence/usage.json"),
    "codex_last": Path("/generation-evidence/codex-last.txt"),
    "codex_output": Path("/generation-evidence/codex-output.log"),
    "prompt": Path("/generation-evidence/prompt.txt"),
    "trace": Path(
        "/generation-evidence/codex-trace/2026/07/23/"
        "rollout-2026-07-23T05-24-27-019f8e81-5130-73c3-84ea-e9a1baf016ad.jsonl"
    ),
    "canonical": Path("/reference/canonical.py"),
    "trusted_prompt": Path("/reference/prompt.py"),
    "translator": Path("/reference/py2mpy.py"),
    "candidate_prompt": Path("/candidate/prompt.py"),
    "candidate_translator": Path("/candidate/py2mpy.py"),
}
for name, path in required.items():
    require_regular(path)
    print(f"{name}: regular readable sha256={sha256(path)} size={path.stat().st_size}")

hash_fields = {
    "run_manifest": "run_manifest_sha256",
    "task_manifest": "task_manifest_sha256",
    "stage1_result": "stage1_result_sha256",
    "invocation": "stage1_invocation_sha256",
    "metrics": "generation_metrics_sha256",
    "usage": "generation_usage_sha256",
    "codex_last": "generation_codex_last_sha256",
    "codex_output": "generation_codex_output_sha256",
    "prompt": "generation_prompt_sha256",
    "canonical": "canonical_sha256",
    "trusted_prompt": "trusted_prompt_sha256",
    "translator": "trusted_translator_sha256",
    "candidate_prompt": "candidate_prompt_sha256",
    "candidate_translator": "candidate_translator_sha256",
}
for path_name, hash_name in hash_fields.items():
    actual = sha256(required[path_name])
    recorded = audit["hashes"][hash_name]
    assert actual == recorded, (path_name, actual, recorded)
print("launcher_recorded_file_hashes: all matched")

for name in ("run_manifest", "task_manifest", "stage1_result", "invocation", "metrics", "usage"):
    json.loads(required[name].read_text())
print("required_json_records: parsed")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
assert trusted_semantics.is_dir() and not trusted_semantics.is_symlink()
assert candidate_semantics.is_dir() and not candidate_semantics.is_symlink()
trusted_records = tree_records(trusted_semantics)
candidate_records = tree_records(candidate_semantics)
print("trusted_semantics_entries:", len(trusted_records))
print("candidate_semantics_entries:", len(candidate_records))
print("semantics_type_name_hash_records_equal:", trusted_records == candidate_records)
print("independent_trusted_semantics_record_sha256:", record_digest(trusted_records))
print("independent_candidate_semantics_record_sha256:", record_digest(candidate_records))
assert trusted_records == candidate_records

candidate_tree_records = tree_records(Path("/candidate"))
print("candidate_tree_entries:", len(candidate_tree_records))
print(
    "independent_candidate_tree_record_sha256:",
    record_digest(candidate_tree_records),
)
assert all(kind != "symlink" for _, kind, _ in candidate_tree_records)

assert required["trusted_prompt"].read_bytes() == required["candidate_prompt"].read_bytes()
assert required["translator"].read_bytes() == required["candidate_translator"].read_bytes()
print("candidate_prompt_equals_trusted: true")
print("candidate_translator_equals_trusted: true")

trace_counts: Counter[tuple[str, str]] = Counter()
trace_lines = 0
with required["trace"].open(encoding="utf-8") as stream:
    for trace_lines, line in enumerate(stream, 1):
        record = json.loads(line)
        top_type = str(record.get("type"))
        payload = record.get("payload")
        payload_type = str(payload.get("type")) if isinstance(payload, dict) else "-"
        trace_counts[(top_type, payload_type)] += 1
print("trace_json_lines_parsed:", trace_lines)
for (top_type, payload_type), count in sorted(trace_counts.items()):
    print(f"trace_type {top_type}/{payload_type}: {count}")

output_text = required["codex_output"].read_text(encoding="utf-8")
print("codex_output_utf8_lines:", len(output_text.splitlines()))
print("codex_output_contains_final_marker:", "RESULT: KPROVE_PASSED" in output_text)
print("provenance_status: PASS")
