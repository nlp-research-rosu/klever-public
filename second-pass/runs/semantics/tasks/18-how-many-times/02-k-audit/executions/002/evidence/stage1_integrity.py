#!/usr/bin/env python3
"""Independent, read-only provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import collections
import hashlib
import json
import os
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN_ROOT = Path("/generation-evidence")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str]]:
    """Map relative paths to (kind, file digest or symlink target)."""
    result: dict[str, tuple[str, str]] = {}

    def visit(directory: Path) -> None:
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if entry.is_symlink():
                result[relative] = ("symlink", os.readlink(path))
            elif entry.is_dir(follow_symlinks=False):
                result[relative] = ("directory", "")
                visit(path)
            elif entry.is_file(follow_symlinks=False):
                result[relative] = ("file", sha256(path))
            else:
                result[relative] = ("other", "")

    visit(root)
    return result


def reviewer_tree_digest(items: dict[str, tuple[str, str]]) -> str:
    """Reviewer-defined digest over kind, relative path, and content digest."""
    digest = hashlib.sha256()
    for relative, (kind, value) in sorted(items.items()):
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def check_file(label: str, path: Path, expected: str | None = None) -> bool:
    if not path.is_file() or path.is_symlink():
        print(f"FAIL {label}: missing, non-regular, or symlink: {path}")
        return False
    actual = sha256(path)
    status = "PASS" if expected is None or actual == expected else "FAIL"
    expected_text = f" expected={expected}" if expected is not None else ""
    print(f"{status} {label}: sha256={actual}{expected_text}")
    return status == "PASS"


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    hashes = audit["hashes"]
    ok = True

    print("DECLARATION")
    print(f"record_layout={audit.get('record_layout')}")
    print(f"semantics_mode={audit.get('semantics_mode')}")
    print(f"mount_reference_semantics={audit.get('mount_reference_semantics')}")

    print("\nCAMPAIGN LOCK")
    ok &= check_file(
        "audit campaign lock",
        LOCK,
        hashes["audit_campaign_lock_sha256"],
    )
    campaign_equal = lock == audit["audit_campaign"]
    print(f"{'PASS' if campaign_equal else 'FAIL'} parsed lock equals audit_campaign block")
    ok &= campaign_equal

    print("\nDECLARED CONTAINER PATHS")
    for label, raw_path in sorted(audit["container_paths"].items()):
        path = Path(raw_path)
        exists = path.exists()
        not_link = not path.is_symlink()
        print(
            f"{'PASS' if exists and not_link else 'FAIL'} "
            f"{label}: path={path} exists={exists} symlink={path.is_symlink()}"
        )
        ok &= exists and not_link

    print("\nREQUIRED LEGACY-SELECTED-STAGE1 RECORDS")
    required_records = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN_ROOT / "invocation.json",
        GEN_ROOT / "metrics.json",
        GEN_ROOT / "codex-last.txt",
        GEN_ROOT / "codex-output.log",
        GEN_ROOT / "prompt.txt",
    ]
    if (GEN_ROOT / "usage.json").exists():
        required_records.append(GEN_ROOT / "usage.json")
    trace_files = sorted((GEN_ROOT / "codex-trace").rglob("*"))
    trace_regular = [
        path for path in trace_files if path.is_file() and not path.is_symlink()
    ]
    for path in required_records:
        regular = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
        print(f"{'PASS' if regular else 'FAIL'} required record: {path}")
        ok &= regular
    trace_ok = bool(trace_regular) and not any(path.is_symlink() for path in trace_files)
    print(
        f"{'PASS' if trace_ok else 'FAIL'} structured trace: "
        f"regular_files={len(trace_regular)} symlinks="
        f"{sum(path.is_symlink() for path in trace_files)}"
    )
    ok &= trace_ok

    print("\nRECORDED FILE HASHES")
    expected_files = [
        ("run manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
        ("task manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
        (
            "generation result",
            Path("/generation-result.json"),
            hashes["stage1_result_sha256"],
        ),
        (
            "generation invocation",
            GEN_ROOT / "invocation.json",
            hashes["stage1_invocation_sha256"],
        ),
        (
            "generation metrics",
            GEN_ROOT / "metrics.json",
            hashes["generation_metrics_sha256"],
        ),
        (
            "generation last",
            GEN_ROOT / "codex-last.txt",
            hashes["generation_codex_last_sha256"],
        ),
        (
            "generation output",
            GEN_ROOT / "codex-output.log",
            hashes["generation_codex_output_sha256"],
        ),
        (
            "generation prompt",
            GEN_ROOT / "prompt.txt",
            hashes["generation_prompt_sha256"],
        ),
        (
            "generation usage",
            GEN_ROOT / "usage.json",
            hashes["generation_usage_sha256"],
        ),
        ("canonical", REFERENCE / "canonical.py", hashes["canonical_sha256"]),
        ("trusted prompt", REFERENCE / "prompt.py", hashes["trusted_prompt_sha256"]),
        (
            "trusted translator",
            REFERENCE / "py2mpy.py",
            hashes["trusted_translator_sha256"],
        ),
        ("candidate prompt", CANDIDATE / "prompt.py", hashes["candidate_prompt_sha256"]),
        (
            "candidate translator",
            CANDIDATE / "py2mpy.py",
            hashes["candidate_translator_sha256"],
        ),
    ]
    for label, path, expected in expected_files:
        ok &= check_file(label, path, expected)

    print("\nGENERATION-RESULT EVIDENCE HASHES")
    generation_result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    for relative, expected in sorted(
        generation_result["outputs"]["evidence"].items()
    ):
        ok &= check_file(
            f"generation-result evidence {relative}",
            GEN_ROOT / relative,
            expected,
        )

    print("\nPROMPT AND TRANSLATOR BYTE IDENTITY")
    for name in ("prompt.py", "py2mpy.py"):
        candidate_bytes = (CANDIDATE / name).read_bytes()
        reference_bytes = (REFERENCE / name).read_bytes()
        equal = candidate_bytes == reference_bytes
        print(f"{'PASS' if equal else 'FAIL'} {name}: byte_equal={equal}")
        ok &= equal

    print("\nSUPPLIED SEMANTICS TREE IDENTITY")
    candidate_semantics = CANDIDATE / "reference-semantics"
    trusted_semantics = REFERENCE / "reference-semantics"
    mode_ok = (
        audit.get("semantics_mode") == "SUPPLIED_SEMANTICS"
        and trusted_semantics.is_dir()
        and not trusted_semantics.is_symlink()
    )
    print(
        f"{'PASS' if mode_ok else 'FAIL'} trusted semantics mount consistent "
        f"with SUPPLIED_SEMANTICS"
    )
    ok &= mode_ok
    candidate_inventory = inventory(candidate_semantics)
    trusted_inventory = inventory(trusted_semantics)
    all_paths = sorted(set(candidate_inventory) | set(trusted_inventory))
    mismatches = [
        (
            relative,
            candidate_inventory.get(relative),
            trusted_inventory.get(relative),
        )
        for relative in all_paths
        if candidate_inventory.get(relative) != trusted_inventory.get(relative)
    ]
    no_bad_types = all(
        kind in {"directory", "file"}
        for kind, _ in candidate_inventory.values()
    )
    semantics_equal = not mismatches and no_bad_types
    print(
        f"{'PASS' if semantics_equal else 'FAIL'} semantics recursive identity: "
        f"candidate_entries={len(candidate_inventory)} "
        f"trusted_entries={len(trusted_inventory)} mismatches={len(mismatches)} "
        f"candidate_bad_types={sum(kind not in {'directory', 'file'} for kind, _ in candidate_inventory.values())}"
    )
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch}")
    print(
        "reviewer_candidate_semantics_tree_sha256="
        f"{reviewer_tree_digest(candidate_inventory)}"
    )
    print(
        "reviewer_trusted_semantics_tree_sha256="
        f"{reviewer_tree_digest(trusted_inventory)}"
    )
    ok &= semantics_equal

    print("\nCANDIDATE AND TRACE INVENTORIES")
    candidate_all = inventory(CANDIDATE)
    trace_inventory = inventory(GEN_ROOT / "codex-trace")
    print(f"candidate_entries={len(candidate_all)}")
    print(f"candidate_symlinks={sum(kind == 'symlink' for kind, _ in candidate_all.values())}")
    print(f"reviewer_candidate_tree_sha256={reviewer_tree_digest(candidate_all)}")
    print(f"trace_entries={len(trace_inventory)}")
    print(f"reviewer_trace_tree_sha256={reviewer_tree_digest(trace_inventory)}")
    for relative, (kind, value) in sorted(candidate_all.items()):
        if kind == "file":
            print(f"CANDIDATE_FILE {relative} {value}")
        else:
            print(f"CANDIDATE_ENTRY {relative} {kind} {value}")

    print("\nSTRUCTURED TRACE PARSE")
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    event_count = 0
    parse_ok = True
    for trace in trace_regular:
        with trace.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                try:
                    item = json.loads(line)
                except Exception as error:
                    parse_ok = False
                    print(f"TRACE_PARSE_ERROR {trace}:{line_number}: {error}")
                    continue
                event_count += 1
                top_types[str(item.get("type"))] += 1
                payload_types[str(item.get("payload", {}).get("type"))] += 1
    print(
        f"{'PASS' if parse_ok and event_count else 'FAIL'} "
        f"trace_jsonl_events={event_count}"
    )
    print(f"top_types={dict(sorted(top_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    ok &= parse_ok and bool(event_count)

    print("\nFINAL")
    print(f"STAGE1_INTEGRITY={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
