#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def check(label: str, condition: bool, details: object = "") -> None:
    status = "PASS" if condition else "FAIL"
    print(f"{status}: {label}")
    if details != "":
        print(json.dumps(details, ensure_ascii=False, sort_keys=True, indent=2))
    if not condition:
        failures.append(label)


failures: list[str] = []
audit = json.loads(AUDIT_INPUT.read_text())
resolution = audit["resolution"]
recorded_hashes = resolution["hashes"]

print("== Producer identity ==")
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
check(
    "generation producer file hashes match source-manifest",
    producer_hashes == source_manifest["files"],
    {"actual": producer_hashes, "recorded": source_manifest["files"]},
)
check(
    "klean_export.py hash matches generator-manifest",
    producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"],
)
check(
    "klean.py hash matches generator-manifest",
    producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"],
)
producer_tree = pipeline_contract.sha256_tree(PRODUCERS)
check(
    "producer source tree matches audit-input",
    producer_tree == recorded_hashes["generation_producer_sources_sha256"],
    {"actual": producer_tree, "recorded": recorded_hashes["generation_producer_sources_sha256"]},
)
generator_image_ids = {
    "generator_manifest": generator_manifest["provenance"]["generator_image_id"],
    "source_manifest": source_manifest["generator_image_id"],
    "audit_input_path": "sha256:" + Path(resolution["generation_producer_sources"]).name,
}
check(
    "immutable generator image ID agrees in all three records",
    len(set(generator_image_ids.values())) == 1,
    generator_image_ids,
)

print("\n== Mounted and recorded hashes ==")
mounted_hashes = {
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "generation_producer_sources_sha256": producer_tree,
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
}
for key, actual in mounted_hashes.items():
    check(
        f"audit-input {key}",
        actual == recorded_hashes[key],
        {"actual": actual, "recorded": recorded_hashes[key]},
    )
source_hashes = resolution["stage1_source_hashes"]
source_results: dict[str, object] = {"recorded_count": len(source_hashes)}
source_mismatches: list[dict[str, str]] = []
for relative, expected in source_hashes.items():
    path = K_WORKSPACE / relative
    if not path.is_file() or path.is_symlink():
        source_mismatches.append({"path": relative, "error": "not a regular file"})
        continue
    actual = sha256_file(path)
    if actual != expected:
        source_mismatches.append({"path": relative, "expected": expected, "actual": actual})
source_results["mismatch_count"] = len(source_mismatches)
source_results["mismatches"] = source_mismatches[:20]
check("all 835 recorded Stage 1 file hashes", not source_mismatches, source_results)

print("\n== Canonical rule inventory and protected classification ==")
inventory = inventory_verification(K_WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
classified_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
check(
    "whole inventory hash recomputes from ordered canonical documents",
    inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"]),
    {"inventory_sha256": inventory["inventory_sha256"]},
)
check(
    "protected inventory hash equals reconstruction",
    discovery["inventory_sha256"] == inventory["inventory_sha256"],
)
check(
    "rule identity order is exact",
    classified_ids == canonical_ids,
    {"canonical_count": len(canonical_ids), "classified_count": len(classified_ids)},
)
check("no duplicate protected source_rule_id", len(set(classified_ids)) == len(classified_ids))
check("no omitted or extra protected source_rule_id", set(classified_ids) == set(canonical_ids))
normalization_mismatches: list[dict[str, object]] = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    digest = sha256_bytes(normalized.encode())
    expected_id = "rule-" + digest
    if digest != rule["normalized_sha256"] or expected_id != rule["source_rule_id"]:
        normalization_mismatches.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "computed_sha256": digest,
                "recorded_sha256": rule["normalized_sha256"],
            }
        )
check(
    "every normalized source hash and source_rule_id independently recomputes",
    not normalization_mismatches,
    normalization_mismatches,
)
validated = lemma_discovery_contract.validate_trust_boundary(K_WORKSPACE, DISCOVERY)
check(
    "trusted trust-boundary validator accepts exact bijection",
    validated["inventory_sha256"] == inventory["inventory_sha256"],
)
expected_roles = ["DEFINITION"] * (len(canonical_ids) - 1) + ["DOMAIN_LEMMA"]
observed_roles = [entry["classification"] for entry in discovery["rules"]]
check(
    "protected roles equal independent 22-definition/1-domain classification",
    observed_roles == expected_roles,
    {"observed": dict(zip(classified_ids, observed_roles, strict=True))},
)
simplification_violations = []
role_by_id = dict(zip(classified_ids, observed_roles, strict=True))
for rule in inventory["rules"]:
    if "simplification" in rule["attributes"] and role_by_id[rule["source_rule_id"]] not in {
        "DEFINITION",
        "DOMAIN_LEMMA",
    }:
        simplification_violations.append(rule["source_rule_id"])
check("every simplification is DEFINITION or DOMAIN_LEMMA", not simplification_violations)
domain_ids = [
    rule["source_rule_id"]
    for rule in inventory["rules"]
    if role_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]
