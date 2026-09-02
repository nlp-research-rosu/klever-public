#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


reference_generated = Path("/reference/klean-generation/generated")
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/proof-audit.QWcnih")
fresh_base = fresh / "Base"

reference_files = sorted(
    str(path.relative_to(reference_generated))
    for path in reference_generated.rglob("*")
    if path.is_file() and ".lake" not in path.parts
)
fresh_files = sorted(
    str(path.relative_to(fresh_base))
    for path in fresh_base.rglob("*")
    if path.is_file() and ".lake" not in path.parts
)

checks = {
    "fresh_base_tree_matches_reference": (
        klean_export.tree_digest(fresh_base)
        == klean_export.tree_digest(reference_generated)
    ),
    "fresh_base_source_file_list_matches": reference_files == fresh_files,
    "fresh_proof_matches_candidate": (
        sha256_file(fresh / "Proof.lean")
        == sha256_file(candidate / "Proof.lean")
    ),
    "fresh_lakefile_matches_candidate": (
        sha256_file(fresh / "lakefile.lean")
        == sha256_file(candidate / "lakefile.lean")
    ),
    "fresh_lean_toolchain_matches_candidate": (
        sha256_file(fresh / "lean-toolchain")
        == sha256_file(candidate / "lean-toolchain")
    ),
}

print(
    json.dumps(
        {
            "fresh_workspace": str(fresh),
            "reference_generated_tree_sha256": klean_export.tree_digest(
                reference_generated
            ),
            "fresh_base_tree_sha256": klean_export.tree_digest(fresh_base),
            "reference_source_files": reference_files,
            "fresh_source_files": fresh_files,
            "candidate_Proof_lean_sha256": sha256_file(
                candidate / "Proof.lean"
            ),
            "fresh_Proof_lean_sha256": sha256_file(fresh / "Proof.lean"),
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
