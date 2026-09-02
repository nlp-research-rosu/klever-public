#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

The report uses per-file SHA-256 hashes and a documented manifest digest:
SHA256 of UTF-8 lines "<type>\\t<relative-path>\\t<file-sha-or-dash>\\n"
sorted by relative path.  This deliberately does not assume the launcher's
private directory-digest encoding.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as err:
        errors.append(f"absent/unreadable: {path}: {err}")
        return
    if stat.S_ISLNK(mode):
        errors.append(f"symlinked required file: {path}")
    elif not stat.S_ISREG(mode):
        errors.append(f"mistyped required file: {path}: mode={oct(mode)}")
    elif not os.access(path, os.R_OK):
        errors.append(f"unreadable required file: {path}")


def tree_entries(root: Path, errors: list[str]) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    try:
        root_mode = root.lstat().st_mode
    except OSError as err:
        errors.append(f"absent/unreadable tree: {root}: {err}")
        return entries
    if stat.S_ISLNK(root_mode) or not stat.S_ISDIR(root_mode):
        errors.append(f"tree root is symlinked or not a directory: {root}")
        return entries
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[rel] = ("symlink", os.readlink(path))
            errors.append(f"symlinked tree entry: {path} -> {os.readlink(path)}")
        elif stat.S_ISDIR(mode):
            entries[rel] = ("directory", "-")
        elif stat.S_ISREG(mode):
            entries[rel] = ("file", sha256(path))
        else:
            entries[rel] = ("other", oct(mode))
            errors.append(f"mistyped tree entry: {path}: mode={oct(mode)}")
    return entries


def manifest_digest(entries: dict[str, tuple[str, str]]) -> str:
    material = "".join(
        f"{kind}\t{rel}\t{value}\n"
        for rel, (kind, value) in sorted(entries.items())
    ).encode()
    return hashlib.sha256(material).hexdigest()


def compare_declared(
    label: str, path: Path, expected: str | None, errors: list[str]
) -> None:
    require_regular(path, errors)
    if path.is_file() and not path.is_symlink():
        actual = sha256(path)
        result = "OBSERVED" if expected is None else ("MATCH" if expected == actual else "MISMATCH")
        print(f"FILE_HASH {label} {result} expected={expected} actual={actual} path={path}")
        if expected is not None and actual != expected:
            errors.append(f"recorded hash mismatch for {label}: {path}")


