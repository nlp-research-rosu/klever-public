#!/usr/bin/env python3
"""Independent read-only provenance and mount-integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the recorded pipeline workspace/source-trace tree digest."""
    h = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
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
                raise RuntimeError(f"unsupported tree node: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            h.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            h.update(path.read_bytes())
    return h.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print("record_layout:", audit["record_layout"])
print("semantics_mode:", audit["semantics_mode"])
print("campaign_block_matches_lock:", audit["audit_campaign"] == lock)
print(
    "campaign_lock_hash:",
    digest(Path("/audit-campaign-lock.json")),
    "expected:",
    audit["hashes"]["audit_campaign_lock_sha256"],
)

required = [
    "/audit-input.json",
    "/audit-campaign-lock.json",
    "/run.json",
    "/task.json",
    "/generation-result.json",
    "/generation-evidence/invocation.json",
    "/generation-evidence/metrics.json",
    "/generation-evidence/usage.json",
    "/generation-evidence/codex-last.txt",
    "/generation-evidence/codex-output.log",
    "/generation-evidence/prompt.txt",
    "/generation-evidence/codex-trace",
    "/reference/canonical.py",
    "/reference/prompt.py",
    "/reference/py2mpy.py",
    "/candidate",
]
for name in required:
    path = Path(name)
    exists = path.exists()
    symlink = path.is_symlink()
    readable = os.access(path, os.R_OK)
    print(f"required {name}: exists={exists} readable={readable} symlink={symlink}")

checks = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
}
for name, key in checks.items():
    actual = digest(Path(name))
    expected = audit["hashes"][key]
    print(f"hash {name}: {actual} expected={expected} match={actual == expected}")

print(
    "candidate_prompt_byte_identity:",
    Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
)
print(
    "candidate_translator_byte_identity:",
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes(),
)
print(
    "reference_semantics_exists:",
    Path("/reference/reference-semantics").exists()
    or Path("/reference/reference-semantics").is_symlink(),
)
generation_result = json.loads(Path("/generation-result.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
candidate_pipeline_digest = pipeline_tree_digest(Path("/candidate"))
trace_pipeline_digest = pipeline_tree_digest(Path("/generation-evidence/codex-trace"))
print(
    "candidate_pipeline_tree_digest:",
    candidate_pipeline_digest,
    "expected_workspace:",
    generation_result["outputs"]["workspace_sha256"],
    "match:",
    candidate_pipeline_digest == generation_result["outputs"]["workspace_sha256"],
)
print(
    "trace_pipeline_tree_digest:",
    trace_pipeline_digest,
    "expected_source_trace:",
    usage["source_trace_sha256"],
    "match:",
    trace_pipeline_digest == usage["source_trace_sha256"],
)

trace_manifest = json.loads(Path("/generation-result.json").read_text())["outputs"][
    "evidence"
]
for rel, expected in sorted(trace_manifest.items()):
    path = Path("/generation-evidence") / rel
    actual = digest(path)
    print(f"generation evidence {rel}: {actual} expected={expected} match={actual == expected}")

trace_events = 0
trace_types: dict[str, int] = {}
for trace in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    with trace.open() as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            trace_events += 1
            key = f"{item.get('type')}/{item.get('payload', {}).get('type')}"
            trace_types[key] = trace_types.get(key, 0) + 1
    print(f"trace parsed: {trace} lines={line_number}")
print("trace_events:", trace_events)
for key, count in sorted(trace_types.items()):
    print(f"trace_type {key}: {count}")

for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference")):
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISREG(mode):
            kind = "file"
            value = digest(path)
        elif stat.S_ISDIR(mode):
            kind = "dir"
            value = "-"
        else:
            kind = "other"
            value = "-"
        print(f"inventory {kind} {path} {value}")
