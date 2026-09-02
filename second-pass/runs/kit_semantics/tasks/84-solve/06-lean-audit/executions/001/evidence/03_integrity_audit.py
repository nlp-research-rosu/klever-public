#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path

import klean_export as producer_export
from tools import pipeline_contract
from tools.k_rule_inventory import inventory_verification


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def show(label: str, actual, expected=None) -> None:
    if expected is None:
        print(f"{label}={actual}")
    else:
        print(f"{label}: actual={actual} expected={expected} match={actual == expected}")


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = json.loads(obligation_map_path.read_text())
discovery_path = Path("/reference/lemma-discovery.json")
discovery = json.loads(discovery_path.read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
reconstructed = inventory_verification(Path("/reference/k-proof"))

print("## launcher mode")
show("environment_AUDIT_MODE", __import__("os").environ.get("AUDIT_MODE"), resolution["mode"])
show("problem_id", resolution["problem_id"], "84-solve")
show("condition", resolution["condition"], "kit-semantics")
show("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

print("## mounted tree and file hashes")
tree_bindings = [
    ("k_workspace_sha256", Path("/reference/k-proof")),
    ("k_audit_sha256", Path("/reference/k-audit")),
    ("klean_generation_sha256", Path("/reference/klean-generation")),
    ("generation_producer_sources_sha256", Path("/reference/generation-tools")),
    ("lean_workspace_sha256", Path("/candidate")),
]
for field, path in tree_bindings:
    show(field, pipeline_contract.sha256_tree(path), hashes[field])
show(
    "stage1_export_sha256",
    producer_export.tree_digest(Path("/reference/k-proof")),
    hashes["stage1_export_sha256"],
)
show(
    "discovery_manifest_sha256",
    file_sha256(discovery_path),
    hashes["discovery_manifest_sha256"],
)
show(
    "generated_tree_sha256",
    producer_export.tree_digest(Path("/reference/klean-generation/generated")),
    hashes["generated_tree_sha256"],
)
print(
    "lean_invocation_sha256=NOT_RECOMPUTABLE:"
    " launcher records it but no independent lean-invocation mount was supplied"
)

print("## Stage 1 per-file source hash map")
stage1_expected = resolution["stage1_source_hashes"]
stage1_root = Path("/reference/k-proof")
actual_files = sorted(
    path.relative_to(stage1_root).as_posix()
    for path in stage1_root.rglob("*")
    if path.is_file() and not path.is_symlink()
)
missing = sorted(set(stage1_expected) - set(actual_files))
extra = sorted(set(actual_files) - set(stage1_expected))
mismatched = []
for relative, expected in stage1_expected.items():
    path = stage1_root / relative
    if path.is_file() and not path.is_symlink():
        actual = file_sha256(path)
        if actual != expected:
            mismatched.append((relative, actual, expected))
show("stage1_expected_file_count", len(stage1_expected))
show("stage1_actual_regular_file_count", len(actual_files))
show("stage1_missing_files", missing)
show("stage1_extra_files", extra)
show("stage1_mismatched_files", mismatched)

print("## producer source provenance")
for name in ("klean_export.py", "klean.py"):
    actual = file_sha256(Path("/reference/generation-tools") / name)
    show(f"{name}_sha256_vs_source_manifest", actual, source_manifest["files"][name])
show(
    "klean_export.py_sha256_vs_generator_manifest",
    file_sha256(Path("/reference/generation-tools/klean_export.py")),
    generator["exporter_sha256"],
)
show(
    "klean.py_sha256_vs_generator_manifest",
    file_sha256(Path("/reference/generation-tools/klean.py")),
    generator["klean_py_sha256"],
)
recorded_sources_name = Path(resolution["generation_producer_sources"]).name
recorded_image_id = "sha256:" + recorded_sources_name
show(
    "source_manifest_generator_image_id_vs_audit_input_path",
    source_manifest["generator_image_id"],
    recorded_image_id,
)
show(
    "generator_manifest_image_id_vs_audit_input_path",
    generator["provenance"]["generator_image_id"],
    recorded_image_id,
)

print("## Stage 3 inventory binding")
show("verification_sha256", reconstructed["verification_sha256"], input_manifest["verification_sha256"])
show("inventory_sha256_reconstructed_vs_discovery", reconstructed["inventory_sha256"], discovery["inventory_sha256"])
show("inventory_sha256_reconstructed_vs_input_manifest", reconstructed["inventory_sha256"], input_manifest["inventory_sha256"])
show("inventory_sha256_reconstructed_vs_generator", reconstructed["inventory_sha256"], generator["provenance"]["inventory_sha256"])
show(
    "discovery_manifest_hash_vs_input_manifest",
    file_sha256(discovery_path),
    input_manifest["stage3_discovery_manifest_sha256"],
)
show(
    "discovery_manifest_hash_vs_generator",
    file_sha256(discovery_path),
    generator["provenance"]["stage3_discovery_manifest_sha256"],
)
show(
    "stage1_export_hash_vs_input_manifest",
    producer_export.tree_digest(stage1_root),
    input_manifest["stage1_workspace_sha256"],
)
show(
    "stage1_export_hash_vs_generator",
    producer_export.tree_digest(stage1_root),
    generator["provenance"]["stage1_workspace_sha256"],
)

reconstructed_by_id = {rule["source_rule_id"]: rule for rule in reconstructed["rules"]}
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
reconstructed_ids = [rule["source_rule_id"] for rule in reconstructed["rules"]]
show("discovery_order_equals_reconstructed_order", discovery_ids, reconstructed_ids)
show(
    "discovery_duplicate_ids",
    sorted(key for key, value in Counter(discovery_ids).items() if value != 1),
    [],
)
for collection_name in ("definitions", "source_rules", "operational_rules", "proved_derived_lemmas"):
    entries = input_manifest[collection_name]
    for entry in entries:
        source = reconstructed_by_id[entry["source_rule_id"]]
        exact_fields = {
            key: entry[key] == source[key]
            for key in (
                "source_rule_id",
                "normalized_sha256",
                "module",
                "start_line",
                "end_line",
                "attributes",
                "text",
            )
        }
        print(
            f"input_manifest_{collection_name}_{entry['source_rule_id']}_"
            f"exact_source_fields={exact_fields}"
        )

print("## Stage 4 obligation and target hashes")
show(
    "obligation_map_sha256",
    file_sha256(obligation_map_path),
    generator["obligation_map_sha256"],
)
show(
    "generated_tree_sha256_vs_generator",
    producer_export.tree_digest(Path("/reference/klean-generation/generated")),
    generator["generated_tree_sha256"],
)
show(
    "generated_tree_sha256_vs_export_result",
    producer_export.tree_digest(Path("/reference/klean-generation/generated")),
    export_result["generated_tree_sha256"],
)
show(
    "obligation_count_map_vs_generator",
    len(obligation_map["obligations"]),
    generator["obligation_count"],
)
show(
    "obligation_count_map_vs_export_result",
    len(obligation_map["obligations"]),
    export_result["obligation_count"],
)
source_rule_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
independent_domain_ids = [
    "rule-6c41bb59ad1d9e21227b52ea306abb7b34b84c951d9e8989d939daab63c61f3a",
    "rule-6344cd09b31e724e82ac03ee3cc9f48110eb927e01daa5195f7b27029c68dc3d",
]
show("source_rule_ids_vs_independent_domain_ids", source_rule_ids, independent_domain_ids)
show("obligation_ids_vs_independent_domain_ids", obligation_ids, independent_domain_ids)
show(
    "obligation_duplicate_ids",
    sorted(key for key, value in Counter(obligation_ids).items() if value != 1),
    [],
)
for obligation in obligation_map["obligations"]:
    source = reconstructed_by_id[obligation["source_rule_id"]]
    show(
        f"{obligation['source_rule_id']}_lean_conjunct_sha256",
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest(),
        obligation["lean_conjunct_sha256"],
    )
    show(
        f"{obligation['source_rule_id']}_normalized_sha256",
        obligation["normalized_sha256"],
        source["normalized_sha256"],
    )
    show(
        f"{obligation['source_rule_id']}_source_span",
        obligation["source_span"],
        {"start_line": source["start_line"], "end_line": source["end_line"]},
    )

computed_target = producer_export.target_statement(
    Path("/reference/klean-generation/generated")
)
show("computed_target_vs_generator_manifest", computed_target, generator["target"])
show("computed_target_vs_audit_input", computed_target, resolution["target"])
show(
    "computed_target_vs_audit_preflight",
    computed_target,
    resolution["stage4_preflight"]["target"],
)
returned_preflight = json.loads(
    Path("/audit-output/evidence/preflight-returned-evidence.json").read_text()
)
show("computed_target_vs_rerun_preflight", computed_target, returned_preflight["target"])
show(
    "toolchain_lock_vs_generator",
    json.loads(Path("/reference/klean-toolchain.lock.json").read_text()),
    generator["toolchain"],
)
