#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction using the trusted inventory code."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
stage4_input_path = Path("/reference/klean-generation/input-manifest.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())
stage4_input = json.loads(stage4_input_path.read_text())

reconstructed_rules = inventory["rules"]
reconstructed_ids = [entry["source_rule_id"] for entry in reconstructed_rules]
classified = discovery["rules"]
classified_ids = [entry["source_rule_id"] for entry in classified]

assert len(reconstructed_ids) == len(set(reconstructed_ids)), (
    "reconstructed inventory contains duplicate IDs"
)
assert len(classified_ids) == len(set(classified_ids)), (
    "classification contains duplicate IDs"
)
assert reconstructed_ids == classified_ids, (
    "classification IDs are omitted, extra, or reordered"
)
assert inventory["inventory_sha256"] == discovery["inventory_sha256"], (
    "classification inventory hash differs from reconstruction"
)

stage4_entries = stage4_input["definitions"] + stage4_input["source_rules"]
stage4_by_id = {entry["source_rule_id"]: entry for entry in stage4_entries}
assert len(stage4_by_id) == len(stage4_entries), "Stage 4 input duplicates a rule"
assert set(stage4_by_id) == set(reconstructed_ids), (
    "Stage 4 input omits or adds an inventory rule"
)

for reconstructed, classification in zip(reconstructed_rules, classified):
    assert classification["source_rule_id"] == reconstructed["source_rule_id"]
    recorded = stage4_by_id[reconstructed["source_rule_id"]]
    for key in (
        "module",
        "start_line",
        "end_line",
        "normalized_sha256",
        "source_rule_id",
        "attributes",
        "text",
    ):
        assert recorded[key] == reconstructed[key], (
            f"{key} differs for {reconstructed['source_rule_id']}"
        )
    assert recorded["classification"] == classification["classification"], (
        f"classification differs for {reconstructed['source_rule_id']}"
    )

print(json.dumps(inventory, indent=2, sort_keys=True))
print("BIJECTION_CHECK: PASS")
print(f"RECONSTRUCTED_RULE_COUNT: {len(reconstructed_rules)}")
print(f"RECONSTRUCTED_INVENTORY_SHA256: {inventory['inventory_sha256']}")
