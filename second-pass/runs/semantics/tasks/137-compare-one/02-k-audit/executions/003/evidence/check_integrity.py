#!/usr/bin/env python3
"""Independent mounted-input and legacy-selected-stage1 integrity check."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reproduce the launcher tree digest while rejecting non-file entries."""
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
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_kind(path: Path, expected: str) -> None:
    mode = path.lstat().st_mode
    actual = (
        "file"
        if stat.S_ISREG(mode)
        else "directory"
        if stat.S_ISDIR(mode)
        else "symlink"
        if stat.S_ISLNK(mode)
        else "other"
    )
    print(f"TYPE {path}: {actual}")
    if actual != expected:
        raise AssertionError(f"{path}: expected {expected}, got {actual}")


def compare_file(actual: Path, trusted: Path, label: str) -> None:
    require_kind(actual, "file")
    require_kind(trusted, "file")
    actual_hash = sha256_file(actual)
    trusted_hash = sha256_file(trusted)
    print(f"COMPARE {label}: actual={actual_hash} trusted={trusted_hash}")
    if actual_hash != trusted_hash or actual.read_bytes() != trusted.read_bytes():
        raise AssertionError(f"{label} differs")


def tree_inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    inventory: dict[str, tuple[str, str | None]] = {}
    for path in [root, *sorted(root.rglob("*"))]:
        relative = "." if path == root else path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            inventory[relative] = ("directory", None)
        elif stat.S_ISREG(mode):
            inventory[relative] = ("file", sha256_file(path))
        elif stat.S_ISLNK(mode):
            inventory[relative] = ("symlink", os.readlink(path))
        else:
            inventory[relative] = ("other", None)
    return inventory


def expected_hash(label: str, path: Path, expected: str) -> None:
    actual = sha256_file(path)
    print(f"HASH {label}: actual={actual} expected={expected}")
    if actual != expected:
        raise AssertionError(f"hash mismatch for {label}")


