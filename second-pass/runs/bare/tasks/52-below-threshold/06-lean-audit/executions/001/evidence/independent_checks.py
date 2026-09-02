#!/usr/bin/env python3
"""Independent Stage 3/4 integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict), f"{path} is not a JSON object"
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, condition: bool, detail: Any = None) -> None:
    if not condition:
        raise AssertionError(f"{name}: {detail!r}")
    print(json.dumps({"check": name, "detail": detail, "result": "PASS"},
                     sort_keys=True))


audit = read_json(AUDIT_INPUT)
resolution = audit["resolution"]
hashes = resolution["hashes"]
discovery = read_json(DISCOVERY)
generator = read_json(GENERATION / "generator-manifest.json")
input_manifest = read_json(GENERATION / "input-manifest.json")
obligation_map = read_json(GENERATED / "obligation-map.json")
export_result = read_json(GENERATION / "export-result.json")
recorded_preflight = read_json(GENERATION / "preflight.json")
source_manifest = read_json(PRODUCERS / "source-manifest.json")

check("audit schema", audit["schema_version"] == 4, audit["schema_version"])
check("problem identity", resolution["problem_id"] == "52-below-threshold",
      resolution["problem_id"])
check("condition identity", resolution["condition"] == "bare",
      resolution["condition"])
check("semantics mode", resolution["semantics_mode"] == "GENERATED_SEMANTICS",
      resolution["semantics_mode"])
check("environment/launcher audit mode",
      os.environ.get("AUDIT_MODE") == resolution["mode"]
      == "CLASSIFICATION_ONLY",
      {"environment": os.environ.get("AUDIT_MODE"),
       "launcher": resolution["mode"]})
check("classification-only candidate absent", not Path("/candidate").exists(),
      str(Path("/candidate")))

# Stage 4 producer-source authentication.
producer_files = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.rglob("*")
    if path.is_file() and not path.is_symlink()
)
check("producer bundle exact file set",
      producer_files == ["klean.py", "klean_export.py", "source-manifest.json"],
      producer_files)
expected_producer_hashes = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
check("producer manifest exact keys",
      set(source_manifest) == {"schema_version", "generator_image_id", "files"},
      sorted(source_manifest))
check("producer manifest expected file hashes",
      source_manifest["files"] == expected_producer_hashes,
      source_manifest["files"])
actual_producer_hashes = {
    name: file_sha256(PRODUCERS / name)
    for name in sorted(expected_producer_hashes)
}
check("producer source bytes match both manifests",
      actual_producer_hashes == expected_producer_hashes,
      actual_producer_hashes)
generator_image = generator["provenance"]["generator_image_id"]
audit_image = (
    "sha256:"
    + Path(resolution["generation_producer_sources"]).name
)
check("immutable generator image identity",
      generator_image == source_manifest["generator_image_id"] == audit_image,
      {"generator_manifest": generator_image,
       "source_manifest": source_manifest["generator_image_id"],
       "audit_input_path_image": audit_image})
producer_tree_hash = pipeline_contract.sha256_tree(PRODUCERS)
check("producer tree hash bound by audit input",
      producer_tree_hash == hashes["generation_producer_sources_sha256"],
      producer_tree_hash)

# Every launcher-recorded frozen file/tree hash.
stage1_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): file_sha256(path)
    for path in sorted(K_WORKSPACE.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check("Stage 1 source file hash map",
      stage1_source_hashes == resolution["stage1_source_hashes"],
      stage1_source_hashes)
tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
}
for field, observed in tree_hashes.items():
    check(f"launcher tree hash {field}", observed == hashes[field], observed)
stage1_export_hash = klean_export.tree_digest(K_WORKSPACE)
check("Stage 1 deterministic export hash",
      stage1_export_hash == hashes["stage1_export_sha256"]
      == input_manifest["frozen_input_sha256"]
      == input_manifest["stage1_workspace_sha256"]
      == generator["provenance"]["stage1_workspace_sha256"],
      stage1_export_hash)
discovery_hash = file_sha256(DISCOVERY)
check("Stage 3 manifest file hash",
      discovery_hash == hashes["discovery_manifest_sha256"]
      == input_manifest["stage3_discovery_manifest_sha256"]
      == generator["provenance"]["stage3_discovery_manifest_sha256"],
      discovery_hash)
generated_tree_hash = klean_export.tree_digest(GENERATED)
check("generated project tree hash",
      generated_tree_hash == hashes["generated_tree_sha256"]
      == generator["generated_tree_sha256"]
      == export_result["generated_tree_sha256"]
      == recorded_preflight["generated_tree_sha256"],
      generated_tree_hash)

# Canonical inventory plus independent recomputation of every recorded identity.
inventory = inventory_verification(K_WORKSPACE)
check("verification SHA-256",
      inventory["verification_sha256"]
      == resolution["stage1_source_hashes"]["verification.k"]
      == input_manifest["verification_sha256"],
      inventory["verification_sha256"])
check("local verification closure",
      inventory["verification_module"] == "VERIFICATION"
      and inventory["verification_modules"] == ["VERIFICATION"],
      inventory["verification_modules"])
rules = inventory["rules"]
check("inventory has three rules", len(rules) == 3, len(rules))
verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
for index, rule in enumerate(rules):
    span_text = "\n".join(
        verification_lines[rule["start_line"] - 1:rule["end_line"]]
    ).rstrip(" \t\r\n")
    normalized_hash = hashlib.sha256(
        " ".join(span_text.split()).encode()
    ).hexdigest()
    check(f"rule {index} source span", span_text == rule["text"],
          {"start_line": rule["start_line"], "end_line": rule["end_line"],
           "text": span_text})
    check(f"rule {index} normalized SHA-256",
          normalized_hash == rule["normalized_sha256"], normalized_hash)
    check(f"rule {index} source_rule_id",
          rule["source_rule_id"] == f"rule-{normalized_hash}",
          rule["source_rule_id"])
independent_inventory_hash = canonical_json_sha256(rules)
check("whole inventory SHA-256",
      independent_inventory_hash == inventory["inventory_sha256"]
      == discovery["inventory_sha256"]
      == input_manifest["inventory_sha256"]
      == generator["provenance"]["inventory_sha256"],
      independent_inventory_hash)

manifest_entries = discovery["rules"]
canonical_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [entry["source_rule_id"] for entry in manifest_entries]
check("Stage 3 exact rule count", len(manifest_entries) == len(rules),
      len(manifest_entries))
check("Stage 3 no duplicate identities",
      len(manifest_ids) == len(set(manifest_ids)), manifest_ids)
check("Stage 3 exact ordered identity bijection",
      manifest_ids == canonical_ids,
      {"canonical": canonical_ids, "manifest": manifest_ids})
validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY
)
check("trusted Stage 3 boundary validation",
      validated["inventory_sha256"] == independent_inventory_hash,
      validated["inventory_sha256"])

# The independently judged classification for the three frozen rules.
independent_classes = {
    canonical_ids[0]: "DEFINITION",  # allBelow(nil, t)
    canonical_ids[1]: "DEFINITION",  # allBelow(cons(i,xs), t)
    canonical_ids[2]: "DEFINITION",  # solutionProgram macro
}
observed_classes = {
    entry["source_rule_id"]: entry["classification"]
    for entry in manifest_entries
}
check("independent classifications match Stage 3",
      observed_classes == independent_classes,
      observed_classes)
for rule in rules:
    if "simplification" in rule["attributes"]:
        check(f"simplification category {rule['source_rule_id']}",
              observed_classes[rule["source_rule_id"]]
              in {"DEFINITION", "DOMAIN_LEMMA"},
              observed_classes[rule["source_rule_id"]])
check("independent domain set genuinely empty",
      not validated["domain_lemmas"]
      and all(value != "DOMAIN_LEMMA"
              for value in independent_classes.values()),
      [rule["source_rule_id"] for rule in validated["domain_lemmas"]])

# Exact empty source-rule/obligation bijection and fixed null target.
check("Stage 4 input source-rule set empty",
      input_manifest["source_rules"] == [], input_manifest["source_rules"])
check("generated source-rule set empty",
      obligation_map["source_rules"] == [], obligation_map["source_rules"])
check("generated obligation set empty",
      obligation_map["obligations"] == [], obligation_map["obligations"])
check("generated trust-parameter set empty",
      obligation_map["trust_parameters"] == [],
      obligation_map["trust_parameters"])
obligation_map_hash = file_sha256(GENERATED / "obligation-map.json")
check("obligation map SHA-256",
      obligation_map_hash == generator["obligation_map_sha256"],
      obligation_map_hash)
check("all recorded obligation counts zero",
      generator["obligation_count"] == export_result["obligation_count"]
      == recorded_preflight["obligation_count"] == 0,
      {"generator": generator["obligation_count"],
       "export": export_result["obligation_count"],
       "preflight": recorded_preflight["obligation_count"]})
observed_target = klean_export.target_statement(GENERATED)
check("fixed generated target absent",
      observed_target is None
      and generator["target"] is None
      and recorded_preflight["target"] is None
      and resolution["target"] is None,
      {"observed": observed_target, "generator": generator["target"],
       "preflight": recorded_preflight["target"],
       "audit_input": resolution["target"]})
check("selected Stage 4 no-obligations status",
      resolution["selections"]["klean_generation"]["status"]
      == "KLEAN_NO_OBLIGATIONS"
      and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
      and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS",
      {"selection": resolution["selections"]["klean_generation"]["status"],
       "export": export_result["status"],
       "preflight": recorded_preflight["status"]})
check("classification-only Stage 5 absent",
      resolution["lean_workspace"] is None
      and resolution["lean_invocation"] is None
      and resolution["stage5_result"] is None
      and hashes["lean_workspace_sha256"] is None
      and hashes["lean_invocation_sha256"] is None,
      {"lean_workspace": resolution["lean_workspace"],
       "lean_invocation": resolution["lean_invocation"],
       "stage5_result": resolution["stage5_result"]})

print(json.dumps({"result": "ALL_INDEPENDENT_CHECKS_PASS"},
                 sort_keys=True))
