#!/usr/bin/env python3
"""Independent structural comparison of domain rules, obligations, and target."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


domain_ids = [
    "rule-050c02c309a5a530a8227be9add80d806c43948fb2a4cee44e6a4d8da7a1a71d",
    "rule-6a2681616cee874c5a1856e102a2ab5794a9175a210318f62d58e2c74647c6a2",
]
generated = Path("/reference/klean-generation/generated")
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text(encoding="utf-8")
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text(
        encoding="utf-8"
    )
)
audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
inventory = inventory_verification(Path("/reference/k-proof"))
inventory_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}

source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [rule["source_rule_id"] for rule in obligations]

per_obligation = []
for source, obligation in zip(source_rules, obligations, strict=True):
    source_id = source["source_rule_id"]
    frozen = inventory_by_id[source_id]
    conjunct_hash = hashlib.sha256(
        obligation["lean_conjunct"].encode("utf-8")
    ).hexdigest()
    per_obligation.append(
        {
            "source_rule_id": source_id,
            "source_entry_equals_frozen_inventory": all(
                source.get(key) == frozen.get(key)
                for key in (
                    "source_rule_id",
                    "module",
                    "start_line",
                    "end_line",
                    "normalized_sha256",
                    "attributes",
                    "text",
                    "file",
                )
            ),
            "source_span_matches": obligation["source_span"]
            == {
                "start_line": frozen["start_line"],
                "end_line": frozen["end_line"],
            },
            "normalized_hash_matches": (
                obligation["normalized_sha256"]
                == frozen["normalized_sha256"]
            ),
            "conjunct_hash_recomputed": conjunct_hash,
            "conjunct_hash_recorded": obligation["lean_conjunct_sha256"],
            "conjunct_hash_matches": (
                conjunct_hash == obligation["lean_conjunct_sha256"]
            ),
        }
    )

target = klean_export.target_statement(generated)
parameter_checks = []
target_definition = (
    generated / generator["target"]["file"]
).read_text(encoding="utf-8")
for parameter in generator["target"]["parameters"]:
    parameter_checks.append(
        {
            "name": parameter["name"],
            "all_bound_rules_are_domain_rules": set(
                parameter["source_rule_ids"]
            ).issubset(domain_ids),
            "name_occurs_in_target_definition": (
                parameter["name"] in target_definition
            ),
        }
    )

result = {
    "independently_classified_domain_rule_ids": domain_ids,
    "source_rule_ids": source_ids,
    "obligation_rule_ids": obligation_ids,
    "domain_ids_unique": len(domain_ids) == len(set(domain_ids)),
    "source_ids_unique": len(source_ids) == len(set(source_ids)),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "exact_ordered_domain_source_obligation_bijection": (
        domain_ids == source_ids == obligation_ids
    ),
    "obligation_count": len(obligations),
    "generator_obligation_count": generator["obligation_count"],
    "per_obligation": per_obligation,
    "target_recomputed": target,
    "target_equals_generator_manifest": target == generator["target"],
    "target_equals_audit_input": (
        target == audit_input["resolution"]["target"]
    ),
    "parameter_checks": parameter_checks,
}
result["all_structural_checks_pass"] = (
    result["exact_ordered_domain_source_obligation_bijection"]
    and len(obligations) == generator["obligation_count"]
    and all(
        entry["source_entry_equals_frozen_inventory"]
        and entry["source_span_matches"]
        and entry["normalized_hash_matches"]
        and entry["conjunct_hash_matches"]
        for entry in per_obligation
    )
    and result["target_equals_generator_manifest"]
    and result["target_equals_audit_input"]
    and all(
        entry["all_bound_rules_are_domain_rules"]
        and entry["name_occurs_in_target_definition"]
        for entry in parameter_checks
    )
)
print(json.dumps(result, indent=2, sort_keys=False))
