#!/usr/bin/env python3
"""Independent source-rule/obligation and target-identity checks."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification
from tools.klean_export import sha256_text, target_statement


generation = Path("/reference/klean-generation")
generated = generation / "generated"
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
inventory = inventory_verification(Path("/reference/k-proof"))
reconstructed_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}

independently_classified_domain_ids = [
    "rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2",
    "rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918",
    "rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9",
]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
source_ids = [entry["source_rule_id"] for entry in source_rules]
obligation_ids = [entry["source_rule_id"] for entry in obligations]

per_obligation = []
for source, obligation in zip(source_rules, obligations, strict=True):
    reconstructed = reconstructed_by_id[source["source_rule_id"]]
    per_obligation.append(
        {
            "source_rule_id": source["source_rule_id"],
            "source_equals_input_manifest": (
                source
                == input_manifest["source_rules"][len(per_obligation)]
            ),
            "span_matches_reconstruction": (
                obligation["source_span"]
                == {
                    "start_line": reconstructed["start_line"],
                    "end_line": reconstructed["end_line"],
                }
            ),
            "normalized_hash_matches_reconstruction": (
                obligation["normalized_sha256"]
                == reconstructed["normalized_sha256"]
                == source["normalized_sha256"]
            ),
            "inventory_hash_matches": (
                obligation["inventory_sha256"]
                == inventory["inventory_sha256"]
                == source["inventory_sha256"]
            ),
            "conjunct_hash_matches": (
                obligation["lean_conjunct_sha256"]
                == sha256_text(obligation["lean_conjunct"])
            ),
        }
    )

expected_definition_lines = ["def targetStatement"]
for parameter in obligation_map["trust_parameters"]:
    expected_definition_lines.append(
        f'    ({parameter["name"]} : {parameter["type"]})'
    )
expected_definition_lines.extend(
    (
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(
            f'({obligation["lean_conjunct"]})'
            for obligation in obligations
        ),
    )
)
expected_definition = "\n".join(expected_definition_lines)
lemmas_text = (
    generated / "Klean33SortThird/Lemmas.lean"
).read_text()
definition_matches = re.search(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    lemmas_text,
)
actual_definition = (
    definition_matches.group(0).strip()
    if definition_matches is not None
    else None
)

parameter_binding_checks = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    parameter_binding_checks.append(
        {
            "name": parameter["name"],
            "binding_sha256_matches": (
                parameter["binding_sha256"]
                == sha256_text(
                    json.dumps(
                        binding,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                )
            ),
            "source_rule_ids_in_domain_set": all(
                source_id in independently_classified_domain_ids
                for source_id in parameter["source_rule_ids"]
            ),
        }
    )

computed_target = target_statement(generated)
checks = {
    "domain_id_order_exact": (
        source_ids == independently_classified_domain_ids
    ),
    "obligation_id_order_exact": (
        obligation_ids == independently_classified_domain_ids
    ),
    "source_ids_unique": len(source_ids) == len(set(source_ids)),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "one_obligation_per_domain_rule": (
        len(source_ids) == len(obligation_ids) == 3
    ),
    "per_obligation_provenance_exact": all(
        all(
            value
            for key, value in item.items()
            if key != "source_rule_id"
        )
        for item in per_obligation
    ),
    "parameter_bindings_exact": all(
        item["binding_sha256_matches"]
        and item["source_rule_ids_in_domain_set"]
        for item in parameter_binding_checks
    ),
    "target_definition_is_exact_conjunction": (
        actual_definition == expected_definition
    ),
    "target_definition_hash_matches": (
        sha256_text(actual_definition or "")
        == generator_manifest["target"]["definition_sha256"]
    ),
    "target_matches_audit_and_manifest": (
        computed_target
        == generator_manifest["target"]
        == audit["target"]
    ),
    "obligation_count_matches": (
        generator_manifest["obligation_count"] == len(obligations) == 3
    ),
}

print(
    json.dumps(
        {
            "independent_domain_ids": independently_classified_domain_ids,
            "source_ids": source_ids,
            "obligation_ids": obligation_ids,
            "per_obligation": per_obligation,
            "parameter_binding_checks": parameter_binding_checks,
            "actual_target_definition": actual_definition,
            "expected_target_definition": expected_definition,
            "computed_target": computed_target,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
