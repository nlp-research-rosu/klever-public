#!/usr/bin/env python3
"""Independent structural/hash reconstruction using the mounted trusted tools."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def read_json(path: str) -> dict:
    return json.loads(Path(path).read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool, detail: object = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"{status} {label}: {detail}")
    if not condition:
        raise SystemExit(1)


audit = read_json("/audit-input.json")
resolution = audit["resolution"]
discovery = read_json("/reference/lemma-discovery.json")
source_manifest = read_json("/reference/generation-tools/source-manifest.json")
generator = read_json("/reference/klean-generation/generator-manifest.json")
input_manifest = read_json("/reference/klean-generation/input-manifest.json")
export_result = read_json("/reference/klean-generation/export-result.json")
obligation_map = read_json(
    "/reference/klean-generation/generated/obligation-map.json"
)
preflight = read_json("/reference/klean-generation/preflight.json")

check("mode environment/file", os.environ.get("AUDIT_MODE") == resolution["mode"], resolution["mode"])
check("classification-only candidate absence", resolution["mode"] != "CLASSIFICATION_ONLY" or not Path("/candidate").exists())

hashes = resolution["hashes"]
actual_trees = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    "generated_tree_sha256": klean_export.tree_digest(Path("/reference/klean-generation/generated")),
}
for name, observed in actual_trees.items():
    check(f"audit-input {name}", hashes[name] == observed, observed)
check(
    "audit-input discovery_manifest_sha256",
    hashes["discovery_manifest_sha256"] == sha256(Path("/reference/lemma-discovery.json")),
    hashes["discovery_manifest_sha256"],
)

recorded_source_hashes = resolution["stage1_source_hashes"]
observed_source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): sha256(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
check(
    "Stage 1 source-file/hash bijection",
    recorded_source_hashes == observed_source_hashes,
    f"{len(observed_source_hashes)} files",
)

producer_files = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/generation-tools"), "producer bundle"
    )
)
check(
    "producer bundle exact file set",
    producer_files == ["klean.py", "klean_export.py", "source-manifest.json"],
    producer_files,
)
exporter_hash = sha256(Path("/reference/generation-tools/klean_export.py"))
klean_hash = sha256(Path("/reference/generation-tools/klean.py"))
check(
    "klean_export.py hash across source/generator manifests",
    exporter_hash == source_manifest["files"]["klean_export.py"] == generator["exporter_sha256"],
    exporter_hash,
)
check(
    "klean.py hash across source/generator manifests",
    klean_hash == source_manifest["files"]["klean.py"] == generator["klean_py_sha256"],
    klean_hash,
)
source_image = source_manifest["generator_image_id"]
generator_image = generator["provenance"]["generator_image_id"]
audit_bundle_key = Path(resolution["generation_producer_sources"]).name
check(
    "immutable generator image ID across source manifest/generator/audit input bundle",
    source_image == generator_image == f"sha256:{audit_bundle_key}",
    source_image,
)

inventory = inventory_verification(Path("/reference/k-proof"))
check("verification closure", inventory["verification_modules"] == ["VERIFICATION"], inventory["verification_modules"])
check("verification source hash", inventory["verification_sha256"] == input_manifest["verification_sha256"], inventory["verification_sha256"])
check("whole inventory hash discovery", inventory["inventory_sha256"] == discovery["inventory_sha256"], inventory["inventory_sha256"])
check("whole inventory hash input manifest", inventory["inventory_sha256"] == input_manifest["inventory_sha256"], inventory["inventory_sha256"])

check(
    "reconstructed/discovery ordered ID bijection",
    [rule["source_rule_id"] for rule in inventory["rules"]]
    == [rule["source_rule_id"] for rule in discovery["rules"]],
    f"{len(inventory['rules'])} ordered identities",
)
check(
    "reconstructed ID/normalized-hash identity",
    all(
        rule["source_rule_id"] == f"rule-{rule['normalized_sha256']}"
        for rule in inventory["rules"]
    ),
)
check(
    "no duplicate discovery IDs",
    len({rule["source_rule_id"] for rule in discovery["rules"]}) == len(discovery["rules"]),
)
check(
    "no duplicate reconstructed normalized hashes",
    len({rule["normalized_sha256"] for rule in inventory["rules"]}) == len(inventory["rules"]),
)
for index, (observed, classified) in enumerate(zip(inventory["rules"], discovery["rules"]), 1):
    print(
        f"RULE {index:02d} lines {observed['start_line']}-{observed['end_line']} "
        f"{observed['source_rule_id']} classification={classified['classification']} "
        f"attributes={observed['attributes']}"
    )

enriched_inventory = [
    observed
    | {
        "classification": classified["classification"],
        "rationale": classified["rationale"],
    }
    for observed, classified in zip(inventory["rules"], discovery["rules"])
]
check(
    "input definitions exact reconstructed/classified inventory",
    input_manifest["definitions"] == enriched_inventory,
    f"{len(discovery['rules'])} rules",
)
check("input source_rules empty", input_manifest["source_rules"] == [], input_manifest["source_rules"])
check("obligation-map source_rules empty", obligation_map["source_rules"] == [], obligation_map["source_rules"])
check("obligation-map obligations empty", obligation_map["obligations"] == [], obligation_map["obligations"])
check("obligation-map trust_parameters empty", obligation_map["trust_parameters"] == [], obligation_map["trust_parameters"])
check("generator obligation count zero", generator["obligation_count"] == 0, generator["obligation_count"])
check("generator target null", generator["target"] is None, generator["target"])
check("audit-input target null", resolution.get("target") is None, resolution.get("target"))
check("generated target file absent", not Path("/reference/klean-generation/generated/Klean132IsNested/Target.lean").exists())
check("generator obligation-map hash", generator["obligation_map_sha256"] == sha256(Path("/reference/klean-generation/generated/obligation-map.json")), generator["obligation_map_sha256"])
check("generator generated-tree hash", generator["generated_tree_sha256"] == actual_trees["generated_tree_sha256"], generator["generated_tree_sha256"])
check("input Stage 1 tree hash", input_manifest["stage1_workspace_sha256"] == actual_trees["stage1_export_sha256"], input_manifest["stage1_workspace_sha256"])
check("input frozen tree hash", input_manifest["frozen_input_sha256"] == actual_trees["stage1_export_sha256"], input_manifest["frozen_input_sha256"])
discovery_hash = sha256(Path("/reference/lemma-discovery.json"))
check("input discovery hash", input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash, discovery_hash)
check("generator provenance Stage 1", generator["provenance"]["stage1_workspace_sha256"] == actual_trees["stage1_export_sha256"])
check("generator provenance Stage 3", generator["provenance"]["stage3_discovery_manifest_sha256"] == discovery_hash)
check("generator provenance inventory", generator["provenance"]["inventory_sha256"] == inventory["inventory_sha256"])
trust_hash = sha256(Path("/reference/klean-generation/trust-inventory.json"))
check("export trust inventory hash", export_result["trust_inventory_sha256"] == trust_hash, trust_hash)
check("export no-obligations status/count", export_result["status"] == "KLEAN_NO_OBLIGATIONS" and export_result["obligation_count"] == 0)
check("export Stage 1 hash", export_result["frozen_input_sha256"] == actual_trees["stage1_export_sha256"])
check("export Stage 3 hash", export_result["stage3_discovery_manifest_sha256"] == discovery_hash)
check("export generated tree hash", export_result["generated_tree_sha256"] == actual_trees["generated_tree_sha256"])
check("preflight no-obligations status/count/target", preflight["status"] == "KLEAN_NO_OBLIGATIONS" and preflight["obligation_count"] == 0 and preflight["target"] is None)
check("embedded/file Stage 4 preflight identity", resolution["stage4_preflight"] == preflight)
check("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS")
check("no Stage 5 hashes", hashes["lean_workspace_sha256"] is None and hashes["lean_invocation_sha256"] is None)

print("ALL INTEGRITY CHECKS PASSED")
