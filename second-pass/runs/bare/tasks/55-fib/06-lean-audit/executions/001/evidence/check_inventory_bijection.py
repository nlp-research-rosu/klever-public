#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


inventory = json.loads(
    Path("/audit-output/evidence/inventory-reconstructed.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()

rule_checks = []
for rule in inventory["rules"]:
    exact_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span_matches": exact_span == rule["text"],
            "normalized_sha256_matches": digest == rule["normalized_sha256"],
            "source_rule_id_matches": rule["source_rule_id"] == f"rule-{digest}",
        }
    )

canonical_rules_json = json.dumps(
    inventory["rules"],
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode()
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
checks = {
    "inventory_hash_recomputed": hashlib.sha256(canonical_rules_json).hexdigest()
    == inventory["inventory_sha256"],
    "manifest_inventory_hash_matches": discovery["inventory_sha256"]
    == inventory["inventory_sha256"],
    "identity_order_exact": classified_ids == canonical_ids,
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "classified_ids_unique": len(classified_ids) == len(set(classified_ids)),
    "identity_sets_exact": set(classified_ids) == set(canonical_ids),
    "entry_count_exact": len(classified_ids) == len(canonical_ids),
    "all_source_spans_and_hashes_exact": all(
        all(value for key, value in entry.items() if key != "source_rule_id")
        for entry in rule_checks
    ),
}
print(
    json.dumps(
        {
            "canonical_ids": canonical_ids,
            "classified_ids": classified_ids,
            "inventory_sha256": inventory["inventory_sha256"],
            "rule_checks": rule_checks,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
