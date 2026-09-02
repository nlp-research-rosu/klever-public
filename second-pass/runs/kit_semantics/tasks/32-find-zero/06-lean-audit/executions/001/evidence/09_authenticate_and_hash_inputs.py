#!/usr/bin/env python3
"""Authenticate Stage 4 producers and independently re-hash mounted inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
STAGE1 = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in list(dirnames):
            path = directory_path / name
            if not stat.S_ISDIR(path.lstat().st_mode):
                raise RuntimeError(f"unsafe non-directory in tree: {path}")
        for name in filenames:
            path = directory_path / name
            if not stat.S_ISREG(path.lstat().st_mode):
                raise RuntimeError(f"unsafe non-regular file in tree: {path}")
            result[path.relative_to(root).as_posix()] = path
    return result


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    hashes = resolution["hashes"]
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())

    checks: dict[str, object] = {}
    errors: list[str] = []

    producer_files = regular_files(PRODUCERS)
    checks["producer_file_set"] = sorted(producer_files)
    checks["producer_file_set_exact"] = set(producer_files) == {
        "klean.py",
        "klean_export.py",
        "source-manifest.json",
    }
    producer_observed = {
        name: file_sha256(PRODUCERS / name)
        for name in ("klean.py", "klean_export.py")
    }
    checks["producer_observed_sha256"] = producer_observed
    checks["producer_hashes_match_source_manifest"] = (
        source_manifest.get("files") == producer_observed
    )
    checks["producer_hashes_match_generator_manifest"] = (
        generator.get("klean_py_sha256") == producer_observed["klean.py"]
        and generator.get("exporter_sha256")
        == producer_observed["klean_export.py"]
    )

    generator_image_id = generator["provenance"]["generator_image_id"]
    source_image_id = source_manifest.get("generator_image_id")
    launcher_source_path = Path(
        resolution["generation_producer_sources"]
    )
    launcher_image_id = f"sha256:{launcher_source_path.name}"
    checks["generator_image_ids"] = {
        "generator_manifest": generator_image_id,
        "source_manifest": source_image_id,
        "audit_input_producer_path": launcher_image_id,
    }
    checks["generator_image_id_matches_all_records"] = (
        generator_image_id == source_image_id == launcher_image_id
    )

    observed_pipeline_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(STAGE1),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
        "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
    }
    checks["observed_pipeline_tree_hashes"] = observed_pipeline_hashes
    checks["pipeline_tree_hashes_match_audit_input"] = all(
        observed == hashes[name]
        for name, observed in observed_pipeline_hashes.items()
    )

    stage1_export_hash = klean_export.tree_digest(STAGE1)
    generated_tree_hash = klean_export.tree_digest(GENERATED)
    checks["stage1_export_tree_sha256"] = stage1_export_hash
    checks["generated_tree_sha256"] = generated_tree_hash
    checks["stage1_export_hash_matches_all_records"] = all(
        value == stage1_export_hash
        for value in (
            hashes["stage1_export_sha256"],
            generator["provenance"]["stage1_workspace_sha256"],
            input_manifest["frozen_input_sha256"],
            input_manifest["stage1_workspace_sha256"],
            export_result["frozen_input_sha256"],
            preflight["frozen_input_sha256"],
            preflight["stage1_workspace_sha256"],
        )
    )
    checks["generated_tree_hash_matches_all_records"] = all(
        value == generated_tree_hash
        for value in (
            hashes["generated_tree_sha256"],
            generator["generated_tree_sha256"],
            export_result["generated_tree_sha256"],
            preflight["generated_tree_sha256"],
        )
    )

    discovery_hash = file_sha256(DISCOVERY)
    checks["discovery_sha256"] = discovery_hash
    checks["discovery_hash_matches_all_records"] = all(
        value == discovery_hash
        for value in (
            hashes["discovery_manifest_sha256"],
            generator["provenance"]["stage3_discovery_manifest_sha256"],
            input_manifest["stage3_discovery_manifest_sha256"],
            export_result["stage3_discovery_manifest_sha256"],
            preflight["stage3_discovery_manifest_sha256"],
        )
    )

    stage1_files = regular_files(STAGE1)
    expected_stage1_files = resolution["stage1_source_hashes"]
    missing = sorted(set(expected_stage1_files) - set(stage1_files))
    extra = sorted(set(stage1_files) - set(expected_stage1_files))
    mismatched = sorted(
        name
        for name in set(stage1_files) & set(expected_stage1_files)
        if file_sha256(stage1_files[name]) != expected_stage1_files[name]
    )
    checks["stage1_source_hash_file_count"] = len(expected_stage1_files)
    checks["stage1_observed_regular_file_count"] = len(stage1_files)
    checks["stage1_source_hash_missing"] = missing
    checks["stage1_source_hash_extra"] = extra
    checks["stage1_source_hash_mismatched"] = mismatched
    checks["stage1_source_hashes_all_match"] = not (missing or extra or mismatched)

    obligation_map_hash = file_sha256(GENERATED / "obligation-map.json")
    trust_inventory_hash = file_sha256(GENERATION / "trust-inventory.json")
    checks["obligation_map_sha256"] = obligation_map_hash
    checks["trust_inventory_sha256"] = trust_inventory_hash
    checks["obligation_map_hash_matches_generator"] = (
        obligation_map_hash == generator["obligation_map_sha256"]
    )
    checks["trust_inventory_hash_matches_export_result"] = (
        trust_inventory_hash == export_result["trust_inventory_sha256"]
    )

    checks["generation_status_consistent"] = (
        resolution["selections"]["klean_generation"]["status"]
        == preflight["status"]
        == "PASS"
    )
    checks["obligation_count_consistent"] = (
        generator["obligation_count"]
        == export_result["obligation_count"]
        == preflight["obligation_count"]
        == 4
    )

    for name, value in checks.items():
        if isinstance(value, bool) and not value:
            errors.append(name)

    print(
        json.dumps(
            {
                "status": "PASS" if not errors else "AUDIT_ERROR",
                "errors": errors,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
