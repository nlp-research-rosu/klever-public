#!/usr/bin/env python3
"""Independently validate the launcher records and mounted artifact hashes."""

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
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the length-delimited tree hash used by pipeline-v2 records."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root.resolve()]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root.resolve()).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise ValueError(f"not a real regular file: {path}")


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISDIR(mode):
        raise ValueError(f"not a real directory: {path}")


def compare(label: str, actual: Any, expected: Any) -> bool:
    ok = actual == expected
    print(f"{'OK' if ok else 'MISMATCH'} {label}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    return ok


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))
    failures = 0

    print("DECLARED CONTEXT")
    for key in ("problem_id", "condition", "record_layout", "semantics_mode"):
        print(f"{key}: {audit[key]}")

    required_files = [
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
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    if Path("/generation-evidence/usage.json").exists():
        required_files.append(Path("/generation-evidence/usage.json"))
    required_directories = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
        Path("/reference"),
    ]

    print("\nREQUIRED NODE TYPES")
    for path in required_files:
        try:
            require_regular(path)
            print(f"OK regular file {path}")
        except (OSError, ValueError) as error:
            failures += 1
            print(f"FAIL {error}")
    for path in required_directories:
        try:
            require_directory(path)
            print(f"OK real directory {path}")
        except (OSError, ValueError) as error:
            failures += 1
            print(f"FAIL {error}")

    print("\nCAMPAIGN LOCK")
    failures += not compare(
        "campaign block equals lock JSON", audit["audit_campaign"], campaign
    )
    failures += not compare(
        "campaign lock sha256",
        sha256_file(CAMPAIGN_LOCK),
        audit["hashes"]["audit_campaign_lock_sha256"],
    )

    file_expectations = {
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    }
    print("\nRECORDED FILE HASHES")
    for path, field in file_expectations.items():
        if not path.exists() and audit["hashes"].get(field) is None:
            print(f"OK intentionally absent {path}")
            continue
        actual = sha256_file(path)
        expected = audit["hashes"][field]
        failures += not compare(f"{path} ({field})", actual, expected)

    print("\nBYTE IDENTITY")
    failures += not compare(
        "candidate prompt equals trusted prompt",
        Path("/candidate/prompt.py").read_bytes()
        == Path("/reference/prompt.py").read_bytes(),
        True,
    )
    failures += not compare(
        "candidate translator equals trusted translator",
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes(),
        True,
    )

    print("\nTREE INTEGRITY")
    candidate_hash = pipeline_tree_hash(Path("/candidate"))
    trace_hash = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    print("\nGENERATION-RESULT EVIDENCE HASHES")
    for relative, expected_hash in sorted(
        generation_result["outputs"]["evidence"].items()
    ):
        evidence_path = Path("/generation-evidence") / relative
        try:
            require_regular(evidence_path)
        except (OSError, ValueError) as error:
            failures += 1
            print(f"FAIL {error}")
            continue
        failures += not compare(
            f"generation evidence {relative}",
            sha256_file(evidence_path),
            expected_hash,
        )
    failures += not compare(
        "candidate tree against retained workspace hash",
        candidate_hash,
        generation_result["outputs"]["workspace_sha256"],
    )
    failures += not compare(
        "candidate tree against invocation retained workspace hash",
        candidate_hash,
        invocation["retained_workspace_sha256"],
    )
    failures += not compare(
        "trace tree against usage source trace hash",
        trace_hash,
        usage["source_trace_sha256"],
    )
    print(
        "NOTE audit-input candidate_tree_sha256 and "
        "generation_codex_trace_sha256 use a launcher-specific digest encoding; "
        "the independently recomputed pipeline-v2 hashes are checked against the "
        "producer records above."
    )
    print(f"audit-input candidate_tree_sha256: {audit['hashes']['candidate_tree_sha256']}")
    print(
        "audit-input generation_codex_trace_sha256: "
        f"{audit['hashes']['generation_codex_trace_sha256']}"
    )

    reference_semantics = Path("/reference/reference-semantics")
    expected_absent = (
        audit["semantics_mode"] == "GENERATED_SEMANTICS"
        and not audit["mount_reference_semantics"]
        and audit["reference_semantics"] is None
        and audit["hashes"]["trusted_reference_semantics_sha256"] is None
        and audit["hashes"]["candidate_reference_semantics_sha256"] is None
    )
    failures += not compare(
        "generated-semantics boundary declarations are consistent",
        expected_absent,
        True,
    )
    failures += not compare(
        "trusted reference-semantics mount is absent",
        reference_semantics.exists(),
        False,
    )

    print(f"\nFAILURE_COUNT: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
