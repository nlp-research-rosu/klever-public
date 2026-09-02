#!/usr/bin/env python3
"""Explicit ordered/bijective comparison using the trusted rule inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]

checks = {
    "inventory hash": (
        inventory["inventory_sha256"],
        manifest["inventory_sha256"],
    ),
    "ordered identity list": (canonical_ids, manifest_ids),
    "canonical identity uniqueness": (
        len(canonical_ids),
        len(set(canonical_ids)),
    ),
    "manifest identity uniqueness": (
        len(manifest_ids),
        len(set(manifest_ids)),
    ),
    "rule count": (len(inventory["rules"]), len(manifest["rules"])),
}

failures = 0
for label, (observed, expected) in checks.items():
    status = "PASS" if observed == expected else "FAIL"
    failures += status == "FAIL"
    print(f"{status}: {label}")
    print(f"  canonical: {observed!r}")
    print(f"  manifest:  {expected!r}")

print("\nCanonical rule reconstruction:")
for index, rule in enumerate(inventory["rules"], start=1):
    print(
        f"{index}. {rule['source_rule_id']} "
        f"{rule['module']}:{rule['start_line']}-{rule['end_line']} "
        f"normalized_sha256={rule['normalized_sha256']} "
        f"attributes={rule['attributes']!r}"
    )
    print(rule["text"])

print(f"\nFAILURES: {failures}")
if failures:
    raise SystemExit(1)
