#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        errors.append(f"missing/unreadable required file {path}: {err}")
        return
    if stat.S_ISLNK(mode):
        errors.append(f"required file is a symlink: {path}")
    elif not stat.S_ISREG(mode):
        errors.append(f"required file is not regular: {path}")


def compare_trees(left: Path, right: Path, errors: list[str]) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        found: dict[str, tuple[str, str | None]] = {}
        for base, dirs, files in os.walk(root, topdown=True, followlinks=False):
            base_path = Path(base)
            names = sorted(dirs + files)
            for name in names:
                path = base_path / name
                rel = path.relative_to(root).as_posix()
                mode = path.lstat().st_mode
                if stat.S_ISLNK(mode):
                    kind = "symlink"
                    digest = os.readlink(path)
                elif stat.S_ISDIR(mode):
                    kind = "directory"
                    digest = None
                elif stat.S_ISREG(mode):
                    kind = "file"
                    digest = sha256(path)
                else:
                    kind = "other"
                    digest = None
                found[rel] = (kind, digest)
            dirs[:] = [
                name
                for name in dirs
                if not (base_path / name).is_symlink()
            ]
        return found

    lhs = entries(left)
    rhs = entries(right)
    print(f"TREE {left}: {len(lhs)} entries")
    print(f"TREE {right}: {len(rhs)} entries")
    for rel in sorted(lhs.keys() | rhs.keys()):
        if rel not in lhs:
            errors.append(f"candidate semantics has additional entry: {rel}")
        elif rel not in rhs:
            errors.append(f"candidate semantics is missing entry: {rel}")
        elif lhs[rel] != rhs[rel]:
            errors.append(
                f"semantics entry mismatch {rel}: trusted={lhs[rel]} candidate={rhs[rel]}"
            )


def check_hash(
    path: Path, expected: str | None, label: str, errors: list[str]
) -> None:
    require_regular(path, errors)
    if not path.is_file() or path.is_symlink():
        return
    actual = sha256(path)
    print(f"SHA256 {label} {actual} {path}")
    if expected is not None and actual != expected:
        errors.append(f"hash mismatch {label}: expected {expected}, got {actual}")


def main() -> int:
    errors: list[str] = []
    require_regular(AUDIT_INPUT, errors)
    if errors:
        print("\n".join(f"ERROR {error}" for error in errors))
        return 1

    audit = json.loads(AUDIT_INPUT.read_text())
    paths = audit["container_paths"]
    hashes = audit["hashes"]
    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")

    if audit["record_layout"] != "legacy-selected-stage1":
        errors.append(f"unexpected record layout {audit['record_layout']!r}")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        errors.append(f"unexpected semantics mode {audit['semantics_mode']!r}")

    lock_path = Path(paths["audit_campaign_lock"])
    check_hash(
        lock_path,
        hashes["audit_campaign_lock_sha256"],
        "audit_campaign_lock",
        errors,
    )
    if lock_path.is_file():
        lock = json.loads(lock_path.read_text())
        if lock != audit["audit_campaign"]:
            errors.append("audit campaign lock differs from audit_input.audit_campaign")
        else:
            print("CAMPAIGN exact JSON object match")

    direct_hashes = [
        ("run_manifest", paths["run_manifest"], "run_manifest_sha256"),
        ("task_manifest", paths["task_manifest"], "task_manifest_sha256"),
        ("stage1_result", paths["stage1_result"], "stage1_result_sha256"),
        ("generation_manifest", paths["generation_manifest"], "stage1_invocation_sha256"),
        ("generation_metrics", paths["generation_metrics"], "generation_metrics_sha256"),
        ("generation_last", paths["generation_last"], "generation_codex_last_sha256"),
        ("generation_output", paths["generation_output"], "generation_codex_output_sha256"),
        ("trusted_prompt", paths["trusted_prompt"], "trusted_prompt_sha256"),
        ("canonical", paths["canonical"], "canonical_sha256"),
        ("translator", paths["translator"], "trusted_translator_sha256"),
    ]
    for label, path_text, hash_key in direct_hashes:
        check_hash(Path(path_text), hashes[hash_key], label, errors)

    generation_root = Path(paths["generation_root"])
    layout_required = [
        generation_root / "invocation.json",
        generation_root / "metrics.json",
        generation_root / "codex-last.txt",
        generation_root / "codex-output.log",
        generation_root / "prompt.txt",
    ]
    for path in layout_required:
        require_regular(path, errors)
    usage = generation_root / "usage.json"
    if usage.exists():
        check_hash(usage, hashes.get("generation_usage_sha256"), "generation_usage", errors)

    trace_root = Path(paths["generation_trace"])
    if not trace_root.is_dir() or trace_root.is_symlink():
        errors.append(f"required structured trace is absent, unreadable, or symlinked: {trace_root}")
    trace_files = sorted(trace_root.rglob("*")) if trace_root.is_dir() else []
    trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    trace_bad = [path for path in trace_files if path.is_symlink() or not path.is_file()]
    for path in trace_bad:
        if path.is_symlink():
            errors.append(f"structured trace contains symlink: {path}")
    if not trace_regular:
        errors.append("structured trace contains no regular records")
    for path in trace_regular:
        print(f"TRACE_SHA256 {sha256(path)} {path}")

    evidence_hashes = {}
    manifest_path = Path(paths["generation_manifest"])
    if manifest_path.is_file():
        invocation = json.loads(manifest_path.read_text())
        evidence_hashes = invocation.get("outputs", {}).get("evidence", {})
    for rel, expected in sorted(evidence_hashes.items()):
        check_hash(generation_root / rel, expected, f"invocation:{rel}", errors)

    candidate = Path(paths["candidate"])
    for rel in [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "prompt.py",
        "py2mpy.py",
    ]:
        require_regular(candidate / rel, errors)

    trusted_prompt = Path(paths["trusted_prompt"])
    candidate_prompt = candidate / "prompt.py"
    if trusted_prompt.is_file() and candidate_prompt.is_file():
        print(f"SHA256 candidate_prompt {sha256(candidate_prompt)} {candidate_prompt}")
        if trusted_prompt.read_bytes() != candidate_prompt.read_bytes():
            errors.append("candidate prompt differs byte-for-byte from trusted prompt")

    trusted_translator = Path(paths["translator"])
    candidate_translator = candidate / "py2mpy.py"
    if trusted_translator.is_file() and candidate_translator.is_file():
        print(f"SHA256 candidate_translator {sha256(candidate_translator)} {candidate_translator}")
        if trusted_translator.read_bytes() != candidate_translator.read_bytes():
            errors.append("candidate translator differs byte-for-byte from trusted translator")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = candidate / "reference-semantics"
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        errors.append("trusted supplied semantics mount is absent, mistyped, or symlinked")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        errors.append("candidate supplied semantics tree is absent, mistyped, or symlinked")
    if trusted_semantics.is_dir() and candidate_semantics.is_dir():
        compare_trees(trusted_semantics, candidate_semantics, errors)

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"RESULT FAIL ({len(errors)} integrity error(s))")
        return 1
    print("RESULT PASS (all required provenance and integrity checks passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
