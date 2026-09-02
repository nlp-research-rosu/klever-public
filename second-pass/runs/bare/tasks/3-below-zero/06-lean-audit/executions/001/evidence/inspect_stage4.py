#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target/hash checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    classified = validate_trust_boundary(WORKSPACE, DISCOVERY)
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    trust_inventory = json.loads(
        (GENERATION / "trust-inventory.json").read_text()
    )
    recorded_preflight = json.loads(
        (GENERATION / "preflight.json").read_text()
    )
    toolchain_lock = json.loads(
        Path("/reference/klean-toolchain.lock.json").read_text()
    )
    audit_input = json.loads(Path("/audit-input.json").read_text())
    audit_resolution = audit_input["resolution"]
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )

    independently_classified_domain_ids: list[str] = []
    mapped_source_ids = [
        rule["source_rule_id"] for rule in obligation_map["source_rules"]
    ]
    obligation_ids = [
        obligation["source_rule_id"]
        for obligation in obligation_map["obligations"]
    ]
    target = klean_export.target_statement(GENERATED)
    lemmas_text = (
        GENERATED / "Klean3BelowZero" / "Lemmas.lean"
    ).read_text()
    declaration_lines = [
        line.strip()
        for line in lemmas_text.splitlines()
        if re.match(
            r"\\s*(?:def|theorem|lemma|axiom|opaque)\\s+", line
        )
    ]
    expected_target_definition = klean_export.expected_target_definition(
        obligation_map
    )
    stage1_tree = klean_export.tree_digest(WORKSPACE)
    discovery_hash = sha256(DISCOVERY)
    generated_tree = klean_export.tree_digest(GENERATED)
    expected_domain_rules = klean_export._domain_source_rules(
        classified, discovery_hash
    )

    checks = {
        "input_frozen_hash": (
            input_manifest["frozen_input_sha256"] == stage1_tree
        ),
        "input_stage1_hash": (
            input_manifest["stage1_workspace_sha256"] == stage1_tree
        ),
        "inventory_hash_input_manifest": (
            inventory["inventory_sha256"]
            == input_manifest["inventory_sha256"]
        ),
        "discovery_hash_input_manifest": (
            discovery_hash
            == input_manifest["stage3_discovery_manifest_sha256"]
        ),
        "verification_hash_input_manifest": (
            sha256(WORKSPACE / "verification.k")
            == input_manifest["verification_sha256"]
        ),
        "generated_tree_hash_manifest": (
            generated_tree
            == generator_manifest["generated_tree_sha256"]
        ),
        "obligation_map_hash_manifest": (
            sha256(GENERATED / "obligation-map.json")
            == generator_manifest["obligation_map_sha256"]
        ),
        "domain_ids_input_manifest": (
            independently_classified_domain_ids
            == [
                rule["source_rule_id"]
                for rule in input_manifest["source_rules"]
            ]
        ),
        "input_definition_partition_exact": (
            input_manifest["definitions"] == classified["definitions"]
        ),
        "input_operational_partition_exact": (
            input_manifest["operational_rules"]
            == classified["operational_rules"]
        ),
        "input_derived_partition_exact": (
            input_manifest["proved_derived_lemmas"]
            == classified["proved_derived_lemmas"]
        ),
        "input_domain_partition_exact": (
            input_manifest["source_rules"] == expected_domain_rules
        ),
        "generator_toolchain_lock_exact": (
            generator_manifest["toolchain"] == toolchain_lock
        ),
        "generator_provenance_stage1": (
            generator_manifest["provenance"]["stage1_workspace_sha256"]
            == stage1_tree
        ),
        "generator_provenance_discovery": (
            generator_manifest["provenance"][
                "stage3_discovery_manifest_sha256"
            ]
            == discovery_hash
        ),
        "generator_provenance_inventory": (
            generator_manifest["provenance"]["inventory_sha256"]
            == inventory["inventory_sha256"]
        ),
        "export_frozen_hash": (
            export_result["frozen_input_sha256"] == stage1_tree
        ),
        "export_discovery_hash": (
            export_result["stage3_discovery_manifest_sha256"]
            == discovery_hash
        ),
        "export_generated_hash": (
            export_result["generated_tree_sha256"] == generated_tree
        ),
        "export_trust_inventory_hash": (
            export_result["trust_inventory_sha256"]
            == sha256(GENERATION / "trust-inventory.json")
        ),
        "audit_preflight_document_exact": (
            audit_resolution["stage4_preflight"] == recorded_preflight
        ),
        "preflight_stage1_hash": (
            recorded_preflight["stage1_workspace_sha256"] == stage1_tree
            and recorded_preflight["frozen_input_sha256"] == stage1_tree
        ),
        "preflight_discovery_hash": (
            recorded_preflight["stage3_discovery_manifest_sha256"]
            == discovery_hash
        ),
        "preflight_generated_hash": (
            recorded_preflight["generated_tree_sha256"] == generated_tree
        ),
        "source_rule_bijection": (
            mapped_source_ids == independently_classified_domain_ids
            and len(mapped_source_ids) == len(set(mapped_source_ids))
        ),
        "obligation_bijection": (
            obligation_ids == independently_classified_domain_ids
            and len(obligation_ids) == len(set(obligation_ids))
        ),
        "zero_obligations_everywhere": (
            not independently_classified_domain_ids
            and not input_manifest["source_rules"]
            and not obligation_map["source_rules"]
            and not obligation_map["obligations"]
            and not obligation_map["trust_parameters"]
            and generator_manifest["obligation_count"] == 0
            and export_result["obligation_count"] == 0
        ),
        "target_absent_everywhere": (
            target is None
            and generator_manifest["target"] is None
            and expected_target_definition is None
            and not declaration_lines
        ),
        "no_candidate": not Path("/candidate").exists(),
        "status_exact": (
            generator_manifest["obligation_count"] == 0
            and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
            and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        ),
    }
    current_tool_hashes = {
        "exporter_sha256": sha256(Path("/reference/tools/klean_export.py")),
        "klean_py_sha256": sha256(Path("/reference/tools/klean.py")),
    }
    recorded_tool_hashes = {
        key: generator_manifest[key] for key in current_tool_hashes
    }
    document = {
        "trusted_classified_counts": {
            "definitions": len(classified["definitions"]),
            "operational_rules": len(classified["operational_rules"]),
            "proved_derived_lemmas": len(
                classified["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(classified["domain_lemmas"]),
        },
        "independent_domain_ids": independently_classified_domain_ids,
        "mapped_source_ids": mapped_source_ids,
        "obligation_ids": obligation_ids,
        "expected_target_definition": expected_target_definition,
        "parsed_target": target,
        "lemmas_declaration_lines": declaration_lines,
        "historical_generator_identity": {
            "generator_image_id": generator_manifest["provenance"][
                "generator_image_id"
            ],
            "audit_image_id": audit_input["audit"]["image_id"],
            "recorded_tool_hashes": recorded_tool_hashes,
            "current_audit_tool_hashes": current_tool_hashes,
            "same_image": (
                generator_manifest["provenance"]["generator_image_id"]
                == audit_input["audit"]["image_id"]
            ),
            "matches_current_audit_tools": (
                recorded_tool_hashes == current_tool_hashes
            ),
            "interpretation": (
                "The source hashes identify the historical generator image; "
                "the audit uses a different trusted image revision."
            ),
        },
        "trust_inventory_allowlist_count": len(
            trust_inventory["allowlist"]
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print(json.dumps(document, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
