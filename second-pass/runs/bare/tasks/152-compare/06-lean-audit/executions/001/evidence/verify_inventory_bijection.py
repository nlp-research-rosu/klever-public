#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
source_lines = verification.read_text().splitlines()
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_bytes())

facts: list[dict[str, object]] = []


def record(name: str, value: object) -> None:
    facts.append({"name": name, "value": value})


rules = inventory["rules"]
manifest_rules = discovery["rules"]
inventory_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

assert len(rules) == 4
assert len(manifest_rules) == len(rules)
assert len(set(inventory_ids)) == len(inventory_ids)
assert len(set(manifest_ids)) == len(manifest_ids)
assert manifest_ids == inventory_ids
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
assert canonical_json_sha256(rules) == inventory["inventory_sha256"]

record("verification module", inventory["verification_module"])
record("local verification-module closure", inventory["verification_modules"])
record("rule count", len(rules))
record("manifest identities exactly preserve canonical order", True)
record("manifest identities are unique", True)
record("no missing or extra identities", True)
record("recomputed whole inventory SHA-256", inventory["inventory_sha256"])

reconstructed: list[dict[str, object]] = []
for rule in rules:
    text = rule["text"]
    normalized = " ".join(text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    source_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    assert source_span == text
    assert normalized_sha256 == rule["normalized_sha256"]
    assert source_rule_id == rule["source_rule_id"]
    reconstructed.append(
        {
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "normalized_sha256": normalized_sha256,
            "source_rule_id": source_rule_id,
            "source_span_exact": True,
        }
    )

record("per-rule independent span/hash/identity reconstruction", reconstructed)
print(
    json.dumps(
        {"all_passed": True, "facts": facts},
        indent=2,
        sort_keys=True,
    )
)
