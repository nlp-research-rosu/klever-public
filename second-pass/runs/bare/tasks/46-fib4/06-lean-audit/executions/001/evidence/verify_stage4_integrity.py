#!/usr/bin/env python3
"""Independent Stage 4 provenance, bijection, and fixed-target checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree


AUDIT_INPUT = Path("/audit-input.json")
K_INPUT = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(AUDIT_INPUT)
resolution = audit["resolution"]
audit_hashes = resolution["hashes"]
source_manifest = load(PRODUCERS / "source-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
export_result = load(GENERATION / "export-result.json")
stored_preflight = load(GENERATION / "preflight.json")
obligation_map = load(GENERATED / "obligation-map.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
toolchain_lock = load(TOOLCHAIN_LOCK)
validated = validate_trust_boundary(K_INPUT, DISCOVERY)

recomputed = {
    "audit_input_sha256": file_sha256(AUDIT_INPUT),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "generated_tree_sha256": tree_digest(GENERATED),
    "generation_tree_sha256": sha256_tree(GENERATION),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "k_audit_tree_sha256": sha256_tree(Path("/reference/k-audit")),
    "k_workspace_export_sha256": tree_digest(K_INPUT),
    "k_workspace_tree_sha256": sha256_tree(K_INPUT),
    "klean_export_py_sha256": file_sha256(PRODUCERS / "klean_export.py"),
    "klean_py_sha256": file_sha256(PRODUCERS / "klean.py"),
    "obligation_map_sha256": file_sha256(GENERATED / "obligation-map.json"),
    "trust_inventory_sha256": file_sha256(
        GENERATION / "trust-inventory.json"
    ),
    "verification_sha256": file_sha256(K_INPUT / "verification.k"),
}

image_id = generator_manifest["provenance"]["generator_image_id"]
producer_path_image = Path(
    resolution["generation_producer_sources"]
).name
discovery_domain_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]

# This is the independently reached semantic classification recorded by the
# audit, not a value copied from the discovery manifest.
independent_domain_ids: list[str] = []
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]
observed_target = target_statement(GENERATED)

checks = {
    "audit_discovery_hash": recomputed["discovery_manifest_sha256"]
    == audit_hashes["discovery_manifest_sha256"],
    "audit_generated_tree_hash": recomputed["generated_tree_sha256"]
    == audit_hashes["generated_tree_sha256"],
    "audit_generation_tree_hash": recomputed["generation_tree_sha256"]
    == audit_hashes["klean_generation_sha256"],
    "audit_producer_tree_hash": recomputed[
        "generation_producer_sources_sha256"
    ]
    == audit_hashes["generation_producer_sources_sha256"],
    "audit_k_audit_tree_hash": recomputed["k_audit_tree_sha256"]
    == audit_hashes["k_audit_sha256"],
    "audit_k_workspace_export_hash": recomputed["k_workspace_export_sha256"]
    == audit_hashes["stage1_export_sha256"],
    "audit_k_workspace_tree_hash": recomputed["k_workspace_tree_sha256"]
    == audit_hashes["k_workspace_sha256"],
    "producer_exporter_hash_manifest": recomputed["klean_export_py_sha256"]
    == source_manifest["files"]["klean_export.py"]
    == generator_manifest["exporter_sha256"],
    "producer_klean_hash_manifest": recomputed["klean_py_sha256"]
    == source_manifest["files"]["klean.py"]
    == generator_manifest["klean_py_sha256"],
    "producer_image_id_all_records": source_manifest["generator_image_id"]
    == image_id
    == f"sha256:{producer_path_image}",
    "generator_generated_tree_hash": recomputed["generated_tree_sha256"]
    == generator_manifest["generated_tree_sha256"],
    "generator_obligation_map_hash": recomputed["obligation_map_sha256"]
    == generator_manifest["obligation_map_sha256"],
    "generator_inventory_hash": generator_manifest["provenance"][
        "inventory_sha256"
    ]
    == input_manifest["inventory_sha256"]
    == validated["inventory_sha256"],
    "generator_stage1_hash": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == input_manifest["stage1_workspace_sha256"]
    == input_manifest["frozen_input_sha256"]
    == recomputed["k_workspace_export_sha256"],
    "generator_stage3_hash": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == recomputed["discovery_manifest_sha256"],
    "input_verification_hash": input_manifest["verification_sha256"]
    == recomputed["verification_sha256"],
    "generator_toolchain_lock_exact": generator_manifest["toolchain"]
    == toolchain_lock,
    "export_frozen_hash": export_result["frozen_input_sha256"]
    == recomputed["k_workspace_export_sha256"],
    "export_discovery_hash": export_result[
        "stage3_discovery_manifest_sha256"
    ]
    == recomputed["discovery_manifest_sha256"],
    "export_generated_tree_hash": export_result["generated_tree_sha256"]
    == recomputed["generated_tree_sha256"],
    "export_trust_inventory_hash": export_result["trust_inventory_sha256"]
    == recomputed["trust_inventory_sha256"],
    "stored_preflight_hashes": (
        stored_preflight["frozen_input_sha256"]
        == recomputed["k_workspace_export_sha256"]
        and stored_preflight["stage1_workspace_sha256"]
        == recomputed["k_workspace_export_sha256"]
        and stored_preflight["stage3_discovery_manifest_sha256"]
        == recomputed["discovery_manifest_sha256"]
        and stored_preflight["generated_tree_sha256"]
        == recomputed["generated_tree_sha256"]
    ),
    "independent_domain_set_equals_discovery": independent_domain_ids
    == discovery_domain_ids,
    "domain_set_equals_input_source_rules": independent_domain_ids
    == [rule["source_rule_id"] for rule in input_manifest["source_rules"]],
    "domain_set_equals_map_source_rules": independent_domain_ids
    == map_source_ids,
    "source_obligation_ordered_bijection": map_source_ids == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
    "empty_obligations": obligation_map["obligations"] == [],
    "empty_trust_parameters": obligation_map["trust_parameters"] == [],
    "all_obligation_counts_zero": generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == stored_preflight["obligation_count"]
    == len(obligation_map["obligations"])
    == 0,
    "all_statuses_no_obligations": generator_manifest["target"] is None
    and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and stored_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    "fixed_target_absent_everywhere": observed_target is None
    and generator_manifest["target"] is None
    and stored_preflight["target"] is None
    and resolution["target"] is None,
    "classification_mode_and_no_candidate": resolution["mode"]
    == "CLASSIFICATION_ONLY"
    and not Path("/candidate").exists()
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None,
    "trust_inventory_shape": trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0
    and len(trust_inventory["allowlist"]) == 41,
}

print(
    json.dumps(
        {
            "checks": checks,
            "all_checks_pass": all(checks.values()),
            "recomputed": recomputed,
            "independent_domain_rule_ids": independent_domain_ids,
            "discovery_domain_rule_ids": discovery_domain_ids,
            "map_source_rule_ids": map_source_ids,
            "obligation_rule_ids": obligation_ids,
            "observed_target": observed_target,
        },
        indent=2,
        sort_keys=True,
    )
)
