#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and target audit for Stage 4."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import canonical_json_sha256


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution = audit_document["resolution"]
    hashes = resolution["hashes"]
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    recorded_preflight = json.loads(
        (GENERATION / "preflight.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    trust_inventory = json.loads(
        (GENERATION / "trust-inventory.json").read_text()
    )
    toolchain_lock = json.loads(LOCK.read_text())
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )

    actual_hashes = {
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
        "k_audit_sha256": sha256_tree(K_AUDIT),
        "k_workspace_sha256": sha256_tree(WORKSPACE),
        "klean_generation_sha256": sha256_tree(GENERATION),
        "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
    }
    for name, actual in actual_hashes.items():
        assert hashes[name] == actual, (name, hashes[name], actual)
    assert hashes["lean_invocation_sha256"] is None
    assert hashes["lean_workspace_sha256"] is None

    assert canonical_json_sha256(resolution) == audit_document[
        "resolved_input_sha256"
    ]
    assert resolution["mode"] == os.environ["AUDIT_MODE"] == (
        "CLASSIFICATION_ONLY"
    )
    assert resolution["problem_id"] == "50-decode-shift"
    assert resolution["condition"] == "bare"
    assert resolution["semantics_mode"] == "GENERATED_SEMANTICS"
    assert resolution["target"] is None
    assert resolution["stage5_result"] is None
    assert not Path("/candidate").exists()

    for name, expected in resolution["stage1_source_hashes"].items():
        assert file_sha256(WORKSPACE / name) == expected

    assert resolution["selections"]["k_audit"]["artifact_sha256"] == (
        actual_hashes["k_audit_sha256"]
    )
    assert resolution["selections"]["klean_generation"][
        "artifact_sha256"
    ] == actual_hashes["klean_generation_sha256"]
    assert resolution["selections"]["klean_generation"]["status"] == (
        "KLEAN_NO_OBLIGATIONS"
    )

    producer_hashes = {
        "klean.py": file_sha256(PRODUCERS / "klean.py"),
        "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
    }
    assert producer_hashes == source_manifest["files"]
    assert producer_hashes["klean.py"] == generator_manifest[
        "klean_py_sha256"
    ]
    assert producer_hashes["klean_export.py"] == generator_manifest[
        "exporter_sha256"
    ]
    assert source_manifest["generator_image_id"] == generator_manifest[
        "provenance"
    ]["generator_image_id"]
    assert Path(resolution["generation_producer_sources"]).name == (
        source_manifest["generator_image_id"].removeprefix("sha256:")
    )

    inventory = inventory_verification(WORKSPACE)
    validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
    discovery_hash = actual_hashes["discovery_manifest_sha256"]
    domain_rules = validated["domain_lemmas"]
    expected_source_rules = klean_export._domain_source_rules(
        validated, discovery_hash
    )
    assert domain_rules == []
    assert expected_source_rules == []
    assert len(validated["definitions"]) == 9
    assert validated["operational_rules"] == []
    assert validated["proved_derived_lemmas"] == []

    assert input_manifest["inventory_sha256"] == inventory[
        "inventory_sha256"
    ]
    assert input_manifest["verification_sha256"] == inventory[
        "verification_sha256"
    ]
    assert input_manifest["frozen_input_sha256"] == actual_hashes[
        "stage1_export_sha256"
    ]
    assert input_manifest["stage1_workspace_sha256"] == actual_hashes[
        "stage1_export_sha256"
    ]
    assert input_manifest["stage3_discovery_manifest_sha256"] == (
        discovery_hash
    )
    assert input_manifest["source_rules"] == expected_source_rules
    assert [item["source_rule_id"] for item in input_manifest["definitions"]] == [
        item["source_rule_id"] for item in validated["definitions"]
    ]
    assert input_manifest["operational_rules"] == []
    assert input_manifest["proved_derived_lemmas"] == []

    assert obligation_map == {
        "obligations": [],
        "schema_version": 3,
        "source_rules": [],
        "trust_parameters": [],
    }
    expected_ids = [rule["source_rule_id"] for rule in expected_source_rules]
    observed_ids = [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ]
    assert observed_ids == expected_ids == []
    assert len(observed_ids) == len(set(observed_ids))
    assert generator_manifest["obligation_count"] == len(observed_ids) == 0
    assert file_sha256(GENERATED / "obligation-map.json") == (
        generator_manifest["obligation_map_sha256"]
    )
    assert generator_manifest["generated_tree_sha256"] == actual_hashes[
        "generated_tree_sha256"
    ]
    assert generator_manifest["toolchain"] == toolchain_lock
    assert generator_manifest["provenance"]["stage1_workspace_sha256"] == (
        actual_hashes["stage1_export_sha256"]
    )
    assert generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ] == discovery_hash
    assert generator_manifest["provenance"]["inventory_sha256"] == (
        inventory["inventory_sha256"]
    )

    assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    assert export_result["obligation_count"] == 0
    assert export_result["frozen_input_sha256"] == actual_hashes[
        "stage1_export_sha256"
    ]
    assert export_result["stage3_discovery_manifest_sha256"] == discovery_hash
    assert export_result["generated_tree_sha256"] == actual_hashes[
        "generated_tree_sha256"
    ]
    assert export_result["trust_inventory_sha256"] == file_sha256(
        GENERATION / "trust-inventory.json"
    )
    assert trust_inventory["designated_sorries"] == 0
    assert trust_inventory["other_sorries"] == 0

    assert klean_export.expected_target_definition(obligation_map) is None
    assert klean_export.target_statement(GENERATED) is None
    assert generator_manifest["target"] is None
    assert recorded_preflight["target"] is None
    assert resolution["stage4_preflight"]["target"] is None
    assert recorded_preflight == resolution["stage4_preflight"]
    assert recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    assert recorded_preflight["obligation_count"] == 0

    generated_lean = "\n".join(
        path.read_text()
        for path in sorted(GENERATED.rglob("*.lean"))
    )
    assert re.search(r"(?m)^\s*(?:theorem|lemma)\s+", generated_lean) is None
    assert re.search(r"\b(?:sorry|admit|unsafe)\b", generated_lean) is None

    print(
        json.dumps(
            {
                "actual_hashes": actual_hashes,
                "resolved_input_sha256": audit_document[
                    "resolved_input_sha256"
                ],
                "inventory_sha256": inventory["inventory_sha256"],
                "producer_hashes": producer_hashes,
                "generator_image_id": source_manifest["generator_image_id"],
                "domain_rule_count": len(domain_rules),
                "source_rule_count": len(expected_source_rules),
                "obligation_count": len(observed_ids),
                "source_rule_obligation_bijection": True,
                "vacuous_conjunct_count": 0,
                "target": None,
                "candidate_present": False,
                "selected_status": "KLEAN_NO_OBLIGATIONS",
                "recorded_preflight_matches_launcher": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
