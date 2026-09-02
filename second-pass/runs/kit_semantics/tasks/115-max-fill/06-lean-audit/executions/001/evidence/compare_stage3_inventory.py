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

print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={inventory['verification_modules']}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"rule_count={len(inventory_ids)}")
print(f"unique_inventory_ids={len(set(inventory_ids))}")
print(f"unique_manifest_ids={len(set(manifest_ids))}")
print(f"ordered_ids_equal={inventory_ids == manifest_ids}")
print(f"omitted={sorted(set(inventory_ids) - set(manifest_ids))}")
print(f"extra={sorted(set(manifest_ids) - set(inventory_ids))}")
print(
    "inventory_sha256_recomputed="
    + canonical_json_sha256(inventory["rules"])
)
print("inventory_sha256_tool=" + inventory["inventory_sha256"])
print("inventory_sha256_manifest=" + manifest["inventory_sha256"])
print(
    "inventory_hashes_equal="
    + str(
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
        == manifest["inventory_sha256"]
    )
)
print(
    "discovery_manifest_sha256="
    + hashlib.sha256(manifest_path.read_bytes()).hexdigest()
)
print(
    "validated_partition_counts="
    + json.dumps(
        {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        sort_keys=True,
    )
)
print("\nORDERED RULE IDENTITIES")
for index, source_rule_id in enumerate(inventory_ids, 1):
    rule = inventory_by_id[source_rule_id]
    normalized = " ".join(rule["text"].split())
    independently_hashed = hashlib.sha256(normalized.encode()).hexdigest()
    print(
        f"{index:02d} {source_rule_id} "
        f"{rule['module']}:{rule['start_line']}-{rule['end_line']} "
        f"recorded_hash={rule['normalized_sha256']} "
        f"rehashed={independently_hashed} "
        f"match={rule['normalized_sha256'] == independently_hashed}"
    )
