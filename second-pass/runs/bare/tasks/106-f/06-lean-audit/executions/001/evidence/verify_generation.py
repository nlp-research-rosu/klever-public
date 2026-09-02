import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.klean_export import (
    expected_target_definition,
    target_statement,
    tree_digest,
)


k = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust = json.loads((generation / "trust-inventory.json").read_text())
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
validated = validate_trust_boundary(k, discovery_path)
inventory = inventory_verification(k)

# The separate independent classification in reconstruct_inventory.py found
# zero DOMAIN_LEMMA entries. The protected manifest must encode that same set.
source_rules = validated["domain_lemmas"]
obligations = obligation_map["obligations"]
expected_ids = [rule["source_rule_id"] for rule in source_rules]
observed_ids = [item["source_rule_id"] for item in obligations]
actual_target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)
actual = {
    "frozen_input_sha256": tree_digest(k),
    "discovery_manifest_sha256": hashlib.sha256(
        discovery_path.read_bytes()
    ).hexdigest(),
    "generated_tree_sha256": tree_digest(generated),
    "verification_sha256": hashlib.sha256(
        (k / "verification.k").read_bytes()
    ).hexdigest(),
    "obligation_map_sha256": hashlib.sha256(
        obligation_path.read_bytes()
    ).hexdigest(),
    "trust_inventory_sha256": hashlib.sha256(
        (generation / "trust-inventory.json").read_bytes()
    ).hexdigest(),
}
checks = {
    "input_frozen_hash": (
        input_manifest["frozen_input_sha256"]
        == actual["frozen_input_sha256"]
    ),
    "input_stage1_hash": (
        input_manifest["stage1_workspace_sha256"]
        == actual["frozen_input_sha256"]
    ),
    "input_discovery_hash": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "input_inventory_hash": (
        input_manifest["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "input_verification_hash": (
        input_manifest["verification_sha256"]
        == actual["verification_sha256"]
    ),
    "input_definitions_exact": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "input_operational_rules_exact": (
        input_manifest["operational_rules"]
        == validated["operational_rules"]
    ),
    "input_proved_derived_exact": (
        input_manifest["proved_derived_lemmas"]
        == validated["proved_derived_lemmas"]
    ),
    "input_domain_source_rules_exact": (
        input_manifest["source_rules"] == source_rules
    ),
    "generator_generated_tree_hash": (
        generator_manifest["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "generator_obligation_map_hash": (
        generator_manifest["obligation_map_sha256"]
        == actual["obligation_map_sha256"]
    ),
    "generator_inventory_provenance": (
        generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"]
    ),
    "generator_stage1_provenance": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == actual["frozen_input_sha256"]
    ),
    "generator_stage3_provenance": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == actual["discovery_manifest_sha256"]
    ),
    "generator_toolchain_lock_exact": (
        generator_manifest["toolchain"]
        == json.loads(
            Path("/reference/klean-toolchain.lock.json").read_text()
        )
    ),
    "source_rule_ordered_bijection": expected_ids == observed_ids,
    "source_rule_ids_unique": len(expected_ids) == len(set(expected_ids)),
    "obligation_ids_unique": len(observed_ids) == len(set(observed_ids)),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"] == source_rules
    ),
    "obligation_count_exact": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == len(obligations)
    ),
    "trust_parameters_empty": obligation_map["trust_parameters"] == [],
    "expected_target_definition_absent": expected_definition is None,
    "actual_target_absent": actual_target is None,
    "all_target_records_null": (
        generator_manifest["target"] is None
        and preflight["target"] is None
        and audit["target"] is None
    ),
    "export_status_exact": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "preflight_status_exact": (
        preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
    "export_generated_tree_hash": (
        export_result["generated_tree_sha256"]
        == actual["generated_tree_sha256"]
    ),
    "export_frozen_hash": (
        export_result["frozen_input_sha256"]
        == actual["frozen_input_sha256"]
    ),
    "export_discovery_hash": (
        export_result["stage3_discovery_manifest_sha256"]
        == actual["discovery_manifest_sha256"]
    ),
    "export_trust_inventory_hash": (
        export_result["trust_inventory_sha256"]
        == actual["trust_inventory_sha256"]
    ),
    "trust_inventory_zero_holes": (
        trust["designated_sorries"] == trust["other_sorries"] == 0
    ),
    "audit_preflight_exact": audit["stage4_preflight"] == preflight,
}
result = {
    "actual_hashes": actual,
    "independently_reclassified_domain_rule_count": 0,
    "protected_manifest_domain_rule_count": len(source_rules),
    "mapped_obligation_count": len(obligations),
    "expected_source_rule_ids": expected_ids,
    "observed_obligation_ids": observed_ids,
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))

assert all(checks.values())
assert len(source_rules) == len(obligations) == 0
