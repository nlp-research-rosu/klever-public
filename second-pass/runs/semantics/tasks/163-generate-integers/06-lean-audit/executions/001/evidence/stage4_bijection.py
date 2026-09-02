import json
from pathlib import Path

from tools import k_rule_inventory
from tools import klean_export
from tools import lemma_discovery_contract


workspace = Path("/reference/k-proof")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
raw = k_rule_inventory.inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery
)
discovery_document = json.loads(discovery.read_text())
input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
obligation_map = json.loads(
    (generation / "generated/obligation-map.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
checks = {
    "manifest_order_exact": (
        [
            entry["source_rule_id"]
            for entry in discovery_document["rules"]
        ]
        == [entry["source_rule_id"] for entry in raw["rules"]]
    ),
    "manifest_id_unique": (
        len(
            {
                entry["source_rule_id"]
                for entry in discovery_document["rules"]
            }
        )
        == len(discovery_document["rules"])
    ),
    "manifest_rule_count": len(discovery_document["rules"]),
    "inventory_rule_count": len(raw["rules"]),
    "inventory_hash_match": (
        discovery_document["inventory_sha256"]
        == raw["inventory_sha256"]
    ),
    "validated_definitions_count": len(validated["definitions"]),
    "validated_operational_rules_count": len(
        validated["operational_rules"]
    ),
    "validated_proved_derived_lemmas_count": len(
        validated["proved_derived_lemmas"]
    ),
    "validated_domain_lemmas_count": len(validated["domain_lemmas"]),
    "input_definitions_exact": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "input_source_rules_exact": (
        input_manifest["source_rules"] == validated["domain_lemmas"]
    ),
    "obligation_source_rules_exact": (
        obligation_map["source_rules"] == input_manifest["source_rules"]
    ),
    "obligations_count": len(obligation_map["obligations"]),
    "obligation_ids_unique": (
        len(
            {
                entry.get("source_rule_id")
                for entry in obligation_map["obligations"]
            }
        )
        == len(obligation_map["obligations"])
    ),
    "generator_obligation_count": generator_manifest[
        "obligation_count"
    ],
    "expected_target_definition": (
        klean_export.expected_target_definition(obligation_map)
    ),
    "observed_target": klean_export.target_statement(
        generation / "generated"
    ),
    "generator_target": generator_manifest["target"],
}
print(json.dumps(checks, indent=2, sort_keys=True))
