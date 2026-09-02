#!/usr/bin/env python3
"""Independent mounted-input integrity checks for audit 126-is-sorted."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hash(root: Path) -> str:
    """Reproduce the recorded length-delimited tree digest independently."""
    root_mode = root.lstat().st_mode
    if not stat.S_ISDIR(root_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
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
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path, label: str, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"{label}: absent or unreadable: {error}")
        return
    if not stat.S_ISREG(mode):
        failures.append(f"{label}: expected real regular file, mode={oct(mode)}")


def require_directory(path: Path, label: str, failures: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as error:
        failures.append(f"{label}: absent or unreadable: {error}")
        return
    if not stat.S_ISDIR(mode):
        failures.append(f"{label}: expected real directory, mode={oct(mode)}")


def check_hash(
    path: Path, expected: str | None, label: str, failures: list[str]
) -> None:
    if expected is None:
        failures.append(f"{label}: unexpectedly has null recorded hash")
        return
    actual = file_hash(path)
    status = "MATCH" if actual == expected else "MISMATCH"
    print(f"{label}: {status}\n  expected={expected}\n  actual  ={actual}")
    if actual != expected:
        failures.append(f"{label}: hash mismatch")


def main() -> int:
    failures: list[str] = []
    require_regular(AUDIT_INPUT, "audit input", failures)
    document = json.loads(AUDIT_INPUT.read_text())
    paths = {key: Path(value) for key, value in document["container_paths"].items()}
    recorded = document["hashes"]

    required_regular = {
        "audit campaign lock": paths["audit_campaign_lock"],
        "canonical": paths["canonical"],
        "trusted prompt": paths["trusted_prompt"],
        "trusted translator": paths["translator"],
        "run manifest": paths["run_manifest"],
        "task manifest": paths["task_manifest"],
        "generation result": paths["stage1_result"],
        "generation invocation": paths["generation_manifest"],
        "generation metrics": paths["generation_metrics"],
        "generation last": paths["generation_last"],
        "generation output": paths["generation_output"],
        "generation prompt": paths["generation_root"] / "prompt.txt",
    }
    usage = paths["generation_root"] / "usage.json"
    if usage.exists() or usage.is_symlink():
        required_regular["generation usage"] = usage
    for label, path in required_regular.items():
        require_regular(path, label, failures)
    require_directory(paths["candidate"], "candidate root", failures)
    require_directory(paths["generation_root"], "generation root", failures)
    require_directory(paths["generation_trace"], "generation trace", failures)

    candidate_required = [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "semantic.k",
        "verification.k",
        "spec.k",
        "prove.sh",
    ]
    for name in candidate_required:
        require_regular(paths["candidate"] / name, f"candidate/{name}", failures)

    recorded_file_checks = {
        "audit_campaign_lock_sha256": paths["audit_campaign_lock"],
        "canonical_sha256": paths["canonical"],
        "trusted_prompt_sha256": paths["trusted_prompt"],
        "trusted_translator_sha256": paths["translator"],
        "candidate_prompt_sha256": paths["candidate"] / "prompt.py",
        "candidate_translator_sha256": paths["candidate"] / "py2mpy.py",
        "run_manifest_sha256": paths["run_manifest"],
        "task_manifest_sha256": paths["task_manifest"],
        "stage1_result_sha256": paths["stage1_result"],
        "stage1_invocation_sha256": paths["generation_manifest"],
        "generation_metrics_sha256": paths["generation_metrics"],
        "generation_codex_last_sha256": paths["generation_last"],
        "generation_codex_output_sha256": paths["generation_output"],
        "generation_prompt_sha256": paths["generation_root"] / "prompt.txt",
    }
    if usage.exists():
        recorded_file_checks["generation_usage_sha256"] = usage
    for field, path in recorded_file_checks.items():
        check_hash(path, recorded.get(field), field, failures)

    invocation = json.loads(paths["generation_manifest"].read_text())
    generation_result = json.loads(paths["stage1_result"].read_text())
    usage_document = json.loads(usage.read_text()) if usage.exists() else None

    candidate_digest = tree_hash(paths["candidate"])
    retained_workspace_hashes = {
        invocation.get("retained_workspace_sha256"),
        invocation.get("outputs", {}).get("workspace_sha256"),
        generation_result.get("outputs", {}).get("workspace_sha256"),
    }
    print(
        "candidate retained-workspace tree digest:"
        f" {'MATCH' if retained_workspace_hashes == {candidate_digest} else 'MISMATCH'}"
        f"\n  generation records={sorted(str(value) for value in retained_workspace_hashes)}"
        f"\n  actual  ={candidate_digest}"
    )
    if retained_workspace_hashes != {candidate_digest}:
        failures.append("candidate differs from retained generation workspace")
    print(
        "audit-input candidate_tree_sha256 uses an unspecified aggregate encoding:"
        f"\n  recorded={recorded['candidate_tree_sha256']}"
        f"\n  independently computed length-delimited digest={candidate_digest}"
    )

    trace_digest = tree_hash(paths["generation_trace"])
    recorded_source_trace = (
        usage_document.get("source_trace_sha256") if usage_document else None
    )
    print(
        "generation source-trace tree digest:"
        f" {'MATCH' if trace_digest == recorded_source_trace else 'MISMATCH'}"
        f"\n  usage record={recorded_source_trace}"
        f"\n  actual  ={trace_digest}"
    )
    if usage_document and trace_digest != recorded_source_trace:
        failures.append("generation trace differs from usage source trace")
    print(
        "audit-input generation_codex_trace_sha256 uses an unspecified aggregate encoding:"
        f"\n  recorded={recorded['generation_codex_trace_sha256']}"
        f"\n  independently computed length-delimited digest={trace_digest}"
    )

    evidence_hashes = generation_result.get("outputs", {}).get("evidence", {})
    for relative, expected in sorted(evidence_hashes.items()):
        path = paths["generation_root"] / relative
        require_regular(path, f"generation evidence/{relative}", failures)
        actual = file_hash(path)
        status = "MATCH" if actual == expected else "MISMATCH"
        print(
            f"generation-result evidence {relative}: {status}"
            f"\n  expected={expected}\n  actual  ={actual}"
        )
        if actual != expected:
            failures.append(f"generation evidence hash mismatch: {relative}")

    campaign = json.loads(paths["audit_campaign_lock"].read_text())
    if campaign == document["audit_campaign"]:
        print("campaign block: EXACT MATCH")
    else:
        failures.append("campaign block differs from mounted lock")

    prompt_equal = (
        (paths["candidate"] / "prompt.py").read_bytes()
        == paths["trusted_prompt"].read_bytes()
    )
    translator_equal = (
        (paths["candidate"] / "py2mpy.py").read_bytes()
        == paths["translator"].read_bytes()
    )
    print(f"candidate prompt versus trusted prompt: {prompt_equal}")
    print(f"candidate translator versus trusted translator: {translator_equal}")
    if not prompt_equal:
        failures.append("candidate prompt differs from trusted prompt")
    if not translator_equal:
        failures.append("candidate translator differs from trusted translator")

    forbidden_reference_semantics = Path("/reference/reference-semantics")
    if forbidden_reference_semantics.exists() or forbidden_reference_semantics.is_symlink():
        failures.append("reference semantics exists in GENERATED_SEMANTICS mode")
    else:
        print("trusted reference semantics: ABSENT AS REQUIRED")

    if document["record_layout"] != "legacy-selected-stage1":
        failures.append(f"unexpected record layout: {document['record_layout']}")
    if document["semantics_mode"] != "GENERATED_SEMANTICS":
        failures.append(f"unexpected semantics mode: {document['semantics_mode']}")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAIL: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
