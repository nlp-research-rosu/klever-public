#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script only reads launcher/candidate/reference mounts and prints a bounded
report.  It deliberately does not trust booleans in audit-input.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_manifest(root: Path) -> tuple[str, list[str]]:
    """Return an independent digest and a type/hash manifest for a tree."""
    rows: list[str] = []
    for path in sorted([root, *root.rglob("*")], key=lambda p: str(p.relative_to(root))):
        rel = "." if path == root else path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            row = f"L\t{rel}\t{os.readlink(path)}"
        elif stat.S_ISDIR(mode):
            row = f"D\t{rel}"
        elif stat.S_ISREG(mode):
            row = f"F\t{rel}\t{path.stat().st_size}\t{sha256_file(path)}"
        else:
            row = f"O\t{rel}\t{oct(mode)}"
        rows.append(row)
    payload = ("\n".join(rows) + "\n").encode()
    return hashlib.sha256(payload).hexdigest(), rows


def pipeline_sha256_tree(root: Path) -> str:
    """Reimplement the pipeline-v3 sha256_tree framing convention."""
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
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def required_regular(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING"
    if path.is_symlink():
        return False, "SYMLINK"
    if not path.is_file():
        return False, f"NOT_REGULAR mode={oct(path.lstat().st_mode)}"
    if not os.access(path, os.R_OK):
        return False, "UNREADABLE"
    return True, f"regular readable size={path.stat().st_size}"


audit = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
hashes = audit["hashes"]
paths = audit["container_paths"]

print("record_layout:", audit.get("record_layout"))
print("semantics_mode:", audit.get("semantics_mode"))
print("campaign_object_equals_lock:", audit["audit_campaign"] == lock)
print(
    "campaign_lock_sha256:",
    sha256_file(LOCK),
    "expected:",
    hashes["audit_campaign_lock_sha256"],
    "match:",
    sha256_file(LOCK) == hashes["audit_campaign_lock_sha256"],
)

required = {
    "audit-input": AUDIT,
    "audit-campaign-lock": LOCK,
    "run": Path(paths["run_manifest"]),
    "task": Path(paths["task_manifest"]),
    "generation-result": Path(paths["stage1_result"]),
    "invocation": Path(paths["generation_manifest"]),
    "metrics": Path(paths["generation_metrics"]),
    "runtime-metrics": Path("/generation-evidence/runtime-metrics.json"),
    "usage": Path("/generation-evidence/usage.json"),
    "codex-last": Path(paths["generation_last"]),
    "codex-output": Path(paths["generation_output"]),
    "generation-prompt": Path("/generation-evidence/prompt.txt"),
    "trusted-canonical": Path(paths["canonical"]),
    "trusted-prompt": Path(paths["trusted_prompt"]),
    "trusted-translator": Path(paths["translator"]),
}
print("required_regular_records:")
all_required_ok = True
for name, path in required.items():
    ok, detail = required_regular(path)
    all_required_ok &= ok
    print(f"  {name}: {path}: {detail}")
print("all_required_regular_readable:", all_required_ok)

expected_hashes = {
    Path(paths["run_manifest"]): hashes["run_manifest_sha256"],
    Path(paths["task_manifest"]): hashes["task_manifest_sha256"],
    Path(paths["stage1_result"]): hashes["stage1_result_sha256"],
    Path(paths["generation_manifest"]): hashes["stage1_invocation_sha256"],
    Path(paths["generation_metrics"]): hashes["generation_metrics_sha256"],
    Path("/generation-evidence/runtime-metrics.json"): hashes[
        "generation_runtime_metrics_sha256"
    ],
    Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
    Path(paths["generation_last"]): hashes["generation_codex_last_sha256"],
    Path(paths["generation_output"]): hashes["generation_codex_output_sha256"],
    Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
    Path(paths["canonical"]): hashes["canonical_sha256"],
    Path(paths["trusted_prompt"]): hashes["trusted_prompt_sha256"],
    Path(paths["translator"]): hashes["trusted_translator_sha256"],
}
print("declared_file_hash_checks:")
all_hashes_ok = True
for path, expected in expected_hashes.items():
    actual = sha256_file(path)
    ok = actual == expected
    all_hashes_ok &= ok
    print(f"  {path}: {actual} expected={expected} match={ok}")
print("all_declared_file_hashes_match:", all_hashes_ok)

candidate = Path(paths["candidate"])
candidate_required = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
]
print("candidate_required_artifacts:")
candidate_required_ok = True
for rel in candidate_required:
    ok, detail = required_regular(candidate / rel)
    candidate_required_ok &= ok
    print(f"  {rel}: {detail}")
print("candidate_required_artifacts_ok:", candidate_required_ok)

print("candidate_prompt_byte_equal:", (candidate / "prompt.py").read_bytes() == Path(paths["trusted_prompt"]).read_bytes())
print("candidate_translator_byte_equal:", (candidate / "py2mpy.py").read_bytes() == Path(paths["translator"]).read_bytes())
print(
    "candidate_prompt_sha256:",
    sha256_file(candidate / "prompt.py"),
    "expected:",
    hashes["candidate_prompt_sha256"],
)
print(
    "candidate_translator_sha256:",
    sha256_file(candidate / "py2mpy.py"),
    "expected:",
    hashes["candidate_translator_sha256"],
)

