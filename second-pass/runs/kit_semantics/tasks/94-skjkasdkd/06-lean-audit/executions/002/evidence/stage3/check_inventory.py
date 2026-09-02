#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256
from tools.lemma_discovery_contract import validate_trust_boundary


inventory_path = Path("/audit-output/evidence/stage3/reconstructed-inventory.json")
source_path = Path("/reference/k-proof/verification.k")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = json.loads(inventory_path.read_text())
manifest = json.loads(manifest_path.read_text())
source_lines = source_path.read_text().splitlines()
rules = inventory["rules"]
manifest_rules = manifest["rules"]

checks = {}
checks["inventory_rule_ids_unique"] = len({r["source_rule_id"] for r in rules}) == len(rules)
checks["manifest_rule_ids_unique"] = len({r["source_rule_id"] for r in manifest_rules}) == len(manifest_rules)
checks["rule_count_equal"] = len(rules) == len(manifest_rules)
checks["ordered_ids_equal"] = [r["source_rule_id"] for r in rules] == [r["source_rule_id"] for r in manifest_rules]
checks["id_sets_equal"] = {r["source_rule_id"] for r in rules} == {r["source_rule_id"] for r in manifest_rules}
checks["inventory_hash_recomputed"] = canonical_json_sha256(rules) == inventory["inventory_sha256"]
checks["manifest_inventory_hash_equal"] = manifest["inventory_sha256"] == inventory["inventory_sha256"]
checks["verification_hash_recomputed"] = hashlib.sha256(source_path.read_bytes()).hexdigest() == inventory["verification_sha256"]

per_rule = []
for index, rule in enumerate(rules):
    source_span_text = "\n".join(source_lines[rule["start_line"] - 1:rule["end_line"]])
    normalized_hash = hashlib.sha256(" ".join(rule["text"].split()).encode()).hexdigest()
    row = {
        "index": index,
        "source_rule_id": rule["source_rule_id"],
        "source_span": [rule["start_line"], rule["end_line"]],
        "span_text_exact": source_span_text == rule["text"],
        "normalized_hash_exact": normalized_hash == rule["normalized_sha256"],
        "id_from_hash_exact": rule["source_rule_id"] == "rule-" + normalized_hash,
        "manifest_classification": manifest_rules[index]["classification"],
        "manifest_id_exact": manifest_rules[index]["source_rule_id"] == rule["source_rule_id"],
    }
    per_rule.append(row)

checks["all_span_text_exact"] = all(row["span_text_exact"] for row in per_rule)
checks["all_normalized_hashes_exact"] = all(row["normalized_hash_exact"] for row in per_rule)
checks["all_ids_from_hash_exact"] = all(row["id_from_hash_exact"] for row in per_rule)
checks["all_manifest_ids_exact"] = all(row["manifest_id_exact"] for row in per_rule)

validated = validate_trust_boundary(Path("/reference/k-proof"), manifest_path)
checks["trusted_contract_inventory_equal"] = validated["inventory_sha256"] == inventory["inventory_sha256"]
checks["trusted_contract_partition_count"] = sum(len(validated[key]) for key in (
    "definitions", "operational_rules", "proved_derived_lemmas", "domain_lemmas"
)) == len(rules)

result = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "inventory_sha256": inventory["inventory_sha256"],
    "verification_sha256": inventory["verification_sha256"],
    "rule_count": len(rules),
    "classification_counts": {
        key: sum(entry["classification"] == key for entry in manifest_rules)
        for key in ("DEFINITION", "OPERATIONAL_RULE", "PROVED_DERIVED_LEMMA", "DOMAIN_LEMMA")
    },
    "rules": per_rule,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_checks_pass"] else 1)
