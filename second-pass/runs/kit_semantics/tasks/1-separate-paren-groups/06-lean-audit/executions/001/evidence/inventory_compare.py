#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source_lines = verification.read_text().splitlines()

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]

rule_checks = []
for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    source_slice = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    rule_checks.append(
        {
            "index": index,
            "module": rule["module"],
            "span": [rule["start_line"], rule["end_line"]],
            "normalized_sha256": rule["normalized_sha256"],
            "normalized_hash_recomputed": digest,
            "source_rule_id": rule["source_rule_id"],
            "source_rule_id_recomputed": f"rule-{digest}",
            "source_span_text_exact": source_slice == rule["text"],
            "manifest_classification": manifest["rules"][index]["classification"],
            "manifest_id_at_same_index": manifest_ids[index],
        }
    )

result = {
    "verification_file_sha256": hashlib.sha256(
        verification.read_bytes()
    ).hexdigest(),
    "verification_module": inventory["verification_module"],
    "local_verification_module_closure": inventory["verification_modules"],
    "inventory_rule_count": len(inventory["rules"]),
    "manifest_rule_count": len(manifest["rules"]),
    "inventory_sha256": inventory["inventory_sha256"],
    "inventory_sha256_recomputed": canonical_json_sha256(inventory["rules"]),
    "manifest_inventory_sha256": manifest["inventory_sha256"],
    "same_ordered_identities": inventory_ids == manifest_ids,
    "inventory_ids_unique": len(set(inventory_ids)) == len(inventory_ids),
    "manifest_ids_unique": len(set(manifest_ids)) == len(manifest_ids),
    "omitted_ids": sorted(set(inventory_ids) - set(manifest_ids)),
    "extra_ids": sorted(set(manifest_ids) - set(inventory_ids)),
    "all_spans_hashes_and_ids_recompute": all(
        check["normalized_sha256"] == check["normalized_hash_recomputed"]
        and check["source_rule_id"] == check["source_rule_id_recomputed"]
        and check["source_span_text_exact"]
        and check["source_rule_id"] == check["manifest_id_at_same_index"]
        for check in rule_checks
    ),
    "rule_checks": rule_checks,
}

print(json.dumps(result, indent=2, sort_keys=True))