trusted_sem = Path("/reference/reference-semantics")
candidate_sem = candidate / "reference-semantics"
print("trusted_reference_semantics_exists:", trusted_sem.is_dir())
trusted_digest, trusted_rows = tree_manifest(trusted_sem)
candidate_digest, candidate_rows = tree_manifest(candidate_sem)
print("trusted_semantics_independent_manifest_sha256:", trusted_digest)
print("candidate_semantics_independent_manifest_sha256:", candidate_digest)
print("semantics_manifests_byte_equal:", trusted_rows == candidate_rows)
print("semantics_entry_count:", len(trusted_rows))
sem_symlinks = [row for row in trusted_rows + candidate_rows if row.startswith("L\t")]
sem_other = [row for row in trusted_rows + candidate_rows if row.startswith("O\t")]
print("semantics_symlink_entries:", len(sem_symlinks))
print("semantics_other_type_entries:", len(sem_other))
if trusted_rows != candidate_rows:
    only_trusted = sorted(set(trusted_rows) - set(candidate_rows))
    only_candidate = sorted(set(candidate_rows) - set(trusted_rows))
    print("semantics_only_trusted:", only_trusted[:20])
    print("semantics_only_candidate:", only_candidate[:20])

candidate_digest_all, candidate_rows_all = tree_manifest(candidate)
print("candidate_independent_manifest_sha256:", candidate_digest_all)
print("candidate_entry_count:", len(candidate_rows_all))
print(
    "candidate_symlink_count:",
    sum(row.startswith("L\t") for row in candidate_rows_all),
)
print(
    "candidate_other_type_count:",
    sum(row.startswith("O\t") for row in candidate_rows_all),
)
generation_result = json.loads(Path(paths["stage1_result"]).read_text())
task_manifest = json.loads(Path(paths["task_manifest"]).read_text())
candidate_pipeline_digest = pipeline_sha256_tree(candidate)
trusted_sem_pipeline_digest = pipeline_sha256_tree(trusted_sem)
candidate_sem_pipeline_digest = pipeline_sha256_tree(candidate_sem)
print(
    "candidate_pipeline_sha256_tree:",
    candidate_pipeline_digest,
    "expected_stage1_workspace:",
    generation_result["outputs"]["workspace_sha256"],
    "match:",
    candidate_pipeline_digest == generation_result["outputs"]["workspace_sha256"],
)
print(
    "trusted_semantics_pipeline_sha256_tree:",
    trusted_sem_pipeline_digest,
    "expected_task_input:",
    task_manifest["inputs"]["reference_semantics_sha256"],
    "match:",
    trusted_sem_pipeline_digest == task_manifest["inputs"]["reference_semantics_sha256"],
)
print(
    "candidate_semantics_pipeline_sha256_tree:",
    candidate_sem_pipeline_digest,
    "matches_trusted:",
    candidate_sem_pipeline_digest == trusted_sem_pipeline_digest,
)

trace_root = Path(paths["generation_trace"])
print(
    "generation_trace_root:",
    trace_root,
    "is_dir:",
    trace_root.is_dir(),
    "is_symlink:",
    trace_root.is_symlink(),
    "readable:",
    os.access(trace_root, os.R_OK),
)
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
print("generation_trace_file_count:", len(trace_files))
trace_expected_map = {
    rel.removeprefix("codex-trace/"): digest
    for rel, digest in generation_result["outputs"]["evidence"].items()
    if rel.startswith("codex-trace/")
}
trace_hash_ok = True
for path in trace_files:
    rel = path.relative_to(trace_root).as_posix()
    actual = sha256_file(path)
    expected = trace_expected_map.get(rel)
    ok = expected == actual
    trace_hash_ok &= ok
    print(f"  trace {rel}: size={path.stat().st_size} sha256={actual} expected={expected} match={ok}")
print("trace_file_set_equals_declared:", set(trace_expected_map) == {p.relative_to(trace_root).as_posix() for p in trace_files})
print("trace_hashes_match:", trace_hash_ok)
usage_document = json.loads(Path("/generation-evidence/usage.json").read_text())
trace_pipeline_digest = pipeline_sha256_tree(trace_root)
print(
    "trace_pipeline_sha256_tree:",
    trace_pipeline_digest,
    "expected_usage_source_trace:",
    usage_document["source_trace_sha256"],
    "match:",
    trace_pipeline_digest == usage_document["source_trace_sha256"],
)

# Parse every structured-trace line, proving readability and obtaining a bounded
# shape summary without treating any event as authoritative.
trace_type_counts: Counter[str] = Counter()
trace_parse_errors: list[str] = []
trace_lines = 0
for path in trace_files:
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            trace_lines += 1
            try:
                event = json.loads(line)
            except Exception as err:  # pragma: no cover - audit diagnostic
                trace_parse_errors.append(f"{path}:{line_no}:{err}")
                continue
            event_type = str(event.get("type", "<missing>"))
            payload = event.get("payload")
            payload_type = (
                str(payload.get("type", "<missing>"))
                if isinstance(payload, dict)
                else type(payload).__name__
            )
            trace_type_counts[f"{event_type}/{payload_type}"] += 1
print("trace_lines_parsed:", trace_lines)
print("trace_parse_errors:", trace_parse_errors[:10])
print("trace_event_shape_counts:")
for key, value in sorted(trace_type_counts.items()):
    print(f"  {key}: {value}")

# Read both large untrusted text records completely and report bounded summaries.
for label, path in [
    ("codex-output", Path(paths["generation_output"])),
    ("codex-last", Path(paths["generation_last"])),
    ("generation-prompt", Path("/generation-evidence/prompt.txt")),
]:
    raw = path.read_bytes()
    print(
        f"{label}_full_read: bytes={len(raw)} lines={raw.count(bytes([10]))} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
