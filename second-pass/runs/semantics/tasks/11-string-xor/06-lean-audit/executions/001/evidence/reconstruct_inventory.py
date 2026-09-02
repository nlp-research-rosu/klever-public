#!/usr/bin/env python3
import collections
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
canonical = inventory["rules"]
classified = discovery["rules"]

canonical_ids = [rule["source_rule_id"] for rule in canonical]
classified_ids = [rule["source_rule_id"] for rule in classified]
canonical_counts = collections.Counter(canonical_ids)
classified_counts = collections.Counter(classified_ids)
canonical_by_id = {rule["source_rule_id"]: rule for rule in canonical}

ordered_comparison = []
for index in range(max(len(canonical), len(classified))):
    canonical_rule = canonical[index] if index < len(canonical) else None
    classified_rule = classified[index] if index < len(classified) else None
    ordered_comparison.append(
        {
            "index": index,
            "canonical_source_rule_id": (
                canonical_rule["source_rule_id"] if canonical_rule else None
            ),
            "classified_source_rule_id": (
                classified_rule["source_rule_id"] if classified_rule else None
            ),
            "same_identity": (
                canonical_rule is not None
                and classified_rule is not None
                and canonical_rule["source_rule_id"]
                == classified_rule["source_rule_id"]
            ),
            "canonical_span": (
                {
                    "module": canonical_rule["module"],
                    "start_line": canonical_rule["start_line"],
                    "end_line": canonical_rule["end_line"],
                }
                if canonical_rule
                else None
            ),
            "canonical_normalized_sha256": (
                canonical_rule["normalized_sha256"] if canonical_rule else None
            ),
            "canonical_text": canonical_rule["text"] if canonical_rule else None,
            "classification": (
                classified_rule.get("classification") if classified_rule else None
            ),
            "rationale": (
                classified_rule.get("rationale") if classified_rule else None
            ),
        }
    )

checks = {
    "manifest_schema_version_is_2": discovery.get("schema_version") == 2,
    "inventory_hash_matches": (
        discovery.get("inventory_sha256") == inventory["inventory_sha256"]
    ),
    "same_rule_count": len(canonical) == len(classified),
    "canonical_has_no_duplicate_ids": all(
        count == 1 for count in canonical_counts.values()
    ),
    "manifest_has_no_duplicate_ids": all(
        count == 1 for count in classified_counts.values()
    ),
    "no_manifest_omissions": set(canonical_ids) <= set(classified_ids),
    "no_manifest_extras": set(classified_ids) <= set(canonical_ids),
    "same_ordered_identities": canonical_ids == classified_ids,
    "every_id_binds_its_recomputed_hash": all(
        rule["source_rule_id"] == f"rule-{rule['normalized_sha256']}"
        for rule in canonical
    ),
}

result = {
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "inventory_sha256": inventory["inventory_sha256"],
    "rule_count": len(canonical),
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "missing_ids": sorted(set(canonical_ids) - set(classified_ids)),
    "extra_ids": sorted(set(classified_ids) - set(canonical_ids)),
    "duplicate_canonical_ids": sorted(
        source_rule_id
        for source_rule_id, count in canonical_counts.items()
        if count != 1
    ),
    "duplicate_manifest_ids": sorted(
        source_rule_id
        for source_rule_id, count in classified_counts.items()
        if count != 1
    ),
    "ordered_comparison": ordered_comparison,
    "canonical_inventory": canonical,
}
print(json.dumps(result, indent=2, sort_keys=True))
