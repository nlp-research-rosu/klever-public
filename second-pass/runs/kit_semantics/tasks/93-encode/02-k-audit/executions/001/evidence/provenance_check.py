#!/usr/bin/env python3
"""Independent mounted-input integrity and generation-record inspection."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), f"not a regular file: {path}"


def tree_entries(root: Path) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            entries.append(("symlink", relative, os.readlink(path)))
        elif stat.S_ISDIR(info.st_mode):
            entries.append(("directory", relative, ""))
        elif stat.S_ISREG(info.st_mode):
            entries.append(("file", relative, sha256_file(path)))
        else:
            entries.append(("other", relative, oct(info.st_mode)))
    return entries


def manifest_digest(entries: list[tuple[str, str, str]]) -> str:
    """Reviewer-defined digest of canonical JSON entry records."""
    payload = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


with AUDIT_INPUT.open() as stream:
    audit = json.load(stream)

assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

with Path(audit["container_paths"]["audit_campaign_lock"]).open() as stream:
    campaign_lock = json.load(stream)
assert audit["audit_campaign"] == campaign_lock

hashes = audit["hashes"]
checks = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
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

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print("campaign_lock_exact_match=True")
for path, key in checks.items():
    require_regular(path)
    actual = sha256_file(path)
    expected = hashes[key]
    print(f"{path}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

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
    require_regular(path)

for path in [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]:
    with path.open() as stream:
        record = json.load(stream)
    print(
        f"record:{path}: schema={record.get('schema_version')} "
        f"status={record.get('status')} problem_id={record.get('problem_id')} "
        f"condition={record.get('condition')} exit_code={record.get('exit_code')}"
    )

with Path("/run.json").open() as stream:
    run_record = json.load(stream)
assert "93-encode" in run_record["tasks"]
print(
    "run_record: "
    f"config={run_record['config']} model={run_record['model']} "
    f"k_version={run_record['runtime']['k_version']} contains_task_93=True"
)
with Path("/task.json").open() as stream:
    task_record = json.load(stream)
assert task_record["problem_id"] == "93-encode"
print(f"task_record: current_stage={task_record['current_stage']}")
with Path("/generation-evidence/usage.json").open() as stream:
    usage_record = json.load(stream)
print(
    "usage_record: "
    f"status={usage_record['status']} selected_event={usage_record['selected_event']} "
    f"total_tokens={usage_record['cumulative']['total_tokens']}"
)

generation_last = Path("/generation-evidence/codex-last.txt").read_text(encoding="utf-8")
generation_output = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
print(f"codex_last_lines={len(generation_last.splitlines())}")
print(f"codex_output_lines={len(generation_output.splitlines())}")
print(f"codex_output_top_marker_count={generation_output.splitlines().count('#Top')}")
print(f"codex_output_has_final_result_marker={'RESULT: KPROVE_PASSED' in generation_output}")

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
assert all(kind != "symlink" for kind, _, _ in candidate_semantics)
assert all(kind != "symlink" for kind, _, _ in trusted_semantics)
assert candidate_semantics == trusted_semantics
print(f"reference_semantics_entries={len(trusted_semantics)}")
print(f"reference_semantics_exact_recursive_match={candidate_semantics == trusted_semantics}")
print(f"reviewer_reference_semantics_manifest_sha256={manifest_digest(trusted_semantics)}")
for kind, relative, digest in trusted_semantics:
    print(f"reference-semantics/{relative}\t{kind}\t{digest}")

assert sha256_file(Path("/candidate/prompt.py")) == sha256_file(Path("/reference/prompt.py"))
assert sha256_file(Path("/candidate/py2mpy.py")) == sha256_file(Path("/reference/py2mpy.py"))
print("candidate_prompt_matches_trusted=True")
print("candidate_translator_matches_trusted=True")

for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
    links = [entry for entry in tree_entries(root) if entry[0] == "symlink"]
    print(f"{root}: symlink_count={len(links)}")
    assert not links

with Path("/generation-result.json").open() as stream:
    generation_result = json.load(stream)
recorded_evidence = generation_result["outputs"]["evidence"]
for relative, expected in sorted(recorded_evidence.items()):
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256_file(path)
    print(f"generation-result:{relative}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
assert trace_files
line_count = 0
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
for path in trace_files:
    require_regular(path)
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            event = json.loads(line)
            line_count += 1
            top_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
    print(f"trace_file={path.relative_to(trace_root)} sha256={sha256_file(path)}")

print(f"trace_json_lines={line_count}")
print(f"trace_top_types={dict(sorted(top_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print("PROVENANCE_CHECK=PASS")
