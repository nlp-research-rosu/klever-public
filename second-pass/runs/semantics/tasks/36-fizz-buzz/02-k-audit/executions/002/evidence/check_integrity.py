#!/usr/bin/env python3
"""Independent, read-only integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def tree_inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            digest = sha256(path) if kind == "file" else None
            result[rel] = (kind, digest)
    return result


def check_declared_hash(
    label: str, path: Path, key: str, audit: dict[str, object]
) -> None:
    expected = audit["hashes"][key]  # type: ignore[index]
    actual = sha256(path)
    print(
        f"HASH {label}: actual={actual} expected={expected} "
        f"match={actual == expected}"
    )


audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal={audit['audit_campaign'] == lock}")
check_declared_hash(
    "audit_campaign_lock",
    CAMPAIGN_LOCK,
    "audit_campaign_lock_sha256",
    audit,
)

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    GENERATION / "invocation.json",
    GENERATION / "metrics.json",
    GENERATION / "codex-last.txt",
    GENERATION / "codex-output.log",
    GENERATION / "prompt.txt",
    GENERATION / "codex-trace",
]
for path in required:
    kind = entry_kind(path) if os.path.lexists(path) else "missing"
    readable = os.access(path, os.R_OK) if os.path.lexists(path) else False
    print(f"REQUIRED {path}: kind={kind} readable={readable}")

optional_usage = GENERATION / "usage.json"
print(
    f"OPTIONAL {optional_usage}: kind={entry_kind(optional_usage)} "
    f"readable={os.access(optional_usage, os.R_OK)}"
)

declared_files = [
    ("run", Path("/run.json"), "run_manifest_sha256"),
    ("task", Path("/task.json"), "task_manifest_sha256"),
    ("generation_result", Path("/generation-result.json"), "stage1_result_sha256"),
    (
        "generation_invocation",
        GENERATION / "invocation.json",
        "stage1_invocation_sha256",
    ),
    ("generation_metrics", GENERATION / "metrics.json", "generation_metrics_sha256"),
    ("generation_usage", GENERATION / "usage.json", "generation_usage_sha256"),
    (
        "generation_codex_last",
        GENERATION / "codex-last.txt",
        "generation_codex_last_sha256",
    ),
    (
        "generation_codex_output",
        GENERATION / "codex-output.log",
        "generation_codex_output_sha256",
    ),
    ("generation_prompt", GENERATION / "prompt.txt", "generation_prompt_sha256"),
    ("canonical", REFERENCE / "canonical.py", "canonical_sha256"),
    ("trusted_prompt", REFERENCE / "prompt.py", "trusted_prompt_sha256"),
    ("candidate_prompt", CANDIDATE / "prompt.py", "candidate_prompt_sha256"),
    ("trusted_translator", REFERENCE / "py2mpy.py", "trusted_translator_sha256"),
    ("candidate_translator", CANDIDATE / "py2mpy.py", "candidate_translator_sha256"),
]
for args in declared_files:
    check_declared_hash(*args, audit)

generation_result = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
invocation = json.loads(
    (GENERATION / "invocation.json").read_text(encoding="utf-8")
)
trace_files = sorted((GENERATION / "codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
print(f"trace_regular_files={len(trace_files)}")
for path in trace_files:
    rel = path.relative_to(GENERATION).as_posix()
    actual = sha256(path)
    result_expected = generation_result["outputs"]["evidence"].get(rel)
    invocation_expected = invocation["outputs"]["evidence"].get(rel)
    print(
        f"TRACE {rel}: sha256={actual} "
        f"result_match={actual == result_expected} "
        f"invocation_match={actual == invocation_expected}"
    )

prompt_same = (REFERENCE / "prompt.py").read_bytes() == (
    CANDIDATE / "prompt.py"
).read_bytes()
translator_same = (REFERENCE / "py2mpy.py").read_bytes() == (
    CANDIDATE / "py2mpy.py"
).read_bytes()
print(f"candidate_prompt_byte_identical={prompt_same}")
print(f"candidate_translator_byte_identical={translator_same}")

trusted_semantics = tree_inventory(REFERENCE / "reference-semantics")
candidate_semantics = tree_inventory(CANDIDATE / "reference-semantics")
missing = sorted(set(trusted_semantics) - set(candidate_semantics))
additional = sorted(set(candidate_semantics) - set(trusted_semantics))
changed = sorted(
    rel
    for rel in set(trusted_semantics) & set(candidate_semantics)
    if trusted_semantics[rel] != candidate_semantics[rel]
)
kind_counts = Counter(kind for kind, _ in candidate_semantics.values())
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"candidate_semantics_kind_counts={dict(sorted(kind_counts.items()))}")
print(f"semantics_missing={missing}")
print(f"semantics_additional={additional}")
print(f"semantics_changed_or_mistyped={changed}")
print(f"semantics_trees_exact={not (missing or additional or changed)}")

candidate_inventory = tree_inventory(CANDIDATE)
reference_inventory = tree_inventory(REFERENCE)
print("CANDIDATE_FILE_HASHES_BEGIN")
for rel, (kind, digest) in sorted(candidate_inventory.items()):
    if kind == "file":
        print(f"{digest}  {rel}")
    else:
        print(f"{kind}  {rel}")
print("CANDIDATE_FILE_HASHES_END")
print("REFERENCE_FILE_HASHES_BEGIN")
for rel, (kind, digest) in sorted(reference_inventory.items()):
    if kind == "file":
        print(f"{digest}  {rel}")
    else:
        print(f"{kind}  {rel}")
print("REFERENCE_FILE_HASHES_END")
