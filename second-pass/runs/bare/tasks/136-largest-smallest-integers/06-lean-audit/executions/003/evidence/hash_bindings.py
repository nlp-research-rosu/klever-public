#!/usr/bin/env python3
"""Independently recompute launcher, Stage 1, and Stage 4 hash bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        audit
    )
    expected = resolution["hashes"]
    stage1 = Path("/reference/k-proof")
    stage2 = Path("/reference/k-audit")
    discovery = Path("/reference/lemma-discovery.json")
    generation = Path("/reference/klean-generation")
    generated = generation / "generated"
    producers = Path("/reference/generation-tools")

    observed = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
        "stage1_export_sha256": klean_export.tree_digest(stage1),
        "discovery_manifest_sha256": sha256_file(discovery),
        "generated_tree_sha256": klean_export.tree_digest(generated),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            producers
        ),
        "k_audit_sha256": pipeline_contract.sha256_tree(stage2),
        "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
        "lean_invocation_sha256": None,
        "lean_workspace_sha256": None,
    }
    hash_matches = {
        key: {"expected": expected.get(key), "observed": value,
              "match": expected.get(key) == value}
        for key, value in observed.items()
    }

    source_manifest = json.loads(
        (producers / "source-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (generation / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads((generation / "input-manifest.json").read_text())
    export_result = json.loads((generation / "export-result.json").read_text())
    obligation_map = json.loads(
        (generated / "obligation-map.json").read_text()
    )
    preflight = json.loads((generation / "preflight.json").read_text())
    toolchain_lock = json.loads(
        Path("/reference/klean-toolchain.lock.json").read_text()
    )
    producer_hashes = {
        name: sha256_file(producers / name)
        for name in ("klean.py", "klean_export.py")
    }
    image_id = source_manifest["generator_image_id"]
    recorded_source_store_id = (
        "sha256:" + Path(resolution["generation_producer_sources"]).name
    )

    current_stage1_files = regular_file_hashes(stage1)
    expected_stage1_files = resolution["stage1_source_hashes"]
    stage1_file_check = {
        "expected_count": len(expected_stage1_files),
        "observed_count": len(current_stage1_files),
        "exact_file_and_hash_map": current_stage1_files == expected_stage1_files,
        "missing": sorted(set(expected_stage1_files) - set(current_stage1_files)),
        "extra": sorted(set(current_stage1_files) - set(expected_stage1_files)),
        "mismatches": sorted(
            name
            for name in set(expected_stage1_files) & set(current_stage1_files)
            if expected_stage1_files[name] != current_stage1_files[name]
        ),
    }

    checks = {
        "resolved_input_sha256_recomputed": resolved_digest,
        "resolved_input_sha256_match": (
            resolved_digest == audit["resolved_input_sha256"]
        ),
        "all_launcher_hashes_match": all(
            item["match"] for item in hash_matches.values()
        ),
        "stage1_source_hash_map": stage1_file_check,
        "producer_files_match_source_manifest": (
            producer_hashes == source_manifest["files"]
        ),
        "exporter_matches_generator_manifest": (
            producer_hashes["klean_export.py"]
            == generator_manifest["exporter_sha256"]
        ),
        "klean_py_matches_generator_manifest": (
            producer_hashes["klean.py"]
            == generator_manifest["klean_py_sha256"]
        ),
        "generator_image_source_vs_generator": (
            image_id == generator_manifest["provenance"]["generator_image_id"]
        ),
        "generator_image_source_vs_audit_input_store": (
            image_id == recorded_source_store_id
        ),
        "generator_inventory_matches_stage3": (
            generator_manifest["provenance"]["inventory_sha256"]
            == input_manifest["inventory_sha256"]
        ),
        "generator_toolchain_matches_pinned_lock": (
            generator_manifest["toolchain"] == toolchain_lock
        ),
        "input_stage1_matches_observed": (
            input_manifest["stage1_workspace_sha256"]
            == observed["stage1_export_sha256"]
            == input_manifest["frozen_input_sha256"]
        ),
        "input_stage3_matches_observed": (
            input_manifest["stage3_discovery_manifest_sha256"]
            == observed["discovery_manifest_sha256"]
        ),
        "generator_generated_tree_matches_observed": (
            generator_manifest["generated_tree_sha256"]
            == observed["generated_tree_sha256"]
        ),
        "obligation_map_hash_matches_generator": (
            sha256_file(generated / "obligation-map.json")
            == generator_manifest["obligation_map_sha256"]
        ),
        "trust_inventory_hash_matches_export": (
            sha256_file(generation / "trust-inventory.json")
            == export_result["trust_inventory_sha256"]
        ),
        "recorded_preflight_hashes_match_observed": (
            preflight["stage1_workspace_sha256"]
            == observed["stage1_export_sha256"]
            and preflight["stage3_discovery_manifest_sha256"]
            == observed["discovery_manifest_sha256"]
            and preflight["generated_tree_sha256"]
            == observed["generated_tree_sha256"]
        ),
        "zero_obligation_shape": (
            generator_manifest["obligation_count"] == 0
            and export_result["obligation_count"] == 0
            and preflight["obligation_count"] == 0
            and obligation_map
            == {
                "schema_version": 3,
                "source_rules": [],
                "obligations": [],
                "trust_parameters": [],
            }
            and generator_manifest["target"] is None
            and preflight["target"] is None
        ),
    }

    report = {
        "launcher_hash_bindings": hash_matches,
        "producer_hashes": producer_hashes,
        "source_manifest": source_manifest,
        "recorded_source_store_image_id": recorded_source_store_id,
        "checks": checks,
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    bool_checks = {
        key: value
        for key, value in checks.items()
        if isinstance(value, bool)
    }
    if not all(bool_checks.values()):
        raise SystemExit(1)
    if not stage1_file_check["exact_file_and_hash_map"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
