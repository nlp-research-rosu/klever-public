#!/usr/bin/env python3
"""Independent audit-input and mounted-artifact integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path, excluded_top_levels: frozenset[str] = frozenset()) -> str:
    """Reimplement the launcher tree digest, rejecting links/special entries."""
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"not a real directory: {root}")
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if relative.split("/", 1)[0] in excluded_top_levels:
                continue
            mode = child.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def real_directory(path: Path) -> bool:
    try:
        return stat.S_ISDIR(path.lstat().st_mode)
    except OSError:
        return False


def report_check(label: str, actual: Any, expected: Any) -> bool:
    ok = actual == expected
    print(f"{label}: {'OK' if ok else 'MISMATCH'}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    return ok


def main() -> int:
    failures = 0
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    paths = audit["container_paths"]
    hashes = audit["hashes"]

    print(f"record_layout: {audit['record_layout']}")
    print(f"semantics_mode: {audit['semantics_mode']}")
    if audit["record_layout"] != "legacy-selected-stage1":
        print("ERROR: unexpected record layout")
        failures += 1
    if audit["semantics_mode"] != "GENERATED_SEMANTICS":
        print("ERROR: unexpected semantics mode")
        failures += 1

    failures += not report_check("campaign block equals lock", audit["audit_campaign"], lock)
    failures += not report_check(
        "campaign lock hash",
        sha256_file(CAMPAIGN_LOCK),
        hashes["audit_campaign_lock_sha256"],
    )

    required_files = {
        "audit_input": AUDIT_INPUT,
        "audit_campaign_lock": CAMPAIGN_LOCK,
        "run_manifest": Path(paths["run_manifest"]),
        "task_manifest": Path(paths["task_manifest"]),
        "stage1_result": Path(paths["stage1_result"]),
        "generation_manifest": Path(paths["generation_manifest"]),
        "generation_metrics": Path(paths["generation_metrics"]),
        "generation_usage": Path(paths["generation_root"]) / "usage.json",
        "generation_last": Path(paths["generation_last"]),
        "generation_output": Path(paths["generation_output"]),
        "generation_prompt": Path(paths["generation_root"]) / "prompt.txt",
        "trusted_prompt": Path(paths["trusted_prompt"]),
        "translator": Path(paths["translator"]),
        "canonical": Path(paths["canonical"]),
    }
    required_directories = {
        "candidate": Path(paths["candidate"]),
        "generation_root": Path(paths["generation_root"]),
        "generation_trace": Path(paths["generation_trace"]),
    }
    for label, path in required_files.items():
        ok = regular_file(path)
        print(f"required regular file {label}: {'OK' if ok else 'MISSING_OR_MISTYPED'} {path}")
        failures += not ok
    for label, path in required_directories.items():
        ok = real_directory(path)
        print(f"required real directory {label}: {'OK' if ok else 'MISSING_OR_MISTYPED'} {path}")
        failures += not ok

    reference_semantics = Path("/reference/reference-semantics")
    boundary_ok = not reference_semantics.exists() and not reference_semantics.is_symlink()
    print(
        "generated-semantics boundary (/reference/reference-semantics absent): "
        f"{'OK' if boundary_ok else 'BREACH'}"
    )
    failures += not boundary_ok

    file_hash_checks = {
        "canonical": (Path(paths["canonical"]), "canonical_sha256"),
        "trusted_prompt": (Path(paths["trusted_prompt"]), "trusted_prompt_sha256"),
        "trusted_translator": (Path(paths["translator"]), "trusted_translator_sha256"),
        "candidate_prompt": (Path(paths["candidate"]) / "prompt.py", "candidate_prompt_sha256"),
        "candidate_translator": (
            Path(paths["candidate"]) / "py2mpy.py",
            "candidate_translator_sha256",
        ),
        "generation_invocation": (
            Path(paths["generation_manifest"]),
            "stage1_invocation_sha256",
        ),
        "generation_metrics": (
            Path(paths["generation_metrics"]),
            "generation_metrics_sha256",
        ),
        "generation_usage": (
            Path(paths["generation_root"]) / "usage.json",
            "generation_usage_sha256",
        ),
        "generation_last": (
            Path(paths["generation_last"]),
            "generation_codex_last_sha256",
        ),
        "generation_output": (
            Path(paths["generation_output"]),
            "generation_codex_output_sha256",
        ),
        "generation_prompt": (
            Path(paths["generation_root"]) / "prompt.txt",
            "generation_prompt_sha256",
        ),
        "run_manifest": (Path(paths["run_manifest"]), "run_manifest_sha256"),
        "task_manifest": (Path(paths["task_manifest"]), "task_manifest_sha256"),
        "stage1_result": (Path(paths["stage1_result"]), "stage1_result_sha256"),
    }
    for label, (path, key) in file_hash_checks.items():
        if regular_file(path):
            failures += not report_check(label + " hash", sha256_file(path), hashes[key])

    # The legacy audit envelope's directory digests use a launcher-private
    # snapshot convention that is not the pipeline-v2 sha256_tree convention.
    # Independently recompute the latter and compare it to the generation
    # records that name that convention explicitly.
    result = json.loads(Path(paths["stage1_result"]).read_text())
    invocation = json.loads(Path(paths["generation_manifest"]).read_text())
    usage = json.loads((Path(paths["generation_root"]) / "usage.json").read_text())
    candidate_tree = sha256_tree(Path(paths["candidate"]))
    failures += not report_check(
        "candidate pipeline sha256_tree vs stage1 result",
        candidate_tree,
        result["outputs"]["workspace_sha256"],
    )
    failures += not report_check(
        "candidate pipeline sha256_tree vs invocation retained workspace",
        candidate_tree,
        invocation["retained_workspace_sha256"],
    )
    trace_tree = sha256_tree(Path(paths["generation_trace"]))
    failures += not report_check(
        "generation trace pipeline sha256_tree vs usage source trace",
        trace_tree,
        usage["source_trace_sha256"],
    )
    print(f"audit-envelope candidate snapshot digest (different convention): {hashes['candidate_tree_sha256']}")
    print(
        "audit-envelope trace snapshot digest (different convention): "
        f"{hashes['generation_codex_trace_sha256']}"
    )

    prompt_equal = (
        (Path(paths["candidate"]) / "prompt.py").read_bytes()
        == Path(paths["trusted_prompt"]).read_bytes()
    )
    translator_equal = (
        (Path(paths["candidate"]) / "py2mpy.py").read_bytes()
        == Path(paths["translator"]).read_bytes()
    )
    failures += not report_check("candidate prompt byte identity", prompt_equal, True)
    failures += not report_check("candidate translator byte identity", translator_equal, True)

    task = json.loads(Path(paths["task_manifest"]).read_text())
    embedded_manifest = dict(audit["manifest"])
    embedded_manifest.pop("config", None)
    failures += not report_check(
        "audit embedded manifest equals task manifest after envelope config removal",
        embedded_manifest,
        task,
    )
    failures += not report_check(
        "task manifest hash equals audit manifest hash",
        sha256_file(Path(paths["task_manifest"])),
        hashes["manifest_sha256"],
    )

    generation_root = Path(paths["generation_root"])
    for relative, expected in sorted(result["outputs"]["evidence"].items()):
        evidence_path = generation_root / relative
        ok_type = regular_file(evidence_path)
        print(
            f"result-declared evidence {relative}: "
            f"{'REGULAR' if ok_type else 'MISSING_OR_MISTYPED'}"
        )
        failures += not ok_type
        if ok_type:
            failures += not report_check(
                f"result-declared evidence hash {relative}",
                sha256_file(evidence_path),
                expected,
            )
    for relative, expected in sorted(invocation["outputs"]["evidence"].items()):
        evidence_path = generation_root / relative
        ok_type = regular_file(evidence_path)
        print(
            f"invocation-declared evidence {relative}: "
            f"{'REGULAR' if ok_type else 'MISSING_OR_MISTYPED'}"
        )
        failures += not ok_type
        if ok_type:
            failures += not report_check(
                f"invocation-declared evidence hash {relative}",
                sha256_file(evidence_path),
                expected,
            )

    for root in (
        Path(paths["candidate"]),
        Path("/reference"),
        Path(paths["generation_root"]),
    ):
        links = [path for path in root.rglob("*") if path.is_symlink()]
        failures += not report_check(f"no symlinks under {root}", links, [])

    print(f"TOTAL_FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
