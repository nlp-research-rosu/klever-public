#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source_lines = verification.read_text().splitlines()

span_checks = []
for rule in inventory["rules"]:
    extracted = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(extracted.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "span_text_exact": extracted == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_exact": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_exact": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
            "attributes": rule["attributes"],
            "text": rule["text"],
        }
    )

inventory_hash_recomputed = canonical_json_sha256(inventory["rules"])
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
validated = validate_trust_boundary(workspace, manifest_path)

checks = {
    "verification_sha256_exact": (
        inventory["verification_sha256"]
        == hashlib.sha256(verification.read_bytes()).hexdigest()
    ),
    "inventory_sha256_recomputed": inventory_hash_recomputed,
    "inventory_sha256_internal_exact": (
        inventory_hash_recomputed == inventory["inventory_sha256"]
    ),
    "manifest_inventory_sha256_exact": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "ordered_identity_exact": manifest_ids == inventory_ids,
    "manifest_identity_unique": len(manifest_ids) == len(set(manifest_ids)),
    "manifest_count": len(manifest_ids),
    "inventory_count": len(inventory_ids),
    "contract_validated_inventory_sha256": validated["inventory_sha256"],
    "all_span_checks_pass": all(
        entry["span_text_exact"]
        and entry["normalized_sha256_exact"]
        and entry["source_rule_id_exact"]
        for entry in span_checks
    ),
}

print(
    json.dumps(
        {
            "inventory": inventory,
            "manifest": manifest,
            "span_checks": span_checks,
            "checks": checks,
            "contract_partition_counts": {
                "definitions": len(validated["definitions"]),
                "operational_rules": len(validated["operational_rules"]),
                "proved_derived_lemmas": len(
                    validated["proved_derived_lemmas"]
                ),
                "domain_lemmas": len(validated["domain_lemmas"]),
            },
        },
        indent=2,
        sort_keys=True,
    )
)

assert all(
    value is True
    for key, value in checks.items()
    if key.endswith("_exact")
)
assert checks["ordered_identity_exact"]
assert checks["manifest_identity_unique"]
assert checks["manifest_count"] == checks["inventory_count"]
assert checks["all_span_checks_pass"]
