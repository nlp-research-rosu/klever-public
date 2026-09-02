#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equals_lock={audit['audit_campaign'] == lock}")

expected_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
]
if (GEN / "usage.json").exists():
    expected_records.append(GEN / "usage.json")

print("required_records:")
for path in expected_records:
    print(
        f"  {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
        f"symlink={path.is_symlink()} sha256={sha256(path) if path.is_file() else '-'}"
    )

declared_hash_paths = {
    "audit_campaign_lock_sha256": LOCK,
    "candidate_prompt_sha256": CANDIDATE / "prompt.py",
    "candidate_translator_sha256": CANDIDATE / "py2mpy.py",
    "canonical_sha256": REFERENCE / "canonical.py",
    "generation_codex_last_sha256": GEN / "codex-last.txt",
    "generation_codex_output_sha256": GEN / "codex-output.log",
    "generation_metrics_sha256": GEN / "metrics.json",
    "generation_prompt_sha256": GEN / "prompt.txt",
    "generation_usage_sha256": GEN / "usage.json",
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": GEN / "invocation.json",
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
    "trusted_prompt_sha256": REFERENCE / "prompt.py",
    "trusted_translator_sha256": REFERENCE / "py2mpy.py",
}
print("declared_hash_checks:")
all_hashes_match = True
for key, path in declared_hash_paths.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    match = actual == expected
    all_hashes_match &= match
    print(f"  {key}: match={match} actual={actual} expected={expected}")
print(f"all_declared_file_hashes_match={all_hashes_match}")

print(
    "candidate_prompt_byte_identical="
    f"{(CANDIDATE / 'prompt.py').read_bytes() == (REFERENCE / 'prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_identical="
    f"{(CANDIDATE / 'py2mpy.py').read_bytes() == (REFERENCE / 'py2mpy.py').read_bytes()}"
)
print(
    "generated_semantics_boundary_ok="
    f"{not (REFERENCE / 'reference-semantics').exists()}"
)

print("candidate_entries:")
for path in sorted(CANDIDATE.rglob("*")):
    kind = "symlink" if path.is_symlink() else ("dir" if path.is_dir() else "file")
    digest = sha256(path) if path.is_file() and not path.is_symlink() else "-"
    print(f"  {path.relative_to(CANDIDATE)} kind={kind} sha256={digest}")

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GEN / "invocation.json").read_text())
declared_evidence = generation_result["outputs"]["evidence"]
print("generation_result_evidence_hash_checks:")
for rel, expected in sorted(declared_evidence.items()):
    path = GEN / rel
    actual = sha256(path)
    print(f"  {rel}: match={actual == expected} actual={actual} expected={expected}")
print(
    "generation_result_equals_invocation_evidence_map="
    f"{declared_evidence == invocation['outputs']['evidence']}"
)

trace_files = sorted((GEN / "codex-trace").rglob("*"))
trace_files = [p for p in trace_files if p.is_file()]
print(f"trace_file_count={len(trace_files)}")
outer_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
roles: Counter[str] = Counter()
trace_lines = 0
for path in trace_files:
    print(f"trace_file={path.relative_to(GEN)} sha256={sha256(path)}")
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            trace_lines += 1
            outer_types[str(item.get("type"))] += 1
            payload = item.get("payload", {})
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
print(f"trace_json_lines={trace_lines}")
print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_message_roles={dict(sorted(roles.items()))}")

output_text = (GEN / "codex-output.log").read_text(errors="strict")
print(f"codex_output_utf8_chars={len(output_text)}")
print(f"codex_output_lines={len(output_text.splitlines())}")
for needle in ("kprove", "#Top", "Randomized Python testing", "RESULT: KPROVE_PASSED"):
    print(f"codex_output_count[{needle!r}]={output_text.count(needle)}")
