#!/usr/bin/env python3
"""Recompute mounted source, tree, manifest, target, and binding hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree


audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")

source_hashes = {}
source_hash_matches = {}
for relative, expected in audit_input["stage1_source_hashes"].items():
    path = Path("/reference/k-proof") / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    source_hashes[relative] = actual
    source_hash_matches[relative] = actual == expected

obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)

binding_checks = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    actual = sha256_text(
        json.dumps(binding, sort_keys=True, separators=(",", ":"))
    )
    binding_checks.append(
        {
            "name": parameter["name"],
            "actual": actual,
            "recorded": parameter["binding_sha256"],
            "matches": actual == parameter["binding_sha256"],
        }
    )

tree_hashes = {
    "stage1_export_klean_digest": tree_digest(Path("/reference/k-proof")),
    "generated_klean_digest": tree_digest(generated),
    "k_workspace_pipeline_digest": sha256_tree(Path("/reference/k-proof")),
    "generation_mount_pipeline_digest": sha256_tree(generation),
    "k_audit_mount_pipeline_digest": sha256_tree(Path("/reference/k-audit")),
    "candidate_mount_pipeline_digest": sha256_tree(candidate),
}

recorded_tree_comparisons = {
    "stage1_export": {
        "actual": tree_hashes["stage1_export_klean_digest"],
        "recorded": audit_input["hashes"]["stage1_export_sha256"],
    },
    "generated": {
        "actual": tree_hashes["generated_klean_digest"],
        "recorded": audit_input["hashes"]["generated_tree_sha256"],
    },
    "k_workspace": {
        "actual": tree_hashes["k_workspace_pipeline_digest"],
        "recorded": audit_input["hashes"]["k_workspace_sha256"],
    },
    "generation_mount": {
        "actual": tree_hashes["generation_mount_pipeline_digest"],
        "recorded": audit_input["hashes"]["klean_generation_sha256"],
    },
    "k_audit_mount": {
        "actual": tree_hashes["k_audit_mount_pipeline_digest"],
        "recorded": audit_input["hashes"]["k_audit_sha256"],
    },
    "candidate_mount": {
        "actual": tree_hashes["candidate_mount_pipeline_digest"],
        "recorded": audit_input["hashes"]["lean_workspace_sha256"],
    },
}
for comparison in recorded_tree_comparisons.values():
    comparison["matches"] = comparison["actual"] == comparison["recorded"]

file_hash_comparisons = {
    "discovery_manifest": {
        "actual": hashlib.sha256(
            Path("/reference/lemma-discovery.json").read_bytes()
        ).hexdigest(),
        "recorded": audit_input["hashes"]["discovery_manifest_sha256"],
    },
    "verification": {
        "actual": hashlib.sha256(
            Path("/reference/k-proof/verification.k").read_bytes()
        ).hexdigest(),
        "recorded": audit_input["stage1_source_hashes"]["verification.k"],
    },
}
for comparison in file_hash_comparisons.values():
    comparison["matches"] = comparison["actual"] == comparison["recorded"]

result = {
    "stage1_source_hashes": source_hashes,
    "stage1_source_hash_matches": source_hash_matches,
    "tree_hashes": tree_hashes,
    "recorded_tree_comparisons": recorded_tree_comparisons,
    "file_hash_comparisons": file_hash_comparisons,
    "target_recomputed": target,
    "target_matches_audit_input": target == audit_input["target"],
    "target_matches_generator_manifest": (
        target == generator_manifest["target"]
    ),
    "target_matches_recorded_stage4_preflight": (
        target == audit_input["stage4_preflight"]["target"]
    ),
    "target_definition_from_obligations": expected_definition,
    "target_definition_sha256_recomputed": (
        None if expected_definition is None else sha256_text(expected_definition)
    ),
    "binding_checks": binding_checks,
}

print(json.dumps(result, indent=2, sort_keys=True))
