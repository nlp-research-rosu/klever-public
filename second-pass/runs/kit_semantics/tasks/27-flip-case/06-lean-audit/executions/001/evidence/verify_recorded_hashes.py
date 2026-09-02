#!/usr/bin/env python3
"""Independently recompute every hash bound into the Stage 6 audit input."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(label: str, expected: object, actual: object) -> bool:
    match = expected == actual
    print(f"{label}: {'MATCH' if match else 'MISMATCH'}")
    print(f"  expected={expected}")
    print(f"  actual={actual}")
    return match


def regular_files(root: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                found[relative] = path
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    return found


def main() -> int:
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = (
        stage6_resolution_contract.verify_audit_input(envelope)
    )
    print("audit envelope: VALID")
    matches: list[bool] = [
        record(
            "resolved_input_sha256",
            envelope["resolved_input_sha256"],
            resolved_digest,
        )
    ]

    hashes = resolution["hashes"]
    matches.extend(
        [
            record(
                "k_workspace_sha256",
                hashes["k_workspace_sha256"],
                pipeline_contract.sha256_tree(K_WORKSPACE),
            ),
            record(
                "stage1_export_sha256",
                hashes["stage1_export_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "discovery_manifest_sha256",
                hashes["discovery_manifest_sha256"],
                file_sha256(DISCOVERY),
            ),
            record(
                "k_audit_sha256",
                hashes["k_audit_sha256"],
                pipeline_contract.sha256_tree(K_AUDIT),
            ),
            record(
                "klean_generation_sha256",
                hashes["klean_generation_sha256"],
                pipeline_contract.sha256_tree(GENERATION),
            ),
            record(
                "generation_producer_sources_sha256",
                hashes["generation_producer_sources_sha256"],
                pipeline_contract.sha256_tree(PRODUCERS),
            ),
            record(
                "generated_tree_sha256",
                hashes["generated_tree_sha256"],
                klean_export.tree_digest(GENERATED),
            ),
            record(
                "lean_workspace_sha256",
                hashes["lean_workspace_sha256"],
                None,
            ),
            record(
                "lean_invocation_sha256",
                hashes["lean_invocation_sha256"],
                None,
            ),
        ]
    )
    selections = resolution["selections"]
    matches.extend(
        [
            record(
                "selection.k_audit.artifact_sha256",
                selections["k_audit"]["artifact_sha256"],
                pipeline_contract.sha256_tree(K_AUDIT),
            ),
            record(
                "selection.klean_generation.artifact_sha256",
                selections["klean_generation"]["artifact_sha256"],
                pipeline_contract.sha256_tree(GENERATION),
            ),
        ]
    )
    recorded_preflight = resolution["stage4_preflight"]
    matches.extend(
        [
            record(
                "audit stage4_preflight.frozen_input_sha256",
                recorded_preflight["frozen_input_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "audit stage4_preflight.stage1_workspace_sha256",
                recorded_preflight["stage1_workspace_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "audit stage4_preflight.stage3_discovery_manifest_sha256",
                recorded_preflight[
                    "stage3_discovery_manifest_sha256"
                ],
                file_sha256(DISCOVERY),
            ),
            record(
                "audit stage4_preflight.generated_tree_sha256",
                recorded_preflight["generated_tree_sha256"],
                klean_export.tree_digest(GENERATED),
            ),
        ]
    )

    expected_source_hashes = resolution["stage1_source_hashes"]
    actual_files = regular_files(K_WORKSPACE)
    expected_names = set(expected_source_hashes)
    actual_names = set(actual_files)
    matches.append(
        record(
            "stage1_source_hashes missing files",
            [],
            sorted(expected_names - actual_names),
        )
    )
    matches.append(
        record(
            "stage1_source_hashes unexpected files",
            [],
            sorted(actual_names - expected_names),
        )
    )
    source_mismatches = [
        (
            relative,
            expected_source_hashes[relative],
            file_sha256(actual_files[relative]),
        )
        for relative in sorted(expected_names & actual_names)
        if expected_source_hashes[relative]
        != file_sha256(actual_files[relative])
    ]
    matches.append(
        record("stage1_source_hashes mismatches", [], source_mismatches)
    )
    print(f"stage1_source_hashes checked={len(expected_source_hashes)}")

    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    trust_inventory_path = GENERATION / "trust-inventory.json"
    canonical_inventory_hash = k_rule_inventory.inventory_verification(
        K_WORKSPACE
    )["inventory_sha256"]

    matches.extend(
        [
            record(
                "input_manifest.verification_sha256",
                input_manifest["verification_sha256"],
                file_sha256(K_WORKSPACE / "verification.k"),
            ),
            record(
                "input_manifest.stage3_discovery_manifest_sha256",
                input_manifest["stage3_discovery_manifest_sha256"],
                file_sha256(DISCOVERY),
            ),
            record(
                "input_manifest.frozen_input_sha256",
                input_manifest["frozen_input_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "input_manifest.stage1_workspace_sha256",
                input_manifest["stage1_workspace_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "input_manifest.inventory_sha256",
                input_manifest["inventory_sha256"],
                canonical_inventory_hash,
            ),
            record(
                "generator_manifest.generated_tree_sha256",
                generator_manifest["generated_tree_sha256"],
                klean_export.tree_digest(GENERATED),
            ),
            record(
                "generator_manifest.obligation_map_sha256",
                generator_manifest["obligation_map_sha256"],
                file_sha256(obligation_map_path),
            ),
            record(
                "generator_manifest.provenance.inventory_sha256",
                generator_manifest["provenance"]["inventory_sha256"],
                canonical_inventory_hash,
            ),
            record(
                "generator_manifest.provenance.stage1_workspace_sha256",
                generator_manifest["provenance"][
                    "stage1_workspace_sha256"
                ],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "generator_manifest.provenance.stage3_discovery_manifest_sha256",
                generator_manifest["provenance"][
                    "stage3_discovery_manifest_sha256"
                ],
                file_sha256(DISCOVERY),
            ),
            record(
                "export_result.trust_inventory_sha256",
                export_result["trust_inventory_sha256"],
                file_sha256(trust_inventory_path),
            ),
            record(
                "export_result.generated_tree_sha256",
                export_result["generated_tree_sha256"],
                klean_export.tree_digest(GENERATED),
            ),
            record(
                "export_result.frozen_input_sha256",
                export_result["frozen_input_sha256"],
                klean_export.tree_digest(K_WORKSPACE),
            ),
            record(
                "export_result.stage3_discovery_manifest_sha256",
                export_result["stage3_discovery_manifest_sha256"],
                file_sha256(DISCOVERY),
            ),
        ]
    )

    producer_expectations = {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    }
    matches.append(
        record(
            "producer source manifest file map",
            producer_expectations,
            source_manifest["files"],
        )
    )
    for name, expected_hash in producer_expectations.items():
        matches.append(
            record(
                f"producer {name} SHA-256",
                expected_hash,
                file_sha256(PRODUCERS / name),
            )
        )

    manifest_image = generator_manifest["provenance"]["generator_image_id"]
    source_image = source_manifest["generator_image_id"]
    audit_image = (
        "sha256:"
        + Path(resolution["generation_producer_sources"]).name
    )
    matches.extend(
        [
            record(
                "generator image: generator/source manifests",
                manifest_image,
                source_image,
            ),
            record(
                "generator image: generator manifest/audit input",
                manifest_image,
                audit_image,
            ),
        ]
    )

    expected_bundle_names = {
        "klean.py",
        "klean_export.py",
        "source-manifest.json",
    }
    matches.append(
        record(
            "producer bundle file set",
            sorted(expected_bundle_names),
            sorted(regular_files(PRODUCERS)),
        )
    )

    print(
        "OVERALL="
        + ("MATCH" if matches and all(matches) else "MISMATCH")
    )
    return 0 if matches and all(matches) else 1


if __name__ == "__main__":
    raise SystemExit(main())
