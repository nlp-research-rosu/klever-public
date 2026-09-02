#!/usr/bin/env python3
"""Read-only reconstruction and provenance checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    klean_audit_contract,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATION_TOOLS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(label: str, actual: object, expected: object) -> bool:
    matched = actual == expected
    print(
        json.dumps(
            {
                "check": label,
                "actual": actual,
                "expected": expected,
                "match": matched,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return matched


def main() -> int:
    overall = True
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        envelope
    )
    print(
        json.dumps(
            {
                "audit_input_envelope": "VALID",
                "resolved_input_sha256": resolved_digest,
            },
            sort_keys=True,
        )
    )
    overall &= report(
        "AUDIT_MODE matches signed mode",
        os.environ.get("AUDIT_MODE"),
        resolution["mode"],
    )

    recorded_hashes = resolution["hashes"]
    actual_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            GENERATION_TOOLS
        ),
        "generated_tree_sha256": klean_export.tree_digest(
            GENERATION / "generated"
        ),
        "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
    }
    for name, actual in actual_hashes.items():
        overall &= report(name, actual, recorded_hashes[name])

    actual_source_hashes = klean_audit_contract._stage1_source_hashes(K_WORKSPACE)
    expected_source_hashes = resolution["stage1_source_hashes"]
    source_missing = sorted(set(expected_source_hashes) - set(actual_source_hashes))
    source_extra = sorted(set(actual_source_hashes) - set(expected_source_hashes))
    source_changed = sorted(
        name
        for name in set(actual_source_hashes) & set(expected_source_hashes)
        if actual_source_hashes[name] != expected_source_hashes[name]
    )
    source_hashes_match = not (source_missing or source_extra or source_changed)
    overall &= source_hashes_match
    print(
        json.dumps(
            {
                "check": "all Stage 1 recorded source hashes",
                "actual_count": len(actual_source_hashes),
                "expected_count": len(expected_source_hashes),
                "missing": source_missing,
                "extra": source_extra,
                "changed": source_changed,
                "match": source_hashes_match,
            },
            sort_keys=True,
        )
    )

    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    source_manifest = json.loads(
        (GENERATION_TOOLS / "source-manifest.json").read_text()
    )
    producer_hashes = {
        "klean_export.py": file_sha256(GENERATION_TOOLS / "klean_export.py"),
        "klean.py": file_sha256(GENERATION_TOOLS / "klean.py"),
    }
    overall &= report(
        "producer hashes match source manifest",
        producer_hashes,
        source_manifest["files"],
    )
    overall &= report(
        "producer exporter hash matches generator manifest",
        producer_hashes["klean_export.py"],
        generator_manifest["exporter_sha256"],
    )
    overall &= report(
        "producer klean.py hash matches generator manifest",
        producer_hashes["klean.py"],
        generator_manifest["klean_py_sha256"],
    )
    generator_image_id = generator_manifest["provenance"]["generator_image_id"]
    overall &= report(
        "generator image ID matches source manifest",
        generator_image_id,
        source_manifest["generator_image_id"],
    )
    audit_bundle_image_id = (
        "sha256:" + Path(resolution["generation_producer_sources"]).name
    )
    overall &= report(
        "generator image ID matches signed audit input producer path",
        generator_image_id,
        audit_bundle_image_id,
    )
    overall &= report(
        "generator target matches signed audit input",
        generator_manifest["target"],
        resolution["target"],
    )
    overall &= report(
        "generator Stage 1 export provenance",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        recorded_hashes["stage1_export_sha256"],
    )
    overall &= report(
        "input Stage 1 export provenance",
        input_manifest["stage1_workspace_sha256"],
        recorded_hashes["stage1_export_sha256"],
    )
    overall &= report(
        "generator Stage 3 provenance",
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
        recorded_hashes["discovery_manifest_sha256"],
    )

    inventory = inventory_verification(K_WORKSPACE)
    print("RECONSTRUCTED_INVENTORY_BEGIN")
    print(json.dumps(inventory, indent=2, ensure_ascii=False, sort_keys=True))
    print("RECONSTRUCTED_INVENTORY_END")
    discovery_document = json.loads(DISCOVERY.read_text())
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [
        rule["source_rule_id"] for rule in discovery_document["rules"]
    ]
    overall &= report(
        "inventory hash matches Stage 3",
        inventory["inventory_sha256"],
        discovery_document["inventory_sha256"],
    )
    overall &= report(
        "Stage 3 identity order is canonical",
        discovery_ids,
        canonical_ids,
    )
    overall &= report(
        "Stage 3 identities are unique",
        len(set(discovery_ids)),
        len(discovery_ids),
    )
    validated = lemma_discovery_contract.validate_trust_boundary(
        K_WORKSPACE, DISCOVERY
    )
    print(
        json.dumps(
            {
                "trust_boundary_validation": "PASS",
                "definitions": len(validated["definitions"]),
                "operational_rules": len(validated["operational_rules"]),
                "proved_derived_lemmas": len(
                    validated["proved_derived_lemmas"]
                ),
                "domain_lemmas": len(validated["domain_lemmas"]),
            },
            sort_keys=True,
        )
    )
    overall &= report(
        "input-manifest inventory hash",
        input_manifest["inventory_sha256"],
        inventory["inventory_sha256"],
    )
    overall &= report(
        "generator inventory provenance",
        generator_manifest["provenance"]["inventory_sha256"],
        inventory["inventory_sha256"],
    )
    overall &= report(
        "verification.k recorded SHA-256",
        inventory["verification_sha256"],
        input_manifest["verification_sha256"],
    )

    print(f"STATIC_CHECKS_OVERALL={'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
