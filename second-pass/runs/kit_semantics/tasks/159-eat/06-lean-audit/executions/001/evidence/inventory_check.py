#!/usr/bin/env python3
"""Reconstruct and compare the local verification-module rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def main() -> None:
    verification = (WORKSPACE / "verification.k").read_text()
    print("FROZEN verification.k WITH PHYSICAL LINE NUMBERS")
    for number, line in enumerate(verification.splitlines(), 1):
        print(f"{number:4d}: {line}")

    inventory = inventory_verification(WORKSPACE)
    protected = json.loads(DISCOVERY.read_text())
    validated = validate_trust_boundary(WORKSPACE, DISCOVERY)

    print("RECONSTRUCTED INVENTORY")
    print(json.dumps(inventory, indent=2, sort_keys=True))
    print("PROTECTED STAGE 3 MANIFEST")
    print(json.dumps(protected, indent=2, sort_keys=True))

    independent_empty_hash = hashlib.sha256(b"[]").hexdigest()
    print(f"canonical_json_sha256(rules)={canonical_json_sha256(inventory['rules'])}")
    print(f"sha256(b'[]')={independent_empty_hash}")
    assert inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"])
    assert inventory["inventory_sha256"] == protected["inventory_sha256"]

    inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    protected_ids = [entry["source_rule_id"] for entry in protected["rules"]]
    print(f"inventory source-rule IDs in order={inventory_ids}")
    print(f"protected source-rule IDs in order={protected_ids}")
    print(f"duplicate inventory IDs={len(inventory_ids) - len(set(inventory_ids))}")
    print(f"duplicate protected IDs={len(protected_ids) - len(set(protected_ids))}")
    assert inventory_ids == protected_ids

    counts = {
        key: len(validated[key])
        for key in (
            "rules",
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    }
    print("CLASSIFICATION COUNTS")
    print(json.dumps(counts, indent=2, sort_keys=True))
    assert counts == {
        "rules": 0,
        "definitions": 0,
        "operational_rules": 0,
        "proved_derived_lemmas": 0,
        "domain_lemmas": 0,
    }
    print("INVENTORY_RESULT: PASS")


if __name__ == "__main__":
    main()
