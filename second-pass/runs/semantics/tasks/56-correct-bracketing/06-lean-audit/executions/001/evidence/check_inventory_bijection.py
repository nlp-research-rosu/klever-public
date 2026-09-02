#!/usr/bin/env python3
"""Explicit ordered/bijective comparison of reconstructed Stage 1 rules."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
INPUT_MANIFEST_PATH = Path("/reference/klean-generation/input-manifest.json")


def ids(records: list[dict]) -> list[str]:
    return [record["source_rule_id"] for record in records]


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY_PATH.read_bytes())
validated = validate_trust_boundary(WORKSPACE, DISCOVERY_PATH)
input_manifest = json.loads(INPUT_MANIFEST_PATH.read_bytes())

canonical_ids = ids(inventory["rules"])
discovery_ids = ids(discovery["rules"])
manifest_partition = (
    input_manifest["definitions"]
    + input_manifest["operational_rules"]
    + input_manifest["proved_derived_lemmas"]
    + input_manifest["source_rules"]
)
manifest_ids_in_source_order = [
    source_rule_id
    for source_rule_id in canonical_ids
    if source_rule_id in set(ids(manifest_partition))
]

classification_by_id = {
    record["source_rule_id"]: record["classification"]
    for record in discovery["rules"]
}
expected_partitions = {
    "definitions": [
        rule
        for rule in validated["rules"]
        if classification_by_id[rule["source_rule_id"]] == "DEFINITION"
    ],
    "operational_rules": [
        rule
        for rule in validated["rules"]
        if classification_by_id[rule["source_rule_id"]] == "OPERATIONAL_RULE"
    ],
    "proved_derived_lemmas": [
        rule
        for rule in validated["rules"]
        if classification_by_id[rule["source_rule_id"]]
        == "PROVED_DERIVED_LEMMA"
    ],
    "source_rules": [
        rule
        for rule in validated["rules"]
        if classification_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
    ],
}

# Input-manifest records add classification/rationale and, for source_rules,
# immutable discovery provenance. Compare the common canonical fields exactly.
canonical_fields = {
    "source_rule_id",
    "module",
    "start_line",
    "end_line",
    "normalized_sha256",
    "attributes",
    "text",
}
partition_common_fields_match = {}
for name, expected in expected_partitions.items():
    observed = input_manifest[name]
    expected_common = [
        {key: value for key, value in record.items() if key in canonical_fields}
        for record in expected
    ]
    observed_common = [
        {key: value for key, value in record.items() if key in canonical_fields}
        for record in observed
    ]
    partition_common_fields_match[name] = observed_common == expected_common

checks = {
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "discovery_order_exact": discovery_ids == canonical_ids,
    "discovery_count_exact": len(discovery_ids) == len(canonical_ids),
    "discovery_ids_unique": len(set(discovery_ids)) == len(discovery_ids),
    "all_source_ids_equal_rule_hash": all(
        rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
        for rule in inventory["rules"]
    ),
    "manifest_partition_count_exact": len(manifest_partition) == len(canonical_ids),
    "manifest_partition_ids_unique": (
        len(set(ids(manifest_partition))) == len(manifest_partition)
    ),
    "manifest_partition_bijection": set(ids(manifest_partition)) == set(canonical_ids),
    "manifest_partition_source_order_recoverable": (
        manifest_ids_in_source_order == canonical_ids
    ),
    "manifest_partition_common_fields_match": all(
        partition_common_fields_match.values()
    ),
    "all_simplification_classifications_allowed": all(
        "simplification" not in rule["attributes"]
        or classification_by_id[rule["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in inventory["rules"]
    ),
}

output = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "inventory_sha256": inventory["inventory_sha256"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "canonical_order": canonical_ids,
    "classification_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
    "partition_common_fields_match": partition_common_fields_match,
}
print(json.dumps(output, indent=2, sort_keys=True))
