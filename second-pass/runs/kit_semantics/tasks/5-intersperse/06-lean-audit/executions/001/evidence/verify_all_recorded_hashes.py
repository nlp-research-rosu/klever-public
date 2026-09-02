#!/usr/bin/env python3
import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def regular_files(root):
    root = Path(root)
    result = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[path.relative_to(root).as_posix()] = sha256_file(path)
            else:
                raise RuntimeError(f"unsafe tree entry: {path}")
    return dict(sorted(result.items()))


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, signed_digest = verify_audit_input(audit_input)
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

discovery = json.loads(discovery_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory = json.loads(
    (generation / "trust-inventory.json").read_text()
)
preflight = json.loads((generation / "preflight.json").read_text())
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)
source_manifest = json.loads((producer / "source-manifest.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
validated = validate_trust_boundary(workspace, discovery_path)
inventory = inventory_verification(workspace)

stage1_actual_files = regular_files(workspace)
stage1_expected_files = resolution["stage1_source_hashes"]
stage1_missing = sorted(set(stage1_expected_files) - set(stage1_actual_files))
stage1_extra = sorted(set(stage1_actual_files) - set(stage1_expected_files))
stage1_mismatches = {
    name: {
        "expected": stage1_expected_files[name],
        "actual": stage1_actual_files[name],
    }
    for name in sorted(set(stage1_actual_files) & set(stage1_expected_files))
    if stage1_actual_files[name] != stage1_expected_files[name]
}

hash_checks = {
    "signed_resolution": {
        "actual": canonical_json_sha256(resolution),
        "expected": signed_digest,
    },
    "stage1_full_tree": {
        "actual": pipeline_contract.sha256_tree(workspace),
        "expected": resolution["hashes"]["k_workspace_sha256"],
    },
    "stage1_export_tree": {
        "actual": klean_export.tree_digest(workspace),
        "expected": resolution["hashes"]["stage1_export_sha256"],
    },
    "stage2_full_tree": {
        "actual": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
        "expected": resolution["hashes"]["k_audit_sha256"],
    },
    "discovery_file": {
        "actual": sha256_file(discovery_path),
        "expected": resolution["hashes"]["discovery_manifest_sha256"],
    },
    "generation_full_tree": {
        "actual": pipeline_contract.sha256_tree(generation),
        "expected": resolution["hashes"]["klean_generation_sha256"],
    },
    "generated_export_tree": {
        "actual": klean_export.tree_digest(generated),
        "expected": resolution["hashes"]["generated_tree_sha256"],
    },
    "producer_full_tree": {
        "actual": pipeline_contract.sha256_tree(producer),
        "expected": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
    },
    "producer_klean_export": {
        "actual": sha256_file(producer / "klean_export.py"),
        "expected": generator_manifest["exporter_sha256"],
    },
    "producer_klean": {
        "actual": sha256_file(producer / "klean.py"),
        "expected": generator_manifest["klean_py_sha256"],
    },
    "verification": {
        "actual": sha256_file(workspace / "verification.k"),
        "expected": input_manifest["verification_sha256"],
    },
    "inventory": {
        "actual": inventory["inventory_sha256"],
        "expected": input_manifest["inventory_sha256"],
    },
    "obligation_map": {
        "actual": sha256_file(generated / "obligation-map.json"),
        "expected": generator_manifest["obligation_map_sha256"],
    },
    "trust_inventory": {
        "actual": sha256_file(generation / "trust-inventory.json"),
        "expected": export_result["trust_inventory_sha256"],
    },
}

actual_stage1_export = hash_checks["stage1_export_tree"]["actual"]
actual_discovery = hash_checks["discovery_file"]["actual"]
actual_generated = hash_checks["generated_export_tree"]["actual"]

cross_manifest_hash_checks = {
    "input_frozen": input_manifest["frozen_input_sha256"]
    == actual_stage1_export,
    "input_stage1": input_manifest["stage1_workspace_sha256"]
    == actual_stage1_export,
    "input_discovery": input_manifest["stage3_discovery_manifest_sha256"]
    == actual_discovery,
    "generator_stage1": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == actual_stage1_export,
    "generator_discovery": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == actual_discovery,
    "generator_inventory": generator_manifest["provenance"][
        "inventory_sha256"
    ]
    == inventory["inventory_sha256"],
    "generator_generated": generator_manifest["generated_tree_sha256"]
    == actual_generated,
    "export_frozen": export_result["frozen_input_sha256"]
    == actual_stage1_export,
    "export_discovery": export_result["stage3_discovery_manifest_sha256"]
    == actual_discovery,
    "export_generated": export_result["generated_tree_sha256"]
    == actual_generated,
    "preflight_frozen": preflight["frozen_input_sha256"]
    == actual_stage1_export,
    "preflight_stage1": preflight["stage1_workspace_sha256"]
    == actual_stage1_export,
    "preflight_discovery": preflight["stage3_discovery_manifest_sha256"]
    == actual_discovery,
    "preflight_generated": preflight["generated_tree_sha256"]
    == actual_generated,
}

expected_definition_documents = validated["definitions"]
independently_reclassified_domain_ids = []
mapped_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
target_statement = klean_export.target_statement(generated)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)

preflight_transcript = Path(
    "/audit-output/evidence/34_required_check_generation_success.txt"
).read_text()
returned_evidence = json.loads(
    preflight_transcript.split("RETURNED_EVIDENCE_JSON\n", 1)[1]
)

producer_image_key = generator_manifest["provenance"][
    "generator_image_id"
].removeprefix("sha256:")

result = {
    "stage1_per_file_hashes": {
        "expected_count": len(stage1_expected_files),
        "actual_count": len(stage1_actual_files),
        "missing": stage1_missing,
        "extra": stage1_extra,
        "mismatches": stage1_mismatches,
        "all_match": (
            not stage1_missing
            and not stage1_extra
            and not stage1_mismatches
        ),
    },
    "hash_checks": {
        name: {
            **values,
            "match": values["actual"] == values["expected"],
        }
        for name, values in hash_checks.items()
    },
    "all_primary_hash_checks_match": all(
        values["actual"] == values["expected"]
        for values in hash_checks.values()
    ),
    "cross_manifest_hash_checks": cross_manifest_hash_checks,
    "all_cross_manifest_hash_checks_match": all(
        cross_manifest_hash_checks.values()
    ),
    "classification_to_generation": {
        "input_definitions_match_validated_inventory": (
            input_manifest["definitions"] == expected_definition_documents
        ),
        "input_operational_rules_match": (
            input_manifest["operational_rules"]
            == validated["operational_rules"]
        ),
        "input_proved_derived_lemmas_match": (
            input_manifest["proved_derived_lemmas"]
            == validated["proved_derived_lemmas"]
        ),
        "independently_reclassified_domain_ids": (
            independently_reclassified_domain_ids
        ),
        "input_source_rule_ids": [
            value["source_rule_id"]
            for value in input_manifest["source_rules"]
        ],
        "obligation_map_source_rule_ids": [
            value["source_rule_id"]
            for value in obligation_map["source_rules"]
        ],
        "mapped_obligation_ids": mapped_ids,
        "mapped_ids_unique": len(mapped_ids) == len(set(mapped_ids)),
        "exact_ordered_bijection": (
            independently_reclassified_domain_ids
            == [
                value["source_rule_id"]
                for value in input_manifest["source_rules"]
            ]
            == [
                value["source_rule_id"]
                for value in obligation_map["source_rules"]
            ]
            == mapped_ids
        ),
        "obligation_count_fields": {
            "obligation_map": len(obligation_map["obligations"]),
            "generator_manifest": generator_manifest["obligation_count"],
            "export_result": export_result["obligation_count"],
            "preflight": preflight["obligation_count"],
            "audit_input_preflight": resolution["stage4_preflight"][
                "obligation_count"
            ],
        },
        "trust_parameters": obligation_map["trust_parameters"],
    },
    "target_identity": {
        "expected_target_definition": expected_target_definition,
        "trusted_parser_target_statement": target_statement,
        "generator_manifest_target": generator_manifest["target"],
        "preflight_target": preflight["target"],
        "audit_input_target": resolution["target"],
        "audit_input_preflight_target": resolution["stage4_preflight"][
            "target"
        ],
        "all_absent": all(
            value is None
            for value in (
                expected_target_definition,
                target_statement,
                generator_manifest["target"],
                preflight["target"],
                resolution["target"],
                resolution["stage4_preflight"]["target"],
            )
        ),
    },
    "producer_and_toolchain_identity": {
        "source_manifest_files_match_actual": source_manifest["files"]
        == {
            "klean_export.py": sha256_file(producer / "klean_export.py"),
            "klean.py": sha256_file(producer / "klean.py"),
        },
        "source_manifest_image_matches_generator": (
            source_manifest["generator_image_id"]
            == generator_manifest["provenance"]["generator_image_id"]
        ),
        "audit_input_path_image_key_matches": (
            Path(resolution["generation_producer_sources"]).name
            == producer_image_key
        ),
        "generator_toolchain_matches_trusted_lock": (
            generator_manifest["toolchain"] == toolchain_lock
        ),
    },
    "preflight_reproduction": {
        "returned_evidence_equals_stage4_preflight": (
            returned_evidence == preflight
        ),
        "returned_evidence_equals_audit_input_preflight": (
            returned_evidence == resolution["stage4_preflight"]
        ),
        "recorded_build_output_hash": preflight["diagnostics"][1][
            "output_sha256"
        ],
        "reproduced_build_output_hash": returned_evidence["diagnostics"][1][
            "output_sha256"
        ],
    },
    "no_proof_mode_artifacts": {
        "audit_mode": resolution["mode"],
        "candidate_exists": Path("/candidate").exists(),
        "lean_workspace_hash": resolution["hashes"][
            "lean_workspace_sha256"
        ],
        "lean_invocation_hash": resolution["hashes"][
            "lean_invocation_sha256"
        ],
        "stage5_result": resolution["stage5_result"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
