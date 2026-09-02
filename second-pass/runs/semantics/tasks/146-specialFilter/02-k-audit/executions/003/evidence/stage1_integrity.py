#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def tree_inventory(root: Path) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            entries.append((relative, "file", sha256_file(path)))
        elif stat.S_ISDIR(mode):
            entries.append((relative, "dir", "-"))
        elif stat.S_ISLNK(mode):
            entries.append((relative, "symlink", os.readlink(path)))
        else:
            entries.append((relative, f"special:{stat.S_IFMT(mode):o}", "-"))
    return entries


def canonical_tree_digest(entries: list[tuple[str, str, str]]) -> str:
    """Reviewer-defined digest over path, entry type, and file hash."""
    digest = hashlib.sha256()
    for relative, kind, value in entries:
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(kind.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def print_hash_check(label: str, path: Path, expected: str | None) -> None:
    actual = sha256_file(path)
    status = "MATCH" if expected == actual else "MISMATCH"
    print(f"{label}: {status} actual={actual} expected={expected} path={path}")


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    campaign = json.loads(CAMPAIGN_LOCK.read_text())
    hashes = audit["hashes"]

    print(f"record_layout={audit['record_layout']}")
    print(f"semantics_mode={audit['semantics_mode']}")
    print(f"campaign_object_equal={campaign == audit['audit_campaign']}")
    print_hash_check(
        "campaign-lock",
        CAMPAIGN_LOCK,
        hashes["audit_campaign_lock_sha256"],
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required:
        kind = (
            "symlink"
            if path.is_symlink()
            else "dir"
            if path.is_dir()
            else "file"
            if path.is_file()
            else "missing-or-special"
        )
        print(f"required_record={path} kind={kind} readable={os.access(path, os.R_OK)}")

    direct_hashes = [
        ("canonical", Path("/reference/canonical.py"), "canonical_sha256"),
        ("trusted-prompt", Path("/reference/prompt.py"), "trusted_prompt_sha256"),
        ("candidate-prompt", Path("/candidate/prompt.py"), "candidate_prompt_sha256"),
        ("trusted-translator", Path("/reference/py2mpy.py"), "trusted_translator_sha256"),
        ("candidate-translator", Path("/candidate/py2mpy.py"), "candidate_translator_sha256"),
        ("run", Path("/run.json"), "run_manifest_sha256"),
        ("task", Path("/task.json"), "task_manifest_sha256"),
        ("result", Path("/generation-result.json"), "stage1_result_sha256"),
        ("invocation", Path("/generation-evidence/invocation.json"), "stage1_invocation_sha256"),
        ("metrics", Path("/generation-evidence/metrics.json"), "generation_metrics_sha256"),
        ("usage", Path("/generation-evidence/usage.json"), "generation_usage_sha256"),
        ("last", Path("/generation-evidence/codex-last.txt"), "generation_codex_last_sha256"),
        ("output", Path("/generation-evidence/codex-output.log"), "generation_codex_output_sha256"),
        ("generation-prompt", Path("/generation-evidence/prompt.txt"), "generation_prompt_sha256"),
    ]
    for label, path, key in direct_hashes:
        print_hash_check(label, path, hashes.get(key))

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    for record_name, record in [("generation-result", result), ("invocation", invocation)]:
        evidence = record["outputs"]["evidence"]
        for relative, expected in sorted(evidence.items()):
            print_hash_check(
                f"{record_name}-evidence:{relative}",
                Path("/generation-evidence") / relative,
                expected,
            )

    trusted_root = Path("/reference/reference-semantics")
    candidate_root = Path("/candidate/reference-semantics")
    trusted_entries = tree_inventory(trusted_root)
    candidate_entries = tree_inventory(candidate_root)
    print(f"trusted_semantics_entry_count={len(trusted_entries)}")
    print(f"candidate_semantics_entry_count={len(candidate_entries)}")
    print(f"semantics_inventories_equal={trusted_entries == candidate_entries}")
    print(f"trusted_semantics_reviewer_tree_sha256={canonical_tree_digest(trusted_entries)}")
    print(f"candidate_semantics_reviewer_tree_sha256={canonical_tree_digest(candidate_entries)}")
    for item in trusted_entries:
        print("trusted-semantics-entry=" + "\t".join(item))
    for item in candidate_entries:
        print("candidate-semantics-entry=" + "\t".join(item))

    candidate_entries_all = tree_inventory(Path("/candidate"))
    generation_entries = tree_inventory(Path("/generation-evidence"))
    print(f"candidate_reviewer_tree_sha256={canonical_tree_digest(candidate_entries_all)}")
    print(f"generation_evidence_reviewer_tree_sha256={canonical_tree_digest(generation_entries)}")
    for root_label, entries in [
        ("candidate", candidate_entries_all),
        ("generation", generation_entries),
    ]:
        bad_types = [entry for entry in entries if entry[1] not in {"file", "dir"}]
        print(f"{root_label}_non_file_dir_entries={bad_types}")

    print(
        "candidate_prompt_byte_equal="
        + str(Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes())
    )
    print(
        "candidate_translator_byte_equal="
        + str(Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes())
    )

    failures = []
    if campaign != audit["audit_campaign"]:
        failures.append("campaign object mismatch")
    if any(not path.exists() or not os.access(path, os.R_OK) for path in required):
        failures.append("required record absent or unreadable")
    if trusted_entries != candidate_entries:
        failures.append("candidate supplied-semantics mismatch")
    if Path("/candidate/prompt.py").read_bytes() != Path("/reference/prompt.py").read_bytes():
        failures.append("candidate prompt mismatch")
    if Path("/candidate/py2mpy.py").read_bytes() != Path("/reference/py2mpy.py").read_bytes():
        failures.append("candidate translator mismatch")

    print(f"integrity_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
