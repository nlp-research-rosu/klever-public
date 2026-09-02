#!/usr/bin/env python3
"""Independent Stage 1 integrity checks for the 27-flip-case audit."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace/2026/07/22/rollout-2026-07-22T22-33-34-019f8d09-24be-79c2-bbb6-2da14d9aa7d4.jsonl"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_snapshot(root: Path) -> dict[str, tuple[str, str | None]]:
    snapshot: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(dirpath)
        names = sorted(dirnames + filenames)
        for name in names:
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                snapshot[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                snapshot[rel] = ("directory", None)
            elif path.is_file():
                snapshot[rel] = ("file", sha256(path))
            else:
                snapshot[rel] = ("other", None)
    return snapshot


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_exact_match={audit['audit_campaign'] == lock}")
print(
    "campaign_lock_hash="
    f"{sha256(LOCK)} expected={audit['hashes']['audit_campaign_lock_sha256']}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
    TRACE,
]
if (GEN / "usage.json").exists():
    required.append(GEN / "usage.json")

print("required_records:")
for path in required:
    print(
        f"  {path}: exists={path.exists()} readable={os.access(path, os.R_OK)} "
        f"symlink={path.is_symlink()} sha256={sha256(path) if path.is_file() else '-'}"
    )

recorded_files = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GEN / "invocation.json": "stage1_invocation_sha256",
    GEN / "metrics.json": "generation_metrics_sha256",
    GEN / "usage.json": "generation_usage_sha256",
    GEN / "codex-last.txt": "generation_codex_last_sha256",
    GEN / "codex-output.log": "generation_codex_output_sha256",
    GEN / "prompt.txt": "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
print("recorded_hash_checks:")
for path, key in recorded_files.items():
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"  {key}: match={actual == expected} actual={actual}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GEN / "invocation.json").read_text())
for record_name, record in [("generation-result", result), ("invocation", invocation)]:
    print(f"{record_name}_evidence_hash_checks:")
    for rel, expected in sorted(record["outputs"]["evidence"].items()):
        path = GEN / rel
        actual = sha256(path)
        print(f"  {rel}: match={actual == expected} actual={actual}")

trusted_semantics = tree_snapshot(Path("/reference/reference-semantics"))
candidate_semantics = tree_snapshot(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"semantics_snapshots_exact_match={trusted_semantics == candidate_semantics}")
print(
    "semantics_symlinks="
    f"{[p for p, value in candidate_semantics.items() if value[0] == 'symlink']}"
)
for rel in sorted(set(trusted_semantics) | set(candidate_semantics)):
    if trusted_semantics.get(rel) != candidate_semantics.get(rel):
        print(
            f"  SEMANTICS_MISMATCH {rel}: "
            f"trusted={trusted_semantics.get(rel)} "
            f"candidate={candidate_semantics.get(rel)}"
        )

print(
    "prompt_byte_identity="
    f"{Path('/reference/prompt.py').read_bytes() == Path('/candidate/prompt.py').read_bytes()}"
)
print(
    "translator_byte_identity="
    f"{Path('/reference/py2mpy.py').read_bytes() == Path('/candidate/py2mpy.py').read_bytes()}"
)

trace_types: Counter[str] = Counter()
trace_records = []
with TRACE.open() as stream:
    for lineno, line in enumerate(stream, 1):
        record = json.loads(line)
        trace_records.append(record)
        trace_types[str(record.get("type", "<none>"))] += 1
print(f"trace_jsonl_records={len(trace_records)}")
print(f"trace_type_counts={dict(sorted(trace_types.items()))}")
selected = json.loads((GEN / "usage.json").read_text())["selected_event"]["line_number"]
print(f"usage_selected_line={selected} exists={1 <= selected <= len(trace_records)}")

output_text = (GEN / "codex-output.log").read_text(errors="replace")
print(
    "codex_output_full_read="
    f"bytes={len(output_text.encode())} lines={len(output_text.splitlines())} "
    f"top_count={output_text.count('#Top')} "
    f"kprove_count={output_text.count('kprove')} "
    f"warning_count={output_text.lower().count('warning')}"
)
print("candidate_file_manifest:")
for rel, (kind, value) in tree_snapshot(Path("/candidate")).items():
    print(f"  {kind} {rel} {value or ''}")