def main() -> None:
    require_kind(AUDIT_INPUT, "file")
    require_kind(LOCK, "file")
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    print(f"RECORD_LAYOUT: {audit['record_layout']}")
    print(f"SEMANTICS_MODE: {audit['semantics_mode']}")
    if audit["record_layout"] != "legacy-selected-stage1":
        raise AssertionError("unexpected record layout")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        raise AssertionError("unexpected semantics mode")
    if audit["audit_campaign"] != lock:
        raise AssertionError("campaign lock JSON differs from embedded campaign block")
    print("CAMPAIGN_BLOCK_MATCH: yes")

    hashes = audit["hashes"]
    expected_hash("audit campaign lock", LOCK, hashes["audit_campaign_lock_sha256"])
    paths = {
        "audit prompt": Path("/audit-prompt.md"),
        "run manifest": Path("/run.json"),
        "task manifest": Path("/task.json"),
        "stage1 result": Path("/generation-result.json"),
        "generation invocation": Path("/generation-evidence/invocation.json"),
        "generation metrics": Path("/generation-evidence/metrics.json"),
        "generation last": Path("/generation-evidence/codex-last.txt"),
        "generation output": Path("/generation-evidence/codex-output.log"),
        "generation prompt": Path("/generation-evidence/prompt.txt"),
        "generation trace": Path("/generation-evidence/codex-trace"),
        "generation usage": Path("/generation-evidence/usage.json"),
        "trusted canonical": Path("/reference/canonical.py"),
        "trusted prompt": Path("/reference/prompt.py"),
        "trusted translator": Path("/reference/py2mpy.py"),
        "trusted semantics": Path("/reference/reference-semantics"),
        "candidate": Path("/candidate"),
    }
    for label, path in paths.items():
        require_kind(path, "directory" if path.is_dir() else "file")

    file_hash_expectations = {
        "audit prompt": audit["audit_campaign"]["audit_prompt_sha256"],
        "run manifest": hashes["run_manifest_sha256"],
        "task manifest": hashes["task_manifest_sha256"],
        "stage1 result": hashes["stage1_result_sha256"],
        "generation invocation": hashes["stage1_invocation_sha256"],
        "generation metrics": hashes["generation_metrics_sha256"],
        "generation last": hashes["generation_codex_last_sha256"],
        "generation output": hashes["generation_codex_output_sha256"],
        "generation prompt": hashes["generation_prompt_sha256"],
        "generation usage": hashes["generation_usage_sha256"],
        "trusted canonical": hashes["canonical_sha256"],
        "trusted prompt": hashes["trusted_prompt_sha256"],
        "trusted translator": hashes["trusted_translator_sha256"],
    }
    for label, expected in file_hash_expectations.items():
        expected_hash(label, paths[label], expected)

    # These are the launcher/pipeline manifest digests whose on-disk algorithm
    # is published in pipeline_contract.py.  audit-input also carries a second
    # set of packaging digests; their encoding is not declared, so preserve
    # those values below without pretending a different digest is comparable.
    usage = json.loads(paths["generation usage"].read_text())
    invocation = json.loads(paths["generation invocation"].read_text())
    result = json.loads(paths["stage1 result"].read_text())
    tree_hash_expectations = {
        "generation trace": usage["source_trace_sha256"],
        "trusted semantics": hashes[
            "trusted_reference_semantics_manifest_sha256"
        ],
        "candidate": invocation["retained_workspace_sha256"],
    }
    for label, expected in tree_hash_expectations.items():
        actual = sha256_tree(paths[label])
        print(f"TREE_HASH {label}: actual={actual} expected={expected}")
        if actual != expected:
            raise AssertionError(f"tree hash mismatch for {label}")
    if result["outputs"]["workspace_sha256"] != invocation[
        "retained_workspace_sha256"
    ]:
        raise AssertionError("result and invocation workspace digests differ")
    if hashes["candidate_reference_semantics_sha256"] != hashes[
        "trusted_reference_semantics_sha256"
    ]:
        raise AssertionError("launcher candidate/trusted semantics digests differ")
    print(
        "LAUNCHER_PACKAGING_DIGESTS: "
        f"candidate={hashes['candidate_tree_sha256']} "
        f"candidate_semantics={hashes['candidate_reference_semantics_sha256']} "
        f"trusted_semantics={hashes['trusted_reference_semantics_sha256']} "
        f"trace={hashes['generation_codex_trace_sha256']}"
    )

    compare_file(
        Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "candidate prompt"
    )
    compare_file(
        Path("/candidate/py2mpy.py"),
        Path("/reference/py2mpy.py"),
        "candidate translator",
    )
    candidate_semantics = tree_inventory(Path("/candidate/reference-semantics"))
    trusted_semantics = tree_inventory(Path("/reference/reference-semantics"))
    if candidate_semantics != trusted_semantics:
        missing = sorted(set(trusted_semantics) - set(candidate_semantics))
        additional = sorted(set(candidate_semantics) - set(trusted_semantics))
        changed = sorted(
            key
            for key in set(candidate_semantics) & set(trusted_semantics)
            if candidate_semantics[key] != trusted_semantics[key]
        )
        raise AssertionError(
            f"semantics tree mismatch missing={missing} additional={additional} "
            f"changed={changed}"
        )
    print(f"SEMANTICS_TREE_BYTE_IDENTITY: yes ({len(trusted_semantics)} entries)")

    # Required generation result hashes are independently checked against files.
    for record_name, record in (("invocation", invocation), ("result", result)):
        for relative, expected in record["outputs"]["evidence"].items():
            path = Path("/generation-evidence") / relative
            require_kind(path, "file")
            expected_hash(f"{record_name}:{relative}", path, expected)

    # Fully parse every structured trace record and read the complete text log.
    trace_files = sorted(paths["generation trace"].rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    counts: Counter[str] = Counter()
    payload_counts: Counter[str] = Counter()
    trace_lines = 0
    for trace_file in trace_files:
        with trace_file.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                trace_lines += 1
                counts[str(record.get("type"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_counts[str(payload.get("type"))] += 1
    output_bytes = paths["generation output"].read_bytes()
    print(
        f"TRACE_PARSE: files={len(trace_files)} lines={trace_lines} "
        f"event_types={dict(sorted(counts.items()))}"
    )
    print(f"TRACE_PAYLOAD_TYPES: {dict(sorted(payload_counts.items()))}")
    print(
        f"CODEX_OUTPUT_FULL_READ: bytes={len(output_bytes)} "
        f"lines={output_bytes.count(bytes([10]))}"
    )

    # Inspect every candidate entry's type; proof artifacts are checked later.
    candidate_inventory = tree_inventory(paths["candidate"])
    odd_entries = {
        key: value
        for key, value in candidate_inventory.items()
        if value[0] not in {"directory", "file"}
    }
    print(f"CANDIDATE_ENTRIES: {len(candidate_inventory)}")
    print(f"CANDIDATE_LINKED_OR_UNSUPPORTED: {odd_entries}")
    if odd_entries:
        raise AssertionError("candidate contains linked or unsupported entries")
    print("INTEGRITY_RESULT: PASS")


if __name__ == "__main__":
    main()
