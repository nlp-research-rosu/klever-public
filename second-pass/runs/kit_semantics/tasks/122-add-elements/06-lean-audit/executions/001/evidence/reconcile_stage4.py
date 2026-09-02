#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


stage1 = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
obligation_map_path = generated / "obligation-map.json"

audit_input = load("/audit-input.json")["resolution"]
discovery = load(str(discovery_path))
input_manifest = load(str(generation / "input-manifest.json"))
generator_manifest = load(str(generation / "generator-manifest.json"))
export_result = load(str(generation / "export-result.json"))
trust_inventory_path = generation / "trust-inventory.json"
obligation_map = load(str(obligation_map_path))
inventory = inventory_verification(stage1)

stage1_hash = tree_digest(stage1)
discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
generated_hash = tree_digest(generated)
verification_hash = hashlib.sha256(
    (stage1 / "verification.k").read_bytes()
).hexdigest()
obligation_map_hash = hashlib.sha256(
    obligation_map_path.read_bytes()
).hexdigest()
trust_inventory_hash = hashlib.sha256(
    trust_inventory_path.read_bytes()
).hexdigest()
target = target_statement(generated)

classified_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
source_rule_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]

checks = {
    "stage1_hash_input_manifest": (
        input_manifest["frozen_input_sha256"] == stage1_hash
        and input_manifest["stage1_workspace_sha256"] == stage1_hash
    ),
    "stage1_hash_generator_provenance": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == stage1_hash
    ),
    "stage1_hash_export_result": (
        export_result["frozen_input_sha256"] == stage1_hash
    ),
    "stage1_hash_audit_input": (
        audit_input["hashes"]["stage1_export_sha256"] == stage1_hash
    ),
    "discovery_hash_input_manifest": (
        input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
    ),
    "discovery_hash_generator_provenance": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_hash
    ),
    "discovery_hash_export_result": (
        export_result["stage3_discovery_manifest_sha256"] == discovery_hash
    ),
    "discovery_hash_audit_input": (
        audit_input["hashes"]["discovery_manifest_sha256"]
        == discovery_hash
    ),
    "verification_hash": (
        input_manifest["verification_sha256"] == verification_hash
        == inventory["verification_sha256"]
    ),
    "inventory_hash": (
        discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "classification_bijection_and_order": classified_ids == inventory_ids,
    "domain_source_bijection_and_order": (
        domain_ids == source_rule_ids == obligation_ids
    ),
    "no_duplicate_ids": (
        len(classified_ids) == len(set(classified_ids))
        and len(source_rule_ids) == len(set(source_rule_ids))
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "obligation_count": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == len(obligation_ids)
    ),
    "obligation_map_hash": (
        generator_manifest["obligation_map_sha256"] == obligation_map_hash
    ),
    "generated_tree_hash": (
        generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == audit_input["hashes"]["generated_tree_sha256"]
        == generated_hash
    ),
    "trust_inventory_hash": (
        export_result["trust_inventory_sha256"] == trust_inventory_hash
    ),
    "fixed_target": (
        target
        == generator_manifest["target"]
        == audit_input["target"]
        is None
    ),
    "no_obligation_status": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
}

print("observed_stage1_tree_sha256=", stage1_hash)
print("observed_discovery_sha256=", discovery_hash)
print("observed_generated_tree_sha256=", generated_hash)
print("observed_verification_sha256=", verification_hash)
print("observed_inventory_sha256=", inventory["inventory_sha256"])
print("inventory_ids=", inventory_ids)
print("classified_ids=", classified_ids)
print("domain_ids=", domain_ids)
print("mapped_source_rule_ids=", source_rule_ids)
print("obligation_ids=", obligation_ids)
print("observed_target=", target)
for name, passed in checks.items():
    print(f"{name}={passed}")
print("all_checks_pass=", all(checks.values()))
