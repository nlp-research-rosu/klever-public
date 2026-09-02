#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_file


stage1 = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
recorded_preflight = json.loads((generation / "preflight.json").read_text())
rerun_preflight = json.loads(
    Path("/audit-output/evidence/03_preflight.log").read_text()
)
trust_inventory_path = generation / "trust-inventory.json"
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
validated = validate_trust_boundary(stage1, discovery_path)

domain_rules = validated["domain_lemmas"]
obligations = obligation_map["obligations"]
target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)
source_ids = [rule["source_rule_id"] for rule in domain_rules]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]

definition_text = None
if target is not None:
    source = (generated / target["file"]).read_text()
    start = source.index("def targetStatement")
    end = source.index("\n\nend ", start)
    definition_text = source[start:end].strip()

checks = {
    "stage1_export_hash_input_manifest": (
        tree_digest(stage1) == input_manifest["stage1_workspace_sha256"]
    ),
    "stage1_export_hash_input_manifest_frozen": (
        tree_digest(stage1) == input_manifest["frozen_input_sha256"]
    ),
    "discovery_hash_input_manifest": (
        sha256_file(discovery_path)
        == input_manifest["stage3_discovery_manifest_sha256"]
    ),
    "inventory_hash_input_manifest": (
        validated["inventory_sha256"] == input_manifest["inventory_sha256"]
    ),
    "verification_hash_input_manifest": (
        sha256_file(stage1 / "verification.k")
        == input_manifest["verification_sha256"]
    ),
    "domain_source_rules_input_manifest": (
        input_manifest["source_rules"] == obligation_map["source_rules"]
    ),
    "domain_obligation_id_order": source_ids == obligation_ids,
    "domain_obligation_unique": len(obligation_ids) == len(set(obligation_ids)),
    "obligation_count_generator_manifest": (
        len(obligations) == generator_manifest["obligation_count"]
    ),
    "obligation_count_export_result": (
        len(obligations) == export_result["obligation_count"]
    ),
    "obligation_map_hash": (
        sha256_file(obligation_map_path)
        == generator_manifest["obligation_map_sha256"]
    ),
    "generated_tree_generator_manifest": (
        tree_digest(generated) == generator_manifest["generated_tree_sha256"]
    ),
    "generated_tree_audit_input": (
        tree_digest(generated)
        == resolution["hashes"]["generated_tree_sha256"]
    ),
    "generator_provenance_stage1": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == tree_digest(stage1)
    ),
    "generator_provenance_discovery": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == sha256_file(discovery_path)
    ),
    "generator_provenance_inventory": (
        generator_manifest["provenance"]["inventory_sha256"]
        == validated["inventory_sha256"]
    ),
    "generator_toolchain_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "export_result_stage1_hash": (
        export_result["frozen_input_sha256"] == tree_digest(stage1)
    ),
    "export_result_discovery_hash": (
        export_result["stage3_discovery_manifest_sha256"]
        == sha256_file(discovery_path)
    ),
    "export_result_generated_tree_hash": (
        export_result["generated_tree_sha256"] == tree_digest(generated)
    ),
    "export_result_trust_inventory_hash": (
        export_result["trust_inventory_sha256"]
        == sha256_file(trust_inventory_path)
    ),
    "rerun_preflight_equals_recorded_preflight": (
        rerun_preflight == recorded_preflight
    ),
    "rerun_preflight_equals_audit_input": (
        rerun_preflight == resolution["stage4_preflight"]
    ),
    "target_generator_manifest": target == generator_manifest["target"],
    "target_audit_input": target == resolution["target"],
    "target_recorded_preflight": target == recorded_preflight["target"],
    "target_definition_exact_conjunction": definition_text == expected_definition,
    "target_definition_hash": (
        target is not None
        and sha256_text(definition_text) == target["definition_sha256"]
    ),
    "target_statement_hash": (
        target is not None
        and sha256_text(target["statement"]) == target["statement_sha256"]
    ),
}

obligation_checks = []
for rule, obligation in zip(domain_rules, obligations, strict=True):
    obligation_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "source_span_match": obligation["source_span"]
            == {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "normalized_sha256_match": (
                obligation["normalized_sha256"]
                == rule["normalized_sha256"]
            ),
            "inventory_sha256_match": (
                obligation["inventory_sha256"]
                == validated["inventory_sha256"]
            ),
            "discovery_manifest_sha256_match": (
                obligation["discovery_manifest_sha256"]
                == sha256_file(discovery_path)
            ),
            "lean_conjunct_sha256_match": (
                obligation["lean_conjunct_sha256"]
                == sha256_text(obligation["lean_conjunct"])
            ),
            "source_text": rule["text"],
            "lean_conjunct": obligation["lean_conjunct"],
        }
    )

result = {
    "checks": checks,
    "domain_source_rule_ids": source_ids,
    "obligation_rule_ids": obligation_ids,
    "obligation_checks": obligation_checks,
    "expected_target_definition": expected_definition,
    "observed_target_definition": definition_text,
    "observed_target": target,
}
result["all_checks_match"] = (
    all(checks.values())
    and all(
        value
        for item in obligation_checks
        for key, value in item.items()
        if key.endswith("_match")
    )
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_checks_match"] else 1)
