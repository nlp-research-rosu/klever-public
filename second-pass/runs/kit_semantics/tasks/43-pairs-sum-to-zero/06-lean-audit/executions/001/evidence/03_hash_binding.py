#!/usr/bin/env python3
"""Recompute every mounted hash bound by the Stage 6 audit input."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
expected = resolution["hashes"]

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

print(
    json.dumps(
        {
            "resolved_input_sha256_recorded": document["resolved_input_sha256"],
            "resolved_input_sha256_verified": resolved_digest,
            "resolved_input_digest_equal": (
                document["resolved_input_sha256"] == resolved_digest
            ),
        },
        indent=2,
    )
)

all_bound_hashes_match = True
for name, actual in observed.items():
    wanted = expected[name]
    matched = actual == wanted
    all_bound_hashes_match &= matched
    print(
        json.dumps(
            {
                "name": name,
                "expected": wanted,
                "observed": actual,
                "match": matched,
            },
            sort_keys=True,
        )
    )

source_expected = resolution["stage1_source_hashes"]
source_missing: list[str] = []
source_mismatches: list[dict[str, str]] = []
for relative, wanted in source_expected.items():
    path = Path("/reference/k-proof") / relative
    if not path.is_file() or path.is_symlink():
        source_missing.append(relative)
        continue
    actual = file_sha256(path)
    if actual != wanted:
        source_mismatches.append(
            {"path": relative, "expected": wanted, "observed": actual}
        )

print(
    json.dumps(
        {
            "stage1_source_hash_count": len(source_expected),
            "stage1_source_missing": source_missing,
            "stage1_source_mismatches": source_mismatches,
            "stage1_source_hashes_all_match": (
                not source_missing and not source_mismatches
            ),
        },
        indent=2,
    )
)

lock_path = Path("/reference/klean-toolchain.lock.json")
toolchain_lock = json.loads(lock_path.read_text())
generator_toolchain = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)["toolchain"]
lock_actual = file_sha256(lock_path)
stage2_input = json.loads(
    Path("/reference/k-audit/audit-input.json").read_text()
)
lock_expected = stage2_input["audit_campaign"]["toolchain_lock_sha256"]
print(
    json.dumps(
        {
            "toolchain_lock_expected_from_stage2_binding": lock_expected,
            "toolchain_lock_observed": lock_actual,
            "toolchain_lock_hash_match": lock_actual == lock_expected,
            "toolchain_lock_matches_generator_manifest": (
                toolchain_lock == generator_toolchain
            ),
            "audit_mechanical_checker_lock_sha256": document["audit"][
                "mechanical_checker_lock_sha256"
            ],
            "audit_mechanical_checker_lock_artifact_mounted": False,
            "note": (
                "The audit-image mechanical-checker lock and the K/Lean "
                "toolchain inventory are distinct launcher artifacts."
            ),
        },
        indent=2,
    )
)

# The Lean invocation tree itself is intentionally not mounted. Record this
# launcher-bound hash as unavailable rather than pretending it was recomputed.
print(
    json.dumps(
        {
            "lean_invocation_sha256_recorded": expected[
                "lean_invocation_sha256"
            ],
            "lean_invocation_tree_mounted": False,
        },
        indent=2,
    )
)

if not (
    all_bound_hashes_match
    and not source_missing
    and not source_mismatches
    and lock_actual == lock_expected
    and toolchain_lock == generator_toolchain
):
    raise SystemExit("MOUNTED_HASH_BINDING: FAIL")

print("MOUNTED_HASH_BINDING: PASS")
