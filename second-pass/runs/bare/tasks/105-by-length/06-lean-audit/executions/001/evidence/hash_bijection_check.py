#!/usr/bin/env python3

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.lemma_discovery_contract import validate_trust_boundary


audit_doc = json.loads(Path("/audit-input.json").read_text())
resolution, digest = stage6_resolution_contract.verify_audit_input(audit_doc)
recorded_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

actual_stage1 = {
    path.relative_to("/reference/k-proof").as_posix(): hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
recorded_stage1 = resolution["stage1_source_hashes"]

generation = Path("/reference/klean-generation")
generated = generation / "generated"
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

producer_path = Path("/reference/generation-tools/klean_export.py")
module_name = "generation_time_klean_export"
spec = importlib.util.spec_from_file_location(module_name, producer_path)
producer = importlib.util.module_from_spec(spec)
sys.modules[module_name] = producer
assert spec.loader is not None
spec.loader.exec_module(producer)
discovery_hash = observed_hashes["discovery_manifest_sha256"]
producer_source_rules = producer._domain_source_rules(
    validated, discovery_hash
)

sidecar_pairs = {
    "input.frozen_input_sha256": (
        input_manifest["frozen_input_sha256"],
        observed_hashes["stage1_export_sha256"],
    ),
    "input.stage1_workspace_sha256": (
        input_manifest["stage1_workspace_sha256"],
        observed_hashes["stage1_export_sha256"],
    ),
    "input.stage3_discovery_manifest_sha256": (
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    "input.verification_sha256": (
        input_manifest["verification_sha256"],
        hashlib.sha256(
            Path("/reference/k-proof/verification.k").read_bytes()
        ).hexdigest(),
    ),
    "generator.generated_tree_sha256": (
        generator_manifest["generated_tree_sha256"],
        observed_hashes["generated_tree_sha256"],
    ),
    "generator.obligation_map_sha256": (
        generator_manifest["obligation_map_sha256"],
        hashlib.sha256(
            (generated / "obligation-map.json").read_bytes()
        ).hexdigest(),
    ),
    "export.generated_tree_sha256": (
        export_result["generated_tree_sha256"],
        observed_hashes["generated_tree_sha256"],
    ),
    "export.frozen_input_sha256": (
        export_result["frozen_input_sha256"],
        observed_hashes["stage1_export_sha256"],
    ),
    "export.stage3_discovery_manifest_sha256": (
        export_result["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    "export.trust_inventory_sha256": (
        export_result["trust_inventory_sha256"],
        hashlib.sha256(
            (generation / "trust-inventory.json").read_bytes()
        ).hexdigest(),
    ),
}

document = {
    "audit_envelope_digest": {
        "recorded": audit_doc["resolved_input_sha256"],
        "observed": digest,
        "match": audit_doc["resolved_input_sha256"] == digest,
    },
    "resolution_hashes": {
        name: {
            "recorded": recorded_hashes[name],
            "observed": value,
            "match": recorded_hashes[name] == value,
        }
        for name, value in observed_hashes.items()
    },
    "all_resolution_hashes_match": all(
        recorded_hashes[name] == value
        for name, value in observed_hashes.items()
    ),
    "stage1_source_hashes": {
        "observed_count": len(actual_stage1),
        "recorded_count": len(recorded_stage1),
        "missing": sorted(set(recorded_stage1) - set(actual_stage1)),
        "extra": sorted(set(actual_stage1) - set(recorded_stage1)),
        "mismatches": sorted(
            name
            for name in set(actual_stage1) & set(recorded_stage1)
            if actual_stage1[name] != recorded_stage1[name]
        ),
        "all_match": actual_stage1 == recorded_stage1,
    },
    "sidecar_hashes": {
        name: {
            "recorded": pair[0],
            "observed": pair[1],
            "match": pair[0] == pair[1],
        }
        for name, pair in sidecar_pairs.items()
    },
    "all_sidecar_hashes_match": all(
        recorded == observed for recorded, observed in sidecar_pairs.values()
    ),
    "generator_toolchain_equals_lock": (
        generator_manifest["toolchain"] == toolchain_lock
    ),
    "inventory_hash_consistent": (
        input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
        == validated["inventory_sha256"]
    ),
    "bijection_and_target": {
        "independent_domain_ids": [
            rule["source_rule_id"] for rule in validated["domain_lemmas"]
        ],
        "producer_domain_ids": [
            rule["source_rule_id"] for rule in producer_source_rules
        ],
        "input_manifest_source_ids": [
            rule["source_rule_id"] for rule in input_manifest["source_rules"]
        ],
        "obligation_map_source_ids": [
            rule["source_rule_id"]
            for rule in obligation_map["source_rules"]
        ],
        "obligation_ids": [
            obligation["source_rule_id"]
            for obligation in obligation_map["obligations"]
        ],
        "unique_obligation_ids": len(
            {
                obligation["source_rule_id"]
                for obligation in obligation_map["obligations"]
            }
        )
        == len(obligation_map["obligations"]),
        "trust_parameters": obligation_map["trust_parameters"],
        "producer_expected_target_definition": (
            producer.expected_target_definition(obligation_map)
        ),
        "producer_observed_target": producer.target_statement(generated),
        "current_checker_expected_target_definition": (
            klean_export.expected_target_definition(obligation_map)
        ),
        "current_checker_observed_target": (
            klean_export.target_statement(generated)
        ),
        "generator_target": generator_manifest["target"],
        "audit_target": resolution["target"],
        "raw_target_declaration_count": sum(
            source.read_text().count("def targetStatement")
            for source in generated.rglob("*.lean")
        ),
    },
    "generation_time_producer": {
        "producer_sha256": hashlib.sha256(
            producer_path.read_bytes()
        ).hexdigest(),
        "producer_tree_digest_generated": producer.tree_digest(generated),
    },
    "mode_shape": {
        "env_mode": os.environ.get("AUDIT_MODE"),
        "recorded_mode": resolution["mode"],
        "candidate_exists": Path("/candidate").exists(),
        "lean_paths_are_null": (
            resolution["lean_workspace"] is None
            and resolution["lean_invocation"] is None
        ),
        "stage5_result_is_null": resolution["stage5_result"] is None,
        "target_is_null": resolution["target"] is None,
    },
}

print(json.dumps(document, indent=2, sort_keys=True))
