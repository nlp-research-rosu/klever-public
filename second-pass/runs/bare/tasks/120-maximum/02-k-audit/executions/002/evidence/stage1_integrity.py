#!/usr/bin/env python3
"""Independent provenance/type/hash checks for the 120-maximum audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def inspect_required(path: Path) -> None:
    readable = os.access(path, os.R_OK)
    print(f"REQUIRED {path}: exists={path.exists()} kind={kind(path) if os.path.lexists(path) else 'missing'} readable={readable}")


def tree_ledger(root: Path) -> str:
    """Print a complete typed, per-file hash ledger and hash that ledger."""
    rows: list[str] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        entry_kind = kind(path)
        mode = stat.S_IMODE(path.lstat().st_mode)
        if entry_kind == "regular":
            detail = sha256_file(path)
        elif entry_kind == "symlink":
            detail = os.readlink(path)
        else:
            detail = "-"
        rows.append(f"{rel}\t{entry_kind}\t{mode:04o}\t{detail}")
    for row in rows:
        print(f"TREE {root}: {row}")
    encoded = ("\n".join(rows) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def compare_hash(label: str, path: Path, expected: str | None) -> None:
    actual = sha256_file(path)
    print(f"HASH {label}: expected={expected} actual={actual} match={actual == expected}")


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"campaign_block_equals_lock={audit.get('audit_campaign') == lock}")
    print(f"reference_semantics_exists={os.path.lexists('/reference/reference-semantics')}")

    required = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/candidate"),
    ]
    if os.path.lexists("/generation-evidence/usage.json"):
        required.append(Path("/generation-evidence/usage.json"))
    for path in required:
        inspect_required(path)

    hashes = audit["hashes"]
    comparisons = [
        ("audit_campaign_lock", CAMPAIGN_LOCK, hashes["audit_campaign_lock_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        ("stage1_invocation", Path("/generation-evidence/invocation.json"), hashes["stage1_invocation_sha256"]),
        ("generation_metrics", Path("/generation-evidence/metrics.json"), hashes["generation_metrics_sha256"]),
        ("generation_usage", Path("/generation-evidence/usage.json"), hashes["generation_usage_sha256"]),
        ("generation_codex_last", Path("/generation-evidence/codex-last.txt"), hashes["generation_codex_last_sha256"]),
        ("generation_codex_output", Path("/generation-evidence/codex-output.log"), hashes["generation_codex_output_sha256"]),
        ("generation_prompt", Path("/generation-evidence/prompt.txt"), hashes["generation_prompt_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
    ]
    for label, path, expected in comparisons:
        compare_hash(label, path, expected)

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    for path in trace_files:
        print(f"TRACE_FILE {path}: sha256={sha256_file(path)}")

    for root in (Path("/candidate"), Path("/reference"), Path("/generation-evidence")):
        print(f"INDEPENDENT_TREE_LEDGER_SHA256 {root}: {tree_ledger(root)}")


if __name__ == "__main__":
    main()
