#!/usr/bin/env python3
import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def manifest_tree_digest(root: Path) -> str:
    """Pipeline-manifest recursive digest, independently recomputed."""
    h = hashlib.sha256()
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        h.update(len(encoded).to_bytes(4, "big"))
        h.update(encoded)
        h.update(kind.encode() + b"\0")
        if kind == "file":
            h.update(path.stat(follow_symlinks=False).st_size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
    return h.hexdigest()


def audit_tree_digest(root: Path) -> str:
    """Audit-record recursive digest, independently recomputed."""
    h = hashlib.sha256()
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported tree entry: {path}")
    for relative, kind, path in sorted(entries):
        h.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
    return h.hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
failures = []

print(f"record_layout={audit.get('record_layout')}")
print(f"semantics_mode={audit.get('semantics_mode')}")

checks = {
    "audit_campaign_lock": (
        Path("/audit-campaign-lock.json"),
        audit["hashes"]["audit_campaign_lock_sha256"],
    ),
    "run_manifest": (Path("/run.json"), audit["hashes"]["run_manifest_sha256"]),
    "task_manifest": (Path("/task.json"), audit["hashes"]["task_manifest_sha256"]),
    "stage1_result": (
        Path("/generation-result.json"),
        audit["hashes"]["stage1_result_sha256"],
    ),
    "stage1_invocation": (
        Path("/generation-evidence/invocation.json"),
        audit["hashes"]["stage1_invocation_sha256"],
    ),
    "generation_metrics": (
        Path("/generation-evidence/metrics.json"),
        audit["hashes"]["generation_metrics_sha256"],
    ),
    "generation_usage": (
        Path("/generation-evidence/usage.json"),
        audit["hashes"]["generation_usage_sha256"],
    ),
    "generation_last": (
        Path("/generation-evidence/codex-last.txt"),
        audit["hashes"]["generation_codex_last_sha256"],
    ),
    "generation_output": (
        Path("/generation-evidence/codex-output.log"),
        audit["hashes"]["generation_codex_output_sha256"],
    ),
    "generation_prompt": (
        Path("/generation-evidence/prompt.txt"),
        audit["hashes"]["generation_prompt_sha256"],
    ),
    "trusted_prompt": (
        Path("/reference/prompt.py"),
        audit["hashes"]["trusted_prompt_sha256"],
    ),
    "candidate_prompt": (
        Path("/candidate/prompt.py"),
        audit["hashes"]["candidate_prompt_sha256"],
    ),
    "trusted_translator": (
        Path("/reference/py2mpy.py"),
        audit["hashes"]["trusted_translator_sha256"],
    ),
    "candidate_translator": (
        Path("/candidate/py2mpy.py"),
        audit["hashes"]["candidate_translator_sha256"],
    ),
    "canonical": (
        Path("/reference/canonical.py"),
        audit["hashes"]["canonical_sha256"],
    ),
}

for label, (path, expected) in checks.items():
    if not path.is_file() or path.is_symlink():
        print(f"BAD_TYPE {label} {path}")
        failures.append(label)
        continue
    actual = digest(path)
    outcome = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label} expected={expected} actual={actual} {outcome}")
    if outcome != "MATCH":
        failures.append(label)

audit_tree_records = {
    "candidate_tree": (
        Path("/candidate"),
        audit["hashes"]["candidate_tree_sha256"],
    ),
    "candidate_reference_semantics_tree": (
        Path("/candidate/reference-semantics"),
        audit["hashes"]["candidate_reference_semantics_sha256"],
    ),
    "trusted_reference_semantics_tree": (
        Path("/reference/reference-semantics"),
        audit["hashes"]["trusted_reference_semantics_sha256"],
    ),
    "generation_trace_tree": (
        Path("/generation-evidence/codex-trace"),
        audit["hashes"]["generation_codex_trace_sha256"],
    ),
}
for label, (path, recorded) in audit_tree_records.items():
    actual = audit_tree_digest(path)
    print(
        f"{label} launcher_recorded={recorded} "
        f"independent_content_digest={actual}"
    )

