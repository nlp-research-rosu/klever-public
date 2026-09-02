#!/usr/bin/env python3
"""Independent bijection checks between the canonical inventory and Stage 3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


inventory = json.loads(
    Path("/audit-output/evidence/reconstructed-rule-inventory.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())

inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [rule["source_rule_id"] for rule in inventory_rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery_rules]

checks: list[tuple[str, bool, object]] = [
    ("inventory schema is 2", inventory["schema_version"] == 2, inventory["schema_version"]),
    ("discovery schema is 2", discovery["schema_version"] == 2, discovery["schema_version"]),
    (
        "inventory hash matches discovery",
        inventory["inventory_sha256"] == discovery["inventory_sha256"],
        (inventory["inventory_sha256"], discovery["inventory_sha256"]),
    ),
    (
        "same rule count",
        len(inventory_rules) == len(discovery_rules),
        (len(inventory_rules), len(discovery_rules)),
    ),
    (
        "inventory IDs unique",
        len(inventory_ids) == len(set(inventory_ids)),
        len(inventory_ids) - len(set(inventory_ids)),
    ),
    (
        "discovery IDs unique",
        len(discovery_ids) == len(set(discovery_ids)),
        len(discovery_ids) - len(set(discovery_ids)),
    ),
    (
        "exact ordered identity bijection",
        inventory_ids == discovery_ids,
        {"inventory": inventory_ids, "discovery": discovery_ids},
    ),
]

allowed = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}
for index, (source, classified) in enumerate(
    zip(inventory_rules, discovery_rules, strict=False)
):
    normalized = " ".join(source["text"].split())
    recomputed = hashlib.sha256(normalized.encode()).hexdigest()
    checks.extend(
        [
            (
                f"rule {index} normalized source hash",
                recomputed == source["normalized_sha256"],
                (recomputed, source["normalized_sha256"]),
            ),
            (
                f"rule {index} source_rule_id binds hash",
                source["source_rule_id"] == f"rule-{recomputed}",
                source["source_rule_id"],
            ),
            (
                f"rule {index} classification accounted",
                classified.get("classification") in allowed,
                classified.get("classification"),
            ),
            (
                f"rule {index} discovery has exact fields",
                set(classified) == {"source_rule_id", "classification", "rationale"},
                sorted(classified),
            ),
        ]
    )

failed = False
for label, passed, observed in checks:
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
    if not passed:
        failed = True
        print(f"  observed={observed!r}")

print(f"RESULT: {'FAIL' if failed else 'PASS'}")
raise SystemExit(1 if failed else 0)
