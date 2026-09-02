#!/usr/bin/env python3
"""Independent launcher-input and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def inventory(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[rel] = ("dir", "")
            elif stat.S_ISREG(mode):
                result[rel] = ("file", digest(path))
            else:
                result[rel] = ("other", oct(mode))
    return result


def tree_manifest_digest(entries: dict[str, tuple[str, str]]) -> str:
    data = "".join(
        f"{kind}\t{path}\t{value}\n"
        for path, (kind, value) in sorted(entries.items())
    ).encode()
    return hashlib.sha256(data).hexdigest()


failures: list[str] = []


def check(condition: bool, label: str) -> None:
    print(f"{'OK' if condition else 'FAIL'}: {label}")
    if not condition:
        failures.append(label)


data = json.loads(AUDIT_INPUT.read_text())
check(data["record_layout"] == "pipeline-v3", "record layout is pipeline-v3")
check(
    data["semantics_mode"] == "SUPPLIED_SEMANTICS",
    "rendered semantics mode is SUPPLIED_SEMANTICS",
)

lock_path = Path(data["container_paths"]["audit_campaign_lock"])
check(regular_nonsymlink(AUDIT_INPUT), "/audit-input.json is a regular non-symlink")
check(regular_nonsymlink(lock_path), "campaign lock is a regular non-symlink")
if regular_nonsymlink(lock_path):
    lock = json.loads(lock_path.read_text())
    check(lock == data["audit_campaign"], "campaign lock JSON equals audit campaign block")
    actual_lock_hash = digest(lock_path)
    print(f"SHA256 {lock_path}: {actual_lock_hash}")
    check(
        actual_lock_hash == data["hashes"]["audit_campaign_lock_sha256"],
        "campaign lock hash matches audit-input",
    )

required = {
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
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
for path_text, key in required.items():
    path = Path(path_text)
    check(regular_nonsymlink(path), f"{path} is a readable regular non-symlink")
    if regular_nonsymlink(path):
        actual = digest(path)
        print(f"SHA256 {path}: {actual}")
        check(actual == data["hashes"][key], f"{path} hash matches audit-input")

trace_root = Path(data["container_paths"]["generation_trace"])
check(trace_root.is_dir() and not trace_root.is_symlink(), "trace root is a real directory")
trace_entries = inventory(trace_root) if trace_root.is_dir() else {}
trace_files = {
    rel: value
    for rel, (kind, value) in trace_entries.items()
    if kind == "file"
}
check(bool(trace_files), "structured trace contains regular files")
check(
    all(kind in {"dir", "file"} for kind, _ in trace_entries.values()),
    "structured trace contains no symlink or special entries",
)
result_json = json.loads(Path("/generation-result.json").read_text())
declared_trace = {
    key.removeprefix("codex-trace/"): value
    for key, value in result_json["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
check(trace_files == declared_trace, "trace file set and hashes match generation-result")
for rel, value in sorted(trace_files.items()):
    print(f"SHA256 {trace_root / rel}: {value}")

check(
    Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes(),
    "candidate prompt is byte-identical to trusted prompt",
)
check(
    Path("/candidate/py2mpy.py").read_bytes()
    == Path("/reference/py2mpy.py").read_bytes(),
    "candidate translator is byte-identical to trusted translator",
)

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
check(
    trusted_semantics.is_dir() and not trusted_semantics.is_symlink(),
    "trusted supplied semantics tree is present and not symlinked",
)
check(
    candidate_semantics.is_dir() and not candidate_semantics.is_symlink(),
    "candidate supplied semantics tree is present and not symlinked",
)
trusted_entries = inventory(trusted_semantics) if trusted_semantics.is_dir() else {}
candidate_entries = inventory(candidate_semantics) if candidate_semantics.is_dir() else {}
print(
    "TRUSTED_SEMANTICS_MANIFEST_SHA256:",
    tree_manifest_digest(trusted_entries),
)
print(
    "CANDIDATE_SEMANTICS_MANIFEST_SHA256:",
    tree_manifest_digest(candidate_entries),
)
check(
    all(kind in {"dir", "file"} for kind, _ in trusted_entries.values()),
    "trusted semantics has only directories and regular files",
)
check(
    all(kind in {"dir", "file"} for kind, _ in candidate_entries.values()),
    "candidate semantics has only directories and regular files",
)
check(
    candidate_entries == trusted_entries,
    "candidate supplied-semantics tree exactly matches trusted tree recursively",
)
if candidate_entries != trusted_entries:
    all_paths = sorted(set(candidate_entries) | set(trusted_entries))
    for rel in all_paths:
        if candidate_entries.get(rel) != trusted_entries.get(rel):
            print(
                "SEMANTICS_DIFFERENCE",
                rel,
                "candidate=",
                candidate_entries.get(rel),
                "trusted=",
                trusted_entries.get(rel),
            )

candidate_top = Path("/candidate")
check(candidate_top.is_dir() and not candidate_top.is_symlink(), "candidate mount is a real directory")
candidate_inventory = inventory(candidate_top)
print("CANDIDATE_INDEPENDENT_MANIFEST_SHA256:", tree_manifest_digest(candidate_inventory))
print("CANDIDATE_ENTRY_COUNT:", len(candidate_inventory))
print("INTEGRITY_FAILURE_COUNT:", len(failures))
if failures:
    for item in failures:
        print("INTEGRITY_FAILURE:", item)
    sys.exit(1)
