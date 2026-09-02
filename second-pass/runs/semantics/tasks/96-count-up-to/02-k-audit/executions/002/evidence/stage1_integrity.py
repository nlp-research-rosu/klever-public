#!/usr/bin/env python3
"""Independent, read-only integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def describe(path: Path) -> tuple[str, int]:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file", path.lstat().st_size
    if stat.S_ISDIR(mode):
        return "directory", path.lstat().st_size
    if stat.S_ISLNK(mode):
        return "symlink", path.lstat().st_size
    return "other", path.lstat().st_size


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        here = Path(directory)
        for name in sorted(dirnames + filenames):
            path = here / name
            rel = path.relative_to(root).as_posix()
            kind, _ = describe(path)
            entries[rel] = (kind, digest(path) if kind == "file" else None)
    return entries


def check_file(label: str, path: Path, expected: str | None = None) -> bool:
    if not path.exists():
        print(f"{label}: MISSING {path}")
        return False
    kind, size = describe(path)
    if kind != "file":
        print(f"{label}: WRONG_TYPE kind={kind} path={path}")
        return False
    actual = digest(path)
    matches = expected is None or actual == expected
    print(
        f"{label}: kind=file size={size} sha256={actual}"
        + (f" expected={expected} match={matches}" if expected else "")
    )
    return matches


def main() -> int:
    with AUDIT_INPUT.open("r", encoding="utf-8") as stream:
        audit = json.load(stream)
    with LOCK.open("r", encoding="utf-8") as stream:
        lock = json.load(stream)

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_object_match={lock == audit['audit_campaign']}")

    hashes = audit["hashes"]
    checks = [
        ("audit_campaign_lock", LOCK, hashes["audit_campaign_lock_sha256"]),
        ("run_manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task_manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        ("stage1_result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
        (
            "generation_invocation",
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
        (
            "candidate_prompt",
            Path("/candidate/prompt.py"),
            hashes["candidate_prompt_sha256"],
        ),
        (
            "trusted_prompt",
            Path("/reference/prompt.py"),
            hashes["trusted_prompt_sha256"],
        ),
        (
            "candidate_translator",
            Path("/candidate/py2mpy.py"),
            hashes["candidate_translator_sha256"],
        ),
        (
            "trusted_translator",
            Path("/reference/py2mpy.py"),
            hashes["trusted_translator_sha256"],
        ),
        (
            "canonical",
            Path("/reference/canonical.py"),
            hashes["canonical_sha256"],
        ),
    ]
    ok = all(check_file(*item) for item in checks)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
    print(f"trace_regular_files={len(trace_files)}")
    for path in trace_files:
        print(
            f"trace_file={path.relative_to(trace_root).as_posix()} "
            f"sha256={digest(path)} size={path.stat().st_size}"
        )
    special_trace = [
        path
        for path in trace_root.rglob("*")
        if path.is_symlink() or (not path.is_file() and not path.is_dir())
    ]
    print(f"trace_special_entries={len(special_trace)}")
    ok &= len(trace_files) > 0 and not special_trace

    required_proof = [
        Path("/candidate/solution.py"),
        Path("/candidate/solution.mpy"),
        Path("/candidate/verification.k"),
        Path("/candidate/spec.k"),
        Path("/candidate/prove.sh"),
    ]
    for path in required_proof:
        ok &= check_file(f"proof_artifact:{path.name}", path)

    prompt_same = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_same = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"candidate_prompt_byte_identical={prompt_same}")
    print(f"candidate_translator_byte_identical={translator_same}")
    ok &= prompt_same and translator_same

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    print(f"candidate_semantics_entries={len(candidate_semantics)}")
    print(f"trusted_semantics_entries={len(trusted_semantics)}")
    missing = sorted(set(trusted_semantics) - set(candidate_semantics))
    additional = sorted(set(candidate_semantics) - set(trusted_semantics))
    changed = sorted(
        rel
        for rel in set(candidate_semantics) & set(trusted_semantics)
        if candidate_semantics[rel] != trusted_semantics[rel]
    )
    print(f"semantics_missing={missing}")
    print(f"semantics_additional={additional}")
    print(f"semantics_changed_or_mistyped={changed}")
    candidate_symlinks = sorted(
        rel for rel, (kind, _) in candidate_semantics.items() if kind == "symlink"
    )
    trusted_symlinks = sorted(
        rel for rel, (kind, _) in trusted_semantics.items() if kind == "symlink"
    )
    print(f"candidate_semantics_symlinks={candidate_symlinks}")
    print(f"trusted_semantics_symlinks={trusted_symlinks}")
    semantics_same = (
        not missing
        and not additional
        and not changed
        and not candidate_symlinks
        and not trusted_symlinks
    )
    print(f"semantics_tree_exact_match={semantics_same}")
    ok &= semantics_same

    print(f"OVERALL_STAGE1_INTEGRITY={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
