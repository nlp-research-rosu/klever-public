#!/usr/bin/env python3
"""Independently validate mounted pipeline-v3 inputs and provenance."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        errors.append(f"{path}: unreadable or absent: {exc}")
        return
    if not stat.S_ISREG(mode):
        errors.append(f"{path}: expected regular file, mode={oct(mode)}")


def tree_manifest(root: Path, errors: list[str]):
    entries = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            errors.append(f"{root}: symlinked entry {rel} -> {os.readlink(path)}")
            entries.append(("symlink", rel, os.readlink(path)))
        elif stat.S_ISDIR(mode):
            entries.append(("dir", rel, ""))
        elif stat.S_ISREG(mode):
            entries.append(("file", rel, sha256(path)))
        else:
            errors.append(f"{root}: unsupported entry type {rel}, mode={oct(mode)}")
            entries.append(("other", rel, oct(mode)))
    encoded = json.dumps(entries, separators=(",", ":"), ensure_ascii=False).encode()
    return entries, hashlib.sha256(encoded).hexdigest()


def main() -> int:
    errors: list[str] = []
    with AUDIT_INPUT.open() as stream:
        audit = json.load(stream)
    paths = {key: Path(value) for key, value in audit["container_paths"].items()}
    hashes = audit["hashes"]

    print("record_layout=", audit["record_layout"], sep="")
    print("semantics_mode=", audit["semantics_mode"], sep="")
    print("problem_id=", audit["problem_id"], sep="")

    required = [
        Path("/audit-input.json"),
        paths["audit_campaign_lock"],
        paths["run_manifest"],
        paths["task_manifest"],
        paths["stage1_result"],
        paths["generation_manifest"],
        paths["generation_metrics"],
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        paths["generation_last"],
        paths["generation_output"],
        Path("/generation-evidence/prompt.txt"),
        paths["canonical"],
        paths["trusted_prompt"],
        paths["translator"],
    ]
    for item in required:
        require_regular(item, errors)
    if not paths["generation_trace"].is_dir():
        errors.append(f"{paths['generation_trace']}: expected trace directory")

    expected_files = {
        paths["audit_campaign_lock"]: hashes["audit_campaign_lock_sha256"],
        paths["canonical"]: hashes["canonical_sha256"],
        paths["trusted_prompt"]: hashes["trusted_prompt_sha256"],
        paths["translator"]: hashes["trusted_translator_sha256"],
        paths["run_manifest"]: hashes["run_manifest_sha256"],
        paths["task_manifest"]: hashes["task_manifest_sha256"],
        paths["stage1_result"]: hashes["stage1_result_sha256"],
        paths["generation_manifest"]: hashes["stage1_invocation_sha256"],
        paths["generation_metrics"]: hashes["generation_metrics_sha256"],
        Path("/generation-evidence/runtime-metrics.json"):
            hashes["generation_runtime_metrics_sha256"],
        Path("/generation-evidence/usage.json"): hashes["generation_usage_sha256"],
        paths["generation_last"]: hashes["generation_codex_last_sha256"],
        paths["generation_output"]: hashes["generation_codex_output_sha256"],
        Path("/generation-evidence/prompt.txt"): hashes["generation_prompt_sha256"],
    }
    for path, expected in expected_files.items():
        actual = sha256(path)
        state = "MATCH" if actual == expected else "MISMATCH"
        print(f"sha256 {state} {path} {actual}")
        if actual != expected:
            errors.append(f"{path}: expected {expected}, got {actual}")

    with paths["audit_campaign_lock"].open() as stream:
        lock = json.load(stream)
    if audit["audit_campaign"] != lock:
        errors.append("audit campaign block differs structurally from campaign lock")
    print("campaign_structural_match=", audit["audit_campaign"] == lock, sep="")

    pairs = [
        (Path("/candidate/prompt.py"), paths["trusted_prompt"], "prompt"),
        (Path("/candidate/py2mpy.py"), paths["translator"], "translator"),
    ]
    for candidate, trusted, label in pairs:
        require_regular(candidate, errors)
        equal = candidate.read_bytes() == trusted.read_bytes()
        print(f"{label}_byte_identity={equal}")
        if not equal:
            errors.append(f"candidate {label} differs from trusted mount")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if audit["semantics_mode"] != "SUPPLIED_SEMANTICS":
        errors.append("rendered mode unexpectedly differs from SUPPLIED_SEMANTICS")
    if not trusted_semantics.is_dir():
        errors.append("trusted supplied semantics mount is absent")
    candidate_entries, candidate_manifest = tree_manifest(candidate_semantics, errors)
    trusted_entries, trusted_manifest = tree_manifest(trusted_semantics, errors)
    semantics_equal = candidate_entries == trusted_entries
    print("candidate_semantics_manifest_sha256=", candidate_manifest, sep="")
    print("trusted_semantics_manifest_sha256=", trusted_manifest, sep="")
    print("semantics_recursive_entry_and_hash_identity=", semantics_equal, sep="")
    if not semantics_equal:
        errors.append("candidate supplied semantics tree differs from trusted tree")

    proof_files = [
        "solution.py",
        "solution.mpy",
        "verification.k",
        "spec.k",
        "prove.sh",
        "PROOF.md",
    ]
    for name in proof_files:
        require_regular(Path("/candidate") / name, errors)

    with paths["generation_manifest"].open() as stream:
        invocation = json.load(stream)
    declared_outputs = invocation["outputs"]["evidence"]
    evidence_root = Path("/generation-evidence")
    for relative, expected in sorted(declared_outputs.items()):
        path = evidence_root / relative
        require_regular(path, errors)
        actual = sha256(path)
        state = "MATCH" if actual == expected else "MISMATCH"
        print(f"invocation_output_sha256 {state} {relative} {actual}")
        if actual != expected:
            errors.append(f"{path}: invocation expected {expected}, got {actual}")

    trace_files = sorted(paths["generation_trace"].rglob("*"))
    trace_regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    if not trace_regular:
        errors.append("structured trace contains no regular files")
    trace_lines = 0
    trace_types: dict[str, int] = {}
    for path in trace_regular:
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                    continue
                record_type = str(record.get("type"))
                trace_types[record_type] = trace_types.get(record_type, 0) + 1
    print("trace_regular_files=", len(trace_regular), sep="")
    print("trace_json_records=", trace_lines, sep="")
    print("trace_type_counts=", json.dumps(trace_types, sort_keys=True), sep="")

    print("ERROR_COUNT=", len(errors), sep="")
    for error in errors:
        print("ERROR", error)
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
