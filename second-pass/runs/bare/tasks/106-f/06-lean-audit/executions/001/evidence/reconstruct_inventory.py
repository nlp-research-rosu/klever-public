import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


inventory = inventory_verification(Path("/reference/k-proof"))
manifest = json.loads(Path("/reference/lemma-discovery.json").read_text())
manifest_by_id = {
    entry["source_rule_id"]: entry for entry in manifest["rules"]
}
independent_roles = {
    12: ("DEFINITION", "base equation for the named mathFactorial summary"),
    13: (
        "DEFINITION",
        "guarded decreasing recurrence for the named mathFactorial summary",
    ),
    16: ("DEFINITION", "base equation for the named mathTriangle summary"),
    17: (
        "DEFINITION",
        "guarded decreasing recurrence for the named mathTriangle summary",
    ),
    20: (
        "DEFINITION",
        "guarded even branch defining the named expectedAt summary",
    ),
    22: (
        "DEFINITION",
        "guarded odd branch defining the named expectedAt summary",
    ),
    28: ("DEFINITION", "initial equation for the named expected list summary"),
    31: (
        "DEFINITION",
        "terminating equation for the named expectedCompletion summary",
    ),
    33: (
        "DEFINITION",
        "even-step recurrence for the named expectedCompletion summary",
    ),
    38: (
        "DEFINITION",
        "odd-step recurrence for the named expectedCompletion summary",
    ),
    47: ("DEFINITION", "macro equation for the named solutionLoop proof term"),
    62: ("DEFINITION", "macro equation for the named solution proof term"),
}
rows = []
for rule in inventory["rules"]:
    role, reason = independent_roles[rule["start_line"]]
    recorded = manifest_by_id[rule["source_rule_id"]]["classification"]
    rows.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            "independent_classification": role,
            "reason": reason,
            "recorded_classification": recorded,
            "match": role == recorded,
        }
    )

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
result = {
    "inventory": inventory,
    "bijection": {
        "inventory_hash_match": (
            manifest["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "inventory_rule_count": len(inventory_ids),
        "manifest_rule_count": len(manifest_ids),
        "ordered_source_rule_ids_match": inventory_ids == manifest_ids,
        "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "id_sets_match": set(inventory_ids) == set(manifest_ids),
        "all_source_rule_ids_bind_normalized_hash": all(
            rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
            for rule in inventory["rules"]
        ),
        "simplification_rule_count": sum(
            "simplification" in rule["attributes"]
            for rule in inventory["rules"]
        ),
    },
    "classification": {
        "all_entries_accounted_for": (
            set(independent_roles)
            == {rule["start_line"] for rule in inventory["rules"]}
        ),
        "all_classifications_match": all(row["match"] for row in rows),
        "independent_counts": {
            role: sum(row["independent_classification"] == role for row in rows)
            for role in [
                "DEFINITION",
                "OPERATIONAL_RULE",
                "PROVED_DERIVED_LEMMA",
                "DOMAIN_LEMMA",
            ]
        },
        "rules": rows,
    },
}
print(json.dumps(result, indent=2, sort_keys=True))

assert all(
    value is True
    for key, value in result["bijection"].items()
    if key.endswith("match")
    or key.endswith("unique")
    or key.startswith("all_")
)
assert result["bijection"]["inventory_rule_count"] == 12
assert result["bijection"]["manifest_rule_count"] == 12
assert result["classification"]["all_entries_accounted_for"]
assert result["classification"]["all_classifications_match"]
assert result["classification"]["independent_counts"] == {
    "DEFINITION": 12,
    "OPERATIONAL_RULE": 0,
    "PROVED_DERIVED_LEMMA": 0,
    "DOMAIN_LEMMA": 0,
}
