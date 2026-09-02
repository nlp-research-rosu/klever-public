#!/usr/bin/env python3
"""Independently check Stage 3/4 rule and target bindings."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

validated = validate_trust_boundary(workspace, discovery_path)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
expected_domain_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
observed_target = klean_export.target_statement(generated)

lean_sources = sorted(generated.rglob("*.lean"))
target_tokens = []
for source in lean_sources:
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", source.read_text()):
        target_tokens.append(
            {
                "file": source.relative_to(generated).as_posix(),
                "offset": match.start(),
            }
        )

source_rule_ids = [
    rule["source_rule_id"] for rule in expected_domain_source_rules
]
mapped_source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/04_stage4_structure_command.py"
    ),
    "validated_counts": {
        "all_rules": len(validated["rules"]),
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
    "independently_accepted_domain_rule_ids": [],
    "mechanically_classified_domain_rule_ids": source_rule_ids,
    "input_manifest_source_rule_ids": [
        rule["source_rule_id"] for rule in input_manifest["source_rules"]
    ],
    "obligation_map_source_rule_ids": mapped_source_rule_ids,
    "obligation_source_rule_ids": obligation_ids,
    "source_obligation_bijection": {
        "expected_equals_input": (
            expected_domain_source_rules == input_manifest["source_rules"]
        ),
        "expected_equals_map": (
            expected_domain_source_rules == obligation_map["source_rules"]
        ),
        "same_order": source_rule_ids
        == mapped_source_rule_ids
        == obligation_ids,
        "no_duplicates": (
            len(source_rule_ids) == len(set(source_rule_ids))
            and len(mapped_source_rule_ids) == len(set(mapped_source_rule_ids))
            and len(obligation_ids) == len(set(obligation_ids))
        ),
    },
    "obligation_count": len(obligation_map["obligations"]),
    "trust_parameters": obligation_map["trust_parameters"],
    "target": {
        "expected_definition": expected_target_definition,
        "observed": observed_target,
        "raw_target_tokens": target_tokens,
        "input_recorded": json.loads(
            Path("/audit-input.json").read_text()
        )["resolution"]["target"],
        "generator_manifest": generator_manifest["target"],
        "preflight": preflight["target"],
    },
    "status": {
        "generator_obligation_count": generator_manifest["obligation_count"],
        "export_status": export_result["status"],
        "export_obligation_count": export_result["obligation_count"],
        "preflight_status": preflight["status"],
        "preflight_obligation_count": preflight["obligation_count"],
    },
    "hash_bindings": {
        "obligation_map": {
            "recorded": generator_manifest["obligation_map_sha256"],
            "recomputed": hashlib.sha256(
                obligation_map_path.read_bytes()
            ).hexdigest(),
        },
        "verification": {
            "recorded": input_manifest["verification_sha256"],
            "recomputed": hashlib.sha256(
                (workspace / "verification.k").read_bytes()
            ).hexdigest(),
        },
        "discovery": {
            "recorded": input_manifest[
                "stage3_discovery_manifest_sha256"
            ],
            "recomputed": discovery_hash,
        },
        "generated_tree": {
            "recorded": generator_manifest["generated_tree_sha256"],
            "recomputed": klean_export.tree_digest(generated),
        },
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
