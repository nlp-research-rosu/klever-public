#!/usr/bin/env python3
"""Independent checks for launcher records and mounted audit inputs."""

from __future__ import annotations

import collections
import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_regular(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the recorded pipeline tree-digest format independently."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
failures: list[str] = []

print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")
print(f"campaign_block_exact_match={audit.get('audit_campaign') == lock}")
if audit.get("audit_campaign") != lock:
    failures.append("campaign block differs from campaign lock")

actual_lock_hash = sha256(LOCK)
expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign_lock_sha256={actual_lock_hash}")
print(f"campaign_lock_hash_match={actual_lock_hash == expected_lock_hash}")
if actual_lock_hash != expected_lock_hash:
    failures.append("campaign lock hash mismatch")

required = {
    "audit_input": AUDIT,
    "campaign_lock": LOCK,
    "run": Path("/run.json"),
    "task": Path("/task.json"),
    "result": Path("/generation-result.json"),
    "invocation": Path("/generation-evidence/invocation.json"),
    "metrics": Path("/generation-evidence/metrics.json"),
    "last": Path("/generation-evidence/codex-last.txt"),
    "output": Path("/generation-evidence/codex-output.log"),
    "prompt": Path("/generation-evidence/prompt.txt"),
    "canonical": Path("/reference/canonical.py"),
    "trusted_prompt": Path("/reference/prompt.py"),
    "translator": Path("/reference/py2mpy.py"),
    "candidate_prompt": Path("/candidate/prompt.py"),
    "candidate_translator": Path("/candidate/py2mpy.py"),
}
for label, path in required.items():
    ok = check_regular(path)
    print(f"regular_nonsymlink[{label}]={ok}:{path}")
    if not ok:
        failures.append(f"missing/mistyped/symlinked required file: {path}")

for root in (Path("/candidate"), Path("/generation-evidence/codex-trace")):
    if not root.is_dir() or root.is_symlink():
        failures.append(f"missing/mistyped/symlinked required directory: {root}")
        continue
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(current, name)
            if path.is_symlink():
                failures.append(f"symlink found in required tree: {path}")

hash_checks = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, key in hash_checks.items():
    expected = audit["hashes"].get(key)
    actual = sha256(path) if check_regular(path) else None
    ok = expected == actual
    print(f"hash_match[{key}]={ok}:expected={expected}:actual={actual}")
    if not ok:
        failures.append(f"hash mismatch for {path}")

generated_mode = audit.get("semantics_mode") == "GENERATED_SEMANTICS"
reference_semantics = Path("/reference/reference-semantics")
absent = not reference_semantics.exists() and not reference_semantics.is_symlink()
print(f"generated_mode_reference_semantics_absent={generated_mode and absent}")
if not generated_mode or not absent:
    failures.append("rendered semantics mode contradicts trusted semantics mount")

prompt_bytes_match = Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
translator_bytes_match = Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print(f"candidate_prompt_byte_match={prompt_bytes_match}")
print(f"candidate_translator_byte_match={translator_bytes_match}")
if not prompt_bytes_match:
    failures.append("candidate prompt differs from trusted prompt")
if not translator_bytes_match:
    failures.append("candidate translator differs from trusted translator")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
evidence_hashes = result.get("outputs", {}).get("evidence", {})
for relative, expected in sorted(evidence_hashes.items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path) if check_regular(path) else None
    ok = actual == expected
    print(f"result_evidence_hash_match[{relative}]={ok}:actual={actual}")
    if not ok:
        failures.append(f"generation-result evidence mismatch: {relative}")

candidate_tree = pipeline_tree_sha256(Path("/candidate"))
workspace_expectations = {
    result.get("outputs", {}).get("workspace_sha256"),
    invocation.get("outputs", {}).get("workspace_sha256"),
    invocation.get("retained_workspace_sha256"),
}
print(f"candidate_pipeline_tree_sha256={candidate_tree}")
print(f"candidate_pipeline_tree_expectations={sorted(workspace_expectations)}")
if workspace_expectations != {candidate_tree}:
    failures.append("candidate tree differs from authenticated generation workspace")

usage = json.loads(Path("/generation-evidence/usage.json").read_text())
trace_tree = pipeline_tree_sha256(Path("/generation-evidence/codex-trace"))
expected_trace_tree = usage.get("source_trace_sha256")
print(f"trace_pipeline_tree_sha256={trace_tree}")
print(f"trace_usage_tree_hash_match={trace_tree == expected_trace_tree}")
if trace_tree != expected_trace_tree:
    failures.append("trace tree differs from authenticated usage record")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file() and not path.is_symlink()]
print(f"trace_regular_file_count={len(trace_files)}")
for path in trace_files:
    counts: collections.Counter[str] = collections.Counter()
    valid = True
    lines = 0
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            lines = number
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                valid = False
                failures.append(f"invalid JSONL at {path}:{number}")
                continue
            counts[str(event.get("type", "<missing>"))] += 1
    print(
        f"trace[{path.relative_to('/generation-evidence')}]:"
        f"lines={lines}:all_json={valid}:types={dict(sorted(counts.items()))}:"
        f"sha256={sha256(path)}"
    )

print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
