#!/usr/bin/env python3
"""Independent provenance/type/hash checks for audit stage 1."""

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


def sha256_tree(root: Path) -> str:
    """Launcher-compatible path/type/size/content tree digest."""
    digest = hashlib.sha256()
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
                raise RuntimeError(f"tree contains linked or unsupported entry: {path}")
    for relative, entry_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_kind.encode() + b"\0")
        if entry_kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = os.lstat(path).st_mode
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({oct(mode)})"


def require_kind(path: Path, expected: str) -> bool:
    try:
        actual = kind(path)
    except FileNotFoundError:
        print(f"TYPE FAIL missing {path}")
        return False
    ok = actual == expected
    print(f"TYPE {'OK' if ok else 'FAIL'} {path}: {actual}, expected {expected}")
    return ok


def check_hash(path: Path, expected: str) -> bool:
    actual = sha256(path)
    ok = actual == expected
    print(
        f"HASH {'OK' if ok else 'FAIL'} {path}: "
        f"actual={actual} expected={expected}"
    )
    return ok


def compare_trees(left: Path, right: Path) -> bool:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for base, dirs, files in os.walk(root, followlinks=False):
            base_path = Path(base)
            for name in dirs + files:
                entry = base_path / name
                rel = entry.relative_to(root).as_posix()
                entry_kind = kind(entry)
                digest = sha256(entry) if entry_kind == "regular" else None
                result[rel] = (entry_kind, digest)
                if entry_kind == "symlink":
                    print(f"TREE FAIL symlink {entry} -> {os.readlink(entry)}")
        return result

    left_inv = inventory(left)
    right_inv = inventory(right)
    ok = left_inv == right_inv
    print(
        f"TREE {'OK' if ok else 'FAIL'} {left} vs {right}: "
        f"{len(left_inv)} entries vs {len(right_inv)} entries"
    )
    for rel in sorted(set(left_inv) | set(right_inv)):
        if left_inv.get(rel) != right_inv.get(rel):
            print(f"TREE DIFF {rel}: candidate={left_inv.get(rel)} trusted={right_inv.get(rel)}")
    return ok


