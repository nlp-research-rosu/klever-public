#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.pipeline_contract import sha256_file, sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
recorded_hashes = resolution["hashes"]

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")

observed_hashes = {
    "k_workspace_sha256": sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": sha256_file(discovery),
    "k_audit_sha256": sha256_tree(k_audit),
    "klean_generation_sha256": sha256_tree(generation),
    "generation_producer_sources_sha256": sha256_tree(producer_sources),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

actual_stage1_files = {
    path.relative_to(k_workspace).as_posix(): file_sha256(path)
    for path in sorted(k_workspace.rglob("*"))
    if path.is_file()
}
recorded_stage1_files = resolution["stage1_source_hashes"]

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = json.loads(
    (generation / "trust-inventory.json").read_text()
)
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

independent_domain_rule_ids = []
input_domain_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_domain_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_rule_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

recorded_diagnostic_hash_checks = []
for diagnostic in preflight["diagnostics"]:
    output_tail = diagnostic["output_tail"]
    recorded_diagnostic_hash_checks.append(
        {
            "command": diagnostic["command"],
            "recorded_output_sha256": diagnostic["output_sha256"],
            "stored_output_tail_sha256": hashlib.sha256(
                output_tail.encode()
            ).hexdigest(),
            "stored_tail_is_complete_output": len(output_tail) < 4000,
            "hash_matches_stored_complete_output": (
                len(output_tail) < 4000
                and hashlib.sha256(output_tail.encode()).hexdigest()
                == diagnostic["output_sha256"]
            ),
        }
    )

target_statement = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

checks = {
    "audit_envelope": {
        "verified_resolved_input_sha256": resolved_digest,
        "recorded_resolved_input_sha256": audit_document[
            "resolved_input_sha256"
        ],
        "matches": resolved_digest
        == audit_document["resolved_input_sha256"],
    },
    "recorded_hashes": recorded_hashes,
    "observed_hashes": observed_hashes,
    "all_launcher_hashes_match": observed_hashes == recorded_hashes,
    "selection_hashes": {
        "k_audit_selection": resolution["selections"]["k_audit"][
            "artifact_sha256"
        ],
        "observed_k_audit": observed_hashes["k_audit_sha256"],
        "k_audit_matches": resolution["selections"]["k_audit"][
            "artifact_sha256"
        ]
        == observed_hashes["k_audit_sha256"],
        "generation_selection": resolution["selections"][
            "klean_generation"
        ]["artifact_sha256"],
        "observed_generation": observed_hashes[
            "klean_generation_sha256"
        ],
        "generation_matches": resolution["selections"]["klean_generation"][
            "artifact_sha256"
        ]
        == observed_hashes["klean_generation_sha256"],
    },
    "stage1_source_files": {
        "recorded_count": len(recorded_stage1_files),
        "observed_count": len(actual_stage1_files),
        "missing": sorted(set(recorded_stage1_files) - set(actual_stage1_files)),
        "extra": sorted(set(actual_stage1_files) - set(recorded_stage1_files)),
        "mismatches": {
            name: {
                "recorded": recorded_stage1_files[name],
                "observed": actual_stage1_files.get(name),
            }
            for name in recorded_stage1_files
            if actual_stage1_files.get(name) != recorded_stage1_files[name]
        },
        "exact_match": actual_stage1_files == recorded_stage1_files,
    },
    "sidecar_hashes": {
        "obligation_map_observed": file_sha256(obligation_map_path),
        "obligation_map_manifest": generator_manifest[
            "obligation_map_sha256"
        ],
        "obligation_map_matches": file_sha256(obligation_map_path)
        == generator_manifest["obligation_map_sha256"],
        "trust_inventory_observed": file_sha256(
            generation / "trust-inventory.json"
        ),
        "trust_inventory_export_result": export_result[
            "trust_inventory_sha256"
        ],
        "trust_inventory_matches": file_sha256(
            generation / "trust-inventory.json"
        )
        == export_result["trust_inventory_sha256"],
    },
    "preflight_record_binding": {
        "audit_input_equals_generation_preflight": resolution[
            "stage4_preflight"
        ]
        == preflight,
        "diagnostic_hash_checks": recorded_diagnostic_hash_checks,
    },
    "source_rule_obligation_bijection": {
        "independent_domain_rule_ids": independent_domain_rule_ids,
        "input_manifest_domain_rule_ids": input_domain_rule_ids,
        "obligation_map_source_rule_ids": mapped_domain_rule_ids,
        "obligation_rule_ids": obligation_rule_ids,
        "unique_obligation_rule_ids": len(obligation_rule_ids)
        == len(set(obligation_rule_ids)),
        "all_four_lists_equal": (
            independent_domain_rule_ids
            == input_domain_rule_ids
            == mapped_domain_rule_ids
            == obligation_rule_ids
        ),
        "generator_obligation_count": generator_manifest[
            "obligation_count"
        ],
        "export_obligation_count": export_result["obligation_count"],
        "actual_obligation_count": len(obligation_rule_ids),
    },
    "fixed_target": {
        "computed_target_statement": target_statement,
        "computed_expected_target_definition": expected_target_definition,
        "generator_manifest_target": generator_manifest["target"],
        "audit_input_target": resolution["target"],
        "stage4_preflight_target": resolution["stage4_preflight"]["target"],
        "all_targets_null": all(
            item is None
            for item in (
                target_statement,
                expected_target_definition,
                generator_manifest["target"],
                resolution["target"],
                resolution["stage4_preflight"]["target"],
            )
        ),
    },
    "status_and_candidate": {
        "generation_selection_status": resolution["selections"][
            "klean_generation"
        ]["status"],
        "export_status": export_result["status"],
        "recorded_preflight_status": preflight["status"],
        "candidate_exists": Path("/candidate").exists(),
        "stage5_result": resolution["stage5_result"],
        "lean_workspace": resolution["lean_workspace"],
        "lean_invocation": resolution["lean_invocation"],
    },
    "trust_inventory_counts": {
        "allowlist_count": len(trust_inventory["allowlist"]),
        "axiom_count": len(trust_inventory["axioms"]),
        "designated_sorries": trust_inventory["designated_sorries"],
        "other_sorries": trust_inventory["other_sorries"],
        "recorded_preflight_trust_declaration_count": preflight[
            "trust_declaration_count"
        ],
    },
}

print(json.dumps(checks, indent=2, sort_keys=True))
