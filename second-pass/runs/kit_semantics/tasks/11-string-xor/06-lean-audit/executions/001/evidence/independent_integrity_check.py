#!/usr/bin/env python3
"""Independent structural and hash checks for the frozen Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


K_PROOF = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT_PATH = Path("/audit-input.json")


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    assert isinstance(document, dict), path
    return document


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equal(label: str, observed: object, expected: object) -> None:
    if observed != expected:
        raise AssertionError(
            f"{label}: observed={observed!r}, expected={expected!r}"
        )
    rendered = repr(observed)
    if len(rendered) > 500:
        encoded = json.dumps(
            observed, sort_keys=True, separators=(",", ":")
        ).encode()
        rendered = (
            f"<{type(observed).__name__} canonical_sha256="
            f"{hashlib.sha256(encoded).hexdigest()} size={len(observed)}>"
        )
    print(f"PASS {label}: {rendered}")


audit_input = load(AUDIT_INPUT_PATH)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
equal(
    "resolved_input_sha256",
    audit_input["resolved_input_sha256"],
    resolved_digest,
)
equal("launcher mode", resolution["mode"], "CLASSIFICATION_ONLY")
equal("launcher semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
equal("launcher target", resolution["target"], None)
equal("launcher Stage 5 result", resolution["stage5_result"], None)
equal("launcher Lean workspace", resolution["lean_workspace"], None)
equal("launcher Lean invocation", resolution["lean_invocation"], None)
equal("candidate absent", Path("/candidate").exists(), False)

observed_stage1_files = {
    path.relative_to(K_PROOF).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_PROOF, "Stage 1 source workspace"
    )
}
equal(
    "Stage 1 file-hash key set",
    sorted(observed_stage1_files),
    sorted(resolution["stage1_source_hashes"]),
)
equal(
    "all Stage 1 per-file hashes",
    observed_stage1_files,
    resolution["stage1_source_hashes"],
)
print(f"PASS Stage 1 per-file hash count: {len(observed_stage1_files)}")

hashes = resolution["hashes"]
equal(
    "Stage 1 complete tree hash",
    pipeline_contract.sha256_tree(K_PROOF),
    hashes["k_workspace_sha256"],
)
equal(
    "Stage 1 deterministic-export tree hash",
    klean_export.tree_digest(K_PROOF),
    hashes["stage1_export_sha256"],
)
equal(
    "Stage 3 discovery file hash",
    sha256_file(DISCOVERY_PATH),
    hashes["discovery_manifest_sha256"],
)
equal(
    "selected Stage 2 tree hash",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    hashes["k_audit_sha256"],
)
equal(
    "selected Stage 4 tree hash",
    pipeline_contract.sha256_tree(GENERATION),
    hashes["klean_generation_sha256"],
)
equal(
    "producer-source tree hash",
    pipeline_contract.sha256_tree(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)
equal(
    "generated-project tree hash",
    klean_export.tree_digest(GENERATED),
    hashes["generated_tree_sha256"],
)
equal("launcher Lean tree hash", hashes["lean_workspace_sha256"], None)
equal("launcher Lean invocation hash", hashes["lean_invocation_sha256"], None)

inventory = inventory_verification(K_PROOF)
discovery = load(DISCOVERY_PATH)
inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [rule["source_rule_id"] for rule in inventory_rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery_rules]
equal("inventory/discovery rule count", len(discovery_ids), len(inventory_ids))
equal("inventory identity order", discovery_ids, inventory_ids)
equal("inventory IDs unique", len(set(discovery_ids)), len(discovery_ids))
equal(
    "inventory hash",
    discovery["inventory_sha256"],
    inventory["inventory_sha256"],
)
for position, rule in enumerate(inventory_rules):
    equal(
        f"rule {position} source_rule_id derives from normalized hash",
        rule["source_rule_id"],
        "rule-" + rule["normalized_sha256"],
    )
print("PASS no omitted, duplicated, extra, or reordered Stage 3 rule identities")

allowed = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}
for entry in discovery_rules:
    if entry["classification"] not in allowed:
        raise AssertionError(f"unknown classification: {entry}")
class_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery_rules
}
for rule in inventory_rules:
    if (
        "simplification" in rule["attributes"]
        and class_by_id[rule["source_rule_id"]]
        not in {"DEFINITION", "DOMAIN_LEMMA"}
    ):
        raise AssertionError(
            f"simplification has forbidden classification: {rule}"
        )
print("PASS every simplification is classified DEFINITION or DOMAIN_LEMMA")

input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)
export_result = load(GENERATION / "export-result.json")
preflight = load(GENERATION / "preflight.json")
toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))

enriched = []
discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery_rules
}
for rule in inventory_rules:
    merged = dict(rule)
    merged.update(discovery_by_id[rule["source_rule_id"]])
    enriched.append(merged)
equal(
    "input-manifest DEFINITION partition",
    input_manifest["definitions"],
    [
        entry
        for entry in enriched
        if entry["classification"] == "DEFINITION"
    ],
)
equal(
    "input-manifest OPERATIONAL_RULE partition",
    input_manifest["operational_rules"],
    [
        entry
        for entry in enriched
        if entry["classification"] == "OPERATIONAL_RULE"
    ],
)
equal(
    "input-manifest PROVED_DERIVED_LEMMA partition",
    input_manifest["proved_derived_lemmas"],
    [
        entry
        for entry in enriched
        if entry["classification"] == "PROVED_DERIVED_LEMMA"
    ],
)

declared_domain_rules = [
    {
        **entry,
        "inventory_sha256": inventory["inventory_sha256"],
        "discovery_manifest_sha256": sha256_file(DISCOVERY_PATH),
    }
    for entry in enriched
    if entry["classification"] == "DOMAIN_LEMMA"
]
equal("declared DOMAIN_LEMMA set", declared_domain_rules, [])
equal("input-manifest source_rules", input_manifest["source_rules"], declared_domain_rules)
equal("obligation-map source_rules", obligation_map["source_rules"], declared_domain_rules)
equal("obligation-map obligations", obligation_map["obligations"], [])
equal("obligation-map trust parameters", obligation_map["trust_parameters"], [])
equal("generator obligation count", generator_manifest["obligation_count"], 0)
equal("export obligation count", export_result["obligation_count"], 0)
equal("preflight obligation count", preflight["obligation_count"], 0)
equal("generator target", generator_manifest["target"], None)
equal("preflight target", preflight["target"], None)
equal("generated target statement", klean_export.target_statement(GENERATED), None)
equal("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
equal("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
equal(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)

equal(
    "input frozen tree hash",
    input_manifest["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
equal(
    "input Stage 1 tree hash",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
equal(
    "input Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
equal(
    "input verification hash",
    input_manifest["verification_sha256"],
    inventory["verification_sha256"],
)
equal(
    "input inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)
equal(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
equal(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    sha256_file(obligation_map_path),
)
equal("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)
equal(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
equal(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
equal(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
equal(
    "export Stage 1 hash",
    export_result["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
equal(
    "export Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
equal(
    "export generated tree hash",
    export_result["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
equal(
    "export trust inventory hash",
    export_result["trust_inventory_sha256"],
    sha256_file(GENERATION / "trust-inventory.json"),
)

source_manifest = load(PRODUCERS / "source-manifest.json")
expected_producer_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
equal("producer source manifest schema", source_manifest["schema_version"], 1)
equal(
    "producer image ID source/generator",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
equal("producer manifest file map", source_manifest["files"], expected_producer_files)
equal(
    "producer bundle entries",
    sorted(path.name for path in PRODUCERS.iterdir()),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
for name, digest in expected_producer_files.items():
    equal(f"producer file hash {name}", sha256_file(PRODUCERS / name), digest)
image_key = source_manifest["generator_image_id"].removeprefix("sha256:")
equal(
    "launcher producer path/image binding",
    Path(resolution["generation_producer_sources"]).name,
    image_key,
)

print("ALL INDEPENDENT INTEGRITY CHECKS PASSED")
