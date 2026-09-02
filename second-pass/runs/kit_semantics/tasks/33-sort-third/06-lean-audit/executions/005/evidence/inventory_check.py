#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification

workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source_lines = (workspace / "verification.k").read_text().splitlines()

entries = manifest.get("rules", [])
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry.get("source_rule_id") for entry in entries]

span_checks = []
for rule in inventory["rules"]:
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    span_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "span_text_equals_inventory_text": span_text == rule["text"],
            "normalized_sha256_recomputed": digest,
            "normalized_sha256_matches": digest == rule["normalized_sha256"],
            "source_rule_id_matches": rule["source_rule_id"] == f"rule-{digest}",
        }
    )

result = {
    "inventory": inventory,
    "stage3_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    "stage3_manifest_inventory_sha256": manifest.get("inventory_sha256"),
    "inventory_sha256_recomputed": canonical_json_sha256(inventory["rules"]),
    "inventory_hash_matches_manifest": (
        inventory["inventory_sha256"] == manifest.get("inventory_sha256")
    ),
    "canonical_rule_ids": canonical_ids,
    "manifest_rule_ids": manifest_ids,
    "ordered_identity_match": canonical_ids == manifest_ids,
    "manifest_has_duplicate_ids": len(manifest_ids) != len(set(manifest_ids)),
    "omitted_ids": [rule_id for rule_id in canonical_ids if rule_id not in manifest_ids],
    "extra_ids": [rule_id for rule_id in manifest_ids if rule_id not in canonical_ids],
    "span_and_identity_checks": span_checks,
    "stage3_entries": entries,
}
print(json.dumps(result, indent=2, sort_keys=True))
