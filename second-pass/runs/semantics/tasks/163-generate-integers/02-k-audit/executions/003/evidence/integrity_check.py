#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        return f"MISSING/UNREADABLE ({err})"
    if stat.S_ISLNK(mode):
        return f"SYMLINK -> {os.readlink(path)}"
    if stat.S_ISREG(mode):
        return f"regular sha256={sha256(path)}"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"unexpected-mode={oct(mode)}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[rel] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(mode):
            entries[rel] = ("directory", None)
        elif stat.S_ISREG(mode):
            entries[rel] = ("regular", sha256(path))
        else:
            entries[rel] = (f"other:{oct(mode)}", None)
    return entries


def launcher_tree_sha256(root: Path) -> str:
    """Reimplement the launcher's length/type/size-delimited tree hash."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"not a real directory: {root}")
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
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


data = json.loads(AUDIT_INPUT.read_text())
assert data["record_layout"] == "legacy-selected-stage1"
assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"

required = [
    AUDIT_INPUT,
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/codex-trace"),
    Path("/candidate"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/reference/reference-semantics"),
    Path("/candidate/prompt.py"),
    Path("/candidate/py2mpy.py"),
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required.append(usage)

print("record_layout:", data["record_layout"])
print("semantics_mode:", data["semantics_mode"])
print("required mounted records:")
for path in required:
    print(f"  {path}: {describe(path)}")

print("container_paths:")
for name, raw_path in sorted(data["container_paths"].items()):
    path = Path(raw_path)
    print(f"  {name}: {path}: {describe(path)}")

lock_path = Path("/audit-campaign-lock.json")
lock = json.loads(lock_path.read_text())
print("campaign block equals lock:", data["audit_campaign"] == lock)
print(
    "campaign lock recorded hash matches:",
    sha256(lock_path) == data["hashes"]["audit_campaign_lock_sha256"],
)
print(
    "task manifest equals embedded manifest:",
    json.loads(Path("/task.json").read_text()) == data["manifest"],
)
print(
    "task manifest differs only by embedded config enrichment:",
    {
        key: value
        for key, value in data["manifest"].items()
        if key != "config"
    }
    == json.loads(Path("/task.json").read_text()),
)

file_hash_checks = {
    "/reference/canonical.py": "canonical_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
}
print("recorded file hash checks:")
for raw_path, key in file_hash_checks.items():
    path = Path(raw_path)
    actual = sha256(path)
    expected = data["hashes"][key]
    print(f"  {raw_path}: {actual == expected} actual={actual} expected={expected}")

print(
    "candidate prompt byte-identical to trusted:",
    Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
)
print(
    "candidate translator byte-identical to trusted:",
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes(),
)

candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
all_semantics_paths = sorted(candidate_semantics.keys() | trusted_semantics.keys())
differences = [
    (path, candidate_semantics.get(path), trusted_semantics.get(path))
    for path in all_semantics_paths
    if candidate_semantics.get(path) != trusted_semantics.get(path)
]
candidate_symlinks = [
    path for path, (kind, _) in candidate_semantics.items() if kind == "symlink"
]
print("candidate semantics entry count:", len(candidate_semantics))
print("trusted semantics entry count:", len(trusted_semantics))
print("candidate semantics symlinks:", candidate_symlinks)
print("candidate semantics exact recursive match:", not differences)
for difference in differences:
    print("  semantics difference:", difference)

trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
trace_bad_types = [
    (str(path), describe(path))
    for path in trace_files
    if not path.is_dir() and not path.is_file()
]
print("structured trace files:", [str(path) for path in trace_files if path.is_file()])
print("structured trace unexpected entries:", trace_bad_types)

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
print("generation-result evidence hash checks:")
for relative, expected in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / relative
    actual = sha256(path)
    print(f"  {relative}: {actual == expected} actual={actual} expected={expected}")

candidate_tree_hash = launcher_tree_sha256(Path("/candidate"))
semantics_tree_hash = launcher_tree_sha256(Path("/reference/reference-semantics"))
trace_tree_hash = launcher_tree_sha256(trace_root)
print("launcher-format independent tree hashes:")
print("  candidate:", candidate_tree_hash)
print("  trusted semantics:", semantics_tree_hash)
print("  structured trace:", trace_tree_hash)
print(
    "candidate tree matches generation-result retained workspace:",
    candidate_tree_hash == generation_result["outputs"]["workspace_sha256"],
)
print(
    "candidate tree matches invocation retained workspace:",
    candidate_tree_hash == invocation["retained_workspace_sha256"],
)
print(
    "trusted semantics matches recorded manifest-format hash:",
    semantics_tree_hash
    == data["hashes"]["trusted_reference_semantics_manifest_sha256"],
)
usage_data = json.loads(Path("/generation-evidence/usage.json").read_text())
print(
    "trace tree matches usage source trace:",
    trace_tree_hash == usage_data["source_trace_sha256"],
)
