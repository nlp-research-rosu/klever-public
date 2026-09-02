#!/usr/bin/env python3
"""Record the independent rule classification and Stage 4 bijection judgment."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


DIGIT = "rule-ab9ad07a78277db66d0daa17d1890ca498e7cfba285dcb571a8014e3726d1543"
SLASH = "rule-c37d3f4e07aa03cba6c5454c87da6676a49c0ee9f8f31c9f2f047d68206cb650"
DOMAIN_IDS = [DIGIT, SLASH]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
recorded = {rule["source_rule_id"]: rule for rule in discovery["rules"]}
obligation_map = json.loads((generated / "obligation-map.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

classification = []
for rule in inventory["rules"]:
    source_rule_id = rule["source_rule_id"]
    if source_rule_id == DIGIT:
        independent = "DOMAIN_LEMMA"
        rationale = (
            "Program-specific operational bridge from the source loop to scanResult. "
            "Stage 1 proves four P-specialized claims but never proves this exact "
            "P-parametric rule against VERIFICATION-BASE; an exact copied claim "
            "rerun against that base exits 1 with WarnStuckClaimState."
        )
    elif source_rule_id == SLASH:
        independent = "DOMAIN_LEMMA"
        rationale = (
            "Program-specific operational bridge for the slash branch. Stage 1 "
            "proves three P-specialized claims but never this exact P-parametric "
            "rule against VERIFICATION-BASE; an exact copied claim rerun against "
            "that base exits 1 with WarnStuckClaimState."
        )
    else:
        independent = "DEFINITION"
        if rule["start_line"] <= 112:
            rationale = (
                "Defines a named proof term or exact structural scope/body macro."
            )
        elif rule["start_line"] <= 143:
            rationale = (
                "Defines a base, recurrence, or totalizing case of named summary "
                "function validScan."
            )
        else:
            rationale = (
                "Defines a base or recurrence of named summary function scanResult."
            )
    classification.append(
        {
            "index": len(classification),
            "source_rule_id": source_rule_id,
            "module": rule["module"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "recorded_classification": recorded[source_rule_id]["classification"],
            "independent_classification": independent,
            "classification_matches": recorded[source_rule_id]["classification"]
            == independent,
            "rationale": rationale,
        }
    )

actual_obligation_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]
actual_source_rule_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
target = klean_export.target_statement(generated)

field_checks = {
    "input.frozen_input_sha256": input_manifest["frozen_input_sha256"]
    == audit["hashes"]["stage1_export_sha256"],
    "input.stage1_workspace_sha256": input_manifest["stage1_workspace_sha256"]
    == audit["hashes"]["stage1_export_sha256"],
    "input.discovery_sha256": input_manifest["stage3_discovery_manifest_sha256"]
    == audit["hashes"]["discovery_manifest_sha256"],
    "input.inventory_sha256": input_manifest["inventory_sha256"]
    == inventory["inventory_sha256"] == discovery["inventory_sha256"],
    "input.verification_sha256": input_manifest["verification_sha256"]
    == sha256(workspace / "verification.k"),
    "generator.generated_tree_sha256": generator_manifest["generated_tree_sha256"]
    == audit["hashes"]["generated_tree_sha256"],
    "generator.obligation_map_sha256": generator_manifest["obligation_map_sha256"]
    == sha256(generated / "obligation-map.json"),
    "generator.provenance.stage1": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == audit["hashes"]["stage1_export_sha256"],
    "generator.provenance.discovery": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == audit["hashes"]["discovery_manifest_sha256"],
    "generator.provenance.inventory": generator_manifest["provenance"][
        "inventory_sha256"
    ]
    == inventory["inventory_sha256"],
    "export.generated_tree_sha256": export_result["generated_tree_sha256"]
    == audit["hashes"]["generated_tree_sha256"],
    "export.discovery_sha256": export_result["stage3_discovery_manifest_sha256"]
    == audit["hashes"]["discovery_manifest_sha256"],
    "preflight.equals_audit_input": preflight == audit["stage4_preflight"],
    "target.generator_manifest_matches_files": generator_manifest["target"]
    == target,
    "target.audit_input_matches_files": audit["target"] == target,
}

result = {
    "inventory_count": len(inventory["rules"]),
    "independent_classification": classification,
    "classification_mismatches": [
        item for item in classification if not item["classification_matches"]
    ],
    "simplification_attribute_rules": [
        item["source_rule_id"]
        for item, rule in zip(classification, inventory["rules"], strict=True)
        if "simplification" in rule["attributes"]
    ],
    "independent_domain_rule_ids": DOMAIN_IDS,
    "independent_domain_count": len(DOMAIN_IDS),
    "recorded_domain_rule_ids": [
        rule["source_rule_id"]
        for rule in discovery["rules"]
        if rule["classification"] == "DOMAIN_LEMMA"
    ],
    "stage4": {
        "recorded_status": export_result["status"],
        "manifest_obligation_count": generator_manifest["obligation_count"],
        "actual_source_rule_ids": actual_source_rule_ids,
        "actual_obligation_ids": actual_obligation_ids,
        "actual_target": target,
        "recorded_classification_bijection": actual_source_rule_ids
        == actual_obligation_ids
        == [],
        "independent_classification_bijection": actual_source_rule_ids
        == actual_obligation_ids
        == DOMAIN_IDS,
        "mathematical_judgment": (
            "KLEAN_NO_OBLIGATIONS is invalid because the independently "
            "classified domain set contains both operational bridge rules."
        ),
    },
    "manifest_field_checks": field_checks,
    "all_manifest_field_checks_pass": all(field_checks.values()),
    "candidate_present": Path("/candidate").exists(),
    "audit_mode": audit["mode"],
}
print(json.dumps(result, indent=2, sort_keys=True))
