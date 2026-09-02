#!/usr/bin/env python3
"""Independent read-only integrity checks for the Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import (
    klean_audit_contract,
    klean_export,
    pipeline_contract,
)
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


FROZEN = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")

failures: list[str] = []


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise TypeError(f"not a JSON object: {path}")
    return document


def check(label: str, observed: Any, expected: Any) -> None:
    ok = observed == expected
    print(f"{'PASS' if ok else 'FAIL'} {label}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if not ok:
        failures.append(label)


audit_document = read_json(AUDIT_INPUT)
resolution, resolved_digest = klean_audit_contract.verify_stage6_audit_input(
    audit_document
)
discovery = read_json(DISCOVERY)
source_manifest = read_json(PRODUCERS / "source-manifest.json")
generator_manifest = read_json(GENERATION / "generator-manifest.json")
input_manifest = read_json(GENERATION / "input-manifest.json")
obligation_map = read_json(GENERATED / "obligation-map.json")
export_result = read_json(GENERATION / "export-result.json")
toolchain_lock = read_json(TOOLCHAIN_LOCK)

print("== Signed audit envelope ==")
check(
    "resolved-input digest",
    resolved_digest,
    audit_document["resolved_input_sha256"],
)
check("environment mode", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem ID", resolution["problem_id"], "157-right-angle-triangle")
check("condition", resolution["condition"], "semantics")
check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

print("\n== Generation-time producer identity ==")
actual_exporter = sha256_file(PRODUCERS / "klean_export.py")
actual_klean = sha256_file(PRODUCERS / "klean.py")
check(
    "klean_export.py vs source manifest",
    actual_exporter,
    source_manifest["files"]["klean_export.py"],
)
check(
    "klean_export.py vs generator manifest",
    actual_exporter,
    generator_manifest["exporter_sha256"],
)
check(
    "klean.py vs source manifest",
    actual_klean,
    source_manifest["files"]["klean.py"],
)
check(
    "klean.py vs generator manifest",
    actual_klean,
    generator_manifest["klean_py_sha256"],
)
producer_tree = pipeline_contract.sha256_tree(PRODUCERS)
check(
    "producer-source tree vs audit input",
    producer_tree,
    resolution["hashes"]["generation_producer_sources_sha256"],
)
check(
    "generator image ID across source/generator manifests",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
check(
    "audit-input producer path binds generator image ID",
    Path(resolution["generation_producer_sources"]).name,
    source_manifest["generator_image_id"].removeprefix("sha256:"),
)

print("\n== Mounted artifact hashes ==")
check(
    "full Stage 1 tree",
    pipeline_contract.sha256_tree(FROZEN),
    resolution["hashes"]["k_workspace_sha256"],
)
check(
    "Stage 1 deterministic export tree",
    klean_export.tree_digest(FROZEN),
    resolution["hashes"]["stage1_export_sha256"],
)
check(
    "selected Stage 2 audit tree",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution["hashes"]["k_audit_sha256"],
)
check(
    "protected discovery file",
    sha256_file(DISCOVERY),
    resolution["hashes"]["discovery_manifest_sha256"],
)
check(
    "selected Stage 4 generation tree",
    pipeline_contract.sha256_tree(GENERATION),
    resolution["hashes"]["klean_generation_sha256"],
)
check(
    "generated project tree",
    klean_export.tree_digest(GENERATED),
    resolution["hashes"]["generated_tree_sha256"],
)

actual_stage1_files = {
    path.relative_to(FROZEN).as_posix(): sha256_file(path)
    for path in sorted(FROZEN.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "complete Stage 1 source-hash map",
    actual_stage1_files,
    resolution["stage1_source_hashes"],
)

print("\n== Rule inventory reconstruction and Stage 3 bijection ==")
inventory = inventory_verification(FROZEN)
manual_inventory_hash = canonical_json_sha256(inventory["rules"])
check(
    "inventory canonical hash recomputation",
    manual_inventory_hash,
    inventory["inventory_sha256"],
)
check(
    "inventory hash vs protected Stage 3",
    inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
check(
    "inventory hash vs Stage 4 input",
    inventory["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("ordered source-rule identity bijection", discovery_ids, inventory_ids)
check(
    "no duplicated discovery identities",
    len(discovery_ids),
    len(set(discovery_ids)),
)
check(
    "verification source hash",
    inventory["verification_sha256"],
    input_manifest["verification_sha256"],
)

allowed_classes = {
    "DEFINITION",
    "DOMAIN_LEMMA",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
}
observed_classes = [rule.get("classification") for rule in discovery["rules"]]
check(
    "all Stage 3 classifications accounted",
    all(item in allowed_classes for item in observed_classes),
    True,
)

classification_by_id = {
    item["source_rule_id"]: item for item in discovery["rules"]
}
enriched: list[dict[str, Any]] = []
for rule in inventory["rules"]:
    stage3 = classification_by_id[rule["source_rule_id"]]
    enriched.append(
        rule
        | {
            "classification": stage3["classification"],
            "rationale": stage3["rationale"],
        }
    )

partitions = {
    "DEFINITION": input_manifest["definitions"],
    "DOMAIN_LEMMA": input_manifest["source_rules"],
    "OPERATIONAL_RULE": input_manifest["operational_rules"],
    "PROVED_DERIVED_LEMMA": input_manifest["proved_derived_lemmas"],
}
for classification, recorded in partitions.items():
    expected = [
        item for item in enriched if item["classification"] == classification
    ]
    check(f"Stage 4 {classification} exact partition", recorded, expected)

print("\n== Stage 4 obligation and target identity ==")
domain_entries = partitions["DOMAIN_LEMMA"]
check("independently classified domain set is empty", domain_entries, [])
check("obligation source rules", obligation_map["source_rules"], domain_entries)
obligation_ids = [
    item.get("source_rule_id") for item in obligation_map["obligations"]
]
domain_ids = [item["source_rule_id"] for item in domain_entries]
check("ordered obligation/source bijection", obligation_ids, domain_ids)
check(
    "no duplicated obligation identities",
    len(obligation_ids),
    len(set(obligation_ids)),
)
check(
    "generator obligation count",
    generator_manifest["obligation_count"],
    len(obligation_map["obligations"]),
)
check(
    "obligation map file hash",
    generator_manifest["obligation_map_sha256"],
    sha256_file(GENERATED / "obligation-map.json"),
)
check("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)
check(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    klean_export.tree_digest(FROZEN),
)
check(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    sha256_file(DISCOVERY),
)
check(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)
check("fixed generated target definition", expected_definition, None)
check("actual generated target", target, generator_manifest["target"])
check("audit-input target", target, resolution["target"])
check("zero-obligation export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("audit-input Stage 4 status", resolution["stage4_preflight"]["status"], "KLEAN_NO_OBLIGATIONS")
check("no Stage 5 workspace in classification-only mode", resolution["lean_workspace"], None)
check("no Stage 5 invocation in classification-only mode", resolution["lean_invocation"], None)
check("no Stage 5 result in classification-only mode", resolution["stage5_result"], None)
check("no mounted candidate in classification-only mode", Path("/candidate").exists(), False)

print("\n== Summary ==")
print(f"failures={len(failures)}")
for failure in failures:
    print(f"FAILURE {failure}")
raise SystemExit(1 if failures else 0)
