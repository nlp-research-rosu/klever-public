#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT = Path("/audit-input.json")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan_tree(root: Path) -> list[tuple[str, str, Path]]:
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
    return sorted(entries)


def modern_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in scan_tree(root):
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


def legacy_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in scan_tree(root):
        short_kind = "d" if kind == "directory" else "f"
        digest.update(relative.encode() + b"\0" + short_kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def require_real(path: Path, expected_kind: str) -> None:
    mode = path.lstat().st_mode
    actual = (
        "file"
        if stat.S_ISREG(mode)
        else "directory"
        if stat.S_ISDIR(mode)
        else "unsupported"
    )
    if actual != expected_kind:
        raise ValueError(f"{path}: expected real {expected_kind}, got {actual}")


def compare_trees(left: Path, right: Path) -> None:
    left_entries = scan_tree(left)
    right_entries = scan_tree(right)
    left_inventory = [(rel, kind) for rel, kind, _ in left_entries]
    right_inventory = [(rel, kind) for rel, kind, _ in right_entries]
    if left_inventory != right_inventory:
        print("TREE_INVENTORY_MATCH: false")
        print("ONLY_LEFT:", sorted(set(left_inventory) - set(right_inventory)))
        print("ONLY_RIGHT:", sorted(set(right_inventory) - set(left_inventory)))
        raise ValueError("tree inventories differ")
    mismatches = []
    right_paths = {rel: path for rel, kind, path in right_entries if kind == "file"}
    for relative, kind, path in left_entries:
        if kind == "file" and path.read_bytes() != right_paths[relative].read_bytes():
            mismatches.append(relative)
    print(f"TREE_INVENTORY_MATCH: true ({len(left_entries)} entries)")
    print(f"TREE_FILE_BYTES_MATCH: {str(not mismatches).lower()}")
    if mismatches:
        print("CHANGED_FILES:", mismatches)
        raise ValueError("tree file bytes differ")


def report_hash(label: str, actual: str, expected: str) -> None:
    match = actual == expected
    print(f"{label}: actual={actual} expected={expected} match={str(match).lower()}")
    if not match:
        raise ValueError(f"hash mismatch for {label}")


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    hashes = audit["hashes"]
    print(
        "DECLARED:",
        audit["problem_id"],
        audit["condition"],
        audit["semantics_mode"],
        audit["record_layout"],
    )
    if audit["record_layout"] != "legacy-selected-stage1":
        raise ValueError("unexpected record layout")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise ValueError("unexpected semantics mode")

    required_files = [
        AUDIT,
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_real(path, "file")
    for path in required_directories:
        require_real(path, "directory")
    trace_files = [
        path
        for _, kind, path in scan_tree(Path("/generation-evidence/codex-trace"))
        if kind == "file"
    ]
    if not trace_files:
        raise ValueError("structured trace tree is empty")
    print(
        f"REQUIRED_RECORDS: all present, real, and readable; "
        f"trace_files={len(trace_files)}; usage_present="
        f"{Path('/generation-evidence/usage.json').is_file()}"
    )

    campaign = json.loads(Path("/audit-campaign-lock.json").read_text())
    if campaign != audit["audit_campaign"]:
        raise ValueError("campaign lock JSON differs from audit campaign block")
    print("CAMPAIGN_BLOCK_MATCH: true")

    file_checks = [
        ("audit_campaign_lock", Path("/audit-campaign-lock.json")),
        ("run_manifest", Path("/run.json")),
        ("task_manifest", Path("/task.json")),
        ("stage1_result", Path("/generation-result.json")),
        ("stage1_invocation", Path("/generation-evidence/invocation.json")),
        ("generation_metrics", Path("/generation-evidence/metrics.json")),
        ("generation_codex_last", Path("/generation-evidence/codex-last.txt")),
        ("generation_codex_output", Path("/generation-evidence/codex-output.log")),
        ("generation_prompt", Path("/generation-evidence/prompt.txt")),
        ("canonical", Path("/reference/canonical.py")),
        ("trusted_prompt", Path("/reference/prompt.py")),
        ("trusted_translator", Path("/reference/py2mpy.py")),
        ("candidate_prompt", Path("/candidate/prompt.py")),
        ("candidate_translator", Path("/candidate/py2mpy.py")),
    ]
    if Path("/generation-evidence/usage.json").is_file():
        require_real(Path("/generation-evidence/usage.json"), "file")
        file_checks.append(
            ("generation_usage", Path("/generation-evidence/usage.json"))
        )
    for label, path in file_checks:
        report_hash(label, file_digest(path), hashes[f"{label}_sha256"])

    generation_result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    report_hash(
        "candidate_tree_pipeline_digest",
        modern_tree_digest(Path("/candidate")),
        generation_result["outputs"]["workspace_sha256"],
    )
    report_hash(
        "generation_codex_trace_pipeline_digest",
        modern_tree_digest(Path("/generation-evidence/codex-trace")),
        usage["source_trace_sha256"],
    )
    for side in ("candidate", "trusted"):
        root = (
            Path("/candidate/reference-semantics")
            if side == "candidate"
            else Path("/reference/reference-semantics")
        )
        report_hash(
            f"{side}_reference_semantics_manifest_digest",
            modern_tree_digest(root),
            hashes["trusted_reference_semantics_manifest_sha256"],
        )
    print(
        "LAUNCHER_RECORDED_TREE_DIGESTS:",
        f"candidate={hashes['candidate_tree_sha256']}",
        f"trace={hashes['generation_codex_trace_sha256']}",
        "candidate_reference_semantics="
        f"{hashes['candidate_reference_semantics_sha256']}",
        "trusted_reference_semantics="
        f"{hashes['trusted_reference_semantics_sha256']}",
    )

    print(
        "PROMPT_BYTES_MATCH:",
        str(
            Path("/candidate/prompt.py").read_bytes()
            == Path("/reference/prompt.py").read_bytes()
        ).lower(),
    )
    print(
        "TRANSLATOR_BYTES_MATCH:",
        str(
            Path("/candidate/py2mpy.py").read_bytes()
            == Path("/reference/py2mpy.py").read_bytes()
        ).lower(),
    )
    compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print("INTEGRITY_RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"INTEGRITY_RESULT: FAIL: {error}", file=sys.stderr)
        raise
