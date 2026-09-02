#!/usr/bin/env python3
"""Read-only independent reconstruction and provenance checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import (
    klean_audit_contract,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
)
from tools.k_rule_inventory import inventory_verification


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_input_sha256 = (
    klean_audit_contract.verify_stage6_audit_input(audit_document)
)
recorded_hashes = resolution["hashes"]

require(
    os.environ.get("AUDIT_MODE") == resolution["mode"],
    "AUDIT_MODE differs from /audit-input.json",
)
require(resolution["mode"] == "CLASSIFICATION_ONLY", "unexpected audit mode")
require(resolution["stage5_result"] is None, "classification-only has Stage 5 result")
require(resolution["lean_workspace"] is None, "classification-only has Lean workspace")
require(resolution["lean_invocation"] is None, "classification-only has Lean invocation")
require(not Path("/candidate").exists(), "classification-only unexpectedly mounted /candidate")

stage1_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 workspace"
    )
}
require(
    stage1_source_hashes == resolution["stage1_source_hashes"],
    "Stage 1 per-file hashes differ from audit input",
)

observed_trees = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
require(observed_trees == recorded_hashes, "mounted tree/file hashes differ from audit input")

inventory = inventory_verification(K_WORKSPACE)
discovery_document = json.loads(DISCOVERY.read_text())
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery_document["rules"]]
require(
    classified_ids == canonical_ids,
    "Stage 3 identities are omitted, duplicated, added, or reordered",
)
require(
    len(classified_ids) == len(set(classified_ids)),
    "Stage 3 has duplicate source_rule_id",
)
require(
    discovery_document["inventory_sha256"] == inventory["inventory_sha256"],
    "Stage 3 inventory hash differs",
)
validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY
)

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
trust_inventory_path = GENERATION / "trust-inventory.json"
recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
require(
    generator_manifest["toolchain"] == toolchain_lock,
    "generator toolchain differs from trusted lock",
)
require(
    generator_manifest["generated_tree_sha256"]
    == observed_trees["generated_tree_sha256"],
    "generator manifest generated-tree hash differs",
)
require(
    generator_manifest["provenance"]["stage1_workspace_sha256"]
    == observed_trees["stage1_export_sha256"],
    "generator Stage 1 provenance differs",
)
require(
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == observed_trees["discovery_manifest_sha256"],
    "generator Stage 3 provenance differs",
)
require(
    generator_manifest["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"],
    "generator inventory provenance differs",
)
require(
    input_manifest["frozen_input_sha256"]
    == observed_trees["stage1_export_sha256"]
    and input_manifest["stage1_workspace_sha256"]
    == observed_trees["stage1_export_sha256"],
    "input manifest Stage 1 hashes differ",
)
require(
    input_manifest["stage3_discovery_manifest_sha256"]
    == observed_trees["discovery_manifest_sha256"],
    "input manifest Stage 3 hash differs",
)
require(
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
    "input manifest inventory hash differs",
)
require(
    input_manifest["verification_sha256"] == sha256(K_WORKSPACE / "verification.k"),
    "input manifest verification.k hash differs",
)
require(
    export_result["frozen_input_sha256"]
    == observed_trees["stage1_export_sha256"]
    and export_result["stage3_discovery_manifest_sha256"]
    == observed_trees["discovery_manifest_sha256"]
    and export_result["generated_tree_sha256"]
    == observed_trees["generated_tree_sha256"]
    and export_result["trust_inventory_sha256"] == sha256(trust_inventory_path),
    "export-result hash binding differs",
)
require(
    resolution["stage4_preflight"] == recorded_preflight,
    "audit input does not embed the selected Stage 4 preflight exactly",
)
require(
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == observed_trees["klean_generation_sha256"]
    and resolution["selections"]["k_audit"]["artifact_sha256"]
    == observed_trees["k_audit_sha256"],
    "selection artifact hash differs",
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(
        PRODUCERS, "mounted Stage 4 producer source bundle"
    )
)
require(
    producer_names == ["klean.py", "klean_export.py", "source-manifest.json"],
    "producer source bundle has missing or unexpected files",
)
require(
    set(source_manifest) == {"schema_version", "generator_image_id", "files"}
    and source_manifest["schema_version"] == 1,
    "producer source manifest shape/version differs",
)
producer_hashes = {
    "klean_export.py": sha256(PRODUCERS / "klean_export.py"),
    "klean.py": sha256(PRODUCERS / "klean.py"),
}
image_id = generator_manifest["provenance"]["generator_image_id"]
require(
    producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"],
    "mounted klean_export.py differs from generator manifest",
)
require(
    producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"],
    "mounted klean.py differs from generator manifest",
)
require(source_manifest["files"] == producer_hashes, "source manifest hashes differ")
require(
    source_manifest["generator_image_id"] == image_id,
    "source manifest image differs from generator manifest",
)
require(
    Path(resolution["generation_producer_sources"]).name
    == image_id.removeprefix("sha256:"),
    "audit-input producer path does not encode generator image ID",
)
require(
    resolution["hashes"]["generation_producer_sources_sha256"]
    == observed_trees["generation_producer_sources_sha256"],
    "audit-input producer bundle tree hash differs",
)

obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
discovery_sha256 = sha256(DISCOVERY)
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_sha256
)
require(
    input_manifest["source_rules"] == expected_source_rules,
    "input manifest source rules differ from classified domain rules",
)
require(
    obligation_map["source_rules"] == expected_source_rules,
    "obligation-map source rules differ from classified domain rules",
)
expected_ids = [entry["source_rule_id"] for entry in expected_source_rules]
observed_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
require(
    observed_ids == expected_ids and len(observed_ids) == len(set(observed_ids)),
    "source-rule/obligation identity bijection fails",
)
require(
    generator_manifest["obligation_count"] == len(obligation_map["obligations"]),
    "generator obligation count differs",
)
require(
    generator_manifest["obligation_map_sha256"] == sha256(obligation_map_path),
    "obligation-map hash differs",
)
target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(obligation_map)
require(target == generator_manifest["target"], "generated target differs from manifest")
require(target == resolution["target"], "generated target differs from audit input")
require(target is None, "zero-obligation generation unexpectedly has a target")
require(expected_target_definition is None, "empty obligations yield a target definition")
require(not expected_source_rules, "recorded domain source-rule set is nonempty")
require(not obligation_map["obligations"], "recorded obligation set is nonempty")
require(not obligation_map["trust_parameters"], "empty obligation map has trust parameters")

rerun_preflight_path = Path("/audit-output/evidence/preflight-return.json")
for diagnostic in recorded_preflight["diagnostics"]:
    require(
        hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest()
        == diagnostic["output_sha256"],
        "recorded preflight output hash cannot be reproduced from preserved output",
    )
rerun_preflight = (
    json.loads(rerun_preflight_path.read_text())
    if rerun_preflight_path.is_file()
    else None
)
diagnostic_hash_comparison = None
if rerun_preflight is not None:
    recorded_diagnostics = recorded_preflight["diagnostics"]
    rerun_diagnostics = rerun_preflight["diagnostics"]
    require(
        [entry["command"] for entry in recorded_diagnostics]
        == [entry["command"] for entry in rerun_diagnostics]
        and [entry["exit_code"] for entry in recorded_diagnostics]
        == [entry["exit_code"] for entry in rerun_diagnostics],
        "rerun preflight commands or exit codes differ",
    )

    def normalized_build_lines(text: str) -> list[str]:
        return sorted(
            re.sub(r"(?<=\[)\d+(?=/\d+\])", "#", line)
            for line in text.splitlines()
        )

    diagnostic_hash_comparison = [
        {
            "command": recorded["command"],
            "recorded_output_sha256": recorded["output_sha256"],
            "recorded_output_hash_verified_from_preserved_output": True,
            "rerun_output_sha256": rerun["output_sha256"],
            "exact_hash_match": (
                recorded["output_sha256"] == rerun["output_sha256"]
            ),
            "normalized_line_multiset_equal": normalized_build_lines(
                recorded["output_tail"]
            )
            == normalized_build_lines(rerun["output_tail"]),
        }
        for recorded, rerun in zip(
            recorded_diagnostics, rerun_diagnostics, strict=True
        )
    ]

result = {
    "audit_mode": os.environ.get("AUDIT_MODE"),
    "audit_input_contract": "PASS",
    "resolved_input_sha256_recomputed": resolved_input_sha256,
    "resolved_input_sha256_recorded": audit_document["resolved_input_sha256"],
    "stage1_source_hashes_match": True,
    "observed_hashes": observed_trees,
    "producer_provenance": {
        "generator_image_id": image_id,
        "audit_input_bundle_path_basename": Path(
            resolution["generation_producer_sources"]
        ).name,
        "files": producer_hashes,
        "bundle_files": producer_names,
        "source_manifest_matches": True,
        "generator_manifest_matches": True,
    },
    "inventory": inventory,
    "stage3": {
        "manifest_sha256": discovery_sha256,
        "ordered_bijection": True,
        "classified_ids": classified_ids,
        "classifications": [
            {
                "source_rule_id": entry["source_rule_id"],
                "classification": entry["classification"],
            }
            for entry in discovery_document["rules"]
        ],
        "validated_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
    },
    "stage4": {
        "manifest_hash_bindings": "PASS",
        "expected_source_rules": expected_source_rules,
        "obligation_source_ids": observed_ids,
        "obligation_bijection": True,
        "obligation_map_sha256": sha256(obligation_map_path),
        "target": target,
        "expected_target_definition": expected_target_definition,
        "preflight_diagnostic_hash_comparison": diagnostic_hash_comparison,
    },
    "stage5_absence": {
        "candidate_exists": Path("/candidate").exists(),
        "stage5_result": resolution["stage5_result"],
        "lean_workspace": resolution["lean_workspace"],
        "lean_invocation": resolution["lean_invocation"],
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
