#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification

workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
output_path = Path("/audit-output/evidence/reconstructed-inventory.json")

inventory = inventory_verification(workspace)
output_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")
manifest = json.loads(manifest_path.read_text())

reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
reconstructed_counts = Counter(reconstructed_ids)
manifest_counts = Counter(manifest_ids)

print("trusted_call=tools.k_rule_inventory.inventory_verification(/reference/k-proof)")
print(f"verification_file={inventory['verification_file']}")
print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={inventory['verification_modules']}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"rule_count={len(inventory['rules'])}")
print(f"recomputed_inventory_sha256={inventory['inventory_sha256']}")
print(f"direct_canonical_inventory_sha256={canonical_json_sha256(inventory['rules'])}")
print(f"manifest_inventory_sha256={manifest['inventory_sha256']}")
print(f"reconstructed_duplicate_ids={sorted(k for k, v in reconstructed_counts.items() if v != 1)}")
print(f"manifest_duplicate_ids={sorted(k for k, v in manifest_counts.items() if v != 1)}")
print(f"omitted_from_manifest={sorted(set(reconstructed_ids) - set(manifest_ids))}")
print(f"extra_in_manifest={sorted(set(manifest_ids) - set(reconstructed_ids))}")
print(f"ordered_ids_equal={reconstructed_ids == manifest_ids}")
print("rules:")
manifest_by_id = {entry["source_rule_id"]: entry for entry in manifest["rules"]}
for index, rule in enumerate(inventory["rules"], 1):
    manifest_entry = manifest_by_id.get(rule["source_rule_id"], {})
    hash_from_id = rule["source_rule_id"].removeprefix("rule-")
    print(
        json.dumps(
            {
                "index": index,
                "module": rule["module"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "attributes": rule["attributes"],
                "normalized_sha256": rule["normalized_sha256"],
                "source_rule_id": rule["source_rule_id"],
                "id_matches_normalized_hash": hash_from_id == rule["normalized_sha256"],
                "manifest_classification": manifest_entry.get("classification"),
                "text": rule["text"],
            },
            sort_keys=True,
        )
    )
