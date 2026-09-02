#!/usr/bin/env python3
"""Re-hash frozen inputs and independently audit the zero-obligation export."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.lemma_discovery_contract import validate_trust_boundary


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


audit_input = load("/audit-input.json")
resolution = audit_input["resolution"]
recorded_hashes = resolution["hashes"]
generator = load("/reference/klean-generation/generator-manifest.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
preflight = load("/reference/klean-generation/preflight.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
discovery = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)

computed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
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

stage1_source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): (
        pipeline_contract.sha256_file(path)
    )
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}

producer_hashes = {
    name: hashlib.sha256(
        (Path("/reference/generation-tools") / name).read_bytes()
    ).hexdigest()
    for name in ("klean.py", "klean_export.py")
}
generator_image_id = generator["provenance"]["generator_image_id"]
recorded_bundle_component = Path(
    resolution["generation_producer_sources"]
).name

domain_source_rules = klean_export._domain_source_rules(
    discovery, computed_hashes["discovery_manifest_sha256"]
)
obligations = obligation_map.get("obligations")
obligation_ids = [
    item.get("source_rule_id") for item in obligations
] if isinstance(obligations, list) else None
domain_ids = [item["source_rule_id"] for item in domain_source_rules]

expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
observed_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)

checks = {
    "resolved_input_digest_exact": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
        == audit_input["resolved_input_sha256"]
    ),
    "all_recorded_mounted_hashes_exact": all(
        computed_hashes[key] == value
        for key, value in recorded_hashes.items()
        if key in computed_hashes
    ),
    "recorded_mounted_hash_comparisons": {
        key: {
            "recorded": recorded_hashes.get(key),
            "computed": value,
            "exact": recorded_hashes.get(key) == value,
        }
        for key, value in computed_hashes.items()
    },
    "stage1_source_file_set_and_hashes_exact": (
        stage1_source_hashes == resolution["stage1_source_hashes"]
    ),
    "stage1_source_file_count": len(stage1_source_hashes),
    "producer_file_hashes": producer_hashes,
    "producer_hashes_match_source_manifest": (
        producer_hashes == source_manifest["files"]
    ),
    "producer_hashes_match_generator_manifest": (
        producer_hashes["klean.py"] == generator["klean_py_sha256"]
        and producer_hashes["klean_export.py"]
        == generator["exporter_sha256"]
    ),
    "generator_image_matches_source_manifest": (
        generator_image_id == source_manifest["generator_image_id"]
    ),
    "generator_image_matches_audit_bundle_path": (
        generator_image_id == f"sha256:{recorded_bundle_component}"
    ),
    "toolchain_lock_exact": (
        generator["toolchain"]
        == load("/reference/klean-toolchain.lock.json")
    ),
    "independent_domain_rule_count": len(domain_source_rules),
    "input_manifest_source_rules_exact": (
        input_manifest.get("source_rules") == domain_source_rules
    ),
    "obligation_map_source_rules_exact": (
        obligation_map.get("source_rules") == domain_source_rules
    ),
    "source_rule_obligation_ids_same_order": obligation_ids == domain_ids,
    "obligation_ids_unique": (
        isinstance(obligation_ids, list)
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "trust_parameters_empty": obligation_map.get("trust_parameters") == [],
    "obligation_map_hash_exact": (
        hashlib.sha256(
            Path(
                "/reference/klean-generation/generated/obligation-map.json"
            ).read_bytes()
        ).hexdigest()
        == generator["obligation_map_sha256"]
    ),
    "expected_target_definition": expected_target_definition,
    "observed_target": observed_target,
    "all_recorded_targets_null": all(
        item is None
        for item in (
            generator.get("target"),
            preflight.get("target"),
            resolution.get("target"),
            resolution.get("stage4_preflight", {}).get("target"),
            observed_target,
            expected_target_definition,
        )
    ),
    "all_zero_obligation_counts": all(
        count == 0
        for count in (
            generator.get("obligation_count"),
            export_result.get("obligation_count"),
            preflight.get("obligation_count"),
            resolution.get("stage4_preflight", {}).get("obligation_count"),
            len(obligations) if isinstance(obligations, list) else None,
        )
    ),
    "all_zero_obligation_statuses": all(
        status == "KLEAN_NO_OBLIGATIONS"
        for status in (
            export_result.get("status"),
            preflight.get("status"),
            resolution["selections"]["klean_generation"].get("status"),
            resolution.get("stage4_preflight", {}).get("status"),
        )
    ),
    "audit_mode_classification_only": (
        resolution.get("mode") == "CLASSIFICATION_ONLY"
    ),
    "no_candidate_recorded": (
        resolution.get("lean_workspace") is None
        and resolution.get("lean_invocation") is None
        and resolution.get("stage5_result") is None
    ),
}

print(json.dumps(checks, indent=2, sort_keys=True))
