#!/usr/bin/env python3
"""Reconstruct and compare the Stage 3 rule inventory bijectively."""

import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
rules = inventory["rules"]
classified = discovery["rules"]

source_ids = [rule["source_rule_id"] for rule in rules]
classified_ids = [rule["source_rule_id"] for rule in classified]
source_duplicate_ids = sorted(
    {source_id for source_id in source_ids if source_ids.count(source_id) > 1}
)
classified_duplicate_ids = sorted(
    {source_id for source_id in classified_ids if classified_ids.count(source_id) > 1}
)
missing = sorted(set(source_ids) - set(classified_ids))
extra = sorted(set(classified_ids) - set(source_ids))
order_match = source_ids == classified_ids
inventory_hash_recomputed = canonical_json_sha256(rules)
hash_match = (
    inventory_hash_recomputed
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
)

source_lines = (workspace / "verification.k").read_text().splitlines()
span_errors = []
identity_errors = []
for index, rule in enumerate(rules, start=1):
    observed_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    if observed_span != rule["text"]:
        span_errors.append(index)
    expected_id = "rule-" + rule["normalized_sha256"]
    if rule["source_rule_id"] != expected_id:
        identity_errors.append(index)

allowed = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}
classification_errors = [
    index
    for index, rule in enumerate(classified, start=1)
    if rule.get("classification") not in allowed
    or not isinstance(rule.get("rationale"), str)
    or not rule["rationale"].strip()
]

ok = not any(
    (
        source_duplicate_ids,
        classified_duplicate_ids,
        missing,
        extra,
        not order_match,
        not hash_match,
        span_errors,
        identity_errors,
        classification_errors,
    )
)

print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={inventory['verification_modules']}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"source_rule_count={len(rules)}")
print(f"classified_rule_count={len(classified)}")
print(f"inventory_sha256_recomputed={inventory_hash_recomputed}")
print(f"inventory_sha256_inventory={inventory['inventory_sha256']}")
print(f"inventory_sha256_discovery={discovery['inventory_sha256']}")
print(f"source_duplicate_ids={source_duplicate_ids}")
print(f"classified_duplicate_ids={classified_duplicate_ids}")
print(f"missing={missing}")
print(f"extra={extra}")
print(f"order_match={order_match}")
print(f"span_errors={span_errors}")
print(f"identity_errors={identity_errors}")
print(f"classification_errors={classification_errors}")
print("RULES")
for index, (rule, label) in enumerate(zip(rules, classified), start=1):
    print(
        f"{index:02d} lines={rule['start_line']}-{rule['end_line']} "
        f"hash={rule['normalized_sha256']} id={rule['source_rule_id']} "
        f"attributes={rule['attributes']} class={label['classification']}"
    )
print(f"OVERALL={'PASS' if ok else 'FAIL'}")
raise SystemExit(0 if ok else 1)
