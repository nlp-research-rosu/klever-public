#!/usr/bin/env python3
"""Independent structural and provenance checks for the Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.stage6_resolution_contract import verify_audit_input


def read_json(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict)
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_tree_names(root: Path) -> list[str]:
    names: list[str] = []
    for path in sorted(root.iterdir()):
        mode = path.stat(follow_symlinks=False).st_mode
        assert stat.S_ISREG(mode), f"non-regular producer entry: {path}"
        names.append(path.name)
    return names


audit_input = read_json(Path("/audit-input.json"))
resolution, resolved_digest = verify_audit_input(audit_input)
assert resolution["mode"] == os.environ["AUDIT_MODE"] == "CLASSIFICATION_ONLY"
assert resolution["problem_id"] == "88-sort-array"
assert resolution["condition"] == "bare"
assert resolution["semantics_mode"] == "GENERATED_SEMANTICS"

inventory = inventory_verification(Path("/reference/k-proof"))
discovery = read_json(Path("/reference/lemma-discovery.json"))
verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()

assert inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"])
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
assert len(discovery["rules"]) == len(inventory["rules"]) == 11
inventory_ids = [item["source_rule_id"] for item in inventory["rules"]]
discovery_ids = [item["source_rule_id"] for item in discovery["rules"]]
assert discovery_ids == inventory_ids
assert len(set(discovery_ids)) == len(discovery_ids)
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    assert normalized_sha256 == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{normalized_sha256}"
    source_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip()
    assert source_span == rule["text"]

validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
assert [item["source_rule_id"] for item in validated["definitions"]] == inventory_ids
assert validated["operational_rules"] == []
assert validated["proved_derived_lemmas"] == []
assert validated["domain_lemmas"] == []
assert all(
    item["classification"] == "DEFINITION" for item in discovery["rules"]
)

for relative, expected in resolution["stage1_source_hashes"].items():
    assert sha256_file(Path("/reference/k-proof") / relative) == expected

hashes = resolution["hashes"]
assert pipeline_contract.sha256_tree(Path("/reference/k-proof")) == hashes[
    "k_workspace_sha256"
]
assert klean_export.tree_digest(Path("/reference/k-proof")) == hashes[
    "stage1_export_sha256"
]
assert sha256_file(Path("/reference/lemma-discovery.json")) == hashes[
    "discovery_manifest_sha256"
]
assert pipeline_contract.sha256_tree(Path("/reference/k-audit")) == hashes[
    "k_audit_sha256"
]
assert pipeline_contract.sha256_tree(Path("/reference/klean-generation")) == hashes[
    "klean_generation_sha256"
]
assert klean_export.tree_digest(
    Path("/reference/klean-generation/generated")
) == hashes["generated_tree_sha256"]
assert hashes["lean_workspace_sha256"] is None
assert hashes["lean_invocation_sha256"] is None

generator_manifest = read_json(
    Path("/reference/klean-generation/generator-manifest.json")
)
source_manifest = read_json(Path("/reference/generation-tools/source-manifest.json"))
producer_names = regular_tree_names(Path("/reference/generation-tools"))
assert producer_names == ["klean.py", "klean_export.py", "source-manifest.json"]
assert source_manifest["schema_version"] == 1
assert set(source_manifest) == {"schema_version", "generator_image_id", "files"}
assert source_manifest["files"] == {
    "klean.py": generator_manifest["klean_py_sha256"],
    "klean_export.py": generator_manifest["exporter_sha256"],
}
assert sha256_file(Path("/reference/generation-tools/klean.py")) == source_manifest[
    "files"
]["klean.py"]
assert sha256_file(
    Path("/reference/generation-tools/klean_export.py")
) == source_manifest["files"]["klean_export.py"]
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
assert source_manifest["generator_image_id"] == generator_image_id
assert (
    Path(resolution["generation_producer_sources"]).name
    == generator_image_id.removeprefix("sha256:")
)
assert pipeline_contract.sha256_tree(Path("/reference/generation-tools")) == hashes[
    "generation_producer_sources_sha256"
]

input_manifest = read_json(Path("/reference/klean-generation/input-manifest.json"))
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = read_json(obligation_map_path)
export_result = read_json(Path("/reference/klean-generation/export-result.json"))
recorded_preflight = read_json(Path("/reference/klean-generation/preflight.json"))
trust_inventory_path = Path("/reference/klean-generation/trust-inventory.json")
toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))
discovery_hash = sha256_file(Path("/reference/lemma-discovery.json"))
expected_source_rules = klean_export._domain_source_rules(validated, discovery_hash)

assert expected_source_rules == []
assert input_manifest["definitions"] == validated["definitions"]
assert input_manifest["operational_rules"] == validated["operational_rules"]
assert input_manifest["proved_derived_lemmas"] == validated[
    "proved_derived_lemmas"
]
assert input_manifest["source_rules"] == expected_source_rules
assert input_manifest["summary_functions"] == [
    {
        "argument_sorts": ["IntList"],
        "name": "expectedSort",
        "return_sort": "IntList",
    },
    {
        "argument_sorts": ["IntList"],
        "name": "endpointEven",
        "return_sort": "Bool",
    },
    {
        "argument_sorts": ["IntList"],
        "name": "nonnegative",
        "return_sort": "Bool",
    },
    {
        "argument_sorts": ["IntList"],
        "name": "ascending",
        "return_sort": "Bool",
    },
    {
        "argument_sorts": ["IntList"],
        "name": "descending",
        "return_sort": "Bool",
    },
]
assert input_manifest["verification_module"] == "MPY-VERIFICATION"
assert input_manifest["syntax_module"] == "MPY-SYNTAX"
assert obligation_map["source_rules"] == expected_source_rules
assert obligation_map["obligations"] == []
assert obligation_map["trust_parameters"] == []
assert generator_manifest["obligation_count"] == 0
assert generator_manifest["obligation_map_sha256"] == sha256_file(obligation_map_path)
assert klean_export.expected_target_definition(obligation_map) is None
assert klean_export.target_statement(
    Path("/reference/klean-generation/generated")
) is None
assert generator_manifest["target"] is None
assert resolution["target"] is None
assert recorded_preflight["target"] is None
assert resolution["stage4_preflight"] == recorded_preflight
assert not Path("/candidate").exists()

assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert generator_manifest["provenance"]["inventory_sha256"] == inventory[
    "inventory_sha256"
]
assert input_manifest["verification_sha256"] == inventory["verification_sha256"]
assert input_manifest["frozen_input_sha256"] == hashes["stage1_export_sha256"]
assert input_manifest["stage1_workspace_sha256"] == hashes["stage1_export_sha256"]
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
assert generator_manifest["provenance"]["stage1_workspace_sha256"] == hashes[
    "stage1_export_sha256"
]
assert generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] == (
    discovery_hash
)
assert generator_manifest["toolchain"] == toolchain_lock
assert generator_manifest["generated_tree_sha256"] == hashes[
    "generated_tree_sha256"
]
assert export_result["generated_tree_sha256"] == hashes["generated_tree_sha256"]
assert export_result["frozen_input_sha256"] == hashes["stage1_export_sha256"]
assert export_result["stage3_discovery_manifest_sha256"] == discovery_hash
assert export_result["trust_inventory_sha256"] == sha256_file(trust_inventory_path)
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert resolution["selections"]["klean_generation"]["status"] == (
    "KLEAN_NO_OBLIGATIONS"
)
assert resolution["selections"]["klean_generation"]["artifact_sha256"] == hashes[
    "klean_generation_sha256"
]
assert resolution["selections"]["k_audit"]["artifact_sha256"] == hashes[
    "k_audit_sha256"
]

print(f"resolved_input_sha256={resolved_digest}")
print(
    "inventory="
    f"{inventory['inventory_sha256']} rules={len(inventory['rules'])} "
    f"module_closure={inventory['verification_modules']}"
)
for index, rule in enumerate(inventory["rules"], start=1):
    print(
        f"rule[{index}] lines={rule['start_line']}-{rule['end_line']} "
        f"normalized_sha256={rule['normalized_sha256']} "
        f"id={rule['source_rule_id']}"
    )
print("stage3_order_bijection=PASS")
print("stage3_class_counts=DEFINITION:11 OPERATIONAL_RULE:0 "
      "PROVED_DERIVED_LEMMA:0 DOMAIN_LEMMA:0")
print(
    "producer="
    f"klean_export.py:{generator_manifest['exporter_sha256']} "
    f"klean.py:{generator_manifest['klean_py_sha256']}"
)
print(f"generator_image_id={generator_image_id}")
print(
    "tree_hashes="
    f"k_workspace:{hashes['k_workspace_sha256']} "
    f"stage1_export:{hashes['stage1_export_sha256']} "
    f"k_audit:{hashes['k_audit_sha256']} "
    f"klean_generation:{hashes['klean_generation_sha256']} "
    f"producer_sources:{hashes['generation_producer_sources_sha256']} "
    f"generated:{hashes['generated_tree_sha256']}"
)
print("source_rule_obligation_bijection=empty/empty PASS")
print("fixed_generated_target=null PASS")
print("stage5_candidate=absent PASS")
print("ALL_INDEPENDENT_STRUCTURAL_CHECKS_PASS")
