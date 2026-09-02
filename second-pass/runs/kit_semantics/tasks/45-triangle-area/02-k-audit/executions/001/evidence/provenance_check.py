#!/usr/bin/env python3
"""Independent launcher-record and mounted-input integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lstat_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_content_equal={audit['audit_campaign'] == lock}")
    actual_lock_hash = sha256_file(LOCK)
    expected_lock_hash = audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"audit_campaign_lock_sha256={actual_lock_hash}")
    print(f"campaign_hash_matches={actual_lock_hash == expected_lock_hash}")

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
        print(
            f"required path={path} exists={path.exists()} readable={os.access(path, os.R_OK)} "
            f"kind={lstat_kind(path)}"
        )

    recorded_hashes = {
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
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
    all_hashes_match = True
    for path, key in recorded_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        matches = actual == expected
        all_hashes_match &= matches
        print(f"hash path={path} actual={actual} expected={expected} matches={matches}")

    candidate_files = sorted(
        str(path.relative_to("/candidate"))
        for path in Path("/candidate").rglob("*")
        if path.is_symlink()
    )
    trusted_files = sorted(
        str(path.relative_to("/reference"))
        for path in Path("/reference").rglob("*")
        if path.is_symlink()
    )
    generation_files = sorted(
        str(path.relative_to("/generation-evidence"))
        for path in Path("/generation-evidence").rglob("*")
        if path.is_symlink()
    )
    print(f"candidate_symlinks={candidate_files}")
    print(f"reference_symlinks={trusted_files}")
    print(f"generation_symlinks={generation_files}")
    print(f"all_recorded_file_hashes_match={all_hashes_match}")
    return 0 if all_hashes_match and audit["audit_campaign"] == lock else 1


if __name__ == "__main__":
    raise SystemExit(main())
