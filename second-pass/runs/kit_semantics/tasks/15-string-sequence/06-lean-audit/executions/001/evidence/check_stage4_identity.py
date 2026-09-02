#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools import k_rule_inventory, klean_export

generation = Path("/reference/klean-generation")
generated = generation / "generated"
workspace = Path("/reference/k-proof")

audit_target = json.loads(Path("/audit-input.json").read_text())[
    "resolution"
]["target"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
inventory = k_rule_inventory.inventory_verification(workspace)

inventory_by_id = {
    entry["source_rule_id"]: entry for entry in inventory["rules"]
}
domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
mapped_source_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
expected_definition_sha256 = klean_export.sha256_text(expected_definition)

span_and_hash_checks = []
for entry in obligation_map["source_rules"]:
    reconstructed = inventory_by_id[entry["source_rule_id"]]
    span_and_hash_checks.append(
        {
            "source_rule_id": entry["source_rule_id"],
            "span_matches": (
                entry["start_line"] == reconstructed["start_line"]
                and entry["end_line"] == reconstructed["end_line"]
            ),
            "normalized_sha256_matches": (
                entry["normalized_sha256"]
                == reconstructed["normalized_sha256"]
            ),
            "text_matches": entry["text"] == reconstructed["text"],
            "classification_is_domain_lemma": (
                entry["classification"] == "DOMAIN_LEMMA"
            ),
        }
    )

checks = {
    "domain_source_ids_unique": len(domain_ids) == len(set(domain_ids)),
    "mapped_source_ids_unique": (
        len(mapped_source_ids) == len(set(mapped_source_ids))
    ),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "domain_to_source_rule_ordered_bijection": domain_ids == mapped_source_ids,
    "source_rule_to_obligation_ordered_bijection": (
        mapped_source_ids == obligation_ids
    ),
    "input_manifest_source_rules_exact": (
        input_manifest["source_rules"] == obligation_map["source_rules"]
    ),
    "generator_obligation_count_exact": (
        generator_manifest["obligation_count"]
        == len(obligation_map["obligations"])
    ),
    "obligation_map_hash_exact": (
        generator_manifest["obligation_map_sha256"]
        == hashlib.sha256(obligation_path.read_bytes()).hexdigest()
    ),
    "actual_target_matches_generator_manifest": (
        actual_target == generator_manifest["target"]
    ),
    "actual_target_matches_audit_input": actual_target == audit_target,
    "target_definition_is_exact_conjunction": (
        actual_target["definition_sha256"] == expected_definition_sha256
    ),
    "target_statement_hash_exact": (
        actual_target["statement_sha256"]
        == klean_export.sha256_text(actual_target["statement"])
    ),
    "all_source_spans_hashes_text_exact": all(
        all(
            value
            for key, value in entry.items()
            if key != "source_rule_id"
        )
        for entry in span_and_hash_checks
    ),
}

print(
    json.dumps(
        {
            "domain_ids": domain_ids,
            "mapped_source_ids": mapped_source_ids,
            "obligation_ids": obligation_ids,
            "obligations": obligation_map["obligations"],
            "span_and_hash_checks": span_and_hash_checks,
            "actual_target": actual_target,
            "generator_target": generator_manifest["target"],
            "audit_input_target": audit_target,
            "expected_target_definition": expected_definition,
            "expected_target_definition_sha256": expected_definition_sha256,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
