#!/usr/bin/env python3
"""Recompute the Stage 3/4 audit bindings from the read-only mounts."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> bool:
    matches = observed == expected
    print(f"{label}: {'MATCH' if matches else 'MISMATCH'}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    return matches


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution, envelope_digest = stage6_resolution_contract.verify_audit_input(
        audit
    )
    hashes = resolution["hashes"]
    all_ok = True

    print("AUDIT ENVELOPE")
    all_ok &= check(
        "resolved_input_sha256",
        envelope_digest,
        audit["resolved_input_sha256"],
    )
    all_ok &= check(
        "AUDIT_MODE",
        os.environ.get("AUDIT_MODE"),
        resolution["mode"],
    )

    print("\nTOP-LEVEL HASHES")
    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    for name, observed in observed_hashes.items():
        all_ok &= check(name, observed, hashes[name])

    print("\nSTAGE 1 PER-FILE HASHES")
    observed_source_hashes = {
        path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
        for path in pipeline_contract._walk_regular_files(
            K_WORKSPACE, "mounted Stage 1 workspace"
        )
    }
    all_ok &= check(
        "stage1_source_hashes",
        observed_source_hashes,
        resolution["stage1_source_hashes"],
    )

    print("\nSELECTION HASHES")
    all_ok &= check(
        "selected k_audit artifact",
        observed_hashes["k_audit_sha256"],
        resolution["selections"]["k_audit"]["artifact_sha256"],
    )
    all_ok &= check(
        "selected klean_generation artifact",
        observed_hashes["klean_generation_sha256"],
        resolution["selections"]["klean_generation"]["artifact_sha256"],
    )

    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    obligation_map = GENERATED / "obligation-map.json"

    print("\nPRODUCER AUTHENTICATION")
    producer_files = sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in pipeline_contract._walk_regular_files(
            PRODUCERS, "mounted producer bundle"
        )
    )
    all_ok &= check(
        "producer file set",
        producer_files,
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
    exporter_hash = sha256_file(PRODUCERS / "klean_export.py")
    klean_hash = sha256_file(PRODUCERS / "klean.py")
    all_ok &= check(
        "klean_export.py vs source manifest",
        exporter_hash,
        source_manifest["files"]["klean_export.py"],
    )
    all_ok &= check(
        "klean_export.py vs generator manifest",
        exporter_hash,
        generator_manifest["exporter_sha256"],
    )
    all_ok &= check(
        "klean.py vs source manifest",
        klean_hash,
        source_manifest["files"]["klean.py"],
    )
    all_ok &= check(
        "klean.py vs generator manifest",
        klean_hash,
        generator_manifest["klean_py_sha256"],
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]
    all_ok &= check(
        "generator image source/generator manifests",
        source_manifest["generator_image_id"],
        image_id,
    )
    recorded_bundle_key = Path(
        resolution["generation_producer_sources"]
    ).name
    all_ok &= check(
        "generator image vs audit-input producer path",
        f"sha256:{recorded_bundle_key}",
        image_id,
    )

    print("\nSTAGE 4 CROSS-BINDINGS")
    all_ok &= check(
        "generator generated tree",
        observed_hashes["generated_tree_sha256"],
        generator_manifest["generated_tree_sha256"],
    )
    all_ok &= check(
        "generator obligation-map hash",
        sha256_file(obligation_map),
        generator_manifest["obligation_map_sha256"],
    )
    all_ok &= check(
        "generator Stage 1 provenance",
        observed_hashes["stage1_export_sha256"],
        generator_manifest["provenance"]["stage1_workspace_sha256"],
    )
    all_ok &= check(
        "generator Stage 3 provenance",
        observed_hashes["discovery_manifest_sha256"],
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
    )
    all_ok &= check(
        "input manifest frozen input",
        observed_hashes["stage1_export_sha256"],
        input_manifest["frozen_input_sha256"],
    )
    all_ok &= check(
        "input manifest Stage 1",
        observed_hashes["stage1_export_sha256"],
        input_manifest["stage1_workspace_sha256"],
    )
    all_ok &= check(
        "input manifest Stage 3",
        observed_hashes["discovery_manifest_sha256"],
        input_manifest["stage3_discovery_manifest_sha256"],
    )
    all_ok &= check(
        "export result frozen input",
        observed_hashes["stage1_export_sha256"],
        export_result["frozen_input_sha256"],
    )
    all_ok &= check(
        "export result Stage 3",
        observed_hashes["discovery_manifest_sha256"],
        export_result["stage3_discovery_manifest_sha256"],
    )
    all_ok &= check(
        "export result generated tree",
        observed_hashes["generated_tree_sha256"],
        export_result["generated_tree_sha256"],
    )
    all_ok &= check(
        "export result trust inventory",
        sha256_file(GENERATION / "trust-inventory.json"),
        export_result["trust_inventory_sha256"],
    )
    all_ok &= check(
        "recorded preflight",
        preflight,
        resolution["stage4_preflight"],
    )

    print(f"\nOVERALL={'MATCH' if all_ok else 'MISMATCH'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
