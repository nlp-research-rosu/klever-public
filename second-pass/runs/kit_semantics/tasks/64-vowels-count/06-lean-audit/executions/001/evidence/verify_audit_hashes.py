#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.stage6_resolution_contract import verify_audit_input


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


failures: list[str] = []


def check(label: str, actual: object, expected: object) -> None:
    ok = actual == expected
    print(f"{label}: {'OK' if ok else 'MISMATCH'}")
    if isinstance(actual, (str, int, type(None), bool)):
        print(f"  actual:   {actual}")
        print(f"  expected: {expected}")
    if not ok:
        failures.append(label)


audit_document = json.loads(Path("/audit-input.json").read_bytes())
resolution, resolved_digest = verify_audit_input(audit_document)
print(f"resolved_input_sha256 verified: {resolved_digest}")
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem_id", resolution["problem_id"], "64-vowels-count")
check("condition", resolution["condition"], "kit-semantics")
check("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

hashes = resolution["hashes"]
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")

check(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(k_workspace),
    hashes["k_workspace_sha256"],
)
check(
    "stage1_export_sha256",
    klean_export.tree_digest(k_workspace),
    hashes["stage1_export_sha256"],
)
check(
    "discovery_manifest_sha256",
    file_sha256(discovery),
    hashes["discovery_manifest_sha256"],
)
check(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(k_audit),
    hashes["k_audit_sha256"],
)
check(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(generation),
    hashes["klean_generation_sha256"],
)
check(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(producer_sources),
    hashes["generation_producer_sources_sha256"],
)
check(
    "generated_tree_sha256",
    klean_export.tree_digest(generated),
    hashes["generated_tree_sha256"],
)
check("lean_workspace_sha256", None, hashes["lean_workspace_sha256"])
check("lean_invocation_sha256", None, hashes["lean_invocation_sha256"])

actual_source_hashes = {
    path.relative_to(k_workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "audit Stage 1 source workspace"
    )
}
recorded_source_hashes = resolution["stage1_source_hashes"]
check(
    "stage1_source_hash_keyset",
    sorted(actual_source_hashes),
    sorted(recorded_source_hashes),
)
source_mismatches = sorted(
    relative
    for relative in actual_source_hashes.keys() & recorded_source_hashes.keys()
    if actual_source_hashes[relative] != recorded_source_hashes[relative]
)
check("stage1_source_hash_values", source_mismatches, [])
print(f"stage1 regular files checked: {len(actual_source_hashes)}")

check(
    "selected_k_audit_artifact_sha256",
    hashes["k_audit_sha256"],
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selected_generation_artifact_sha256",
    hashes["klean_generation_sha256"],
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)

source_manifest = json.loads(
    (producer_sources / "source-manifest.json").read_bytes()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_bytes()
)
input_manifest = json.loads((generation / "input-manifest.json").read_bytes())
export_result = json.loads((generation / "export-result.json").read_bytes())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_bytes())
trust_inventory_path = generation / "trust-inventory.json"

exporter_hash = file_sha256(producer_sources / "klean_export.py")
klean_py_hash = file_sha256(producer_sources / "klean.py")
check(
    "producer klean_export.py versus source manifest",
    exporter_hash,
    source_manifest["files"]["klean_export.py"],
)
check(
    "producer klean_export.py versus generator manifest",
    exporter_hash,
    generator_manifest["exporter_sha256"],
)
check(
    "producer klean.py versus source manifest",
    klean_py_hash,
    source_manifest["files"]["klean.py"],
)
check(
    "producer klean.py versus generator manifest",
    klean_py_hash,
    generator_manifest["klean_py_sha256"],
)
image_id = generator_manifest["provenance"]["generator_image_id"]
check(
    "generator image ID versus source manifest",
    image_id,
    source_manifest["generator_image_id"],
)
check(
    "generator image ID versus audit-input producer path",
    image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)

stage1_export_hash = hashes["stage1_export_sha256"]
discovery_hash = hashes["discovery_manifest_sha256"]
generated_hash = hashes["generated_tree_sha256"]
for label, actual, expected in (
    (
        "input manifest frozen_input_sha256",
        input_manifest["frozen_input_sha256"],
        stage1_export_hash,
    ),
    (
        "input manifest stage1_workspace_sha256",
        input_manifest["stage1_workspace_sha256"],
        stage1_export_hash,
    ),
    (
        "input manifest discovery hash",
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "generator provenance Stage 1 hash",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        stage1_export_hash,
    ),
    (
        "generator provenance discovery hash",
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "generator generated-tree hash",
        generator_manifest["generated_tree_sha256"],
        generated_hash,
    ),
    (
        "generator obligation-map hash",
        generator_manifest["obligation_map_sha256"],
        file_sha256(obligation_map_path),
    ),
    (
        "export result frozen-input hash",
        export_result["frozen_input_sha256"],
        stage1_export_hash,
    ),
    (
        "export result discovery hash",
        export_result["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "export result generated-tree hash",
        export_result["generated_tree_sha256"],
        generated_hash,
    ),
    (
        "export result trust-inventory hash",
        export_result["trust_inventory_sha256"],
        file_sha256(trust_inventory_path),
    ),
):
    check(label, actual, expected)

inventory = inventory_verification(k_workspace)
stage3 = json.loads(discovery.read_bytes())
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
stage3_ids = [entry["source_rule_id"] for entry in stage3["rules"]]
check("Stage 3 inventory hash", stage3["inventory_sha256"], inventory["inventory_sha256"])
check("Stage 3 exact ordered source-rule IDs", stage3_ids, inventory_ids)
check("input manifest inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check(
    "generator provenance inventory hash",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
domain_ids = [
    entry["source_rule_id"]
    for entry in stage3["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
check("domain-rule IDs", domain_ids, [])
check("obligation-map source rules", obligation_map["source_rules"], [])
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check("input-manifest source rules", input_manifest["source_rules"], [])
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("export-result obligation count", export_result["obligation_count"], 0)
check("generator target", generator_manifest["target"], None)
check("audit-input target", resolution["target"], None)
check("generated target declaration", klean_export.target_statement(generated), None)
check("Stage 5 candidate absent", Path("/candidate").exists(), False)
check(
    "stored Stage 4 preflight versus selected preflight",
    resolution["stage4_preflight"],
    json.loads((generation / "preflight.json").read_bytes()),
)

print("Stage 3 classifications in canonical order:")
for inventory_entry, stage3_entry in zip(inventory["rules"], stage3["rules"]):
    print(
        f"  {inventory_entry['start_line']}-{inventory_entry['end_line']} "
        f"{inventory_entry['source_rule_id']} "
        f"{stage3_entry['classification']}"
    )

print(f"TOTAL FAILURES: {len(failures)}")
for failure in failures:
    print(f"  {failure}")
raise SystemExit(1 if failures else 0)