manifest_tree_checks = {
    "candidate_pipeline_manifest_tree": (
        Path("/candidate"),
        json.loads(Path("/generation-result.json").read_text())["outputs"][
            "workspace_sha256"
        ],
    ),
    "trusted_reference_semantics_manifest_tree": (
        Path("/reference/reference-semantics"),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    "generation_trace_usage_source_tree": (
        Path("/generation-evidence/codex-trace"),
        json.loads(Path("/generation-evidence/usage.json").read_text())[
            "source_trace_sha256"
        ],
    ),
}
for label, (path, expected) in manifest_tree_checks.items():
    actual = manifest_tree_digest(path)
    outcome = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label} expected={expected} actual={actual} {outcome}")
    if outcome != "MATCH":
        failures.append(label)

for relative, expected in sorted(invocation["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    if not path.is_file() or path.is_symlink():
        print(f"BAD_GENERATION_RECORD {relative}")
        failures.append(relative)
        continue
    actual = digest(path)
    outcome = "MATCH" if actual == expected else "MISMATCH"
    print(f"invocation_record {relative} expected={expected} actual={actual} {outcome}")
    if outcome != "MATCH":
        failures.append(relative)

if audit["audit_campaign"] == lock:
    print("campaign_block=EXACT_MATCH")
else:
    print("campaign_block=MISMATCH")
    failures.append("campaign_block")

for left, right in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")),
]:
    same = left.read_bytes() == right.read_bytes()
    print(f"byte_identity {left} {right} {'MATCH' if same else 'MISMATCH'}")
    if not same:
        failures.append(str(left))


def tree_entries(root: Path):
    entries = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            value = os.readlink(path)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            value = ""
        elif stat.S_ISREG(mode):
            kind = "file"
            value = digest(path)
        else:
            kind = "other"
            value = stat.S_IFMT(mode)
        entries[rel] = (kind, value)
    return entries


candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
if candidate_semantics == trusted_semantics:
    print(
        "reference_semantics_recursive_identity=MATCH "
        f"entries={len(candidate_semantics)}"
    )
else:
    print("reference_semantics_recursive_identity=MISMATCH")
    for rel in sorted(set(candidate_semantics) | set(trusted_semantics)):
        if candidate_semantics.get(rel) != trusted_semantics.get(rel):
            print(
                f"tree_difference {rel} "
                f"candidate={candidate_semantics.get(rel)} "
                f"trusted={trusted_semantics.get(rel)}"
            )
    failures.append("reference_semantics")

for root in [
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
]:
    links = [str(path) for path in root.rglob("*") if path.is_symlink()]
    print(f"symlinks under {root}: {links if links else 'NONE'}")
    if links:
        failures.extend(links)

required_types = {
    Path("/candidate/solution.py"): "file",
    Path("/candidate/solution.mpy"): "file",
    Path("/candidate/verification.k"): "file",
    Path("/candidate/spec.k"): "file",
    Path("/candidate/prove.sh"): "file",
    Path("/run.json"): "file",
    Path("/task.json"): "file",
    Path("/generation-result.json"): "file",
    Path("/generation-evidence/invocation.json"): "file",
    Path("/generation-evidence/metrics.json"): "file",
    Path("/generation-evidence/codex-last.txt"): "file",
    Path("/generation-evidence/codex-output.log"): "file",
    Path("/generation-evidence/prompt.txt"): "file",
    Path("/generation-evidence/codex-trace"): "directory",
}
for path, expected_type in required_types.items():
    if path.is_symlink():
        actual_type = "symlink"
    elif path.is_file():
        actual_type = "file"
    elif path.is_dir():
        actual_type = "directory"
    elif path.exists():
        actual_type = "other"
    else:
        actual_type = "missing"
    print(f"required_type {path} expected={expected_type} actual={actual_type}")
    if actual_type != expected_type:
        failures.append(str(path))

print(f"failures={len(failures)}")
for failure in failures:
    print(f"failure={failure}")
sys.exit(1 if failures else 0)
