#!/usr/bin/env python3
"""Independently check launcher records and the mounted provenance inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    type_ok = regular_nonsymlink(path)
    actual = sha256(path) if type_ok else None
    match = actual == expected if expected is not None else None
    print(
        f"{label}: path={path} regular_nonsymlink={type_ok} "
        f"actual={actual} expected={expected} match={match}"
    )
    return type_ok and (expected is None or match)


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit["hashes"]
    ok = True

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    lock_equal = lock == audit["audit_campaign"]
    print(f"campaign_lock_structural_equality={lock_equal}")
    ok &= lock_equal

    checks = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
        ("trusted_prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
        ("trusted_translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
        ("candidate_prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
        ("candidate_translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        (
            "stage1_invocation",
            Path("/generation-evidence/invocation.json"),
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        ),
        (
            "generation_last",
            Path("/generation-evidence/codex-last.txt"),
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation_output",
            Path("/generation-evidence/codex-output.log"),
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            hashes["generation_prompt_sha256"],
        ),
    ]
    for label, path, expected in checks:
        ok &= report_hash(label, path, expected)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    trace_symlinks = sorted(path for path in trace_root.rglob("*") if path.is_symlink())
    print(f"trace_regular_file_count={len(trace_files)}")
    print(f"trace_symlink_count={len(trace_symlinks)}")
    for path in trace_files:
        print(f"trace_file={path.relative_to(trace_root)} sha256={sha256(path)}")
    ok &= len(trace_files) == 1 and not trace_symlinks

    result = json.loads(Path("/generation-result.json").read_text())
    declared = result["outputs"]["evidence"]
    for rel, expected in sorted(declared.items()):
        path = Path("/generation-evidence") / rel
        ok &= report_hash(f"generation_result_output[{rel}]", path, expected)

    candidate_files = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    for path in candidate_files:
        ok &= report_hash(f"required_candidate[{path.name}]", path, None)

    print(f"OVERALL_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
