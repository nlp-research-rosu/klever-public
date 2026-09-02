#!/usr/bin/env python3
"""Read-only, reproducible hash and inventory checks for this Stage 6 audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_equal(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} mismatch:\n  actual={actual!r}\n  expected={expected!r}"
        )
    print(f"OK {label}: {actual}")


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
print(f"OK signed audit-input envelope: {resolved_digest}")
require_equal(
    "launcher audit-input copy",
    file_sha256(Path("/audit-output/audit-input.json")),
    file_sha256(AUDIT_INPUT),
)
require_equal("AUDIT mode", resolution["mode"], "CLASSIFICATION_ONLY")
require_equal("semantics mode", resolution["semantics_mode"], "GENERATED_SEMANTICS")

recorded_hashes = resolution["hashes"]
tree_checks = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
for name, actual in tree_checks.items():
    require_equal(f"audit-input hashes.{name}", actual, recorded_hashes[name])

observed_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted frozen Stage 1 workspace"
    )
}
require_equal(
    "audit-input stage1_source_hashes",
    observed_source_hashes,
    resolution["stage1_source_hashes"],
)

generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(
        PRODUCERS, "mounted generation producer sources"
    )
)
require_equal(
    "producer bundle exact file set",
    producer_names,
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
producer_hashes = {
    "klean.py": file_sha256(PRODUCERS / "klean.py"),
    "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
}
require_equal("producer hashes vs source manifest", producer_hashes, source_manifest["files"])
require_equal(
    "klean.py hash vs generator manifest",
    producer_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)
require_equal(
    "klean_export.py hash vs generator manifest",
    producer_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
require_equal(
    "generator image ID vs source manifest",
    generator_image_id,
    source_manifest["generator_image_id"],
)
require_equal(
    "generator image ID vs audit-input producer path",
    generator_image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)

inventory = k_rule_inventory.inventory_verification(K_WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(K_WORKSPACE, DISCOVERY)
discovery_document = json.loads(DISCOVERY.read_text())
require_equal(
    "verification.k SHA-256",
    inventory["verification_sha256"],
    resolution["stage1_source_hashes"]["verification.k"],
)
require_equal(
    "inventory hash recomputation",
    k_rule_inventory.canonical_json_sha256(inventory["rules"]),
    inventory["inventory_sha256"],
)
require_equal(
    "inventory hash vs discovery",
    inventory["inventory_sha256"],
    discovery_document["inventory_sha256"],
)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery_document["rules"]]
require_equal("ordered inventory/discovery source-rule identity", classified_ids, canonical_ids)
require_equal("discovery source-rule uniqueness", len(set(classified_ids)), len(classified_ids))
require_equal("discovery/inventory rule count", len(classified_ids), len(canonical_ids))

verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
for index, rule in enumerate(inventory["rules"], start=1):
    source_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    require_equal(f"rule {index} source span text", source_text, rule["text"])
    normalized_hash = hashlib.sha256(
        " ".join(source_text.split()).encode()
    ).hexdigest()
    require_equal(f"rule {index} normalized SHA-256", normalized_hash, rule["normalized_sha256"])
    require_equal(f"rule {index} source_rule_id", f"rule-{normalized_hash}", rule["source_rule_id"])

print("CANONICAL_INVENTORY_JSON")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("VALIDATED_CLASSIFICATION_JSON")
print(
    json.dumps(
        {
            "definitions": validated["definitions"],
            "operational_rules": validated["operational_rules"],
            "proved_derived_lemmas": validated["proved_derived_lemmas"],
            "domain_lemmas": validated["domain_lemmas"],
        },
        indent=2,
        sort_keys=True,
    )
)

input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight_record = json.loads((GENERATION / "preflight.json").read_text())
discovery_hash = file_sha256(DISCOVERY)
expected_source_rules = klean_export._domain_source_rules(validated, discovery_hash)
require_equal(
    "audit-input selected K audit artifact hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    tree_checks["k_audit_sha256"],
)
require_equal(
    "audit-input selected Klean generation artifact hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    tree_checks["klean_generation_sha256"],
)
require_equal(
    "audit-input embedded Stage 4 preflight record",
    resolution["stage4_preflight"],
    preflight_record,
)
require_equal(
    "input-manifest frozen-input hash",
    input_manifest["frozen_input_sha256"],
    tree_checks["stage1_export_sha256"],
)
require_equal(
    "input-manifest Stage 1 hash",
    input_manifest["stage1_workspace_sha256"],
    tree_checks["stage1_export_sha256"],
)
require_equal(
    "input-manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    tree_checks["discovery_manifest_sha256"],
)
require_equal(
    "input-manifest verification.k hash",
    input_manifest["verification_sha256"],
    inventory["verification_sha256"],
)
require_equal(
    "input-manifest inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)
require_equal("independently selected DOMAIN_LEMMA source rules", expected_source_rules, [])
require_equal("input manifest source-rule bijection", input_manifest["source_rules"], expected_source_rules)
require_equal("obligation-map source-rule bijection", obligation_map["source_rules"], expected_source_rules)
require_equal("obligation-map obligations", obligation_map["obligations"], [])
require_equal("obligation-map trust parameters", obligation_map["trust_parameters"], [])
require_equal("generator obligation count", generator_manifest["obligation_count"], 0)
require_equal("export-result obligation count", export_result["obligation_count"], 0)
require_equal("recorded preflight obligation count", preflight_record["obligation_count"], 0)
require_equal("generator target", generator_manifest["target"], None)
require_equal("audit-input target", resolution["target"], None)
require_equal("recorded preflight target", preflight_record["target"], None)
require_equal("generated target discovery", klean_export.target_statement(GENERATED), None)
require_equal(
    "obligation-map SHA-256",
    file_sha256(GENERATED / "obligation-map.json"),
    generator_manifest["obligation_map_sha256"],
)
require_equal(
    "export-result frozen-input hash",
    export_result["frozen_input_sha256"],
    tree_checks["stage1_export_sha256"],
)
require_equal(
    "export-result Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    tree_checks["discovery_manifest_sha256"],
)
require_equal(
    "export-result generated-tree hash",
    export_result["generated_tree_sha256"],
    tree_checks["generated_tree_sha256"],
)
require_equal(
    "export-result trust-inventory hash",
    export_result["trust_inventory_sha256"],
    file_sha256(GENERATION / "trust-inventory.json"),
)
require_equal(
    "generator toolchain lock",
    generator_manifest["toolchain"],
    json.loads(Path("/reference/klean-toolchain.lock.json").read_text()),
)
require_equal(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    tree_checks["stage1_export_sha256"],
)
require_equal(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    tree_checks["discovery_manifest_sha256"],
)
require_equal(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
require_equal(
    "generator generated-tree provenance",
    generator_manifest["generated_tree_sha256"],
    tree_checks["generated_tree_sha256"],
)
require_equal(
    "Stage 4 selected status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
require_equal("Stage 4 export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
require_equal("Stage 4 preflight status", preflight_record["status"], "KLEAN_NO_OBLIGATIONS")
require_equal("Stage 5 result absence", resolution["stage5_result"], None)
require_equal("Stage 5 candidate mount absence", Path("/candidate").exists(), False)

print("ALL INDEPENDENT HASH, INVENTORY, BIJECTION, AND ZERO-TARGET CHECKS PASSED")
