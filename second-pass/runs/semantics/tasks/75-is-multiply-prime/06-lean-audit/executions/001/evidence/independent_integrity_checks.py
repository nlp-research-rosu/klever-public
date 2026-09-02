#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


ROOT = Path("/reference")
AUDIT_INPUT = Path("/audit-input.json")
results: list[dict[str, Any]] = []


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(name: str, observed: Any, expected: Any) -> None:
    passed = observed == expected
    results.append(
        {
            "name": name,
            "passed": passed,
            "observed": observed,
            "expected": expected,
        }
    )
    if not passed:
        raise AssertionError(
            f"{name}: observed {observed!r}, expected {expected!r}"
        )


audit = json.loads(AUDIT_INPUT.read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
discovery_path = ROOT / "lemma-discovery.json"
generation = ROOT / "klean-generation"
generated = generation / "generated"
producer_dir = ROOT / "generation-tools"

discovery = json.loads(discovery_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
source_manifest = json.loads((producer_dir / "source-manifest.json").read_text())
toolchain_lock = json.loads((ROOT / "klean-toolchain.lock.json").read_text())
trust_inventory_path = generation / "trust-inventory.json"
trust_inventory = json.loads(trust_inventory_path.read_text())

# Signed audit-input envelope.
canonical_resolution = json.dumps(
    resolution,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
).encode()
record(
    "resolved audit-input hash",
    hashlib.sha256(canonical_resolution).hexdigest(),
    audit["resolved_input_sha256"],
)

# Audit-input tree and file hashes.
record(
    "Stage 1 selected tree hash",
    pipeline_contract.sha256_tree(ROOT / "k-proof"),
    hashes["k_workspace_sha256"],
)
record(
    "Stage 2 selected tree hash",
    pipeline_contract.sha256_tree(ROOT / "k-audit"),
    hashes["k_audit_sha256"],
)
record(
    "Stage 4 selected tree hash",
    pipeline_contract.sha256_tree(generation),
    hashes["klean_generation_sha256"],
)
record(
    "generation producer-source tree hash",
    pipeline_contract.sha256_tree(producer_dir),
    hashes["generation_producer_sources_sha256"],
)
record(
    "Stage 3 manifest file hash",
    sha256_file(discovery_path),
    hashes["discovery_manifest_sha256"],
)
record(
    "Stage 1 deterministic export hash",
    klean_export.tree_digest(ROOT / "k-proof"),
    hashes["stage1_export_sha256"],
)
record(
    "generated project tree hash",
    klean_export.tree_digest(generated),
    hashes["generated_tree_sha256"],
)
record(
    "selected Stage 2 artifact hash binding",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    hashes["k_audit_sha256"],
)
record(
    "selected Stage 4 artifact hash binding",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    hashes["klean_generation_sha256"],
)
record("absent Lean invocation hash", hashes["lean_invocation_sha256"], None)
record("absent Lean workspace hash", hashes["lean_workspace_sha256"], None)

# Every source hash and the exact source-file set recorded by the launcher.
actual_stage1_files = sorted(
    path.relative_to(ROOT / "k-proof").as_posix()
    for path in (ROOT / "k-proof").rglob("*")
    if path.is_file() and not path.is_symlink()
)
record(
    "Stage 1 source file set",
    actual_stage1_files,
    sorted(resolution["stage1_source_hashes"]),
)
actual_source_hashes = {
    relative: sha256_file(ROOT / "k-proof" / relative)
    for relative in actual_stage1_files
}
record(
    "all Stage 1 source file hashes",
    actual_source_hashes,
    resolution["stage1_source_hashes"],
)

# Producer sources and immutable generator image provenance.
actual_producer_files = {
    name: sha256_file(producer_dir / name)
    for name in ("klean.py", "klean_export.py")
}
record("producer source file hashes", actual_producer_files, source_manifest["files"])
record(
    "exporter hash in generator manifest",
    actual_producer_files["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
record(
    "klean.py hash in generator manifest",
    actual_producer_files["klean.py"],
    generator_manifest["klean_py_sha256"],
)
record(
    "generator image: source manifest versus generator manifest",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
audit_image_from_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
record(
    "generator image: audit input versus source manifest",
    audit_image_from_path,
    source_manifest["generator_image_id"],
)
record(
    "generator manifest toolchain",
    generator_manifest["toolchain"],
    toolchain_lock,
)

# Canonical local verification-module closure and Stage 3 bijection.
inventory = inventory_verification(ROOT / "k-proof")
record("inventory schema", inventory["schema_version"], 2)
record("verification module", inventory["verification_module"], "VERIFICATION")
record(
    "local verification-module closure",
    inventory["verification_modules"],
    ["VERIFICATION"],
)
record(
    "verification.k file hash",
    inventory["verification_sha256"],
    resolution["stage1_source_hashes"]["verification.k"],
)
record(
    "reconstructed whole inventory hash",
    inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
record("Stage 3 ordered rule identity bijection", discovery_ids, inventory_ids)
record("Stage 3 rule IDs are unique", len(set(discovery_ids)), len(discovery_ids))
record("inventory rule IDs are unique", len(set(inventory_ids)), len(inventory_ids))

# Independent semantic classification, encoded only after reading the source and
# the operational rules for module loading, calls, scopes, returns, and loops.
independent_classes = [
    "OPERATIONAL_RULE",
    "DEFINITION",
    "OPERATIONAL_RULE",
]
record(
    "independent classifications in source order",
    [entry["classification"] for entry in discovery["rules"]],
    independent_classes,
)
record(
    "all classification rationales are nonempty",
    all(
        isinstance(entry.get("rationale"), str)
        and bool(entry["rationale"].strip())
        for entry in discovery["rules"]
    ),
    True,
)
record(
    "every simplification rule is definition or domain lemma",
    all(
        "simplification" not in rule["attributes"]
        or independent_classes[index] in {"DEFINITION", "DOMAIN_LEMMA"}
        for index, rule in enumerate(inventory["rules"])
    ),
    True,
)
record(
    "independently classified domain-lemma IDs",
    [
        inventory_ids[index]
        for index, classification in enumerate(independent_classes)
        if classification == "DOMAIN_LEMMA"
    ],
    [],
)

# Deterministic input-manifest category export, including full reconstructed
# spans, source text, attributes, hashes, IDs, classifications, and rationales.
discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}


def expected_entries(classification: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for rule in inventory["rules"]:
        classified = discovery_by_id[rule["source_rule_id"]]
        if classified["classification"] != classification:
            continue
        entries.append(
            {
                **rule,
                "classification": classification,
                "rationale": classified["rationale"],
            }
        )
    return entries


record(
    "input-manifest definitions",
    input_manifest["definitions"],
    expected_entries("DEFINITION"),
)
record(
    "input-manifest operational rules",
    input_manifest["operational_rules"],
    expected_entries("OPERATIONAL_RULE"),
)
record(
    "input-manifest proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    expected_entries("PROVED_DERIVED_LEMMA"),
)
record("input-manifest domain source rules", input_manifest["source_rules"], [])
record("input-manifest summary functions", input_manifest["summary_functions"], [])
record(
    "input-manifest inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)

# Empty source-domain set must map bijectively to empty obligations and no target.
record("obligation-map source rules", obligation_map["source_rules"], [])
record("obligation-map obligations", obligation_map["obligations"], [])
record("obligation-map trust parameters", obligation_map["trust_parameters"], [])
record(
    "obligation source IDs are unique",
    len(
        {
            obligation.get("source_rule_id")
            for obligation in obligation_map["obligations"]
        }
    ),
    len(obligation_map["obligations"]),
)
record(
    "generator obligation count",
    generator_manifest["obligation_count"],
    len(obligation_map["obligations"]),
)
record(
    "obligation-map file hash",
    sha256_file(generated / "obligation-map.json"),
    generator_manifest["obligation_map_sha256"],
)
record("generated target declaration", klean_export.target_statement(generated), None)
record("generator-manifest target", generator_manifest["target"], None)
record("audit-input target", resolution["target"], None)
record("stored preflight target", preflight["target"], None)
record(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
record("export-result status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
record("stored preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
record(
    "audit-input embedded preflight record",
    resolution["stage4_preflight"],
    preflight,
)
for index, diagnostic in enumerate(preflight["diagnostics"]):
    tail = diagnostic["output_tail"]
    if len(tail) < 4000:
        record(
            f"stored preflight diagnostic {index} output hash",
            hashlib.sha256(tail.encode()).hexdigest(),
            diagnostic["output_sha256"],
        )
record(
    "stored preflight trust declaration count",
    preflight["trust_declaration_count"],
    len(trust_inventory["allowlist"]),
)

# Cross-manifest hashes and provenance, checked separately from preflight.
stage1_export_hash = hashes["stage1_export_sha256"]
stage3_hash = hashes["discovery_manifest_sha256"]
generated_hash = hashes["generated_tree_sha256"]
record(
    "input-manifest frozen hash",
    input_manifest["frozen_input_sha256"],
    stage1_export_hash,
)
record(
    "input-manifest workspace hash",
    input_manifest["stage1_workspace_sha256"],
    stage1_export_hash,
)
record(
    "input-manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    stage3_hash,
)
record(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"],
    generated_hash,
)
record(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    stage1_export_hash,
)
record(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    stage3_hash,
)
record(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
record(
    "export-result frozen hash",
    export_result["frozen_input_sha256"],
    stage1_export_hash,
)
record(
    "export-result Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    stage3_hash,
)
record(
    "export-result generated-tree hash",
    export_result["generated_tree_sha256"],
    generated_hash,
)
record(
    "export-result trust inventory hash",
    export_result["trust_inventory_sha256"],
    sha256_file(trust_inventory_path),
)

# CLASSIFICATION_ONLY requires no Stage 5 candidate or result.
record("audit mode", resolution["mode"], "CLASSIFICATION_ONLY")
record("AUDIT_MODE environment", os.environ.get("AUDIT_MODE"), resolution["mode"])
record("Stage 5 result", resolution["stage5_result"], None)
record("Lean invocation selection", resolution["lean_invocation"], None)
record("Lean workspace selection", resolution["lean_workspace"], None)
record("candidate mount absent", Path("/candidate").exists(), False)

summary = {
    "status": "PASS",
    "check_count": len(results),
    "failed_count": sum(not result["passed"] for result in results),
    "checks": results,
}
print(json.dumps(summary, indent=2, sort_keys=True))
