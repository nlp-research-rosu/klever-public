#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target reconciliation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


stage1 = Path("/reference/k-proof")
stage3_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

validated = validate_trust_boundary(stage1, stage3_path)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

discovery_sha256 = hashlib.sha256(stage3_path.read_bytes()).hexdigest()
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_sha256
)
mapped_source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]
expected_ids = [
    source_rule["source_rule_id"] for source_rule in expected_source_rules
]

raw_target_occurrences = []
for relative, kind, source in klean_export._tree_entries(generated):
    if kind == "file" and source.suffix == ".lean":
        for match in re.finditer(
            r"(?m)^\s*def\s+targetStatement\b", source.read_text()
        ):
            raw_target_occurrences.append(
                {
                    "file": relative,
                    "offset": match.start(),
                }
            )

observed_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
checks = {
    "independent_domain_set_is_empty": not expected_source_rules,
    "input_manifest_source_rules_exactly_match_domain_set": (
        input_manifest["source_rules"] == expected_source_rules
    ),
    "obligation_map_source_rules_exactly_match_domain_set": (
        mapped_source_rules == expected_source_rules
    ),
    "ordered_obligation_ids_exactly_match_domain_ids": (
        obligation_ids == expected_ids
    ),
    "obligation_ids_unique": (
        len(obligation_ids) == len(set(obligation_ids))
    ),
    "no_omitted_or_extra_obligations": (
        len(obligations) == len(expected_source_rules)
    ),
    "no_trust_parameters_for_empty_target": (
        obligation_map["trust_parameters"] == []
    ),
    "obligation_count_matches_every_manifest": (
        len(obligations)
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == 0
    ),
    "obligation_map_hash_matches_generator": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "expected_target_definition_is_absent": (
        expected_definition is None
    ),
    "trusted_target_parser_finds_no_target": observed_target is None,
    "raw_scan_finds_no_target_declaration": not raw_target_occurrences,
    "generator_target_is_null": generator_manifest["target"] is None,
    "export_status_is_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    ),
}
print(
    json.dumps(
        {
            "checks": checks,
            "all_checks_pass": all(checks.values()),
            "expected_domain_source_rules": expected_source_rules,
            "mapped_source_rules": mapped_source_rules,
            "obligations": obligations,
            "trust_parameters": obligation_map["trust_parameters"],
            "expected_target_definition": expected_definition,
            "observed_target": observed_target,
            "raw_target_occurrences": raw_target_occurrences,
        },
        indent=2,
        sort_keys=True,
    )
)
