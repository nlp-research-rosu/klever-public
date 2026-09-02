#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
discovery = json.loads(discovery_path.read_text())

rules = inventory["rules"]
classified = discovery["rules"]
reconstructed_ids = [rule["source_rule_id"] for rule in rules]
classified_ids = [rule["source_rule_id"] for rule in classified]

assert discovery["schema_version"] == 2
assert inventory["inventory_sha256"] == discovery["inventory_sha256"]
assert len(reconstructed_ids) == len(set(reconstructed_ids))
assert len(classified_ids) == len(set(classified_ids))
assert classified_ids == reconstructed_ids

# Independent classifications made from the frozen source and the imported
# operational rules. The final entry rewrites a pre-existing operational
# symbol and is therefore not a definition or an independently proved lemma.
expected_classes = [
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DEFINITION",
    "DOMAIN_LEMMA",
]
observed_classes = [rule["classification"] for rule in classified]
assert observed_classes == expected_classes

records = []
for index, (rule, stage3, expected) in enumerate(
    zip(rules, classified, expected_classes, strict=True), start=1
):
    assert rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
    if "simplification" in rule["attributes"]:
        assert expected in {"DEFINITION", "DOMAIN_LEMMA"}
    records.append(
        {
            "index": index,
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": rule["normalized_sha256"],
            "source_rule_id": rule["source_rule_id"],
            "attributes": rule["attributes"],
            "independent_classification": expected,
            "stage3_classification": stage3["classification"],
            "text": rule["text"],
        }
    )

print(
    json.dumps(
        {
            "status": "PASS",
            "verification_file": inventory["verification_file"],
            "verification_sha256": inventory["verification_sha256"],
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "inventory_sha256": inventory["inventory_sha256"],
            "rule_count": len(records),
            "classification_counts": {
                category: expected_classes.count(category)
                for category in sorted(set(expected_classes))
            },
            "records": records,
        },
        indent=2,
        sort_keys=False,
    )
)
