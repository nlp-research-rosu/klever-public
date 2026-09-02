#!/usr/bin/env python3
"""Independent mounted-input and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def mode_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def tree_entries(root: Path) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            kind = mode_kind(path)
            if kind == "file":
                payload = sha256(path)
            elif kind == "symlink":
                payload = os.readlink(path)
            else:
                payload = ""
            entries[relative] = (kind, payload)
    return entries


def tree_manifest_digest(entries: dict[str, tuple[str, str]]) -> str:
    payload = "".join(
        f"{name}\0{kind}\0{value}\n"
        for name, (kind, value) in sorted(entries.items())
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def report_hash(label: str, path: Path, expected: str | None) -> bool:
    actual = sha256(path)
    status = "MATCH" if expected == actual else "MISMATCH"
    print(f"HASH {label}: {status} actual={actual} expected={expected}")
    return expected == actual


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())

    if audit["audit_campaign"] == lock:
        print("CAMPAIGN_BLOCK: MATCH")
    else:
        print("CAMPAIGN_BLOCK: MISMATCH")
        failures.append("campaign block")

    if not report_hash(
        "audit_campaign_lock",
        CAMPAIGN_LOCK,
        audit["hashes"]["audit_campaign_lock_sha256"],
    ):
        failures.append("campaign lock hash")

    if audit.get("record_layout") != "pipeline-v3":
        failures.append(f"unexpected record layout {audit.get('record_layout')!r}")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append(f"unexpected semantics mode {audit.get('semantics_mode')!r}")
    print(f"RECORD_LAYOUT: {audit.get('record_layout')}")
    print(f"SEMANTICS_MODE: {audit.get('semantics_mode')}")

    required_files = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
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
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    ]

    for path in required_files:
        kind = mode_kind(path) if os.path.lexists(path) else "missing"
        readable = os.access(path, os.R_OK)
        print(f"REQUIRED_FILE {path}: kind={kind} readable={readable}")
        if kind != "file" or not readable:
            failures.append(f"required file {path}")
    for path in required_dirs:
        kind = mode_kind(path) if os.path.lexists(path) else "missing"
        readable = os.access(path, os.R_OK | os.X_OK)
        print(f"REQUIRED_DIR {path}: kind={kind} readable={readable}")
        if kind != "dir" or not readable:
            failures.append(f"required dir {path}")

    hash_checks = [
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted_prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        ("trusted_translator", Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        ("candidate_prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("candidate_translator", Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        ("run_manifest", Path("/run.json"), "run_manifest_sha256"),
        ("task_manifest", Path("/task.json"), "task_manifest_sha256"),
        ("stage1_result", Path("/generation-result.json"), "stage1_result_sha256"),
        (
            "stage1_invocation",
            Path("/generation-evidence/invocation.json"),
            "stage1_invocation_sha256",
        ),
        (
            "generation_metrics",
            Path("/generation-evidence/metrics.json"),
            "generation_metrics_sha256",
        ),
        (
            "generation_runtime_metrics",
            Path("/generation-evidence/runtime-metrics.json"),
            "generation_runtime_metrics_sha256",
        ),
        (
            "generation_usage",
            Path("/generation-evidence/usage.json"),
            "generation_usage_sha256",
        ),
        (
            "generation_codex_last",
            Path("/generation-evidence/codex-last.txt"),
            "generation_codex_last_sha256",
        ),
        (
            "generation_codex_output",
            Path("/generation-evidence/codex-output.log"),
            "generation_codex_output_sha256",
        ),
        (
            "generation_prompt",
            Path("/generation-evidence/prompt.txt"),
            "generation_prompt_sha256",
        ),
    ]
    for label, path, key in hash_checks:
        if not report_hash(label, path, audit["hashes"].get(key)):
            failures.append(f"hash {label}")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    recorded_evidence = generation_result["outputs"]["evidence"]
    for relative, expected in sorted(recorded_evidence.items()):
        path = Path("/generation-evidence") / relative
        if mode_kind(path) != "file":
            print(f"RESULT_EVIDENCE {relative}: missing-or-mistyped")
            failures.append(f"result evidence {relative}")
            continue
        if not report_hash(f"result_evidence/{relative}", path, expected):
            failures.append(f"result evidence hash {relative}")

    candidate_prompt_equal = (
        Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    )
    candidate_translator_equal = (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print(f"CANDIDATE_PROMPT_BYTE_IDENTITY: {candidate_prompt_equal}")
    print(f"CANDIDATE_TRANSLATOR_BYTE_IDENTITY: {candidate_translator_equal}")
    if not candidate_prompt_equal:
        failures.append("candidate prompt differs")
    if not candidate_translator_equal:
        failures.append("candidate translator differs")

    candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
    candidate_digest = tree_manifest_digest(candidate_semantics)
    trusted_digest = tree_manifest_digest(trusted_semantics)
    print(f"CANDIDATE_SEMANTICS_INDEPENDENT_MANIFEST_SHA256: {candidate_digest}")
    print(f"TRUSTED_SEMANTICS_INDEPENDENT_MANIFEST_SHA256: {trusted_digest}")
    missing = sorted(set(trusted_semantics) - set(candidate_semantics))
    additional = sorted(set(candidate_semantics) - set(trusted_semantics))
    changed = sorted(
        key
        for key in set(trusted_semantics) & set(candidate_semantics)
        if trusted_semantics[key] != candidate_semantics[key]
    )
    print(f"SEMANTICS_MISSING: {missing}")
    print(f"SEMANTICS_ADDITIONAL: {additional}")
    print(f"SEMANTICS_CHANGED_OR_MISTYPED: {changed}")
    if missing or additional or changed:
        failures.append("supplied semantics tree mismatch")

    for root in [
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
    ]:
        symlinks = sorted(
            relative
            for relative, (kind, _) in tree_entries(root).items()
            if kind == "symlink"
        )
        print(f"SYMLINKS {root}: {symlinks}")
        if symlinks:
            failures.append(f"symlinks under {root}")

    trace_entries = tree_entries(Path("/generation-evidence/codex-trace"))
    print(
        "TRACE_INDEPENDENT_MANIFEST_SHA256: "
        f"{tree_manifest_digest(trace_entries)} entries={len(trace_entries)}"
    )

    print(f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
