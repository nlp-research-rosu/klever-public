#!/usr/bin/env python3
"""Independent provenance and mounted-tree integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(path: Path) -> str:
    """Reimplement the launcher's length-delimited tree digest independently."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [path]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            entry_path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = entry_path.relative_to(path).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", entry_path))
                pending.append(entry_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", entry_path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {entry_path}")
    for relative, kind, entry_path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = entry_path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with entry_path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required regular file is missing/mistyped/linked: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required real directory is missing/mistyped/linked: {path}"


def tree_entries(path: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for entry in sorted(path.rglob("*")):
        relative = entry.relative_to(path).as_posix()
        mode = entry.lstat().st_mode
        if stat.S_ISDIR(mode):
            result[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            result[relative] = ("file", sha256_file(entry))
        else:
            result[relative] = ("UNSUPPORTED", None)
    return result


audit = json.loads(Path("/audit-input.json").read_text())
campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
run = json.loads(Path("/run.json").read_text())
task = json.loads(Path("/task.json").read_text())
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

assert audit["problem_id"] == "51-remove-vowels"
assert audit["condition"] == "semantics"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["record_layout"] == "legacy-selected-stage1"
assert campaign == audit["audit_campaign"]
embedded_manifest = dict(audit["manifest"])
embedded_config = embedded_manifest.pop("config")
assert task == embedded_manifest
assert embedded_config == audit["manifest_config"] == audit["config"]
assert run["run_id"] == audit["run_id"]
assert result["invocation"] == invocation["name"]
assert result["session_id"] == invocation["session_id"]
assert result["outputs"] == invocation["outputs"]

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
    Path("/generation-evidence/usage.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
required_directories = [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
]
for required in required_files:
    require_regular(required)
for required in required_directories:
    require_directory(required)

expected_files = {
    "/audit-campaign-lock.json": audit["hashes"]["audit_campaign_lock_sha256"],
    "/run.json": audit["hashes"]["run_manifest_sha256"],
    "/task.json": audit["hashes"]["task_manifest_sha256"],
    "/generation-result.json": audit["hashes"]["stage1_result_sha256"],
    "/generation-evidence/invocation.json": audit["hashes"]["stage1_invocation_sha256"],
    "/generation-evidence/metrics.json": audit["hashes"]["generation_metrics_sha256"],
    "/generation-evidence/codex-last.txt": audit["hashes"]["generation_codex_last_sha256"],
    "/generation-evidence/codex-output.log": audit["hashes"]["generation_codex_output_sha256"],
    "/generation-evidence/prompt.txt": audit["hashes"]["generation_prompt_sha256"],
    "/generation-evidence/usage.json": audit["hashes"]["generation_usage_sha256"],
    "/reference/canonical.py": audit["hashes"]["canonical_sha256"],
    "/reference/prompt.py": audit["hashes"]["trusted_prompt_sha256"],
    "/reference/py2mpy.py": audit["hashes"]["trusted_translator_sha256"],
    "/candidate/prompt.py": audit["hashes"]["candidate_prompt_sha256"],
    "/candidate/py2mpy.py": audit["hashes"]["candidate_translator_sha256"],
}
for filename, expected in expected_files.items():
    actual = sha256_file(Path(filename))
    assert actual == expected, f"hash mismatch {filename}: {actual} != {expected}"
    print(f"FILE HASH OK {filename} {actual}")

for relative, expected in invocation["outputs"]["evidence"].items():
    evidence_path = Path("/generation-evidence") / relative
    require_regular(evidence_path)
    actual = sha256_file(evidence_path)
    assert actual == expected, f"invocation evidence mismatch {relative}"
    print(f"INVOCATION EVIDENCE HASH OK {relative} {actual}")

candidate_tree = sha256_tree(Path("/candidate"))
trusted_semantics_tree = sha256_tree(Path("/reference/reference-semantics"))
candidate_semantics_tree = sha256_tree(Path("/candidate/reference-semantics"))
trace_tree = sha256_tree(Path("/generation-evidence/codex-trace"))
assert candidate_tree == invocation["outputs"]["workspace_sha256"]
assert candidate_tree == result["outputs"]["workspace_sha256"]
assert trusted_semantics_tree == audit["hashes"]["trusted_reference_semantics_manifest_sha256"]
assert candidate_semantics_tree == trusted_semantics_tree
assert trace_tree == usage["source_trace_sha256"]
print(f"TREE HASH OK candidate {candidate_tree}")
print(f"TREE HASH OK trusted reference-semantics {trusted_semantics_tree}")
print(f"TREE HASH OK candidate reference-semantics {candidate_semantics_tree}")
print(f"TREE HASH OK generation trace {trace_tree}")

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
trusted_entries = tree_entries(Path("/reference/reference-semantics"))
candidate_entries = tree_entries(Path("/candidate/reference-semantics"))
assert trusted_entries == candidate_entries
assert all(kind != "UNSUPPORTED" for kind, _ in trusted_entries.values())
print("BYTE IDENTITY OK candidate prompt.py == trusted prompt.py")
print("BYTE IDENTITY OK candidate py2mpy.py == trusted py2mpy.py")
print(
    "RECURSIVE IDENTITY OK candidate/reference-semantics == "
    f"trusted/reference-semantics ({len(trusted_entries)} entries)"
)

assert audit["hashes"]["audit_campaign_lock_sha256"] == sha256_file(
    Path("/audit-campaign-lock.json")
)
assert audit["audit_campaign"] == campaign
print("CAMPAIGN LOCK BLOCK AND HASH OK")
print("RECORD LAYOUT OK legacy-selected-stage1; runtime-metrics.json not required")
print("INTEGRITY CHECKS PASSED")
