#!/usr/bin/env python3
"""Independent Stage 4 map/count/target checks after semantic classification."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export


generated = Path("/reference/klean-generation/generated")
map_path = generated / "obligation-map.json"
obligation_map = json.loads(map_path.read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]

independent_classification = {
    "rule-446e7a734fabed5a2e572668cda7855a61d25da12a442b82a62f647c84f77bd3": "DEFINITION",
    "rule-978c7862f1563f18c6de2c29b31592e2015d58e41236161ec41227b34122fc54": "DEFINITION",
    "rule-fff7ec9596c3f8bfea2b8032980d90cb281da9e279b32474488f5f03c5c489f7": "DEFINITION",
    "rule-b63a26b5a4b87f3f77a92f06b896b36655a9114c01cfdee89d791439a893db9e": "DEFINITION",
}
independent_domain_ids = [
    source_rule_id
    for source_rule_id, classification in independent_classification.items()
    if classification == "DOMAIN_LEMMA"
]
mapped_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
target = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

checks = {
    "independent_domain_set_empty": independent_domain_ids == [],
    "input_manifest_source_rules_empty": input_manifest["source_rules"] == [],
    "obligation_map_source_rules_empty": obligation_map["source_rules"] == [],
    "obligation_map_obligations_empty": obligation_map["obligations"] == [],
    "obligation_map_trust_parameters_empty": (
        obligation_map["trust_parameters"] == []
    ),
    "source_rule_obligation_ids_exact_bijection": (
        mapped_ids == independent_domain_ids
        and len(mapped_ids) == len(set(mapped_ids))
    ),
    "obligation_map_hash_matches_generator_manifest": (
        hashlib.sha256(map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "all_recorded_obligation_counts_zero": (
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == audit_input["stage4_preflight"]["obligation_count"]
        == 0
    ),
    "expected_target_definition_absent": expected_target_definition is None,
    "generated_target_absent": target is None,
    "all_recorded_targets_absent": (
        generator_manifest["target"]
        is export_result.get("target")
        is preflight["target"]
        is audit_input["target"]
        is None
    ),
    "all_recorded_statuses_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and audit_input["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and audit_input["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
}
checks["all_checks_pass"] = all(checks.values())

print(
    json.dumps(
        {
            "independent_classification": independent_classification,
            "independent_domain_ids": independent_domain_ids,
            "obligation_map": obligation_map,
            "mapped_ids": mapped_ids,
            "expected_target_definition": expected_target_definition,
            "target_statement": target,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
