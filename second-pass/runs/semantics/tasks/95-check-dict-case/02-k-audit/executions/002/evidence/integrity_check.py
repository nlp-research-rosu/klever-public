#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
TRACE = GEN / "codex-trace"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_tree(root: Path):
    entries = {}
    symlinks = []
    nonregular = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            symlinks.append((rel, os.readlink(path)))
        elif path.is_file():
            entries[rel] = sha256(path)
        elif not path.is_dir():
            nonregular.append(rel)
    return entries, symlinks, nonregular


def manifest_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    entries = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                raise ValueError(f"symlink in manifest tree: {path}")
            if path.is_dir():
                entries.append((rel, "directory", path))
                pending.append(path)
            elif path.is_file():
                entries.append((rel, "file", path))
            else:
                raise ValueError(f"unsupported entry in manifest tree: {path}")
    for rel, kind, path in sorted(entries):
        encoded = rel.encode()
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
errors = []

if lock != audit["audit_campaign"]:
    errors.append("campaign lock JSON differs from audit_campaign block")

record_layout = audit["record_layout"]
required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GEN / "invocation.json",
    GEN / "metrics.json",
    GEN / "codex-last.txt",
    GEN / "codex-output.log",
    GEN / "prompt.txt",
]
if record_layout == "legacy-selected-stage1" and (GEN / "usage.json").exists():
    required.append(GEN / "usage.json")

for path in required:
    if not path.is_file() or path.is_symlink() or not os.access(path, os.R_OK):
        errors.append(f"required record is absent, unreadable, non-file, or symlinked: {path}")

hash_map = {
    LOCK: "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    GEN / "invocation.json": "stage1_invocation_sha256",
    GEN / "metrics.json": "generation_metrics_sha256",
    GEN / "codex-last.txt": "generation_codex_last_sha256",
    GEN / "codex-output.log": "generation_codex_output_sha256",
    GEN / "prompt.txt": "generation_prompt_sha256",
    GEN / "usage.json": "generation_usage_sha256",
}
for path, key in hash_map.items():
    if path.exists() and key in audit["hashes"]:
        actual = sha256(path)
        expected = audit["hashes"][key]
        print(f"HASH {path}: {actual} expected={expected} match={actual == expected}")
        if actual != expected:
            errors.append(f"hash mismatch for {path}")

candidate_sem, candidate_links, candidate_other = regular_tree(
    Path("/candidate/reference-semantics")
)
trusted_sem, trusted_links, trusted_other = regular_tree(
    Path("/reference/reference-semantics")
)
print(f"SEMANTICS_FILES candidate={len(candidate_sem)} trusted={len(trusted_sem)}")
print(f"SEMANTICS_SYMLINKS candidate={candidate_links} trusted={trusted_links}")
print(f"SEMANTICS_NONREGULAR candidate={candidate_other} trusted={trusted_other}")
missing = sorted(set(trusted_sem) - set(candidate_sem))
additional = sorted(set(candidate_sem) - set(trusted_sem))
changed = sorted(
    path
    for path in set(candidate_sem) & set(trusted_sem)
    if candidate_sem[path] != trusted_sem[path]
)
print(f"SEMANTICS_DIFF missing={missing} additional={additional} changed={changed}")
if missing or additional or changed or candidate_links or trusted_links or candidate_other or trusted_other:
    errors.append("candidate/trusted supplied semantics trees are not identical regular-file trees")

for candidate, trusted, label in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
]:
    same = candidate.read_bytes() == trusted.read_bytes()
    print(f"BYTE_IDENTITY {label}: {same}")
    if not same:
        errors.append(f"candidate {label} differs from trusted mount")

trace_files, trace_links, trace_other = regular_tree(TRACE)
print(f"TRACE_FILES count={len(trace_files)} entries={trace_files}")
print(f"TRACE_SYMLINKS {trace_links}; TRACE_NONREGULAR {trace_other}")
result = json.loads(Path("/generation-result.json").read_text())
declared_trace = {
    key.removeprefix("codex-trace/"): value
    for key, value in result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
if trace_files != declared_trace:
    errors.append("structured trace file set or hashes differ from generation-result.json")

candidate_manifest_hash = manifest_tree_sha256(Path("/candidate"))
expected_workspace_hash = result["outputs"]["workspace_sha256"]
print(
    "CANDIDATE_MANIFEST_TREE_SHA256:",
    candidate_manifest_hash,
    f"expected_generation_workspace={expected_workspace_hash}",
    f"match={candidate_manifest_hash == expected_workspace_hash}",
)
if candidate_manifest_hash != expected_workspace_hash:
    errors.append("candidate manifest tree hash differs from finalized generation workspace")

semantics_manifest_hash = manifest_tree_sha256(Path("/reference/reference-semantics"))
expected_semantics_manifest = audit["hashes"][
    "trusted_reference_semantics_manifest_sha256"
]
print(
    "SEMANTICS_MANIFEST_TREE_SHA256:",
    semantics_manifest_hash,
    f"expected={expected_semantics_manifest}",
    f"match={semantics_manifest_hash == expected_semantics_manifest}",
)
if semantics_manifest_hash != expected_semantics_manifest:
    errors.append("trusted semantics manifest tree hash mismatch")

print(f"RECORD_LAYOUT: {record_layout}")
print(f"SEMANTICS_MODE: {audit['semantics_mode']}")
print(f"ERRORS: {errors}")
print("INTEGRITY_RESULT: PASS" if not errors else "INTEGRITY_RESULT: FAIL")
raise SystemExit(1 if errors else 0)
