#!/usr/bin/env python3
"""Independently check mounted hashes, Stage 4 bijection, and target identity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory = json.loads(Path("/audit-output/evidence/reconstructed-inventory.json").read_text())
inventory_by_id = {r["source_rule_id"]: r for r in inventory["rules"]}

mounted_hashes = {
    "discovery_manifest_sha256": file_sha(Path("/reference/lemma-discovery.json")),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
}

stage1_actual = {
    path.relative_to(Path("/reference/k-proof")).as_posix():
        pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
stage1_recorded = resolution["stage1_source_hashes"]

domain_ids = [
    "rule-80907d170695ac0e50e240d5c49a8b32450d664965ed274c57fd0644ebdbd791",
    "rule-0a4fd72c46b3149583834f42a226e0e1c0adf4fda67461b4a052f6c7a887a526",
    "rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4",
]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [obligation["source_rule_id"] for obligation in obligations]

per_obligation = []
for source_rule, obligation in zip(source_rules, obligations, strict=True):
    rid = source_rule["source_rule_id"]
    frozen = inventory_by_id[rid]
    per_obligation.append({
        "source_rule_id": rid,
        "source_rule_matches_reconstruction": all(
            source_rule.get(key) == frozen.get(key)
            for key in (
                "source_rule_id", "module", "start_line", "end_line",
                "normalized_sha256", "attributes", "text",
            )
        ) and source_rule.get("file", "verification.k") == frozen.get("file", "verification.k"),
        "classification_is_domain_lemma": source_rule.get("classification") == "DOMAIN_LEMMA",
        "obligation_source_id_matches": obligation.get("source_rule_id") == rid,
        "obligation_source_span_matches": obligation.get("source_span") == {
            "start_line": frozen["start_line"], "end_line": frozen["end_line"]
        },
        "obligation_normalized_hash_matches": obligation.get("normalized_sha256") == frozen["normalized_sha256"],
        "obligation_inventory_hash_matches": obligation.get("inventory_sha256") == inventory["inventory_sha256"],
        "obligation_discovery_hash_matches": obligation.get("discovery_manifest_sha256") == file_sha(Path("/reference/lemma-discovery.json")),
        "lean_conjunct_hash_matches": obligation.get("lean_conjunct_sha256") == klean_export.sha256_text(obligation["lean_conjunct"]),
        "lean_conjunct_sha256": obligation.get("lean_conjunct_sha256"),
        "lean_conjunct": obligation.get("lean_conjunct"),
    })

target = klean_export.target_statement(generated)
target_copies = {
    "extracted": target,
    "generator_manifest": generator_manifest.get("target"),
    "audit_input": resolution.get("target"),
    "audit_input_stage4_preflight": resolution.get("stage4_preflight", {}).get("target"),
}

result = {
    "mounted_hash_checks": {
        key: {"actual": actual, "recorded": recorded.get(key), "equal": actual == recorded.get(key)}
        for key, actual in mounted_hashes.items()
    },
    "unmounted_hash_not_recomputed": {
        "lean_invocation_sha256": recorded.get("lean_invocation_sha256"),
        "reason": "Stage 5 invocation directory is not among the mounted inputs",
    },
    "stage1_source_hashes": {
        "actual_count": len(stage1_actual),
        "recorded_count": len(stage1_recorded),
        "exact_map_equal": stage1_actual == stage1_recorded,
        "missing_from_mount": sorted(set(stage1_recorded) - set(stage1_actual)),
        "extra_in_mount": sorted(set(stage1_actual) - set(stage1_recorded)),
        "value_mismatches": sorted(
            key for key in set(stage1_actual) & set(stage1_recorded)
            if stage1_actual[key] != stage1_recorded[key]
        ),
    },
    "manifest_bindings": {
        "input_inventory_hash_equal": input_manifest.get("inventory_sha256") == inventory["inventory_sha256"],
        "generator_inventory_hash_equal": generator_manifest.get("provenance", {}).get("inventory_sha256") == inventory["inventory_sha256"],
        "generator_obligation_count_equal": generator_manifest.get("obligation_count") == len(obligations),
        "generator_obligation_map_hash_equal": generator_manifest.get("obligation_map_sha256") == file_sha(obligation_map_path),
        "generator_generated_tree_hash_equal": generator_manifest.get("generated_tree_sha256") == mounted_hashes["generated_tree_sha256"],
    },
    "bijection": {
        "independently_classified_domain_ids": domain_ids,
        "source_rule_ids": source_ids,
        "obligation_ids": obligation_ids,
        "source_ids_unique": len(source_ids) == len(set(source_ids)),
        "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
        "exact_domain_source_order": source_ids == domain_ids,
        "exact_source_obligation_order": source_ids == obligation_ids,
        "per_obligation": per_obligation,
    },
    "target": {
        "all_target_copies_equal": len({json.dumps(value, sort_keys=True) for value in target_copies.values()}) == 1,
        "copies": target_copies,
        "statement_hash_recomputed": klean_export.sha256_text(target["statement"]),
        "statement_hash_matches": klean_export.sha256_text(target["statement"]) == target["statement_sha256"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
