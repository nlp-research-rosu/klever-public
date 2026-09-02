#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.klean_export import expected_target_definition, target_statement


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

canonical = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())
validated = validate_trust_boundary(workspace, discovery_path)
obligation_map = json.loads((generated / "obligation-map.json").read_text())
generator = json.loads((generation / "generator-manifest.json").read_text())
audit_resolution = json.loads(Path("/audit-input.json").read_text())["resolution"]

canonical_ids = [entry["source_rule_id"] for entry in canonical["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
source_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
actual_target = target_statement(generated)

print(
    json.dumps(
        {
            "canonical_inventory": canonical,
            "canonical_manifest_order_equal": canonical_ids == manifest_ids,
            "canonical_manifest_id_sets_equal": set(canonical_ids)
            == set(manifest_ids),
            "manifest_duplicate_ids": len(manifest_ids)
            != len(set(manifest_ids)),
            "validated_classification_counts": {
                key: len(validated[key])
                for key in (
                    "definitions",
                    "operational_rules",
                    "proved_derived_lemmas",
                    "domain_lemmas",
                )
            },
            "source_rule_ids": source_ids,
            "obligation_ids": obligation_ids,
            "source_obligation_order_equal": source_ids == obligation_ids,
            "obligation_duplicate_ids": len(obligation_ids)
            != len(set(obligation_ids)),
            "obligation_count_manifest": generator["obligation_count"],
            "obligation_count_actual": len(obligation_map["obligations"]),
            "expected_target_definition": expected_target_definition(
                obligation_map
            ),
            "actual_target": actual_target,
            "generator_target": generator["target"],
            "audit_input_target": audit_resolution["target"],
            "targets_equal": actual_target
            == generator["target"]
            == audit_resolution["target"],
            "candidate_present": Path("/candidate").exists(),
        },
        indent=2,
        sort_keys=True,
    )
)
