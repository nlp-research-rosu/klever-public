#!/usr/bin/env python3
"""Independent structural checks for the 8-sum-product Stage 3/4/5 audit."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract


STAGE1 = Path("/reference/k-proof")
STAGE2 = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line(label: str, actual: object, expected: object) -> None:
    print(
        f"{label}: {'MATCH' if actual == expected else 'MISMATCH'}\n"
        f"  actual={actual}\n"
        f"  expected={expected}"
    )


audit = load(AUDIT_INPUT)["resolution"]
audit_hashes = audit["hashes"]
generator = load(GENERATION / "generator-manifest.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
discovery = load(DISCOVERY)

print("== launcher mode ==")
line("AUDIT_MODE vs audit input", os.environ.get("AUDIT_MODE"), audit["mode"])
line("problem", audit["problem_id"], "8-sum-product")
line("condition", audit["condition"], "kit-semantics")
line("semantics mode", audit["semantics_mode"], "SUPPLIED_SEMANTICS")

print("\n== producer provenance ==")
producer_files = {
    "klean.py": file_hash(PRODUCERS / "klean.py"),
    "klean_export.py": file_hash(PRODUCERS / "klean_export.py"),
}
line("producer file hashes vs source manifest", producer_files, source_manifest["files"])
line(
    "producer file hashes vs generator manifest",
    producer_files,
    {
        "klean.py": generator["klean_py_sha256"],
        "klean_export.py": generator["exporter_sha256"],
    },
)
image_id = generator["provenance"]["generator_image_id"]
line("image ID generator vs source manifest", image_id, source_manifest["generator_image_id"])
line(
    "image ID vs audit-recorded source bundle basename",
    image_id.removeprefix("sha256:"),
    Path(audit["generation_producer_sources"]).name,
)
line(
    "producer bundle tree hash",
    pipeline_contract.sha256_tree(PRODUCERS),
    audit_hashes["generation_producer_sources_sha256"],
)

print("\n== recorded artifact hashes ==")
artifact_hashes = {
    "discovery_manifest_sha256": file_hash(DISCOVERY),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "k_audit_sha256": pipeline_contract.sha256_tree(STAGE2),
    "k_workspace_sha256": pipeline_contract.sha256_tree(STAGE1),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "stage1_export_sha256": klean_export.tree_digest(STAGE1),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
}
for name, actual in artifact_hashes.items():
    line(name, actual, audit_hashes[name])

recorded_stage1_files = audit["stage1_source_hashes"]
observed_stage1_files = {
    path.relative_to(STAGE1).as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(STAGE1, "Stage 1")
}
line(
    "Stage 1 per-file path set",
    sorted(observed_stage1_files),
    sorted(recorded_stage1_files),
)
bad_stage1_files = {
    name: {"actual": observed_stage1_files.get(name), "expected": expected}
    for name, expected in recorded_stage1_files.items()
    if observed_stage1_files.get(name) != expected
}
line("Stage 1 per-file hash mismatches", bad_stage1_files, {})

print("\n== trusted rule inventory reconstruction ==")
inventory = k_rule_inventory.inventory_verification(STAGE1)
print(json.dumps(inventory, indent=2, sort_keys=True))
line("inventory hash vs discovery", inventory["inventory_sha256"], discovery["inventory_sha256"])
line("inventory hash vs Stage 4 input", inventory["inventory_sha256"], input_manifest["inventory_sha256"])

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
line("ordered inventory/discovery IDs", inventory_ids, discovery_ids)
line("inventory ID duplicates", [key for key, count in Counter(inventory_ids).items() if count != 1], [])
line("discovery ID duplicates", [key for key, count in Counter(discovery_ids).items() if count != 1], [])

for index, (source, classified) in enumerate(zip(inventory["rules"], discovery["rules"], strict=True), 1):
    print(
        f"rule[{index}] {source['source_rule_id']} "
        f"{source['module']}:{source['start_line']}-{source['end_line']} "
        f"normalized_sha256={source['normalized_sha256']} "
        f"classification={classified['classification']} "
        f"attributes={source['attributes']}"
    )
    print(source["text"])

print("\n== independently selected domain set and obligation bijection ==")
independent_domain_ids = [
    "rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43",
    "rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081",
    "rule-3efffca8ed723c4a95578d5fda655b02240729a8ee1b5bd9b6eaab14655f86c0",
    "rule-85c5006f98f122cfdf76b29a11f55cc1643ff616b63512d8cd829b4edc9287c4",
]
discovery_domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
source_rule_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
line("independent domain IDs vs discovery", independent_domain_ids, discovery_domain_ids)
line("independent domain IDs vs source_rules", independent_domain_ids, source_rule_ids)
line("independent domain IDs vs obligations", independent_domain_ids, obligation_ids)
line("obligation duplicate IDs", [key for key, count in Counter(obligation_ids).items() if count != 1], [])
line("generator obligation count", len(obligation_ids), generator["obligation_count"])

inventory_by_id = {entry["source_rule_id"]: entry for entry in inventory["rules"]}
for source_rule, obligation in zip(
    obligation_map["source_rules"], obligation_map["obligations"], strict=True
):
    frozen = inventory_by_id[source_rule["source_rule_id"]]
    print(f"obligation {obligation['source_rule_id']}")
    line(
        "  source span",
        obligation["source_span"],
        {"start_line": frozen["start_line"], "end_line": frozen["end_line"]},
    )
    line("  normalized hash", obligation["normalized_sha256"], frozen["normalized_sha256"])
    line(
        "  conjunct hash",
        obligation["lean_conjunct_sha256"],
        klean_export.sha256_text(obligation["lean_conjunct"]),
    )
    print(f"  conjunct={obligation['lean_conjunct']}")

print("\n== fixed target identity ==")
observed_target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)
line("target vs generator manifest", observed_target, generator["target"])
line("target vs audit input", observed_target, audit["target"])
line(
    "expected target definition hash",
    klean_export.sha256_text(expected_definition),
    observed_target["definition_sha256"],
)
line(
    "obligation map file hash",
    file_hash(GENERATED / "obligation-map.json"),
    generator["obligation_map_sha256"],
)
line("generated tree hash vs generator", artifact_hashes["generated_tree_sha256"], generator["generated_tree_sha256"])

parameter_rule_union = sorted(
    {
        source_rule_id
        for parameter in obligation_map["trust_parameters"]
        for source_rule_id in parameter["source_rule_ids"]
    }
)
line("parameter source-rule union", parameter_rule_union, sorted(independent_domain_ids))

print("\nALL_STRUCTURAL_COMPARISONS_COMPLETED")
