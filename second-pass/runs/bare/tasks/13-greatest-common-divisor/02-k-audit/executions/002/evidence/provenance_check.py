#!/usr/bin/env python3
"""Independent integrity checks for the launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_sha256(root: Path) -> str:
    """Hash paths, entry kinds, file sizes, and contents deterministically."""
    digest = hashlib.sha256()
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
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise RuntimeError(f"required record is not a regular file: {path}")


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
hashes = audit["hashes"]

checks: list[tuple[str, bool, str]] = []


def check(name: str, actual: object, expected: object) -> None:
    checks.append((name, actual == expected, f"actual={actual!r} expected={expected!r}"))


check("campaign block equals campaign lock", audit["audit_campaign"], lock)
check(
    "campaign lock SHA-256",
    file_sha256(Path("/audit-campaign-lock.json")),
    hashes["audit_campaign_lock_sha256"],
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
]
if Path("/generation-evidence/usage.json").exists():
    required_files.append(Path("/generation-evidence/usage.json"))
for path in required_files:
    require_regular(path)

file_expectations = {
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
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
}
for path, key in file_expectations.items():
    require_regular(path)
    check(f"{path} SHA-256", file_sha256(path), hashes[key])

check(
    "candidate prompt byte identity",
    Path("/candidate/prompt.py").read_bytes(),
    Path("/reference/prompt.py").read_bytes(),
)
check(
    "candidate translator byte identity",
    Path("/candidate/py2mpy.py").read_bytes(),
    Path("/reference/py2mpy.py").read_bytes(),
)
check(
    "GENERATED_SEMANTICS has no trusted reference semantics",
    Path("/reference/reference-semantics").exists()
    or Path("/reference/reference-semantics").is_symlink(),
    False,
)
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
candidate_pipeline_digest = tree_sha256(Path("/candidate"))
check(
    "candidate tree equals generation-result workspace (pipeline tree format)",
    candidate_pipeline_digest,
    result["outputs"]["workspace_sha256"],
)
check(
    "candidate tree equals invocation retained workspace (pipeline tree format)",
    candidate_pipeline_digest,
    invocation["retained_workspace_sha256"],
)
trace_hashes = {
    key: value
    for key, value in result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
check("trace manifest agrees across records", trace_hashes, {
    key: value
    for key, value in invocation["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
})

event_counts: Counter[str] = Counter()
payload_counts: Counter[str] = Counter()
trace_lines = 0
for relative, expected in trace_hashes.items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    check(f"{path} SHA-256", file_sha256(path), expected)
    with path.open() as stream:
        for line in stream:
            record = json.loads(line)
            trace_lines += 1
            event_counts[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_counts[str(payload.get("type"))] += 1

usage = json.loads(Path("/generation-evidence/usage.json").read_text())
check(
    "trace tree equals usage source trace (pipeline tree format)",
    tree_sha256(Path("/generation-evidence/codex-trace")),
    usage["source_trace_sha256"],
)

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"candidate_pipeline_tree_sha256={candidate_pipeline_digest}")
print(
    "launcher_candidate_tree_sha256="
    f"{hashes['candidate_tree_sha256']} "
    "(audit-input does not declare this tree digest's serialization)"
)
print(
    "launcher_generation_trace_sha256="
    f"{hashes['generation_codex_trace_sha256']} "
    "(audit-input does not declare this tree digest's serialization)"
)
print(f"trace_lines={trace_lines}")
print(f"trace_event_types={dict(sorted(event_counts.items()))}")
print(f"trace_payload_types={dict(sorted(payload_counts.items()))}")
for name, passed, detail in checks:
    rendered_detail = detail
    if "byte identity" in name:
        rendered_detail = "bytes compared directly"
    print(f"{'PASS' if passed else 'FAIL'}: {name}: {rendered_detail}")

failures = [name for name, passed, _ in checks if not passed]
if failures:
    raise SystemExit(f"integrity failures: {failures}")
