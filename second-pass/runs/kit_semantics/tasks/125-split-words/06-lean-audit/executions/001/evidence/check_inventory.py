#!/usr/bin/env python3
"""Reconstruct and compare the canonical Stage 3 rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
    source = (WORKSPACE / "verification.k").read_text()
    source_lines = source.splitlines()

    print(json.dumps(inventory, indent=2, sort_keys=True))
    print("INDEPENDENT CONSISTENCY CHECKS")
    rules = inventory["rules"]
    discovered_rules = discovery["rules"]
    inventory_ids = [item["source_rule_id"] for item in rules]
    discovered_ids = [item["source_rule_id"] for item in discovered_rules]
    print(f"inventory_rule_count={len(rules)}")
    print(f"discovery_rule_count={len(discovered_rules)}")
    print(f"inventory_ids_unique={len(inventory_ids) == len(set(inventory_ids))}")
    print(f"discovery_ids_unique={len(discovered_ids) == len(set(discovered_ids))}")
    print(f"exact_ordered_identity_match={inventory_ids == discovered_ids}")
    print(f"extra_discovery_ids={sorted(set(discovered_ids) - set(inventory_ids))}")
    print(f"omitted_inventory_ids={sorted(set(inventory_ids) - set(discovered_ids))}")

    all_ok = (
        len(rules) == len(discovered_rules)
        and len(inventory_ids) == len(set(inventory_ids))
        and len(discovered_ids) == len(set(discovered_ids))
        and inventory_ids == discovered_ids
    )
    for index, rule in enumerate(rules):
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        source_rule_id = f"rule-{normalized_hash}"
        span_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        checks = {
            "normalized_hash": normalized_hash == rule["normalized_sha256"],
            "source_rule_id": source_rule_id == rule["source_rule_id"],
            "source_span": span_text == rule["text"],
        }
        all_ok &= all(checks.values())
        print(f"rule[{index}]={rule['source_rule_id']}")
        print(f"  module={rule['module']}")
        print(f"  span={rule['start_line']}-{rule['end_line']}")
        print(f"  normalized_sha256={normalized_hash}")
        print(f"  attributes={rule['attributes']}")
        print(f"  checks={checks}")

    independent_inventory_hash = canonical_json_sha256(rules)
    print(f"independent_inventory_sha256={independent_inventory_hash}")
    print(f"tool_inventory_sha256={inventory['inventory_sha256']}")
    print(f"discovery_inventory_sha256={discovery['inventory_sha256']}")
    inventory_hash_ok = (
        independent_inventory_hash
        == inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    )
    all_ok &= inventory_hash_ok
    print(f"inventory_hash_match={inventory_hash_ok}")
    print(f"verification_sha256={inventory['verification_sha256']}")
    print(f"verification_module={inventory['verification_module']}")
    print(f"verification_modules={inventory['verification_modules']}")
    print(f"validated_definition_count={len(validated['definitions'])}")
    print(f"validated_operational_rule_count={len(validated['operational_rules'])}")
    print(f"validated_proved_derived_lemma_count={len(validated['proved_derived_lemmas'])}")
    print(f"validated_domain_lemma_count={len(validated['domain_lemmas'])}")
    print(f"OVERALL={'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