check(
    "independent domain set is exactly the applyCmp >= bridge",
    domain_ids == ["rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050"],
    domain_ids,
)

print("\n== Stage 4 source/obligation/target bijection ==")
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
mapped_source_ids = [entry["source_rule_id"] for entry in source_rules]
obligation_ids = [entry["source_rule_id"] for entry in obligations]
check("input-manifest inventory hash", input_manifest["inventory_sha256"] == inventory["inventory_sha256"])
check("generator-manifest inventory hash", generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"])
check("mapped source rules equal independent domain IDs in order", mapped_source_ids == domain_ids)
check("obligation IDs equal independent domain IDs in order", obligation_ids == domain_ids)
check("no duplicate source rules or obligations", len(set(mapped_source_ids)) == len(mapped_source_ids) and len(set(obligation_ids)) == len(obligation_ids))
check("one source rule has exactly one obligation", len(source_rules) == len(obligations) == 1)
obligation = obligations[0]
source_rule = next(rule for rule in inventory["rules"] if rule["source_rule_id"] == domain_ids[0])
provenance_ok = (
    obligation["normalized_sha256"] == source_rule["normalized_sha256"]
    and obligation["source_span"] == {"start_line": source_rule["start_line"], "end_line": source_rule["end_line"]}
    and obligation["inventory_sha256"] == inventory["inventory_sha256"]
    and obligation["discovery_manifest_sha256"] == sha256_file(DISCOVERY)
)
check("obligation hashes and source span match frozen rule", provenance_ok, obligation)
check(
    "Lean conjunct hash recomputes",
    obligation["lean_conjunct_sha256"] == klean_export.sha256_text(obligation["lean_conjunct"]),
)
nonvacuous_shape = (
    obligation["lean_conjunct"].startswith("∀ (W : SortVal) (V : SortVal) (h :")
    and 'applyCmp(_,_,_)' in obligation["lean_conjunct"]
    and 'orderGe(_,_)' in obligation["lean_conjunct"]
    and 'orderablePair(_,_)' in obligation["lean_conjunct"]
    and '">=" V W' in obligation["lean_conjunct"]
    and " = true" in obligation["lean_conjunct"]
)
check("generated conjunct retains universal variables, guard, operator, and equality", nonvacuous_shape, obligation["lean_conjunct"])
check(
    "obligation-map file hash",
    sha256_file(obligation_map_path) == generator_manifest["obligation_map_sha256"],
)
expected_definition = klean_export.expected_target_definition(obligation_map)
parsed_target = klean_export.target_statement(GENERATED)
check("generated target exists for nonempty domain set", expected_definition is not None and parsed_target is not None)
check(
    "target definition is exact conjunction generated from obligation map",
    parsed_target["definition_sha256"] == klean_export.sha256_text(expected_definition),
)
check("parsed target equals generator-manifest target", parsed_target == generator_manifest["target"])
check("parsed target equals audit-input target", parsed_target == resolution["target"])
check("parsed target equals audit-input Stage 4 preflight target", parsed_target == resolution["stage4_preflight"]["target"])
check(
    "generated tree digest equals generator-manifest",
    klean_export.tree_digest(GENERATED) == generator_manifest["generated_tree_sha256"],
)
check(
    "trust inventory hash equals export-result binding",
    sha256_file(GENERATION / "trust-inventory.json")
    == json.loads((GENERATION / "export-result.json").read_text())["trust_inventory_sha256"],
)

print("\n== Candidate immutability and new trust declarations ==")
proof_text = (CANDIDATE / "Proof.lean").read_text()
candidate_trust = klean_export.lean_trust_declarations(CANDIDATE / "Proof.lean")
check("candidate adds no axiom or opaque declaration", candidate_trust == [], candidate_trust)
forbidden = {
    token: bool(re.search(rf"\b{token}\b", proof_text))
    for token in ("sorry", "admit", "unsafe", "axiom", "opaque")
}
check("candidate contains no forbidden trust token", not any(forbidden.values()), forbidden)
check(
    "candidate neither defines nor shadows targetStatement",
    re.search(r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+(?:\S+\.)?targetStatement\b", proof_text) is None,
)
check(
    "fresh Base target equals immutable generated target",
    sha256_file(Path("/tmp/audit-work/stage5-project/Base/Klean135CanArrange/Lemmas.lean"))
    == sha256_file(GENERATED / "Klean135CanArrange/Lemmas.lean"),
)
check(
    "fresh candidate Proof equals mounted candidate Proof",
    sha256_file(Path("/tmp/audit-work/stage5-project/Proof.lean")) == sha256_file(CANDIDATE / "Proof.lean"),
)

print("\n== Summary ==")
print(json.dumps({"check_failures": failures, "failure_count": len(failures)}, indent=2, sort_keys=True))
raise SystemExit(1 if failures else 0)
