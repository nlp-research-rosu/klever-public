#!/usr/bin/env python3
"""Independent integrity and Stage 3 inventory reconstruction evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract
from tools.lemma_discovery_contract import validate_trust_boundary


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
K_AUDIT = Path("/reference/k-audit")
CANDIDATE = Path("/candidate")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    expected_hashes = resolution["hashes"]
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    discovery = json.loads(DISCOVERY.read_text())

    producer_observed = {
        name: sha256_file(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    }
    producer_expected_generator = {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    }
    producer_bundle_names = sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in PRODUCERS.iterdir()
        if path.is_file()
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]

    inventory = k_rule_inventory.inventory_verification(WORKSPACE)
    validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()
    independently_recomputed_rules = []
    for rule in inventory["rules"]:
        exact_span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized = " ".join(exact_span.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        independently_recomputed_rules.append(
            {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "exact_span": exact_span,
                "span_matches_inventory_text": exact_span == rule["text"],
                "normalized": normalized,
                "normalized_sha256": normalized_sha256,
                "hash_matches_inventory": (
                    normalized_sha256 == rule["normalized_sha256"]
                ),
                "source_rule_id": f"rule-{normalized_sha256}",
                "id_matches_inventory": (
                    f"rule-{normalized_sha256}" == rule["source_rule_id"]
                ),
            }
        )
    manual_inventory_sha256 = k_rule_inventory.canonical_json_sha256(
        inventory["rules"]
    )
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

    stage1_source_observed = {
        path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
        for path in sorted(WORKSPACE.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    stage1_source_expected = resolution["stage1_source_hashes"]

    report = {
        "producer_provenance": {
            "observed_files": producer_observed,
            "generator_manifest_files": producer_expected_generator,
            "source_manifest_files": source_manifest["files"],
            "all_file_hashes_match": (
                producer_observed
                == producer_expected_generator
                == source_manifest["files"]
            ),
            "bundle_regular_file_names": producer_bundle_names,
            "bundle_file_set_exact": producer_bundle_names
            == ["klean.py", "klean_export.py", "source-manifest.json"],
            "generator_image_id": image_id,
            "source_manifest_image_id": source_manifest["generator_image_id"],
            "audit_input_bundle_basename": Path(
                resolution["generation_producer_sources"]
            ).name,
            "image_ids_match": (
                image_id == source_manifest["generator_image_id"]
                and image_id.removeprefix("sha256:")
                == Path(resolution["generation_producer_sources"]).name
            ),
            "observed_bundle_tree_sha256": pipeline_contract.sha256_tree(PRODUCERS),
            "audit_input_bundle_tree_sha256": expected_hashes[
                "generation_producer_sources_sha256"
            ],
            "bundle_tree_hash_matches": (
                pipeline_contract.sha256_tree(PRODUCERS)
                == expected_hashes["generation_producer_sources_sha256"]
            ),
        },
        "mounted_hashes": {
            "stage1_pipeline_tree_observed": pipeline_contract.sha256_tree(
                WORKSPACE
            ),
            "stage1_pipeline_tree_expected": expected_hashes[
                "k_workspace_sha256"
            ],
            "stage1_export_tree_observed": klean_export.tree_digest(WORKSPACE),
            "stage1_export_tree_expected": expected_hashes[
                "stage1_export_sha256"
            ],
            "discovery_observed": sha256_file(DISCOVERY),
            "discovery_expected": expected_hashes[
                "discovery_manifest_sha256"
            ],
            "generation_pipeline_tree_observed": pipeline_contract.sha256_tree(
                GENERATION
            ),
            "generation_pipeline_tree_expected": expected_hashes[
                "klean_generation_sha256"
            ],
            "k_audit_pipeline_tree_observed": pipeline_contract.sha256_tree(
                K_AUDIT
            ),
            "k_audit_pipeline_tree_expected": expected_hashes[
                "k_audit_sha256"
            ],
            "generated_export_tree_observed": klean_export.tree_digest(
                GENERATED
            ),
            "generated_export_tree_expected": expected_hashes[
                "generated_tree_sha256"
            ],
            "candidate_pipeline_tree_observed": pipeline_contract.sha256_tree(
                CANDIDATE
            ),
            "candidate_pipeline_tree_expected": expected_hashes[
                "lean_workspace_sha256"
            ],
            "stage1_source_file_set_exact": (
                set(stage1_source_observed) == set(stage1_source_expected)
            ),
            "stage1_source_hashes_exact": (
                stage1_source_observed == stage1_source_expected
            ),
        },
        "inventory": inventory,
        "independent_span_hash_recomputation": independently_recomputed_rules,
        "manual_inventory_sha256": manual_inventory_sha256,
        "manual_inventory_hash_matches": (
            manual_inventory_sha256 == inventory["inventory_sha256"]
        ),
        "discovery_comparison": {
            "manifest_inventory_sha256": discovery["inventory_sha256"],
            "canonical_inventory_sha256": inventory["inventory_sha256"],
            "inventory_hash_matches": (
                discovery["inventory_sha256"] == inventory["inventory_sha256"]
            ),
            "canonical_ids": canonical_ids,
            "manifest_ids": discovery_ids,
            "exact_ordered_identity_bijection": canonical_ids == discovery_ids,
            "no_manifest_duplicates": len(discovery_ids) == len(set(discovery_ids)),
            "no_omissions_or_extras": set(canonical_ids) == set(discovery_ids),
            "validated_role_counts": {
                role: len(validated[role])
                for role in (
                    "definitions",
                    "operational_rules",
                    "proved_derived_lemmas",
                    "domain_lemmas",
                )
            },
        },
    }
    mounted_hashes = report["mounted_hashes"]
    mounted_hashes["all_recorded_top_level_hashes_match"] = all(
        mounted_hashes[key] == mounted_hashes[key.replace("_observed", "_expected")]
        for key in (
            "stage1_pipeline_tree_observed",
            "stage1_export_tree_observed",
            "discovery_observed",
            "generation_pipeline_tree_observed",
            "k_audit_pipeline_tree_observed",
            "generated_export_tree_observed",
            "candidate_pipeline_tree_observed",
        )
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
