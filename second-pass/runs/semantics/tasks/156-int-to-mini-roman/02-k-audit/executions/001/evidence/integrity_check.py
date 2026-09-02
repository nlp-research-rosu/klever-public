#!/usr/bin/env python3
"""Independent mounted-input and pipeline-v3 provenance integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def regular_readable(path: Path) -> bool:
    try:
        mode = path.lstat().st_mode
    except OSError:
        return False
    return stat.S_ISREG(mode) and os.access(path, os.R_OK)


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            entries[rel] = ("symlink", os.readlink(path))
        elif stat.S_ISDIR(mode):
            entries[rel] = ("dir", None)
        elif stat.S_ISREG(mode):
            entries[rel] = ("file", digest(path))
        else:
            entries[rel] = ("other", oct(mode))
    return entries


def compare_tree(left: Path, right: Path) -> list[str]:
    left_entries = tree_entries(left)
    right_entries = tree_entries(right)
    differences: list[str] = []
    for rel in sorted(set(left_entries) | set(right_entries)):
        if rel not in left_entries:
            differences.append(f"missing candidate entry: {rel}")
        elif rel not in right_entries:
            differences.append(f"additional candidate entry: {rel} {left_entries[rel]}")
        elif left_entries[rel] != right_entries[rel]:
            differences.append(
                f"changed/mistyped candidate entry: {rel} "
                f"candidate={left_entries[rel]} trusted={right_entries[rel]}"
            )
    return differences


def check_file(
    label: str,
    path: Path,
    expected: str | None,
    failures: list[str],
) -> None:
    if not regular_readable(path):
        failures.append(f"{label}: absent, unreadable, symlinked, or not regular: {path}")
        print(f"FAIL {label}: {path}")
        return
    actual = digest(path)
    status = "OK" if expected is None or actual == expected else "FAIL"
    print(f"{status} {label}: sha256={actual} path={path}")
    if expected is not None and actual != expected:
        failures.append(f"{label}: expected {expected}, got {actual}")


def main() -> int:
    failures: list[str] = []
    audit = json.loads(AUDIT.read_text())
    hashes = audit["hashes"]
    paths = audit["container_paths"]

    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "pipeline-v3":
        failures.append("record_layout is not pipeline-v3")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        failures.append("semantics_mode is not SUPPLIED_SEMANTICS")

    required = {
        "audit campaign lock": (
            Path(paths["audit_campaign_lock"]),
            hashes["audit_campaign_lock_sha256"],
        ),
        "run manifest": (Path(paths["run_manifest"]), hashes["run_manifest_sha256"]),
        "task manifest": (Path(paths["task_manifest"]), hashes["task_manifest_sha256"]),
        "generation result": (
            Path(paths["stage1_result"]),
            hashes["stage1_result_sha256"],
        ),
        "generation invocation": (
            Path(paths["generation_manifest"]),
            hashes["stage1_invocation_sha256"],
        ),
        "generation metrics": (
            Path(paths["generation_metrics"]),
            hashes["generation_metrics_sha256"],
        ),
        "generation runtime metrics": (
            Path(paths["generation_root"]) / "runtime-metrics.json",
            hashes["generation_runtime_metrics_sha256"],
        ),
        "generation usage": (
            Path(paths["generation_root"]) / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        "generation last": (
            Path(paths["generation_last"]),
            hashes["generation_codex_last_sha256"],
        ),
        "generation output": (
            Path(paths["generation_output"]),
            hashes["generation_codex_output_sha256"],
        ),
        "generation prompt": (
            Path(paths["generation_root"]) / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        "canonical": (Path(paths["canonical"]), hashes["canonical_sha256"]),
        "trusted prompt": (
            Path(paths["trusted_prompt"]),
            hashes["trusted_prompt_sha256"],
        ),
        "trusted translator": (
            Path(paths["translator"]),
            hashes["trusted_translator_sha256"],
        ),
        "candidate prompt": (
            Path(paths["candidate"]) / "prompt.py",
            hashes["candidate_prompt_sha256"],
        ),
        "candidate translator": (
            Path(paths["candidate"]) / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    }
    for label, (path, expected) in required.items():
        check_file(label, path, expected, failures)

    lock = json.loads(Path(paths["audit_campaign_lock"]).read_text())
    if lock == audit["audit_campaign"]:
        print("OK campaign lock JSON exactly equals audit_campaign block")
    else:
        failures.append("campaign lock JSON differs from audit_campaign block")
        print("FAIL campaign lock JSON differs from audit_campaign block")

    byte_pairs = (
        ("candidate prompt", Path("/candidate/prompt.py"), Path("/reference/prompt.py")),
        (
            "candidate translator",
            Path("/candidate/py2mpy.py"),
            Path("/reference/py2mpy.py"),
        ),
    )
    for label, candidate, trusted in byte_pairs:
        if candidate.read_bytes() == trusted.read_bytes():
            print(f"OK {label} is byte-identical to trusted mount")
        else:
            failures.append(f"{label} differs from trusted mount")
            print(f"FAIL {label} differs from trusted mount")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    if not trusted_semantics.is_dir():
        failures.append("trusted supplied semantics tree is absent")
        print("FAIL trusted supplied semantics tree is absent")
    elif not candidate_semantics.is_dir():
        failures.append("candidate supplied semantics tree is absent")
        print("FAIL candidate supplied semantics tree is absent")
    else:
        differences = compare_tree(candidate_semantics, trusted_semantics)
        if differences:
            failures.extend(differences)
            for difference in differences:
                print(f"FAIL supplied-semantics integrity: {difference}")
        else:
            entries = tree_entries(candidate_semantics)
            files = sum(kind == "file" for kind, _ in entries.values())
            directories = sum(kind == "dir" for kind, _ in entries.values())
            print(
                "OK supplied-semantics trees recursively identical "
                f"({files} files, {directories} subdirectories, no symlinks)"
            )

    result = json.loads(Path(paths["stage1_result"]).read_text())
    expected_evidence = result["outputs"]["evidence"]
    evidence_root = Path(paths["generation_root"])
    for rel, expected in sorted(expected_evidence.items()):
        check_file(f"generation-result evidence {rel}", evidence_root / rel, expected, failures)

    trace_root = Path(paths["generation_trace"])
    trace_entries = tree_entries(trace_root) if trace_root.is_dir() else {}
    trace_files = sorted(rel for rel, (kind, _) in trace_entries.items() if kind == "file")
    trace_bad = sorted(rel for rel, (kind, _) in trace_entries.items() if kind != "file" and kind != "dir")
    print(f"structured trace files={trace_files}")
    if not trace_files:
        failures.append("structured trace has no regular files")
    if trace_bad:
        failures.append(f"structured trace has non-regular entries: {trace_bad}")

    proof_required = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for rel in proof_required:
        path = Path(paths["candidate"]) / rel
        check_file(f"candidate proof artifact {rel}", path, None, failures)

    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
