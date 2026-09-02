#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
inventory = inventory_verification(workspace)
discovery = json.loads(
    Path("/reference/lemma-discovery.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)

lines = verification.read_text().splitlines()
span_checks = []
for rule in inventory["rules"]:
    exact_span = "\n".join(
        lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "exact_span_equals_inventory_text": exact_span == rule["text"],
            "recomputed_normalized_sha256": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
manifest_classified = (
    input_manifest["definitions"]
    + input_manifest["operational_rules"]
    + input_manifest["proved_derived_lemmas"]
    + input_manifest["source_rules"]
)
manifest_ids = [rule["source_rule_id"] for rule in manifest_classified]

checks = {
    "inventory_hash_recomputed": (
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
    ),
    "inventory_hash_equals_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "inventory_hash_equals_input_manifest": (
        inventory["inventory_sha256"] == input_manifest["inventory_sha256"]
    ),
    "discovery_order_is_exact": discovery_ids == inventory_ids,
    "discovery_has_no_duplicates": (
        len(discovery_ids) == len(set(discovery_ids))
    ),
    "discovery_bijection": (
        len(discovery_ids) == len(inventory_ids)
        and set(discovery_ids) == set(inventory_ids)
    ),
    "input_manifest_has_no_duplicates": (
        len(manifest_ids) == len(set(manifest_ids))
    ),
    "input_manifest_bijection": (
        len(manifest_ids) == len(inventory_ids)
        and set(manifest_ids) == set(inventory_ids)
    ),
    "all_source_spans_and_rule_hashes_match": all(
        entry["exact_span_equals_inventory_text"]
        and entry["normalized_sha256_matches"]
        and entry["source_rule_id_matches"]
        for entry in span_checks
    ),
}

print(
    json.dumps(
        {
            "verification_module": inventory["verification_module"],
            "local_verification_module_closure": inventory[
                "verification_modules"
            ],
            "inventory_ids": inventory_ids,
            "discovery_ids": discovery_ids,
            "input_manifest_ids": manifest_ids,
            "inventory_sha256": inventory["inventory_sha256"],
            "span_checks": span_checks,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
