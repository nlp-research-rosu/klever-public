#!/usr/bin/env python3
"""Reconstruct and bijectively compare the verification-module rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")
manifest = json.loads(manifest_path.read_text())
inventory = inventory_verification(workspace)
source_lines = verification.read_text().splitlines()
failures: list[str] = []


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status}: {label}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        failures.append(label)


print(json.dumps(inventory, indent=2, sort_keys=True))
check("verification module closure", inventory["verification_modules"], ["HEX-KEY-VERIFICATION"])
check(
    "verification.k byte hash",
    inventory["verification_sha256"],
    hashlib.sha256(verification.read_bytes()).hexdigest(),
)

for index, rule in enumerate(inventory["rules"]):
    label = f"rule[{index}] {rule['source_rule_id']}"
    physical_source = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    check(f"{label} physical source span", rule["text"], physical_source)
    normalized_hash = hashlib.sha256(
        " ".join(physical_source.split()).encode()
    ).hexdigest()
    check(f"{label} normalized source hash", rule["normalized_sha256"], normalized_hash)
    check(f"{label} source_rule_id", rule["source_rule_id"], f"rule-{normalized_hash}")

check(
    "whole canonical inventory hash",
    inventory["inventory_sha256"],
    canonical_json_sha256(inventory["rules"]),
)
check(
    "manifest whole inventory hash",
    manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
check("ordered identity bijection", manifest_ids, inventory_ids)
check("manifest has no duplicate identities", len(manifest_ids), len(set(manifest_ids)))
check("manifest rule count", len(manifest_ids), len(inventory_ids))

validated = validate_trust_boundary(workspace, manifest_path)
check("validated definitions count", len(validated["definitions"]), 8)
check("validated operational-rule count", len(validated["operational_rules"]), 0)
check("validated proved-derived-lemma count", len(validated["proved_derived_lemmas"]), 0)
check("validated domain-lemma count", len(validated["domain_lemmas"]), 0)

print("ORDERED_CLASSIFICATIONS")
for source_rule, classified in zip(inventory["rules"], manifest["rules"], strict=True):
    print(
        f"{source_rule['start_line']}-{source_rule['end_line']} "
        f"{source_rule['source_rule_id']} "
        f"{classified['classification']} attributes={source_rule['attributes']!r}"
    )

print(f"TOTAL_FAILURES={len(failures)}")
if failures:
    print("FAILED_LABELS=" + json.dumps(failures))
    raise SystemExit(1)
