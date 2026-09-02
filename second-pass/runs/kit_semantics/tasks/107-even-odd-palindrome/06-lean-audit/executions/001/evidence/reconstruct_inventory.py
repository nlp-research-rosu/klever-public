#!/usr/bin/env python3
"""Reconstruct and independently re-hash the local verification rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
source_lines = verification.read_text().splitlines()
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())

print(f"verification_module={inventory['verification_module']}")
print(f"local_module_closure={inventory['verification_modules']!r}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"rule_count={len(inventory['rules'])}")

all_spans = True
all_ids = True
for index, rule in enumerate(inventory["rules"]):
    exact_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = "rule-" + normalized_sha256
    span_ok = exact_span == rule["text"] and normalized_sha256 == rule["normalized_sha256"]
    id_ok = source_rule_id == rule["source_rule_id"]
    all_spans &= span_ok
    all_ids &= id_ok
    print(f"rule[{index}].module={rule['module']}")
    print(f"rule[{index}].span={rule['start_line']}-{rule['end_line']}")
    print(f"rule[{index}].attributes={rule['attributes']!r}")
    print(f"rule[{index}].normalized_sha256={normalized_sha256}")
    print(f"rule[{index}].source_rule_id={source_rule_id}")
    print(f"rule[{index}].exact_span_match={exact_span == rule['text']}")

canonical = json.dumps(
    inventory["rules"],
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode()
whole_hash = hashlib.sha256(canonical).hexdigest()
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule.get("source_rule_id") for rule in discovery.get("rules", [])]
classifications = [rule.get("classification") for rule in discovery.get("rules", [])]
allowed = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}

print(f"whole_inventory_sha256={whole_hash}")
print(f"trusted_inventory_sha256={inventory['inventory_sha256']}")
print(f"discovery_inventory_sha256={discovery.get('inventory_sha256')}")
print(f"inventory_ids={inventory_ids!r}")
print(f"discovery_ids={discovery_ids!r}")
print(f"classifications={classifications!r}")
print(f"SPAN_HASH_RECOMPUTATION={'PASS' if all_spans else 'FAIL'}")
print(f"SOURCE_RULE_ID_RECOMPUTATION={'PASS' if all_ids else 'FAIL'}")
print(
    "WHOLE_INVENTORY_HASH_RECOMPUTATION="
    + (
        "PASS"
        if whole_hash
        == inventory["inventory_sha256"]
        == discovery.get("inventory_sha256")
        else "FAIL"
    )
)
ordered_bijection = (
    inventory_ids == discovery_ids
    and len(discovery_ids) == len(set(discovery_ids))
    and len(classifications) == len(inventory_ids)
    and all(classification in allowed for classification in classifications)
)
print(f"ORDERED_CLASSIFICATION_BIJECTION={'PASS' if ordered_bijection else 'FAIL'}")
raise SystemExit(
    0
    if all_spans
    and all_ids
    and whole_hash == inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    and ordered_bijection
    else 1
)
