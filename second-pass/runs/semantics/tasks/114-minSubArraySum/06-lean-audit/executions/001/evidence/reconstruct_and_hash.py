#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and provenance hash checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
candidate = Path("/candidate")

audit = load("/audit-input.json")["resolution"]
discovery = load(str(discovery_path))
source_manifest = load(str(producer / "source-manifest.json"))
generator_manifest = load(str(generation / "generator-manifest.json"))
input_manifest = load(str(generation / "input-manifest.json"))
preflight = load(str(generation / "preflight.json"))

inventory = k_rule_inventory.inventory_verification(workspace)
source_lines = verification.read_text(encoding="utf-8").splitlines()

rule_checks = []
seen_ids: set[str] = set()
seen_hashes: set[str] = set()
seen_spans: set[tuple[int, int]] = set()
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    span = (rule["start_line"], rule["end_line"])
    source_span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    checks = {
        "normalized_sha256_matches": digest == rule["normalized_sha256"],
        "source_rule_id_matches": rule["source_rule_id"] == f"rule-{digest}",
        "source_span_matches_text": source_span_text == rule["text"],
        "unique_source_rule_id": rule["source_rule_id"] not in seen_ids,
        "unique_normalized_sha256": digest not in seen_hashes,
        "unique_source_span": span not in seen_spans,
    }
    seen_ids.add(rule["source_rule_id"])
    seen_hashes.add(digest)
    seen_spans.add(span)
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "source_span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "text": rule["text"],
            "checks": checks,
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
classification_by_id = {
    rule["source_rule_id"]: rule["classification"]
    for rule in discovery["rules"]
}

group_keys = {
    "DEFINITION": "definitions",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
    "DOMAIN_LEMMA": "source_rules",
}
group_checks = {}
for classification, key in group_keys.items():
    expected = [
        source_rule_id
        for source_rule_id in canonical_ids
        if classification_by_id[source_rule_id] == classification
    ]
    observed = [
        rule["source_rule_id"] for rule in input_manifest.get(key, [])
    ]
    group_checks[key] = {
        "expected_ids": expected,
        "observed_ids": observed,
        "exact_match": expected == observed,
    }

observed_source_hashes = {
    path.relative_to(workspace).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "Stage 1 source workspace"
    )
}

tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "stage1_export_sha256": klean_export.tree_digest(workspace),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(candidate),
}

producer_hashes = {
    name: file_sha256(producer / name)
    for name in ("klean_export.py", "klean.py")
}
expected_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
producer_files = sorted(
    path.relative_to(producer).as_posix()
    for path in pipeline_contract._walk_regular_files(
        producer, "Stage 4 producer source bundle"
    )
)
image_id = generator_manifest["provenance"]["generator_image_id"]
recorded_bundle_name = Path(audit["generation_producer_sources"]).name

target_copies = {
    "generator_manifest": generator_manifest.get("target"),
    "preflight": preflight.get("target"),
    "audit_input_target": audit.get("target"),
    "audit_input_stage4_preflight": audit.get("stage4_preflight", {}).get("target"),
    "reconstructed": klean_export.target_statement(generated),
}

result = {
    "inventory": {
        "schema_version": inventory["schema_version"],
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "rule_count": len(inventory["rules"]),
        "inventory_sha256": inventory["inventory_sha256"],
        "rules": rule_checks,
        "all_rule_local_checks_pass": all(
            all(rule["checks"].values()) for rule in rule_checks
        ),
    },
    "stage3_bijection": {
        "manifest_inventory_sha256": discovery["inventory_sha256"],
        "inventory_hash_matches": (
            discovery["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "canonical_ids": canonical_ids,
        "classified_ids": classified_ids,
        "same_count": len(canonical_ids) == len(classified_ids),
        "no_classified_duplicates": len(classified_ids) == len(set(classified_ids)),
        "same_id_set": set(canonical_ids) == set(classified_ids),
        "same_order": canonical_ids == classified_ids,
        "classification_groups_in_input_manifest": group_checks,
    },
    "hashes": {
        "observed_tree_hashes": tree_hashes,
        "audit_input_tree_hashes": audit["hashes"],
        "all_mounted_tree_hashes_match_recorded": all(
            tree_hashes[key] == audit["hashes"][key] for key in tree_hashes
        ),
        "discovery_manifest_sha256": file_sha256(discovery_path),
        "discovery_manifest_hash_matches_recorded": (
            file_sha256(discovery_path)
            == audit["hashes"]["discovery_manifest_sha256"]
        ),
        "observed_stage1_source_hashes": observed_source_hashes,
        "stage1_source_hashes_exact_match": (
            observed_source_hashes == audit["stage1_source_hashes"]
        ),
    },
    "producer_provenance": {
        "observed_files": producer_files,
        "exact_expected_file_set": producer_files
        == ["klean.py", "klean_export.py", "source-manifest.json"],
        "observed_hashes": producer_hashes,
        "generator_manifest_hashes": expected_producer_hashes,
        "source_manifest_hashes": source_manifest["files"],
        "producer_hashes_match_both_manifests": (
            producer_hashes == expected_producer_hashes
            and producer_hashes == source_manifest["files"]
        ),
        "generator_manifest_image_id": image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "audit_input_bundle_name": recorded_bundle_name,
        "image_identity_matches_everywhere": (
            image_id == source_manifest["generator_image_id"]
            and recorded_bundle_name == image_id.removeprefix("sha256:")
        ),
    },
    "target_identity": {
        "copies": target_copies,
        "all_target_copies_equal": len(
            {
                json.dumps(value, sort_keys=True, separators=(",", ":"))
                for value in target_copies.values()
            }
        )
        == 1,
    },
}

print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
