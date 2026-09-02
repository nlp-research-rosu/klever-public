#!/usr/bin/env python3
"""Reconstruct and bijectively compare the frozen verification-rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


inventory = k_rule_inventory.inventory_verification(WORKSPACE)
manifest = json.loads(DISCOVERY.read_bytes())
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY
)

verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
rule_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [entry["source_rule_id"] for entry in manifest["rules"]]

require(
    inventory["verification_sha256"]
    == hashlib.sha256((WORKSPACE / "verification.k").read_bytes()).hexdigest(),
    "verification.k SHA-256 did not recompute",
)
require(
    inventory["inventory_sha256"]
    == k_rule_inventory.canonical_json_sha256(inventory["rules"]),
    "whole-inventory SHA-256 did not recompute",
)
require(len(rule_ids) == len(set(rule_ids)), "reconstructed IDs are duplicated")
require(
    len(classified_ids) == len(set(classified_ids)),
    "classified IDs are duplicated",
)
require(
    classified_ids == rule_ids,
    "classification IDs omit, add, or reorder reconstructed identities",
)
require(
    manifest["inventory_sha256"] == inventory["inventory_sha256"],
    "classification inventory hash differs from reconstruction",
)

print("TRUSTED INVENTORY RECONSTRUCTION")
print(json.dumps(inventory, indent=2, sort_keys=True))
print()
print("PER-RULE RECOMPUTATION")
for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    source_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    require(
        source_span == rule["text"],
        f"rule {index} text differs from its recorded source span",
    )
    require(
        normalized_sha256 == rule["normalized_sha256"],
        f"rule {index} normalized hash differs",
    )
    require(
        source_rule_id == rule["source_rule_id"],
        f"rule {index} source_rule_id differs",
    )
    discovery_entry = manifest["rules"][index]
    print(f"rule_index: {index}")
    print(f"  source_span: {rule['start_line']}-{rule['end_line']}")
    print(f"  normalized_text: {normalized}")
    print(f"  normalized_sha256: {normalized_sha256}")
    print(f"  source_rule_id: {source_rule_id}")
    print(f"  attributes: {rule['attributes']}")
    print(f"  classified_as: {discovery_entry['classification']}")

print()
print(
    "MATCH: exact ordered bijection, unique identities, source spans, "
    "normalized hashes, source_rule_ids, and whole inventory hash"
)
print(
    "validated category counts: "
    f"definitions={len(validated['definitions'])}, "
    f"operational_rules={len(validated['operational_rules'])}, "
    f"proved_derived_lemmas={len(validated['proved_derived_lemmas'])}, "
    f"domain_lemmas={len(validated['domain_lemmas'])}"
)
