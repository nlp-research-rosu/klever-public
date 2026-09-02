#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit records."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GENERATION = Path("/generation-evidence")
CANDIDATE = Path("/candidate")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_sha256(root: Path) -> str:
    """Generation-record digest over relative paths, kinds, sizes, and bytes."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
lock = json.loads(LOCK.read_text())
expected = audit["hashes"]

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_exact_match={audit['audit_campaign'] == lock}")
print(
    "campaign_lock_hash_match="
    f"{sha256(LOCK) == expected['audit_campaign_lock_sha256']}"
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "usage.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
]
for path in required:
    status = (
        path.exists()
        and path.is_file()
        and not path.is_symlink()
        and os.access(path, os.R_OK)
    )
    print(f"required_regular_readable_nonsymlink {path}: {status}")

checks = {
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GENERATION / "invocation.json": "stage1_invocation_sha256",
    GENERATION / "metrics.json": "generation_metrics_sha256",
    GENERATION / "usage.json": "generation_usage_sha256",
    GENERATION / "codex-last.txt": "generation_codex_last_sha256",
    GENERATION / "codex-output.log": "generation_codex_output_sha256",
    GENERATION / "prompt.txt": "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    CANDIDATE / "prompt.py": "candidate_prompt_sha256",
    CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
}
for path, key in checks.items():
    actual = sha256(path)
    print(f"recorded_hash_match {path}: {actual == expected[key]} {actual}")

print(
    "candidate_prompt_byte_identity="
    f"{(CANDIDATE / 'prompt.py').read_bytes() == Path('/reference/prompt.py').read_bytes()}"
)
print(
    "candidate_translator_byte_identity="
    f"{(CANDIDATE / 'py2mpy.py').read_bytes() == Path('/reference/py2mpy.py').read_bytes()}"
)
print(
    "generated_semantics_boundary_reference_tree_absent="
    f"{not Path('/reference/reference-semantics').exists()}"
)

bad_candidate_entries: list[str] = []
for path in sorted(CANDIDATE.rglob("*")):
    if path.is_symlink() or not (path.is_dir() or path.is_file()):
        bad_candidate_entries.append(str(path))
print(f"candidate_symlink_or_mistyped_entries={bad_candidate_entries}")
for path in sorted(CANDIDATE.rglob("*")):
    if path.is_file():
        print(f"candidate_file_sha256 {path.relative_to(CANDIDATE)} {sha256(path)}")

invocation = json.loads((GENERATION / "invocation.json").read_text())
for relative, wanted in sorted(invocation["outputs"]["evidence"].items()):
    path = GENERATION / relative
    ok = (
        path.exists()
        and path.is_file()
        and not path.is_symlink()
        and sha256(path) == wanted
    )
    print(f"invocation_evidence_hash_match {relative}: {ok}")
candidate_pipeline_tree_hash = pipeline_tree_sha256(CANDIDATE)
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_tree_hash}")
print(
    "candidate_tree_matches_retained_generation_workspace="
    f"{candidate_pipeline_tree_hash == invocation['retained_workspace_sha256']}"
)

trace_files = sorted((GENERATION / "codex-trace").rglob("*.jsonl"))
trace_records = []
parse_errors = []
for path in trace_files:
    for line_number, line in enumerate(path.open(), 1):
        try:
            trace_records.append(json.loads(line))
        except Exception as err:  # pragma: no cover - retained as audit evidence
            parse_errors.append(f"{path}:{line_number}: {err}")
print(f"trace_files={[str(path) for path in trace_files]}")
print(f"trace_record_count={len(trace_records)}")
print(f"trace_parse_errors={parse_errors}")
print(f"trace_top_level_types={dict(Counter(row.get('type') for row in trace_records))}")
print(
    "trace_payload_types="
    f"{dict(Counter((row.get('payload') or {}).get('type') for row in trace_records if isinstance(row.get('payload'), dict)))}"
)
usage = json.loads((GENERATION / "usage.json").read_text())
trace_pipeline_tree_hash = pipeline_tree_sha256(GENERATION / "codex-trace")
print(f"trace_pipeline_tree_sha256={trace_pipeline_tree_hash}")
print(
    "trace_tree_matches_usage_source_trace="
    f"{trace_pipeline_tree_hash == usage['source_trace_sha256']}"
)
