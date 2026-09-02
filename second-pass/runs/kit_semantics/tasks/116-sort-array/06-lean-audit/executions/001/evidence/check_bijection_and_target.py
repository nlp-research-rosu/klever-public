#!/usr/bin/env python3
"""Independent empty-domain, obligation-bijection, and target-identity checks."""

from __future__ import annotations

import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
inventory = inventory_verification(workspace)

# This table is the audit's independent mathematical classification, derived
# from the frozen rules and recorded here separately from Stage 3's labels.
independent = {
    "rule-f5c7b761ec71892275f909c07e8f29124daca7a634e74c5709cda21666d9b165": {
        "classification": "DEFINITION",
        "judgment": "base equation for the newly declared allIntVS summary",
    },
    "rule-581f4df071fdd7d974c5141cf36a1e876f38b798cc51952636578533c09a0f8a": {
        "classification": "DEFINITION",
        "judgment": "structural recurrence for allIntVS on the strict ValSeq tail",
    },
    "rule-7a08aa58034b9a659c1e60660998e0b301a0f3e3408204cc84b658c58946b4d0": {
        "classification": "DEFINITION",
        "judgment": "nonnegative defining equation for the named popcountAbs summary",
    },
    "rule-caabcce04b85453cd68f8e2e64ab67393a09fdfcffd4cf6a5de838b958201752": {
        "classification": "DEFINITION",
        "judgment": "negative defining equation for popcountAbs via integer magnitude",
    },
}

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
independent_ids = list(independent)
independent_domain_ids = [
    source_rule_id
    for source_rule_id, entry in independent.items()
    if entry["classification"] == "DOMAIN_LEMMA"
]
discovery_domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
obligation_source_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]
generated_target = klean_export.target_statement(generated)

checks = {
    "independent_classification_covers_inventory_in_order": inventory_ids == independent_ids,
    "independent_domain_set_is_empty": independent_domain_ids == [],
    "stage3_domain_set_matches_independent_set": discovery_domain_ids == independent_domain_ids,
    "input_manifest_source_rules_match_domain_set": (
        [rule["source_rule_id"] for rule in input_manifest["source_rules"]]
        == independent_domain_ids
    ),
    "obligation_map_source_rules_match_domain_set": (
        obligation_map["source_rules"] == independent_domain_ids
    ),
    "obligations_biject_with_domain_set": obligation_source_ids == independent_domain_ids,
    "no_duplicate_obligations": len(obligation_source_ids) == len(set(obligation_source_ids)),
    "all_obligation_counts_zero": (
        len(obligation_map["obligations"])
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == 0
    ),
    "fixed_generated_target_absent": (
        generated_target is None
        and generator_manifest["target"] is None
        and audit["target"] is None
    ),
    "stage4_status_is_no_obligations": export_result["status"] == "KLEAN_NO_OBLIGATIONS",
    "no_stage5_candidate": not Path("/candidate").exists(),
}

print(
    json.dumps(
        {
            "inventory_ids": inventory_ids,
            "independent_classification": independent,
            "independent_domain_ids": independent_domain_ids,
            "discovery_domain_ids": discovery_domain_ids,
            "obligation_source_ids": obligation_source_ids,
            "generated_target": generated_target,
            "checks": checks,
            "overall": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
