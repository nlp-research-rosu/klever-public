#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"
verification_text = verification_path.read_text()
verification_lines = verification_text.splitlines()
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())

recomputed_rules = []
for rule in inventory["rules"]:
    source_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(source_span.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    recomputed_rules.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "inventory_text": rule["text"],
            "source_span": source_span,
            "recomputed_normalized_sha256": digest,
            "recorded_normalized_sha256": rule["normalized_sha256"],
            "recomputed_source_rule_id": f"rule-{digest}",
            "span_text_exact_match": source_span == rule["text"],
            "normalized_hash_match": digest == rule["normalized_sha256"],
            "source_rule_id_match": f"rule-{digest}" == rule["source_rule_id"],
        }
    )

manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
unique_manifest_ids = len(manifest_ids) == len(set(manifest_ids))
canonical_inventory_hash = canonical_json_sha256(inventory["rules"])
validated = validate_trust_boundary(workspace, manifest_path)

report = {
    "inventory": inventory,
    "recomputed_rules": recomputed_rules,
    "manifest_rule_ids": manifest_ids,
    "inventory_rule_ids": inventory_ids,
    "manifest_ids_are_unique": unique_manifest_ids,
    "ordered_bijection": manifest_ids == inventory_ids and unique_manifest_ids,
    "canonical_inventory_hash_recomputed": canonical_inventory_hash,
    "inventory_hash_matches_recomputation": (
        canonical_inventory_hash == inventory["inventory_sha256"]
    ),
    "manifest_hash_matches_inventory": (
        manifest["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "validated_classification_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
}
print(json.dumps(report, indent=2, sort_keys=True))

required = [
    unique_manifest_ids,
    manifest_ids == inventory_ids,
    canonical_inventory_hash == inventory["inventory_sha256"],
    manifest["inventory_sha256"] == inventory["inventory_sha256"],
]
required.extend(
    check[key]
    for check in recomputed_rules
    for key in (
        "span_text_exact_match",
        "normalized_hash_match",
        "source_rule_id_match",
    )
)
if not all(required):
    raise SystemExit(1)
