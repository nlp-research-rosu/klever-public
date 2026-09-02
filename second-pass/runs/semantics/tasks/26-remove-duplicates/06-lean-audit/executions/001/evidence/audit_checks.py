#!/usr/bin/env python3
"""Independent structural/hash checks for the 26-remove-duplicates audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import (
    canonical_json_sha256,
    verify_audit_input,
)


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
K_AUDIT = Path("/reference/k-audit")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict), path
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool, detail: object = "") -> None:
    if not condition:
        raise AssertionError(f"FAIL {label}: {detail}")
    print(f"PASS {label}: {detail}")


audit_document = read_json(AUDIT_INPUT)
resolution, resolved_digest = verify_audit_input(audit_document)
check(
    "resolved input canonical hash",
    resolved_digest == canonical_json_sha256(resolution),
    resolved_digest,
)
check("mode", resolution["mode"] == "CLASSIFICATION_ONLY", resolution["mode"])
check(
    "semantics mode",
    resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    resolution["semantics_mode"],
)

producer_manifest = read_json(PRODUCERS / "source-manifest.json")
generator_manifest = read_json(GENERATION / "generator-manifest.json")
input_manifest = read_json(GENERATION / "input-manifest.json")
export_result = read_json(GENERATION / "export-result.json")
obligation_map = read_json(GENERATED / "obligation-map.json")
recorded_preflight = read_json(GENERATION / "preflight.json")
toolchain_lock = read_json(TOOLCHAIN_LOCK)

producer_files = {
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.iterdir()
    if path.is_file() and not path.is_symlink()
}
check(
    "producer bundle exact file set",
    producer_files == {"klean_export.py", "klean.py", "source-manifest.json"},
    sorted(producer_files),
)
producer_hashes = {
    "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
    "klean.py": file_sha256(PRODUCERS / "klean.py"),
}
check(
    "producer source manifest file hashes",
    producer_manifest["files"] == producer_hashes,
    producer_hashes,
)
check(
    "producer hashes in generator manifest",
    generator_manifest["exporter_sha256"] == producer_hashes["klean_export.py"]
    and generator_manifest["klean_py_sha256"] == producer_hashes["klean.py"],
    producer_hashes,
)
generator_image_id = producer_manifest["generator_image_id"]
check(
    "immutable generator image agreement",
    generator_manifest["provenance"]["generator_image_id"] == generator_image_id
    and Path(resolution["generation_producer_sources"]).name
    == generator_image_id.removeprefix("sha256:"),
    generator_image_id,
)

recorded_hashes = resolution["hashes"]
observed_launcher_hashes = {
    "k_workspace_sha256": sha256_tree(WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": sha256_tree(K_AUDIT),
    "klean_generation_sha256": sha256_tree(GENERATION),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
for key, observed in observed_launcher_hashes.items():
    check(
        f"launcher hash {key}",
        recorded_hashes[key] == observed,
        observed,
    )

observed_source_hashes: dict[str, str] = {}
for directory, dirnames, filenames in os.walk(WORKSPACE, followlinks=False):
    directory_path = Path(directory)
    for name in dirnames:
        check(
            f"Stage 1 directory is not symlink {directory_path / name}",
            not (directory_path / name).is_symlink(),
        )
    for name in filenames:
        path = directory_path / name
        check(f"Stage 1 file is regular {path}", path.is_file() and not path.is_symlink())
        observed_source_hashes[path.relative_to(WORKSPACE).as_posix()] = file_sha256(path)
check(
    "complete Stage 1 source-hash map",
    observed_source_hashes == resolution["stage1_source_hashes"],
    f"{len(observed_source_hashes)} files",
)

inventory = inventory_verification(WORKSPACE)
discovery = read_json(DISCOVERY)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
check(
    "verification module closure",
    inventory["verification_modules"] == ["REMOVE-DUPLICATES-VERIFICATION"],
    inventory["verification_modules"],
)
check(
    "verification source hash",
    inventory["verification_sha256"]
    == resolution["stage1_source_hashes"]["verification.k"]
    == input_manifest["verification_sha256"],
    inventory["verification_sha256"],
)
check(
    "inventory whole hash",
    inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)

inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
discovery_ids = [entry["source_rule_id"] for entry in discovery_rules]
check("inventory contains seven rules", len(inventory_rules) == 7, len(inventory_rules))
check(
    "inventory IDs are unique",
    len(inventory_ids) == len(set(inventory_ids)),
    len(inventory_ids),
)
check(
    "Stage 3 exact ordered rule bijection",
    discovery_ids == inventory_ids and len(discovery_ids) == len(set(discovery_ids)),
    discovery_ids,
)
for rule in inventory_rules:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    check(
        f"rule normalized hash {rule['start_line']}-{rule['end_line']}",
        digest == rule["normalized_sha256"],
        digest,
    )
    check(
        f"rule source ID {rule['start_line']}-{rule['end_line']}",
        rule["source_rule_id"] == f"rule-{digest}",
        rule["source_rule_id"],
    )

independent_classifications = {
    source_rule_id: "DEFINITION" for source_rule_id in inventory_ids
}
for entry in discovery_rules:
    source_rule_id = entry["source_rule_id"]
    check(
        f"independent classification {source_rule_id}",
        entry["classification"] == independent_classifications[source_rule_id],
        entry["classification"],
    )
check(
    "validated discovery reproduces inventory",
    validated["inventory_sha256"] == inventory["inventory_sha256"]
    and [rule["source_rule_id"] for rule in validated["rules"]] == inventory_ids,
    validated["inventory_sha256"],
)

definition_ids = [entry["source_rule_id"] for entry in input_manifest["definitions"]]
check(
    "input-manifest definition ordering",
    definition_ids == inventory_ids,
    definition_ids,
)
check(
    "no recorded operational rules",
    input_manifest["operational_rules"] == [],
    input_manifest["operational_rules"],
)
check(
    "no recorded proved-derived lemmas",
    input_manifest["proved_derived_lemmas"] == [],
    input_manifest["proved_derived_lemmas"],
)

independent_domain_ids: list[str] = []
source_rule_ids = [
    entry["source_rule_id"] for entry in input_manifest["source_rules"]
]
mapped_source_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]
obligation_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
check(
    "independent domain set is empty",
    independent_domain_ids == [],
    independent_domain_ids,
)
check(
    "source-rule bijection",
    source_rule_ids == mapped_source_ids == obligation_ids == independent_domain_ids,
    {
        "input": source_rule_ids,
        "map": mapped_source_ids,
        "obligations": obligation_ids,
    },
)
check(
    "obligation IDs unique",
    len(obligation_ids) == len(set(obligation_ids)),
    obligation_ids,
)
check(
    "no trust parameters for absent obligations",
    obligation_map["trust_parameters"] == [],
    obligation_map["trust_parameters"],
)
check(
    "obligation-map hash",
    file_sha256(GENERATED / "obligation-map.json")
    == generator_manifest["obligation_map_sha256"],
    file_sha256(GENERATED / "obligation-map.json"),
)
check(
    "zero obligation counts",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == recorded_preflight["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"]
    == 0,
    0,
)
check(
    "KLEAN_NO_OBLIGATIONS status",
    export_result["status"]
    == recorded_preflight["status"]
    == resolution["stage4_preflight"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    export_result["status"],
)

trusted_target = klean_export.target_statement(GENERATED)
check(
    "fixed generated target is absent",
    trusted_target is None
    and generator_manifest["target"] is None
    and recorded_preflight["target"] is None
    and resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None,
    trusted_target,
)
check(
    "generator toolchain lock",
    generator_manifest["toolchain"] == toolchain_lock,
    toolchain_lock["lean_toolchain"],
)
check(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"]
    == observed_launcher_hashes["stage1_export_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == input_manifest["frozen_input_sha256"],
    generator_manifest["provenance"]["stage1_workspace_sha256"],
)
check(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == observed_launcher_hashes["discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"],
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
)
check(
    "generated tree provenance",
    generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == observed_launcher_hashes["generated_tree_sha256"],
    generator_manifest["generated_tree_sha256"],
)
check(
    "classification-only has no Stage 5 result",
    resolution["stage5_result"] is None
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None,
    None,
)
check("no mounted candidate", not Path("/candidate").exists(), "/candidate absent")

print("ALL STRUCTURAL AND HASH CHECKS PASSED")
