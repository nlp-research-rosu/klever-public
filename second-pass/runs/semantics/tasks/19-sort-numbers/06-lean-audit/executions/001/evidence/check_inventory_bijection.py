#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())
verification_lines = (workspace / "verification.k").read_text().splitlines()

checks: list[tuple[str, bool]] = []
checks.append(
    (
        "whole inventory canonical hash",
        canonical_json_sha256(inventory["rules"]) == inventory["inventory_sha256"],
    )
)
checks.append(
    (
        "protected whole inventory hash",
        discovery["inventory_sha256"] == inventory["inventory_sha256"],
    )
)

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
checks.extend(
    [
        ("inventory IDs unique", len(inventory_ids) == len(set(inventory_ids))),
        ("discovery IDs unique", len(discovery_ids) == len(set(discovery_ids))),
        ("rule counts equal", len(inventory_ids) == len(discovery_ids)),
        ("ordered identity sequence exact", inventory_ids == discovery_ids),
        ("identity sets exact", set(inventory_ids) == set(discovery_ids)),
    ]
)

for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    checks.extend(
        [
            (f"rule[{index}] normalized hash", digest == rule["normalized_sha256"]),
            (
                f"rule[{index}] source_rule_id",
                rule["source_rule_id"] == f"rule-{digest}",
            ),
            (f"rule[{index}] exact source span", source_slice == rule["text"]),
        ]
    )

validated = validate_trust_boundary(workspace, discovery_path)
checks.append(
    (
        "trusted Stage 3 structural validator inventory",
        validated["inventory_sha256"] == inventory["inventory_sha256"],
    )
)

for label, result in checks:
    print(f"{label}: {'PASS' if result else 'FAIL'}")
print(f"inventory_count={len(inventory_ids)}")
print(f"discovery_count={len(discovery_ids)}")
print(f"inventory_sha256={inventory['inventory_sha256']}")
print(
    "classification_counts="
    + json.dumps(
        Counter(entry["classification"] for entry in discovery["rules"]),
        sort_keys=True,
    )
)
print(f"all_checks_pass={all(result for _label, result in checks)}")
