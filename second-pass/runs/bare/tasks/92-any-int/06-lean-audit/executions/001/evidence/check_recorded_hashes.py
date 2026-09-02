#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.klean_audit_contract import verify_stage6_audit_input
from tools.klean_export import tree_digest
from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
inventory = inventory_verification(Path("/reference/k-proof"))

actual = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "obligation_map_sha256": file_sha256(obligation_map_path),
    "trust_inventory_sha256": file_sha256(
        Path("/reference/klean-generation/trust-inventory.json")
    ),
}

stage1_source_actual = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha256(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}

verified_resolution, verified_resolution_hash = verify_stage6_audit_input(
    audit
)
checks = {
    "audit_input_resolution_verified": verified_resolution == resolution,
    "resolved_input_sha256_verified": (
        verified_resolution_hash == audit["resolved_input_sha256"]
    ),
    "all_audit_resolution_hashes_match": all(
        actual[key] == hashes[key]
        for key in (
            "k_workspace_sha256",
            "stage1_export_sha256",
            "discovery_manifest_sha256",
            "k_audit_sha256",
            "klean_generation_sha256",
            "generation_producer_sources_sha256",
            "generated_tree_sha256",
        )
    )
    and hashes["lean_workspace_sha256"] is None
    and hashes["lean_invocation_sha256"] is None,
    "all_stage1_source_hashes_match": (
        stage1_source_actual == resolution["stage1_source_hashes"]
    ),
    "generator_generated_tree_hash_matches": (
        generator["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash_matches": (
        generator["obligation_map_sha256"]
        == actual["obligation_map_sha256"]
    ),
    "generator_stage1_hash_matches": (
        generator["provenance"]["stage1_workspace_sha256"]
        == actual["stage1_export_sha256"]
    ),
    "generator_stage3_hash_matches": (
        generator["provenance"]["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "generator_inventory_hash_matches": (
        generator["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "generator_toolchain_matches_lock": (
        generator["toolchain"] == toolchain_lock
    ),
    "input_manifest_stage1_hashes_match": (
        input_manifest["frozen_input_sha256"]
        == actual["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
    ),
    "input_manifest_stage3_hash_matches": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "input_manifest_verification_hash_matches": (
        input_manifest["verification_sha256"]
        == file_sha256(Path("/reference/k-proof/verification.k"))
    ),
    "export_result_hashes_match": (
        export_result["frozen_input_sha256"]
        == actual["stage1_export_sha256"]
        and export_result["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
        and export_result["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
        and export_result["trust_inventory_sha256"]
        == actual["trust_inventory_sha256"]
    ),
    "preflight_hashes_match": (
        preflight["frozen_input_sha256"]
        == actual["stage1_export_sha256"]
        == preflight["stage1_workspace_sha256"]
        and preflight["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
        and preflight["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
}

print(
    json.dumps(
        {
            "actual": actual,
            "audit_resolution_hashes": hashes,
            "resolved_input_sha256_actual": verified_resolution_hash,
            "resolved_input_sha256_recorded": audit[
                "resolved_input_sha256"
            ],
            "stage1_source_actual": stage1_source_actual,
            "stage1_source_recorded": resolution[
                "stage1_source_hashes"
            ],
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
