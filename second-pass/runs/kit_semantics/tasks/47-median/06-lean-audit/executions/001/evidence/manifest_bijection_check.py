import hashlib
import json
from pathlib import Path

from tools import klean_export, k_rule_inventory, lemma_discovery_contract

root = Path("/reference/k-proof")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

validated = lemma_discovery_contract.validate_trust_boundary(root, discovery)
inventory = k_rule_inventory.inventory_verification(root)
discovery_hash = hashlib.sha256(discovery.read_bytes()).hexdigest()
stage1_hash = klean_export.tree_digest(root)
generated_hash = klean_export.tree_digest(generated)
verification_hash = hashlib.sha256((root / "verification.k").read_bytes()).hexdigest()
obligation_map_hash = hashlib.sha256((generated / "obligation-map.json").read_bytes()).hexdigest()
trust_hash = hashlib.sha256((generation / "trust-inventory.json").read_bytes()).hexdigest()

checks = {
    "input.inventory": input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
    "input.frozen": input_manifest["frozen_input_sha256"] == stage1_hash,
    "input.stage1": input_manifest["stage1_workspace_sha256"] == stage1_hash,
    "input.stage3": input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash,
    "input.verification": input_manifest["verification_sha256"] == verification_hash,
    "input.source_rules_empty": input_manifest["source_rules"] == [],
    "input.all_class_buckets_empty": all(
        input_manifest[key] == []
        for key in ["definitions", "operational_rules", "proved_derived_lemmas"]
    ),
    "generator.generated_tree": generator_manifest["generated_tree_sha256"] == generated_hash,
    "generator.obligation_map": generator_manifest["obligation_map_sha256"] == obligation_map_hash,
    "generator.obligation_count_zero": generator_manifest["obligation_count"] == 0,
    "generator.target_null": generator_manifest["target"] is None,
    "generator.inventory": generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"],
    "generator.stage1": generator_manifest["provenance"]["stage1_workspace_sha256"] == stage1_hash,
    "generator.stage3": generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] == discovery_hash,
    "generator.toolchain_lock": generator_manifest["toolchain"] == toolchain_lock,
    "export.frozen": export_result["frozen_input_sha256"] == stage1_hash,
    "export.generated_tree": export_result["generated_tree_sha256"] == generated_hash,
    "export.stage3": export_result["stage3_discovery_manifest_sha256"] == discovery_hash,
    "export.trust_inventory": export_result["trust_inventory_sha256"] == trust_hash,
    "export.zero_status": export_result["status"] == "KLEAN_NO_OBLIGATIONS" and export_result["obligation_count"] == 0,
    "obligation_map.schema": obligation_map["schema_version"] == 3,
    "obligation_map.source_rules_empty": obligation_map["source_rules"] == [],
    "obligation_map.obligations_empty": obligation_map["obligations"] == [],
    "obligation_map.trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "target_parser_none": klean_export.target_statement(generated) is None,
    "expected_target_none": klean_export.expected_target_definition(obligation_map) is None,
    "discovery_rules_empty": validated["rules"] == [],
    "discovery_domain_empty": validated["domain_lemmas"] == [],
}

print(json.dumps({
    "checks": checks,
    "all_match": all(checks.values()),
    "values": {
        "stage1_export_sha256": stage1_hash,
        "discovery_sha256": discovery_hash,
        "inventory_sha256": inventory["inventory_sha256"],
        "verification_sha256": verification_hash,
        "generated_tree_sha256": generated_hash,
        "obligation_map_sha256": obligation_map_hash,
        "trust_inventory_sha256": trust_hash,
        "trust_allowlist_count": len(trust_inventory["allowlist"]),
    },
}, indent=2, sort_keys=True))
