#!/usr/bin/env python3
"""Reconstruct and bijectively compare the Stage 3 K rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
manifest = json.loads(MANIFEST.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, MANIFEST)

print(json.dumps(inventory, indent=2, sort_keys=True))
print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={inventory['verification_modules']}")
print(f"rule_count={len(inventory['rules'])}")
print(f"inventory_sha256={inventory['inventory_sha256']}")
print(f"manifest_inventory_sha256={manifest['inventory_sha256']}")
assert inventory["inventory_sha256"] == manifest["inventory_sha256"]

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
print(f"canonical_ids={canonical_ids}")
print(f"manifest_ids={manifest_ids}")
print(f"identity_order_exact={canonical_ids == manifest_ids}")
assert canonical_ids == manifest_ids
assert len(canonical_ids) == len(set(canonical_ids))
assert len(manifest_ids) == len(set(manifest_ids))

for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    expected_id = f"rule-{normalized_sha256}"
    print(
        f"rule[{index}] module={rule['module']} "
        f"span={rule['start_line']}-{rule['end_line']} "
        f"normalized_sha256={normalized_sha256} "
        f"source_rule_id={expected_id} attributes={rule['attributes']}"
    )
    assert normalized_sha256 == rule["normalized_sha256"]
    assert expected_id == rule["source_rule_id"]

independent_classes = {
    "rule-ff38bf4352a9d5177710fc8cdb52e149480f3430cbb3889ae520f039fdd1caaf": (
        "DEFINITION",
        "named proof term expanding to the complete translated program AST",
    ),
    "rule-52c678867274bfbe50cfd8894cb300d08fb5f3a018c416a200e725d66ad1ffb7": (
        "DEFINITION",
        "base equation of the bracketSpec execution summary",
    ),
    "rule-0b80080b9a7dd4f80716f34190b5a512ffa576526b020733d3a661e68720cea9": (
        "DEFINITION",
        "opening-character recurrence of bracketSpec",
    ),
    "rule-dab3458a72db386dbad39915bdb52a22d7ee1cccd37c33aa1b8b984a02af13f4": (
        "DEFINITION",
        "zero-depth rejection equation of bracketSpec",
    ),
    "rule-2877c405b261ca01cd0ba4ed8be5aa27101f1fbd6c09d33fb7d78416ef4c6968": (
        "DEFINITION",
        "positive-depth closing-character recurrence of bracketSpec",
    ),
}

for entry in manifest["rules"]:
    expected_class, judgment = independent_classes[entry["source_rule_id"]]
    print(
        f"classification[{entry['source_rule_id']}]: "
        f"recorded={entry['classification']} independent={expected_class} "
        f"judgment={judgment}"
    )
    assert entry["classification"] == expected_class

assert len(validated["definitions"]) == 5
assert validated["operational_rules"] == []
assert validated["proved_derived_lemmas"] == []
assert validated["domain_lemmas"] == []
print("definitions=5")
print("operational_rules=0")
print("proved_derived_lemmas=0")
print("domain_lemmas=0")
print("simplification_class_policy=PASS")
print("inventory_bijection=PASS")
print("independent_classification=PASS")
print("OVERALL=PASS")
