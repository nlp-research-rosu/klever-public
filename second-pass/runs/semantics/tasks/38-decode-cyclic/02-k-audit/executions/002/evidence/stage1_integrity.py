#!/usr/bin/env python3
"""Independent launcher/provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require_regular(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"MISSING {path}")
    elif path.is_symlink():
        errors.append(f"SYMLINK {path} -> {os.readlink(path)}")
    elif not path.is_file():
        errors.append(f"NOT_REGULAR_FILE {path}")
    elif not os.access(path, os.R_OK):
        errors.append(f"UNREADABLE {path}")


def compare_trees(left: Path, right: Path, errors: list[str]) -> None:
    def entries(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            rel = str(path.relative_to(root))
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
            elif path.is_dir():
                result[rel] = ("directory", None)
            elif path.is_file():
                result[rel] = ("file", sha256(path))
            else:
                result[rel] = ("other", None)
        return result

    left_entries = entries(left)
    right_entries = entries(right)
    for rel in sorted(set(left_entries) | set(right_entries)):
        lv = left_entries.get(rel)
        rv = right_entries.get(rel)
        if lv != rv:
            errors.append(f"TREE_MISMATCH {rel}: candidate={lv!r} trusted={rv!r}")
    print(f"candidate_semantics_entries={len(left_entries)}")
    print(f"trusted_semantics_entries={len(right_entries)}")


def stable_tree_digest(root: Path) -> str:
    """Reviewer-local digest over relative path, type, and file bytes."""
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix().encode()
        if path.is_symlink():
            kind = b"L"
            payload = os.readlink(path).encode()
        elif path.is_dir():
            kind = b"D"
            payload = b""
        elif path.is_file():
            kind = b"F"
            payload = path.read_bytes()
        else:
            kind = b"O"
            payload = b""
        h.update(kind + b"\0" + rel + b"\0")
        h.update(len(payload).to_bytes(8, "big"))
        h.update(payload)
    return h.hexdigest()


def trace_summary(trace_root: Path, errors: list[str]) -> None:
    trace_files = sorted(trace_root.rglob("*"))
    regular = [p for p in trace_files if p.is_file() and not p.is_symlink()]
    if not regular:
        errors.append(f"NO_TRACE_FILES {trace_root}")
        return
    for path in trace_files:
        if path.is_symlink():
            errors.append(f"TRACE_SYMLINK {path}")
        elif not (path.is_file() or path.is_dir()):
            errors.append(f"TRACE_SPECIAL_ENTRY {path}")

    event_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    total_lines = 0
    for path in regular:
        print(
            f"trace_file={path.relative_to(trace_root)} "
            f"sha256={sha256(path)} bytes={path.stat().st_size}"
        )
        if path.suffix != ".jsonl":
            continue
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    record = json.loads(line)
                except Exception as err:
                    errors.append(f"INVALID_JSONL {path}:{line_number}: {err}")
                    continue
                event_types[str(record.get("type", "<missing>"))] += 1
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
    print(f"trace_jsonl_lines={total_lines}")
    print(f"trace_top_level_types={dict(sorted(event_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")


def main() -> int:
    errors: list[str] = []
    require_regular(AUDIT_INPUT, errors)
    require_regular(LOCK, errors)
    if errors:
        print("\n".join(errors))
        return 1

    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    if audit.get("record_layout") != "legacy-selected-stage1":
        errors.append(f"UNEXPECTED_RECORD_LAYOUT {audit.get('record_layout')!r}")
    if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
        errors.append(f"UNEXPECTED_SEMANTICS_MODE {audit.get('semantics_mode')!r}")
    if lock != audit.get("audit_campaign"):
        errors.append("CAMPAIGN_BLOCK_MISMATCH")

    expected_hashes = audit["hashes"]
    file_hash_checks = {
        LOCK: "audit_campaign_lock_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    }
    for path, key in file_hash_checks.items():
        require_regular(path, errors)
        if path.is_file() and not path.is_symlink():
            actual = sha256(path)
            expected = expected_hashes[key]
            print(f"hash {path} actual={actual} expected={expected}")
            if actual != expected:
                errors.append(f"HASH_MISMATCH {path}: {actual} != {expected}")

    required_legacy_selected = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    for path in required_legacy_selected:
        require_regular(path, errors)

    candidate_prompt = Path("/candidate/prompt.py")
    trusted_prompt = Path("/reference/prompt.py")
    candidate_translator = Path("/candidate/py2mpy.py")
    trusted_translator = Path("/reference/py2mpy.py")
    if candidate_prompt.read_bytes() != trusted_prompt.read_bytes():
        errors.append("CANDIDATE_PROMPT_DIFFERS")
    if candidate_translator.read_bytes() != trusted_translator.read_bytes():
        errors.append("CANDIDATE_TRANSLATOR_DIFFERS")

    candidate_semantics = Path("/candidate/reference-semantics")
    trusted_semantics = Path("/reference/reference-semantics")
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        errors.append("TRUSTED_SUPPLIED_SEMANTICS_MISSING_OR_INVALID")
    if not candidate_semantics.is_dir() or candidate_semantics.is_symlink():
        errors.append("CANDIDATE_SUPPLIED_SEMANTICS_MISSING_OR_INVALID")
    if candidate_semantics.is_dir() and trusted_semantics.is_dir():
        compare_trees(candidate_semantics, trusted_semantics, errors)
        print(
            "reviewer_tree_digest candidate="
            f"{stable_tree_digest(candidate_semantics)}"
        )
        print(
            "reviewer_tree_digest trusted="
            f"{stable_tree_digest(trusted_semantics)}"
        )

    for mounted in [
        Path("/candidate"),
        Path("/reference"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]:
        if not mounted.exists() or mounted.is_symlink() or not os.access(mounted, os.R_OK):
            errors.append(f"MOUNT_INVALID {mounted}")

    trace_summary(Path("/generation-evidence/codex-trace"), errors)

    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