def main() -> int:
    errors: list[str] = []
    require_regular(AUDIT_INPUT, errors)
    require_regular(LOCK, errors)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 2

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"RECORD_LAYOUT {audit.get('record_layout')}")
    print(f"SEMANTICS_MODE {audit.get('semantics_mode')}")

    if audit.get("record_layout") != "pipeline-v3":
        errors.append(f"unexpected record layout: {audit.get('record_layout')}")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append(f"unexpected semantics mode: {audit.get('semantics_mode')}")
    if audit.get("audit_campaign") != lock:
        errors.append("campaign lock JSON does not equal audit_campaign block")
    else:
        print("CAMPAIGN_BLOCK MATCH")

    hashes = audit.get("hashes", {})
    compare_declared(
        "audit_campaign_lock",
        LOCK,
        hashes.get("audit_campaign_lock_sha256"),
        errors,
    )

    declared_files = {
        "canonical": (Path("/reference/canonical.py"), hashes.get("canonical_sha256")),
        "trusted_prompt": (
            Path("/reference/prompt.py"),
            hashes.get("trusted_prompt_sha256"),
        ),
        "trusted_translator": (
            Path("/reference/py2mpy.py"),
            hashes.get("trusted_translator_sha256"),
        ),
        "run_manifest": (Path("/run.json"), hashes.get("run_manifest_sha256")),
        "task_manifest": (Path("/task.json"), hashes.get("task_manifest_sha256")),
        "stage1_result": (
            Path("/generation-result.json"),
            hashes.get("stage1_result_sha256"),
        ),
        "stage1_invocation": (
            Path("/generation-evidence/invocation.json"),
            hashes.get("stage1_invocation_sha256"),
        ),
        "generation_metrics": (
            Path("/generation-evidence/metrics.json"),
            hashes.get("generation_metrics_sha256"),
        ),
        "generation_runtime_metrics": (
            Path("/generation-evidence/runtime-metrics.json"),
            hashes.get("generation_runtime_metrics_sha256"),
        ),
        "generation_usage": (
            Path("/generation-evidence/usage.json"),
            hashes.get("generation_usage_sha256"),
        ),
        "generation_last": (
            Path("/generation-evidence/codex-last.txt"),
            hashes.get("generation_codex_last_sha256"),
        ),
        "generation_output": (
            Path("/generation-evidence/codex-output.log"),
            hashes.get("generation_codex_output_sha256"),
        ),
        "generation_prompt": (
            Path("/generation-evidence/prompt.txt"),
            hashes.get("generation_prompt_sha256"),
        ),
        "candidate_prompt": (
            Path("/candidate/prompt.py"),
            hashes.get("candidate_prompt_sha256"),
        ),
        "candidate_translator": (
            Path("/candidate/py2mpy.py"),
            hashes.get("candidate_translator_sha256"),
        ),
    }
    for label, (path, expected) in declared_files.items():
        compare_declared(label, path, expected, errors)

    for filename in (
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ):
        compare_declared(
            f"candidate_required:{filename}",
            Path("/candidate") / filename,
            None,
            errors,
        )

    for candidate, trusted, label in (
        (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
        (
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
            "translator",
        ),
    ):
        if candidate.read_bytes() == trusted.read_bytes():
            print(f"BYTE_COMPARE {label} MATCH")
        else:
            print(f"BYTE_COMPARE {label} MISMATCH")
            errors.append(f"candidate {label} differs from trusted mount")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    candidate_entries = tree_entries(candidate_semantics, errors)
    trusted_entries = tree_entries(trusted_semantics, errors)
    print(
        "TREE_MANIFEST candidate_reference_semantics "
        f"entries={len(candidate_entries)} digest={manifest_digest(candidate_entries)}"
    )
    print(
        "TREE_MANIFEST trusted_reference_semantics "
        f"entries={len(trusted_entries)} digest={manifest_digest(trusted_entries)}"
    )
    all_rel = sorted(set(candidate_entries) | set(trusted_entries))
    differences = [
        (rel, candidate_entries.get(rel), trusted_entries.get(rel))
        for rel in all_rel
        if candidate_entries.get(rel) != trusted_entries.get(rel)
    ]
    if differences:
        for rel, candidate_value, trusted_value in differences:
            print(
                "SEMANTICS_DIFF "
                f"{rel} candidate={candidate_value} trusted={trusted_value}"
            )
        errors.append(f"candidate/trusted semantics have {len(differences)} differences")
    else:
        print("SEMANTICS_RECURSIVE_COMPARE MATCH")

    generation_result = json.loads(Path("/generation-result.json").read_text())
    recorded_outputs = generation_result["outputs"]["evidence"]
    generation_root = Path("/generation-evidence")
    for rel, expected in sorted(recorded_outputs.items()):
        path = generation_root / rel
        compare_declared(f"generation_result:{rel}", path, expected, errors)

    trace_root = Path("/generation-evidence/codex-trace")
    trace_entries = tree_entries(trace_root, errors)
    trace_files = [
        rel for rel, (kind, _) in trace_entries.items() if kind == "file"
    ]
    if not trace_files:
        errors.append("structured trace tree contains no regular files")
    print(
        f"TREE_MANIFEST generation_trace entries={len(trace_entries)} "
        f"files={len(trace_files)} digest={manifest_digest(trace_entries)}"
    )

    candidate_entries_all = tree_entries(Path("/candidate"), errors)
    print(
        f"TREE_MANIFEST candidate entries={len(candidate_entries_all)} "
        f"digest={manifest_digest(candidate_entries_all)}"
    )

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"INTEGRITY_RESULT FAIL count={len(errors)}")
        return 1
    print("INTEGRITY_RESULT PASS count=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
