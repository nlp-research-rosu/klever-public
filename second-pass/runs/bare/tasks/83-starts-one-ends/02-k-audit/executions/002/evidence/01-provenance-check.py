#!/usr/bin/env python3
"""Stage-one provenance checks over the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import stat
import sys
from collections import Counter
from pathlib import Path

from reviewer_tree_hash import tree_hash


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except OSError:
        return False


audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
campaign_lock = json.loads(
    Path("/audit-campaign-lock.json").read_text(encoding="utf-8")
)

print("COMMAND: python3 /audit-output/evidence/01-provenance-check.py")
print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
print(
    "campaign_block_equal="
    f"{audit_input['audit_campaign'] == campaign_lock}"
)

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
    Path("/generation-evidence/usage.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
required_directories = [
    Path("/candidate"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
    Path("/reference"),
]

structure_ok = True
for path in required_files:
    ok = regular(path)
    structure_ok &= ok
    print(f"required_file real_regular={ok} readable={path.exists()} path={path}")
for path in required_directories:
    ok = directory(path)
    structure_ok &= ok
    print(f"required_directory real_directory={ok} path={path}")

reference_semantics_absent = not (
    Path("/reference/reference-semantics").exists()
    or Path("/reference/reference-semantics").is_symlink()
)
candidate_reference_semantics_absent = not (
    Path("/candidate/reference-semantics").exists()
    or Path("/candidate/reference-semantics").is_symlink()
)
print(f"trusted_reference_semantics_absent={reference_semantics_absent}")
print(
    "candidate_reference_semantics_absent="
    f"{candidate_reference_semantics_absent}"
)

hash_fields = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_codex_last_sha256": Path(
        "/generation-evidence/codex-last.txt"
    ),
    "generation_codex_output_sha256": Path(
        "/generation-evidence/codex-output.log"
    ),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
}

simple_hashes_ok = True
for field, path in hash_fields.items():
    expected = audit_input["hashes"][field]
    observed = file_hash(path)
    match = expected == observed
    simple_hashes_ok &= match
    print(
        f"file_hash field={field} match={match} "
        f"expected={expected} observed={observed}"
    )

prompt_match = (
    Path("/candidate/prompt.py").read_bytes()
    == Path("/reference/prompt.py").read_bytes()
)
translator_match = (
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes()
)
print(f"candidate_prompt_byte_identity={prompt_match}")
print(f"candidate_translator_byte_identity={translator_match}")

candidate_digest = tree_hash(Path("/candidate"))
trace_digest = tree_hash(Path("/generation-evidence/codex-trace"))
result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
usage = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)

print(
    "candidate_tree "
    f"audit_input={audit_input['hashes']['candidate_tree_sha256']} "
    f"observed={candidate_digest} "
    f"generation_result={result['outputs']['workspace_sha256']} "
    f"invocation_input={invocation['inputs']['workspace_sha256']} "
    f"invocation_output={invocation['outputs']['workspace_sha256']} "
    f"invocation_retained={invocation['retained_workspace_sha256']}"
)
print(
    "trace_tree "
    f"audit_input={audit_input['hashes']['generation_codex_trace_sha256']} "
    f"observed={trace_digest} "
    f"usage_source_trace={usage['source_trace_sha256']}"
)

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*.jsonl"))
invalid_json: list[str] = []
outer_types: Counter[str] = Counter()
line_count = 0
for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            try:
                document = json.loads(line)
                outer_types[str(document.get("type"))] += 1
            except Exception as error:
                invalid_json.append(
                    f"{trace_file}:{line_number}: {type(error).__name__}: {error}"
                )
print(
    f"trace_json files={len(trace_files)} lines={line_count} "
    f"invalid={len(invalid_json)} types={dict(outer_types)}"
)
for error in invalid_json:
    print(f"trace_json_error={error}")

candidate_tree_matches_audit = (
    candidate_digest == audit_input["hashes"]["candidate_tree_sha256"]
)
trace_tree_matches_audit = (
    trace_digest
    == audit_input["hashes"]["generation_codex_trace_sha256"]
)
candidate_tree_matches_generation = (
    candidate_digest == result["outputs"]["workspace_sha256"]
    == invocation["inputs"]["workspace_sha256"]
    == invocation["outputs"]["workspace_sha256"]
    == invocation["retained_workspace_sha256"]
)
trace_tree_matches_usage = trace_digest == usage["source_trace_sha256"]

print(f"candidate_tree_matches_audit_input={candidate_tree_matches_audit}")
print(f"trace_tree_matches_audit_input={trace_tree_matches_audit}")
print(
    "candidate_tree_matches_generation_records="
    f"{candidate_tree_matches_generation}"
)
print(f"trace_tree_matches_usage_record={trace_tree_matches_usage}")

gate_ok = all(
    (
        structure_ok,
        reference_semantics_absent,
        candidate_reference_semantics_absent,
        simple_hashes_ok,
        prompt_match,
        translator_match,
        not invalid_json,
        audit_input["audit_campaign"] == campaign_lock,
        candidate_tree_matches_audit,
        trace_tree_matches_audit,
    )
)
print(f"PROVENANCE_GATE={'PASS' if gate_ok else 'FAIL'}")
sys.exit(0 if gate_ok else 1)
