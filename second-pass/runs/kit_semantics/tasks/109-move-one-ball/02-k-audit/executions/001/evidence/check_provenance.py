#!/usr/bin/env python3
"""Independent integrity checks over launcher-mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reviewer_tree_sha256(root: Path) -> tuple[str, list[tuple[str, str]]]:
    """Hash entry type, relative name, and regular-file content deterministically."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        mode = os.lstat(path).st_mode
        if stat.S_ISREG(mode):
            kind = "file"
            payload = path.read_bytes()
        elif stat.S_ISDIR(mode):
            kind = "dir"
            payload = b""
        elif stat.S_ISLNK(mode):
            kind = "symlink"
            payload = os.readlink(path).encode()
        else:
            kind = f"other:{stat.S_IFMT(mode):o}"
            payload = b""
        digest.update(kind.encode() + b"\0" + rel.encode() + b"\0" + payload + b"\0")
        entries.append((kind, rel))
    return digest.hexdigest(), entries


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
print(f"record_layout={audit['record_layout']}")
print(f"semantics_mode={audit['semantics_mode']}")
print(f"campaign_block_equal={audit['audit_campaign'] == lock}")

checks: dict[str, tuple[Path, str]] = {
    "audit_campaign_lock_sha256": (
        Path("/audit-campaign-lock.json"),
        audit["hashes"]["audit_campaign_lock_sha256"],
    ),
    "canonical_sha256": (Path("/reference/canonical.py"), audit["hashes"]["canonical_sha256"]),
    "trusted_prompt_sha256": (
        Path("/reference/prompt.py"),
        audit["hashes"]["trusted_prompt_sha256"],
    ),
    "candidate_prompt_sha256": (
        Path("/candidate/prompt.py"),
        audit["hashes"]["candidate_prompt_sha256"],
    ),
    "trusted_translator_sha256": (
        Path("/reference/py2mpy.py"),
        audit["hashes"]["trusted_translator_sha256"],
    ),
    "candidate_translator_sha256": (
        Path("/candidate/py2mpy.py"),
        audit["hashes"]["candidate_translator_sha256"],
    ),
    "run_manifest_sha256": (Path("/run.json"), audit["hashes"]["run_manifest_sha256"]),
    "task_manifest_sha256": (Path("/task.json"), audit["hashes"]["task_manifest_sha256"]),
    "stage1_result_sha256": (
        Path("/generation-result.json"),
        audit["hashes"]["stage1_result_sha256"],
    ),
    "stage1_invocation_sha256": (
        Path("/generation-evidence/invocation.json"),
        audit["hashes"]["stage1_invocation_sha256"],
    ),
    "generation_metrics_sha256": (
        Path("/generation-evidence/metrics.json"),
        audit["hashes"]["generation_metrics_sha256"],
    ),
    "generation_runtime_metrics_sha256": (
        Path("/generation-evidence/runtime-metrics.json"),
        audit["hashes"]["generation_runtime_metrics_sha256"],
    ),
    "generation_usage_sha256": (
        Path("/generation-evidence/usage.json"),
        audit["hashes"]["generation_usage_sha256"],
    ),
    "generation_codex_last_sha256": (
        Path("/generation-evidence/codex-last.txt"),
        audit["hashes"]["generation_codex_last_sha256"],
    ),
    "generation_codex_output_sha256": (
        Path("/generation-evidence/codex-output.log"),
        audit["hashes"]["generation_codex_output_sha256"],
    ),
    "generation_prompt_sha256": (
        Path("/generation-evidence/prompt.txt"),
        audit["hashes"]["generation_prompt_sha256"],
    ),
}
failures = 0
for label, (path, expected) in checks.items():
    regular = path.is_file() and not path.is_symlink()
    actual = sha256(path) if regular else "<not-regular>"
    ok = regular and actual == expected
    failures += not ok
    print(f"{label}: regular={regular} expected={expected} actual={actual} ok={ok}")

result = json.loads(Path("/generation-result.json").read_text())
for rel, expected in sorted(result["outputs"]["evidence"].items()):
    path = Path("/generation-evidence") / rel
    regular = path.is_file() and not path.is_symlink()
    actual = sha256(path) if regular else "<not-regular>"
    ok = regular and actual == expected
    failures += not ok
    print(f"stage1_evidence[{rel}]: regular={regular} expected={expected} actual={actual} ok={ok}")

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
required += list(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
for path in required:
    ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
    failures += not ok
    print(f"required_record[{path}]: regular_readable_non_symlink={ok}")

trusted_digest, trusted_entries = reviewer_tree_sha256(Path("/reference/reference-semantics"))
candidate_digest, candidate_entries = reviewer_tree_sha256(Path("/candidate/reference-semantics"))
print(f"trusted_semantics_reviewer_tree_sha256={trusted_digest}")
print(f"candidate_semantics_reviewer_tree_sha256={candidate_digest}")
print(f"semantics_entry_inventory_equal={trusted_entries == candidate_entries}")
print(f"semantics_tree_equal={trusted_digest == candidate_digest}")
print(f"semantics_symlinks={sum(kind == 'symlink' for kind, _ in trusted_entries + candidate_entries)}")
print(f"semantics_other_types={sum(kind.startswith('other:') for kind, _ in trusted_entries + candidate_entries)}")
failures += trusted_digest != candidate_digest
failures += trusted_entries != candidate_entries

full_candidate_digest, full_candidate_entries = reviewer_tree_sha256(Path("/candidate"))
print(f"candidate_reviewer_tree_sha256={full_candidate_digest}")
print(f"candidate_entry_count={len(full_candidate_entries)}")
print(f"candidate_symlinks={sum(kind == 'symlink' for kind, _ in full_candidate_entries)}")
print(f"candidate_other_types={sum(kind.startswith('other:') for kind, _ in full_candidate_entries)}")
for name in ("solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh", "PROOF.md"):
    path = Path("/candidate") / name
    ok = path.is_file() and not path.is_symlink() and os.access(path, os.R_OK)
    failures += not ok
    print(f"required_candidate_artifact[{name}]: regular_readable_non_symlink={ok}")

print(f"provenance_failures={failures}")
raise SystemExit(1 if failures else 0)
