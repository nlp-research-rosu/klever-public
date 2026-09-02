#!/usr/bin/env python3
"""Independent Stage 3 inventory checks using the trusted inventory implementation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


inventory = inventory_verification(WORKSPACE)
manifest = json.loads(MANIFEST.read_text())
validated = validate_trust_boundary(WORKSPACE, MANIFEST)
verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()

canonical_rules = inventory["rules"]
manifest_rules = manifest["rules"]
canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

checks = {
    "canonical_rule_count": len(canonical_rules),
    "manifest_rule_count": len(manifest_rules),
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "ordered_identity_bijection": canonical_ids == manifest_ids,
    "manifest_inventory_hash_matches": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "canonical_inventory_hash_recomputed": (
        canonical_json_sha256(canonical_rules) == inventory["inventory_sha256"]
    ),
    "contract_validation_succeeded": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
}

details = []
for index, (rule, classified) in enumerate(zip(canonical_rules, manifest_rules)):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_lines = verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    details.append(
        {
            "index": index,
            "module": rule["module"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "normalized_sha256_recomputed": normalized_sha256,
            "source_rule_id": rule["source_rule_id"],
            "source_rule_id_recomputed": f"rule-{normalized_sha256}",
            "span_first_line": source_lines[0].strip(),
            "span_last_line": source_lines[-1].strip(),
            "classification": classified["classification"],
            "rationale": classified["rationale"],
            "normalized_text": normalized,
        }
    )

print(
    json.dumps(
        {
            "inventory_header": {
                key: value for key, value in inventory.items() if key != "rules"
            },
            "checks": checks,
            "rules": details,
        },
        indent=2,
        sort_keys=True,
    )
)

if not all(checks.values()):
    raise SystemExit(1)
