#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
normalization_checks = []
for entry in inventory["rules"]:
    normalized = " ".join(entry["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    normalization_checks.append(
        {
            "source_rule_id": entry["source_rule_id"],
            "recomputed_normalized_sha256": digest,
            "hash_matches": digest == entry["normalized_sha256"],
            "id_matches": entry["source_rule_id"] == f"rule-{digest}",
        }
    )

counts = {
    "canonical": len(canonical_ids),
    "manifest": len(manifest_ids),
    "manifest_unique": len(set(manifest_ids)),
    "missing": sorted(set(canonical_ids) - set(manifest_ids)),
    "extra": sorted(set(manifest_ids) - set(canonical_ids)),
}
checks = {
    "verification_sha256_matches_launcher": (
        inventory["verification_sha256"]
        == "f862f6f645a2bf62a530087f0ced39b85a998b8be1be82566b5e86cc73e95d44"
    ),
    "inventory_hash_self_recomputed": (
        inventory["inventory_sha256"]
        == canonical_json_sha256(inventory["rules"])
    ),
    "manifest_inventory_hash_matches": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "identity_order_exact": manifest_ids == canonical_ids,
    "bijection": (
        len(canonical_ids) == len(manifest_ids) == len(set(manifest_ids))
        and set(canonical_ids) == set(manifest_ids)
    ),
    "all_rule_hashes_and_ids_recomputed": all(
        item["hash_matches"] and item["id_matches"]
        for item in normalization_checks
    ),
    "trusted_contract_completed": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
}

print(
    json.dumps(
        {
            "inventory": inventory,
            "manifest": manifest,
            "counts": counts,
            "normalization_checks": normalization_checks,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
