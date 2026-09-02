#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def load(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text())
    assert isinstance(value, dict)
    return value


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        directory_path = Path(directory)
        for name in dirnames:
            path = directory_path / name
            assert path.is_dir() and not path.is_symlink(), path
        for name in filenames:
            path = directory_path / name
            assert path.is_file() and not path.is_symlink(), path
            result[path.relative_to(root).as_posix()] = file_sha256(path)
    return dict(sorted(result.items()))


audit_document = load("/audit-input.json")
resolution, resolution_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
recorded_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha256(
        "/reference/lemma-discovery.json"
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
hash_comparison = {
    key: {
        "recorded": recorded_hashes[key],
        "observed": value,
        "match": recorded_hashes[key] == value,
    }
    for key, value in observed_hashes.items()
}
assert all(entry["match"] for entry in hash_comparison.values())

stage1_source_hashes = regular_file_hashes(Path("/reference/k-proof"))
assert stage1_source_hashes == resolution["stage1_source_hashes"]

source_manifest = load("/reference/generation-tools/source-manifest.json")
generator_manifest = load(
    "/reference/klean-generation/generator-manifest.json"
)
producer_hashes = {
    "klean_export.py": file_sha256(
        "/reference/generation-tools/klean_export.py"
    ),
    "klean.py": file_sha256("/reference/generation-tools/klean.py"),
}
assert producer_hashes == source_manifest["files"]
assert (
    producer_hashes["klean_export.py"]
    == generator_manifest["exporter_sha256"]
)
assert producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
assert (
    source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"]
)
assert (
    Path(resolution["generation_producer_sources"]).name
    == source_manifest["generator_image_id"].removeprefix("sha256:")
)

inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)
discovery = load("/reference/lemma-discovery.json")
validated_discovery = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
assert inventory["inventory_sha256"] == discovery["inventory_sha256"]
assert inventory_ids == discovery_ids
assert len(inventory_ids) == len(set(inventory_ids))
assert len(discovery_ids) == len(set(discovery_ids))

independent_classes = {
    "rule-d467c351c964bfa6aa3699f282303d6447cfcf61979d2a3950f1319a2bfd3c44": "DEFINITION",
    "rule-f0f9d16c2d45c2a40f20bad1f84e2c6cdaad7928fcf033dc6b8c2ffff3f6b10d": "DEFINITION",
    "rule-2337b981dde3e7f5b878ce7ffbb3f2c1c87d9b3c9777edc1dbeab1aeeba99ca5": "DOMAIN_LEMMA",
    "rule-b4cd16bb262eb62089f82976d9f4fde2111bb34eaa3c93afe9502b42d0c2119a": "DEFINITION",
}
recorded_classes = {
    rule["source_rule_id"]: rule["classification"]
    for rule in discovery["rules"]
}
assert independent_classes == recorded_classes
for rule in inventory["rules"]:
    if "simplification" in rule["attributes"]:
        assert independent_classes[rule["source_rule_id"]] in {
            "DEFINITION",
            "DOMAIN_LEMMA",
        }

input_manifest = load("/reference/klean-generation/input-manifest.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
assert target is not None
assert target == generator_manifest["target"]
assert target == resolution["target"]
assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert (
    input_manifest["verification_sha256"]
    == inventory["verification_sha256"]
)
assert (
    input_manifest["stage1_workspace_sha256"]
    == observed_hashes["stage1_export_sha256"]
)
assert (
    input_manifest["stage3_discovery_manifest_sha256"]
    == observed_hashes["discovery_manifest_sha256"]
)

source_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_rule_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
assert source_rule_ids == mapped_rule_ids == obligation_rule_ids
assert len(source_rule_ids) == len(set(source_rule_ids)) == 1
assert generator_manifest["obligation_count"] == len(obligation_rule_ids)
assert generator_manifest["obligation_map_sha256"] == file_sha256(
    "/reference/klean-generation/generated/obligation-map.json"
)

expected_definition = klean_export.expected_target_definition(obligation_map)
assert expected_definition is not None
assert (
    klean_export.sha256_text(expected_definition)
    == target["definition_sha256"]
)
assert klean_export.sha256_text(target["statement"]) == target[
    "statement_sha256"
]

candidate_sources: list[tuple[str, str]] = []
for path in sorted(Path("/candidate").rglob("*.lean")):
    assert path.is_file() and not path.is_symlink()
    relative = path.relative_to("/candidate").as_posix()
    candidate_sources.append((relative, path.read_text()))
for relative, text in candidate_sources:
    forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text)
    assert not forbidden, (relative, forbidden)
candidate_text = "\n".join(text for _, text in candidate_sources)
parameter_name = target["parameters"][0]["name"]
parameter_defs = re.findall(
    rf"(?m)^\s*def\s+{re.escape(parameter_name)}\s*:", candidate_text
)
assert len(parameter_defs) == 1
assert not re.search(r"(?m)^\s*def\s+targetStatement\b", candidate_text)
proof_text = Path("/candidate/Proof.lean").read_text()
final_types = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
assert len(final_types) == 1
assert " ".join(final_types[0].split()) == " ".join(
    target["statement"].split()
)

output = {
    "audit_mode_environment": os.environ.get("AUDIT_MODE"),
    "audit_mode_input": resolution["mode"],
    "audit_input_sha256": resolution_digest,
    "hash_comparison": hash_comparison,
    "lean_invocation_hash_note": (
        "recorded but its invocation tree is not among the mounted inputs"
    ),
    "stage1_source_file_count": len(stage1_source_hashes),
    "stage1_source_hashes_exact_match": True,
    "producer_hashes": producer_hashes,
    "producer_image_id": source_manifest["generator_image_id"],
    "inventory": inventory,
    "inventory_ids_bijective_and_ordered": True,
    "independent_classes": independent_classes,
    "validated_discovery_partitions": {
        key: [
            rule["source_rule_id"] for rule in validated_discovery[key]
        ]
        for key in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    },
    "source_rule_ids": source_rule_ids,
    "obligation_rule_ids": obligation_rule_ids,
    "target": target,
    "expected_target_definition": expected_definition,
    "candidate_sources": [relative for relative, _ in candidate_sources],
    "candidate_forbidden_tokens": [],
    "candidate_parameter_definition_count": len(parameter_defs),
    "candidate_target_definition_count": 0,
    "candidate_final_exact_target": True,
}
print(json.dumps(output, indent=2, sort_keys=True))
