#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and ordered comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

rule_checks = []
for index, rule in enumerate(inventory["rules"]):
    text_from_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    recomputed_hash = hashlib.sha256(normalized.encode()).hexdigest()
    rule_checks.append(
        {
            "index": index,
            "source_span": [rule["start_line"], rule["end_line"]],
            "source_span_exact": text_from_span == rule["text"],
            "normalized_sha256": rule["normalized_sha256"],
            "recomputed_normalized_sha256": recomputed_hash,
            "normalized_hash_matches": recomputed_hash
            == rule["normalized_sha256"],
            "source_rule_id": rule["source_rule_id"],
            "recomputed_source_rule_id": f"rule-{recomputed_hash}",
            "source_rule_id_matches": rule["source_rule_id"]
            == f"rule-{recomputed_hash}",
            "module": rule["module"],
            "attributes": rule["attributes"],
            "text": rule["text"],
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
canonical_hash = canonical_json_sha256(inventory["rules"])
checks = {
    "trusted_contract_validation": True,
    "verification_sha256_matches_source": inventory["verification_sha256"]
    == hashlib.sha256((WORKSPACE / "verification.k").read_bytes()).hexdigest(),
    "inventory_hash_recomputed": canonical_hash,
    "inventory_hash_matches_inventory": canonical_hash
    == inventory["inventory_sha256"],
    "inventory_hash_matches_manifest": canonical_hash
    == discovery["inventory_sha256"],
    "canonical_rule_count": len(canonical_ids),
    "manifest_rule_count": len(manifest_ids),
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "ordered_identities_exact": canonical_ids == manifest_ids,
    "no_omissions": set(canonical_ids) <= set(manifest_ids),
    "no_extras": set(manifest_ids) <= set(canonical_ids),
    "all_source_spans_exact": all(
        check["source_span_exact"] for check in rule_checks
    ),
    "all_normalized_hashes_exact": all(
        check["normalized_hash_matches"] for check in rule_checks
    ),
    "all_source_rule_ids_exact": all(
        check["source_rule_id_matches"] for check in rule_checks
    ),
    "validated_definition_count": len(validated["definitions"]),
    "validated_operational_rule_count": len(validated["operational_rules"]),
    "validated_proved_derived_lemma_count": len(
        validated["proved_derived_lemmas"]
    ),
    "validated_domain_lemma_count": len(validated["domain_lemmas"]),
}

print(
    json.dumps(
        {
            "inventory": inventory,
            "rule_recomputations": rule_checks,
            "comparison_checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
