#!/usr/bin/env python3
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
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def stable_tree(path: Path):
    rows = []
    for entry in sorted(path.rglob("*"), key=lambda p: p.relative_to(path).as_posix()):
        rel = entry.relative_to(path).as_posix()
        kind = entry_kind(entry)
        if kind == "file":
            rows.append((kind, rel, sha256_file(entry)))
        elif kind == "symlink":
            rows.append((kind, rel, os.readlink(entry)))
        else:
            rows.append((kind, rel, ""))
    encoded = "".join("\0".join(row) + "\n" for row in rows).encode()
    return hashlib.sha256(encoded).hexdigest(), rows


def length_delimited_tree(path: Path) -> str:
    digest = hashlib.sha256()
    entries = []
    for entry in path.rglob("*"):
        rel = entry.relative_to(path).as_posix()
        kind = entry_kind(entry)
        if kind not in {"file", "directory"}:
            raise RuntimeError(f"unsupported tree entry {entry}: {kind}")
        entries.append((rel, kind, entry))
    for rel, kind, entry in sorted(entries):
        encoded = rel.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = entry.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with entry.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def content_delimited_tree(path: Path) -> str:
    digest = hashlib.sha256()
    entries = []
    for entry in path.rglob("*"):
        rel = entry.relative_to(path).as_posix()
        kind = entry_kind(entry)
        if kind not in {"file", "directory"}:
            raise RuntimeError(f"unsupported tree entry {entry}: {kind}")
        entries.append((rel, kind, entry))
    for rel, kind, entry in sorted(entries):
        digest.update(rel.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with entry.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


data = json.loads(AUDIT.read_text())
lock = json.loads(LOCK.read_text())
failures = []

print(f"record_layout={data.get('record_layout')}")
print(f"semantics_mode={data.get('semantics_mode')}")
print(f"audit_campaign_equal={lock == data.get('audit_campaign')}")
if lock != data.get("audit_campaign"):
    failures.append("campaign lock content mismatch")

actual_lock_hash = sha256_file(LOCK)
expected_lock_hash = data["hashes"]["audit_campaign_lock_sha256"]
print(f"audit_campaign_lock_sha256 actual={actual_lock_hash} expected={expected_lock_hash}")
if actual_lock_hash != expected_lock_hash:
    failures.append("campaign lock hash mismatch")

required = [
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
    Path("/generation-evidence/codex-trace"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
]
for path in required:
    kind = entry_kind(path) if path.exists() or path.is_symlink() else "missing"
    readable = os.access(path, os.R_OK)
    print(f"required {path}: kind={kind} readable={readable}")
    if kind == "missing" or not readable:
        failures.append(f"missing or unreadable: {path}")

file_hash_checks = {
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
for path, key in file_hash_checks.items():
    actual = sha256_file(path)
    expected = data["hashes"][key]
    ok = actual == expected
    print(f"hash {path}: ok={ok} actual={actual} expected={expected}")
    if not ok:
        failures.append(f"hash mismatch: {path}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = sha256_file(path)
    ok = actual == expected
    print(f"result evidence hash {rel}: ok={ok} actual={actual} expected={expected}")
    if not ok:
        failures.append(f"generation-result evidence hash mismatch: {rel}")

for label, path in [
    ("candidate_reference_semantics", Path("/candidate/reference-semantics")),
    ("trusted_reference_semantics", Path("/reference/reference-semantics")),
    ("candidate_full_tree", Path("/candidate")),
    ("generation_trace_tree", Path("/generation-evidence/codex-trace")),
]:
    digest, rows = stable_tree(path)
    counts = Counter(row[0] for row in rows)
    print(f"stable_tree {label}: digest={digest} entries={len(rows)} types={dict(counts)}")
    bad = [row for row in rows if row[0] in {"symlink", "other"}]
    print(f"stable_tree {label}: symlink_or_other={bad}")

print(
    "audit_recorded_tree_hash candidate_full_tree="
    + data["hashes"]["candidate_tree_sha256"]
)
print(
    "audit_recorded_tree_hash candidate_reference_semantics="
    + data["hashes"]["candidate_reference_semantics_sha256"]
)
print(
    "audit_recorded_tree_hash trusted_reference_semantics="
    + data["hashes"]["trusted_reference_semantics_sha256"]
)
print(
    "audit_recorded_tree_hash generation_trace="
    + data["hashes"]["generation_codex_trace_sha256"]
)
print(
    "audit_recorded_semantics_hashes_equal="
    + str(
        data["hashes"]["candidate_reference_semantics_sha256"]
        == data["hashes"]["trusted_reference_semantics_sha256"]
    )
)
for label, path in [
    ("candidate_full_tree", Path("/candidate")),
    ("candidate_reference_semantics", Path("/candidate/reference-semantics")),
    ("trusted_reference_semantics", Path("/reference/reference-semantics")),
    ("generation_trace", Path("/generation-evidence/codex-trace")),
]:
    print(
        f"independent_content_delimited_tree {label}="
        f"{content_delimited_tree(path)}"
    )

pipeline_tree_checks = [
    (
        "candidate_full_tree",
        Path("/candidate"),
        result["outputs"]["workspace_sha256"],
    ),
    (
        "candidate_reference_semantics",
        Path("/candidate/reference-semantics"),
        data["manifest"]["inputs"]["reference_semantics_sha256"],
    ),
    (
        "trusted_reference_semantics",
        Path("/reference/reference-semantics"),
        data["manifest"]["inputs"]["reference_semantics_sha256"],
    ),
    (
        "generation_trace",
        Path("/generation-evidence/codex-trace"),
        json.loads(Path("/generation-evidence/usage.json").read_text())[
            "source_trace_sha256"
        ],
    ),
]
for label, path, expected in pipeline_tree_checks:
    actual = length_delimited_tree(path)
    ok = actual == expected
    print(
        f"pipeline_tree_hash {label}: ok={ok} "
        f"actual={actual} expected={expected}"
    )
    if not ok:
        failures.append(f"pipeline tree hash mismatch: {label}")

candidate_digest, candidate_rows = stable_tree(Path("/candidate/reference-semantics"))
trusted_digest, trusted_rows = stable_tree(Path("/reference/reference-semantics"))
semantics_equal = candidate_rows == trusted_rows
print(f"reference_semantics_recursive_identity={semantics_equal}")
if not semantics_equal:
    failures.append("candidate reference semantics differs from trusted tree")

print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
