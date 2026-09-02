#!/usr/bin/env python3

import json
import re
from collections import Counter
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


stage1 = Path("/reference/k-proof")
stage3_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

inventory = inventory_verification(stage1)
stage3 = json.loads(stage3_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())

inventory_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
classification_by_id = {
    rule["source_rule_id"]: {
        "classification": rule["classification"],
        "rationale": rule["rationale"],
    }
    for rule in stage3["rules"]
}

enriched = []
for rule in inventory["rules"]:
    classified = dict(rule)
    classified.update(classification_by_id[rule["source_rule_id"]])
    enriched.append(classified)

bucket_names = {
    "DEFINITION": "definitions",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
    "DOMAIN_LEMMA": "source_rules",
}
expected_buckets = {
    bucket: [
        rule for rule in enriched
        if rule["classification"] == classification
    ]
    for classification, bucket in bucket_names.items()
}

all_input_ids = [
    rule["source_rule_id"]
    for bucket in bucket_names.values()
    for rule in input_manifest[bucket]
]
domain_ids = [
    rule["source_rule_id"] for rule in expected_buckets["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

lean_text = "\n".join(
    path.read_text()
    for path in sorted(generated.rglob("*.lean"))
)
proposition_declarations = re.findall(
    r"(?m)^\s*(?:def|theorem|lemma)\s+\S+[^\n]*:\s*Prop\b",
    lean_text,
)

simplification_rules = [
    {
        "source_rule_id": rule["source_rule_id"],
        "classification": classification_by_id[
            rule["source_rule_id"]
        ]["classification"],
    }
    for rule in inventory["rules"]
    if "simplification" in rule["attributes"]
]

checks = {
    "stage3_inventory_hash_exact": (
        stage3["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "stage3_identity_order_exact": (
        [rule["source_rule_id"] for rule in stage3["rules"]]
        == [rule["source_rule_id"] for rule in inventory["rules"]]
    ),
    "stage3_no_duplicate_ids": (
        len(classification_by_id) == len(stage3["rules"])
    ),
    "input_manifest_all_classification_buckets_exact": all(
        input_manifest[bucket] == expected
        for bucket, expected in expected_buckets.items()
    ),
    "input_manifest_inventory_bijection": (
        Counter(all_input_ids)
        == Counter(rule["source_rule_id"] for rule in inventory["rules"])
        and all(count == 1 for count in Counter(all_input_ids).values())
    ),
    "simplification_classes_allowed": all(
        entry["classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for entry in simplification_rules
    ),
    "domain_source_rule_ids_unique": (
        len(domain_ids) == len(set(domain_ids))
    ),
    "domain_obligation_ids_unique": (
        len(obligation_ids) == len(set(obligation_ids))
    ),
    "domain_obligation_identity_order_bijection": (
        domain_ids == obligation_ids
    ),
    "obligation_map_source_rules_exact": (
        obligation_map["source_rules"]
        == input_manifest["source_rules"]
        == expected_buckets["source_rules"]
    ),
    "obligation_count_exact": (
        len(obligation_ids)
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
    ),
    "target_absent_everywhere": (
        not domain_ids
        and not obligation_ids
        and klean_export.target_statement(generated) is None
        and generator_manifest["target"] is None
        and not proposition_declarations
    ),
    "no_vacuous_conjunct_or_trust_parameter": (
        obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
    ),
    "no_obligation_status_exact": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
}

result = {
    "all_checks_pass": all(checks.values()),
    "checks": checks,
    "classification_counts": dict(
        sorted(Counter(
            rule["classification"] for rule in stage3["rules"]
        ).items())
    ),
    "domain_source_rule_ids": domain_ids,
    "obligation_source_rule_ids": obligation_ids,
    "proposition_declarations": proposition_declarations,
    "simplification_rules": simplification_rules,
}
print(json.dumps(result, indent=2, sort_keys=True))