def main() -> int:
    ok = True
    ok &= require_kind(AUDIT_INPUT, "regular")
    ok &= require_kind(CAMPAIGN_LOCK, "regular")

    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(CAMPAIGN_LOCK.read_text())
    print(f"RECORD_LAYOUT {audit.get('record_layout')}")
    print(f"SEMANTICS_MODE {audit.get('semantics_mode')}")
    print(
        "CONTAINER_PATHS "
        + " ".join(
            f"{name}={path}"
            for name, path in sorted(audit.get("container_paths", {}).items())
        )
    )
    print(
        "LAUNCHER_INTEGRITY "
        + " ".join(
            f"{name}={value}"
            for name, value in sorted(audit.get("integrity", {}).items())
        )
    )

    campaign_match = audit["audit_campaign"] == lock
    print(f"CAMPAIGN_BLOCK {'OK' if campaign_match else 'FAIL'}")
    ok &= campaign_match
    ok &= check_hash(CAMPAIGN_LOCK, audit["hashes"]["audit_campaign_lock_sha256"])

    if audit.get("record_layout") != "legacy-selected-stage1":
        print("LAYOUT FAIL expected legacy-selected-stage1")
        ok = False
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        print("MODE FAIL expected SUPPLIED_SEMANTICS")
        ok = False

    required_regular = [
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
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
    ]
    for path in required_regular:
        ok &= require_kind(path, "regular")
    ok &= require_kind(Path("/generation-evidence/codex-trace"), "directory")
    ok &= require_kind(Path("/reference/reference-semantics"), "directory")
    ok &= require_kind(Path("/candidate/reference-semantics"), "directory")

    optional_usage = Path("/generation-evidence/usage.json")
    if optional_usage.exists():
        ok &= require_kind(optional_usage, "regular")
        print("USAGE PRESENT and inspected")

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    regular_trace_files = []
    for path in trace_files:
        actual_kind = kind(path)
        if actual_kind not in {"directory", "regular"}:
            print(f"TRACE TYPE FAIL {path}: {actual_kind}")
            ok = False
        if actual_kind == "regular":
            regular_trace_files.append(path)
    if not regular_trace_files:
        print("TRACE FAIL no structured trace files")
        ok = False
    else:
        print(f"TRACE OK {len(regular_trace_files)} regular file(s), no symlinks/special files")

    json_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
    ]
    if optional_usage.exists():
        json_records.append(optional_usage)
    for path in json_records:
        parsed = json.loads(path.read_text())
        print(
            f"JSON_READ OK {path}: top_level_keys={sorted(parsed)}"
        )
    for path in (
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ):
        text = path.read_text(errors="strict")
        print(f"TEXT_READ OK {path}: characters={len(text)} lines={len(text.splitlines())}")
    trace_line_count = 0
    for path in regular_trace_files:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                json.loads(line)
                trace_line_count += 1
    print(f"TRACE_JSON_READ OK records={trace_line_count}")

    h = audit["hashes"]
    file_hashes = {
        Path("/reference/canonical.py"): h["canonical_sha256"],
        Path("/reference/prompt.py"): h["trusted_prompt_sha256"],
        Path("/reference/py2mpy.py"): h["trusted_translator_sha256"],
        Path("/candidate/prompt.py"): h["candidate_prompt_sha256"],
        Path("/candidate/py2mpy.py"): h["candidate_translator_sha256"],
        Path("/run.json"): h["run_manifest_sha256"],
        Path("/task.json"): h["task_manifest_sha256"],
        Path("/generation-result.json"): h["stage1_result_sha256"],
        Path("/generation-evidence/invocation.json"): h["stage1_invocation_sha256"],
        Path("/generation-evidence/metrics.json"): h["generation_metrics_sha256"],
        Path("/generation-evidence/codex-last.txt"): h["generation_codex_last_sha256"],
        Path("/generation-evidence/codex-output.log"): h["generation_codex_output_sha256"],
        Path("/generation-evidence/prompt.txt"): h["generation_prompt_sha256"],
    }
    if optional_usage.exists():
        file_hashes[optional_usage] = h["generation_usage_sha256"]
    for path, expected in file_hashes.items():
        ok &= check_hash(path, expected)

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    usage = json.loads(optional_usage.read_text()) if optional_usage.exists() else {}

    # audit-input preserves three generations of directory hashes.  sha256_tree
    # is the pipeline manifest algorithm (the algorithm that length-prefixes
    # paths and includes types and file sizes); compare it only to fields known
    # to use that algorithm.  The audit-composite and legacy fields are checked
    # below for their launcher-recorded relationships, not conflated with this
    # digest format.
    tree_hashes = [
        (
            Path("/candidate"),
            result["outputs"]["workspace_sha256"],
            "generation-result outputs.workspace_sha256",
        ),
        (
            Path("/candidate"),
            invocation["retained_workspace_sha256"],
            "invocation retained_workspace_sha256",
        ),
        (
            Path("/candidate/reference-semantics"),
            h["trusted_reference_semantics_manifest_sha256"],
            "audit-input trusted_reference_semantics_manifest_sha256",
        ),
        (
            Path("/reference/reference-semantics"),
            h["trusted_reference_semantics_manifest_sha256"],
            "audit-input trusted_reference_semantics_manifest_sha256",
        ),
        (
            Path("/generation-evidence/codex-trace"),
            usage["source_trace_sha256"],
            "usage source_trace_sha256",
        ),
    ]
    for path, expected, source in tree_hashes:
        actual = sha256_tree(path)
        tree_ok = actual == expected
        print(
            f"TREE_HASH {'OK' if tree_ok else 'FAIL'} {path}: "
            f"actual={actual} expected={expected} source={source}"
        )
        ok &= tree_ok

    semantics_audit_hash_match = (
        h["candidate_reference_semantics_sha256"]
        == h["trusted_reference_semantics_sha256"]
    )
    print(
        "RECORDED_AUDIT_COMPOSITE "
        f"{'OK' if semantics_audit_hash_match else 'FAIL'} "
        "candidate_reference_semantics_sha256 equals "
        "trusted_reference_semantics_sha256 "
        f"({h['trusted_reference_semantics_sha256']})"
    )
    ok &= semantics_audit_hash_match
    print(
        "RECORDED_ALTERNATE_TREE_HASHES "
        f"candidate={h['candidate_tree_sha256']} "
        f"trace={h['generation_codex_trace_sha256']} "
        f"semantics_legacy={h['trusted_reference_semantics_legacy_sha256']}"
    )

    task_manifest_match = sha256(Path("/task.json")) == h["manifest_sha256"]
    print(f"TASK_AS_MANIFEST {'OK' if task_manifest_match else 'FAIL'}")
    ok &= task_manifest_match

    for record_name, record in (("result", result), ("invocation", invocation)):
        outputs = record["outputs"]["evidence"]
        for rel, expected in sorted(outputs.items()):
            path = Path("/generation-evidence") / rel
            ok &= require_kind(path, "regular")
            ok &= check_hash(path, expected)
        print(f"GENERATION_OUTPUTS {record_name} checked={len(outputs)}")

    prompt_bytes_match = Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    translator_bytes_match = Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print(f"PROMPT_BYTE_MATCH {'OK' if prompt_bytes_match else 'FAIL'}")
    print(f"TRANSLATOR_BYTE_MATCH {'OK' if translator_bytes_match else 'FAIL'}")
    ok &= prompt_bytes_match and translator_bytes_match
    ok &= compare_trees(
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )

    print(f"OVERALL {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
