#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{mode:o}"


def tree_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    rows: list[tuple[str, str, str | None]] = []
    for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs.sort()
        files.sort()
        base_path = Path(base)
        for name in dirs + files:
            path = base_path / name
            rel = path.relative_to(root).as_posix()
            path_kind = kind(path)
            digest = sha256(path) if path_kind == "file" else None
            rows.append((rel, path_kind, digest))
    return rows


def compare_trees(left: Path, right: Path) -> list[str]:
    left_rows = {row[0]: row[1:] for row in tree_manifest(left)}
    right_rows = {row[0]: row[1:] for row in tree_manifest(right)}
    issues: list[str] = []
    for rel in sorted(left_rows.keys() | right_rows.keys()):
        if rel not in left_rows:
            issues.append(f"missing candidate entry: {rel}")
        elif rel not in right_rows:
            issues.append(f"additional candidate entry: {rel}")
        elif left_rows[rel] != right_rows[rel]:
            issues.append(
                f"changed/mistyped entry: {rel}: "
                f"candidate={left_rows[rel]} trusted={right_rows[rel]}"
            )
    return issues


def independent_tree_digest(root: Path) -> str:
    """Hash a canonical JSON serialization of relative path/type/file hashes."""
    payload = json.dumps(
        tree_manifest(root), ensure_ascii=False, separators=(",", ":")
    ).encode()
    return hashlib.sha256(payload).hexdigest()


audit_path = Path("/audit-input.json")
lock_path = Path("/audit-campaign-lock.json")
audit = json.loads(audit_path.read_text())
lock = json.loads(lock_path.read_text())

print(f"audit-input kind={kind(audit_path)} sha256={sha256(audit_path)}")
print(f"campaign-lock kind={kind(lock_path)} sha256={sha256(lock_path)}")
print(
    "campaign-lock recorded-hash match="
    f"{sha256(lock_path) == audit['hashes']['audit_campaign_lock_sha256']}"
)
print(f"campaign-lock structural match={lock == audit['audit_campaign']}")
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")

required = [
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
]
for path in required:
    print(f"required {path}: exists={path.exists()} kind={kind(path) if path.exists() else 'MISSING'}")

file_hash_checks = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
}
for path, key in file_hash_checks.items():
    if not path.exists():
        print(f"hash {path}: MISSING")
        continue
    actual = sha256(path)
    expected = audit["hashes"][key]
    print(f"hash {path}: {actual} recorded={expected} match={actual == expected}")

candidate_prompt = Path("/candidate/prompt.py").read_bytes()
trusted_prompt = Path("/reference/prompt.py").read_bytes()
candidate_translator = Path("/candidate/py2mpy.py").read_bytes()
trusted_translator = Path("/reference/py2mpy.py").read_bytes()
print(f"candidate prompt byte-identical={candidate_prompt == trusted_prompt}")
print(f"candidate translator byte-identical={candidate_translator == trusted_translator}")

candidate_semantics = Path("/candidate/reference-semantics")
trusted_semantics = Path("/reference/reference-semantics")
candidate_rows = tree_manifest(candidate_semantics)
trusted_rows = tree_manifest(trusted_semantics)
issues = compare_trees(candidate_semantics, trusted_semantics)
print(f"candidate semantics entries={len(candidate_rows)}")
print(f"trusted semantics entries={len(trusted_rows)}")
print(f"candidate semantics recursive exact match={not issues}")
print(
    "candidate semantics independent-manifest sha256="
    f"{independent_tree_digest(candidate_semantics)}"
)
print(
    "trusted semantics independent-manifest sha256="
    f"{independent_tree_digest(trusted_semantics)}"
)
for issue in issues:
    print(f"SEMANTICS ISSUE: {issue}")
for rel, entry_kind, digest in candidate_rows:
    print(f"SEMANTICS {entry_kind} {rel} {digest or '-'}")

generation_result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(generation_result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    actual = sha256(path) if path.exists() and kind(path) == "file" else None
    print(f"generation-result evidence {rel}: actual={actual} recorded={expected} match={actual == expected}")

all_symlinks = []
for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
    for rel, entry_kind, _ in tree_manifest(root):
        if entry_kind == "symlink":
            all_symlinks.append(f"{root}/{rel}")
print(f"symlink count across mounted candidate/reference/evidence trees={len(all_symlinks)}")
for path in all_symlinks:
    print(f"SYMLINK {path}")
for root in (
    Path("/candidate"),
    Path("/reference"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
):
    print(
        f"independent tree digest {root}: "
        f"{independent_tree_digest(root)} entries={len(tree_manifest(root))}"
    )
