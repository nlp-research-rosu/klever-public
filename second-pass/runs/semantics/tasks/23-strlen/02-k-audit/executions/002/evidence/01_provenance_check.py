#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlinked: {path}"
    assert path.is_file(), f"not a regular file: {path}"


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    assert root.is_dir() and not root.is_symlink(), f"bad tree root: {root}"
    result: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        here = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = here / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("dir", None)
            elif path.is_file():
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
    return result


with AUDIT.open(encoding="utf-8") as stream:
    audit = json.load(stream)
with LOCK.open("rb") as stream:
    lock_bytes = stream.read()
lock = json.loads(lock_bytes)

print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit["audit_campaign"] == lock
actual_lock_hash = hashlib.sha256(lock_bytes).hexdigest()
print(f"campaign_block_equal=true")
print(f"audit_campaign_lock_sha256={actual_lock_hash}")
assert actual_lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required:
    require_regular(path)
require_regular(Path("/generation-evidence/usage.json"))

hash_checks = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/usage.json": "generation_usage_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
}
for raw_path, key in hash_checks.items():
    path = Path(raw_path)
    require_regular(path)
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"{key}: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

with Path("/generation-result.json").open(encoding="utf-8") as stream:
    generation_result = json.load(stream)
for relative, expected in generation_result["outputs"]["evidence"].items():
    path = Path("/generation-evidence") / relative
    require_regular(path)
    actual = sha256(path)
    print(f"generation_result[{relative}]: expected={expected} actual={actual} match={actual == expected}")
    assert actual == expected

candidate = Path("/candidate")
assert candidate.is_dir() and not candidate.is_symlink()
candidate_entries = tree_entries(candidate)
candidate_symlinks = sorted(k for k, (kind, _) in candidate_entries.items() if kind == "symlink")
print(f"candidate_entry_count={len(candidate_entries)}")
print(f"candidate_symlinks={candidate_symlinks}")
assert not candidate_symlinks

prompt_equal = Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
translator_equal = Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print(f"candidate_prompt_byte_equal={prompt_equal}")
print(f"candidate_translator_byte_equal={translator_equal}")
assert prompt_equal and translator_equal

trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_entries={len(trusted_semantics)}")
print(f"candidate_semantics_entries={len(candidate_semantics)}")
print(f"semantics_trees_type_and_byte_equal={trusted_semantics == candidate_semantics}")
assert trusted_semantics == candidate_semantics

print("PROVENANCE_CHECK=PASS")
