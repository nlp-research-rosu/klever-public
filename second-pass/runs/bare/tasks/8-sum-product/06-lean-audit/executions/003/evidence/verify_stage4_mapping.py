#!/usr/bin/env python3
"""Verify the complete Stage 3 partition and empty Stage 4 mapping."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, klean_export


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
RULE_ID = (
    "rule-08e473cc777c3fe3dfbffc47a89f7ed00a323ab5af8be120c20538dd19dbc3e1"
)


inventory = k_rule_inventory.inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)

rule_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}

# This is the independent semantic classification, stated here rather than
# copied from the protected manifest.
independent_classification = {RULE_ID: "DEFINITION"}
expected_definitions = [
    {
        **rule_by_id[RULE_ID],
        "classification": independent_classification[RULE_ID],
        "rationale": discovery_by_id[RULE_ID]["rationale"],
    }
]

raw_target_declarations: list[str] = []
for source in sorted(GENERATED.rglob("*.lean")):
    for match in re.finditer(
        r"(?m)^\s*def\s+targetStatement\b", source.read_text()
    ):
        raw_target_declarations.append(
            f"{source.relative_to(GENERATED).as_posix()}:{match.start()}"
        )

observed_ids = [
    obligation.get("source_rule_id")
    for obligation in obligation_map["obligations"]
]
expected_domain_ids: list[str] = []
checks = {
    "independent_classification_covers_inventory": (
        list(independent_classification) == [
            rule["source_rule_id"] for rule in inventory["rules"]
        ]
    ),
    "protected_classification_matches_independent": (
        {
            source_rule_id: entry["classification"]
            for source_rule_id, entry in discovery_by_id.items()
        }
        == independent_classification
    ),
    "input_definitions_exact": (
        input_manifest["definitions"] == expected_definitions
    ),
    "input_nondefinition_partitions_empty": (
        input_manifest["operational_rules"] == []
        and input_manifest["proved_derived_lemmas"] == []
        and input_manifest["source_rules"] == []
    ),
    "summary_function_exact": (
        input_manifest["summary_functions"]
        == [
            {
                "name": "expectedSumProduct",
                "argument_sorts": ["Ints"],
                "return_sort": "PyVal",
            }
        ]
    ),
    "required_k_files_exact": (
        input_manifest["required_k_files"]
        == ["/frozen-k/semantic.k", "/frozen-k/verification.k"]
    ),
    "obligation_map_exact_empty_shape": (
        obligation_map
        == {
            "schema_version": 3,
            "source_rules": [],
            "obligations": [],
            "trust_parameters": [],
        }
    ),
    "source_rule_obligation_ordered_bijection": (
        observed_ids == expected_domain_ids
        and len(observed_ids) == len(set(observed_ids))
    ),
    "no_vacuous_or_weakened_conjuncts": (
        obligation_map["obligations"] == []
    ),
    "expected_target_definition_absent": (
        klean_export.expected_target_definition(obligation_map) is None
    ),
    "actual_target_absent": (
        klean_export.target_statement(GENERATED) is None
        and raw_target_declarations == []
    ),
    "manifest_target_absent": generator_manifest["target"] is None,
    "obligation_count_exact": generator_manifest["obligation_count"] == 0,
    "obligation_map_hash_exact": (
        hashlib.sha256(
            (GENERATED / "obligation-map.json").read_bytes()
        ).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
}

print("INDEPENDENT_CLASSIFICATION")
print(json.dumps(independent_classification, indent=2, sort_keys=True))
print("EXPECTED_DOMAIN_IDS", json.dumps(expected_domain_ids))
print("OBSERVED_OBLIGATION_IDS", json.dumps(observed_ids))
print("RAW_TARGET_DECLARATIONS", json.dumps(raw_target_declarations))
print("CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit("FAIL: Stage 3 partition or Stage 4 mapping mismatch")
print("RESULT PASS: exact empty obligation bijection and absent target confirmed")
