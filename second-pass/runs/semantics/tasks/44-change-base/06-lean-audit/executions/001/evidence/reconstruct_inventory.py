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

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_by_id = {
    entry["source_rule_id"]: entry for entry in inventory["rules"]
}

per_rule = []
for index, entry in enumerate(inventory["rules"]):
    normalized_again = " ".join(entry["text"].split())
    normalized_again_hash = hashlib.sha256(normalized_again.encode()).hexdigest()
    per_rule.append(
        {
            "index": index,
            "module": entry["module"],
            "start_line": entry["start_line"],
            "end_line": entry["end_line"],
            "attributes": entry["attributes"],
            "normalized_sha256": entry["normalized_sha256"],
            "independent_normalized_sha256": normalized_again_hash,
            "source_rule_id": entry["source_rule_id"],
            "recomputed_source_rule_id": "rule-" + normalized_again_hash,
            "classification": manifest["rules"][index]["classification"],
            "rationale": manifest["rules"][index]["rationale"],
            "text": entry["text"],
        }
    )

checks = {
    "verification_sha256": (
        inventory["verification_sha256"]
        == hashlib.sha256((workspace / "verification.k").read_bytes()).hexdigest()
    ),
    "inventory_hash_recomputed": (
        inventory["inventory_sha256"]
        == canonical_json_sha256(inventory["rules"])
    ),
    "manifest_inventory_hash": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "ordered_identity_list": manifest_ids == inventory_ids,
    "no_inventory_duplicates": len(inventory_ids) == len(set(inventory_ids)),
    "no_manifest_duplicates": len(manifest_ids) == len(set(manifest_ids)),
    "same_identity_set": set(manifest_ids) == set(inventory_ids),
    "all_rule_hashes_recomputed": all(
        entry["normalized_sha256"] == entry["independent_normalized_sha256"]
        and entry["source_rule_id"] == entry["recomputed_source_rule_id"]
        for entry in per_rule
    ),
    "trusted_contract_validated": len(validated["rules"]) == len(inventory["rules"]),
}

print(
    json.dumps(
        {
            "schema_version": inventory["schema_version"],
            "verification_file": inventory["verification_file"],
            "verification_sha256": inventory["verification_sha256"],
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "rule_count": len(inventory["rules"]),
            "inventory_sha256": inventory["inventory_sha256"],
            "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "manifest_inventory_sha256": manifest["inventory_sha256"],
            "checks": checks,
            "all_checks_pass": all(checks.values()),
            "rules": per_rule,
        },
        indent=2,
        sort_keys=True,
    )
)
