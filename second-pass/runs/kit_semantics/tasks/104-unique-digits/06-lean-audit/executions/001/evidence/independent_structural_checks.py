#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict), path
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool, detail: object = None) -> None:
    status = "PASS" if condition else "FAIL"
    print(f"{status} {label}" + (f": {detail}" if detail is not None else ""))
    if not condition:
        raise AssertionError(label)


reference = Path("/reference")
audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
source_manifest = load(reference / "generation-tools/source-manifest.json")
discovery = load(reference / "lemma-discovery.json")
input_manifest = load(reference / "klean-generation/input-manifest.json")
generator_manifest = load(reference / "klean-generation/generator-manifest.json")
export_result = load(reference / "klean-generation/export-result.json")
trust_inventory = load(reference / "klean-generation/trust-inventory.json")
obligation_map = load(reference / "klean-generation/generated/obligation-map.json")

producer_exporter = reference / "generation-tools/klean_export.py"
producer_klean = reference / "generation-tools/klean.py"
exporter_hash = file_hash(producer_exporter)
klean_hash = file_hash(producer_klean)
check("producer klean_export.py hash matches source manifest",
      exporter_hash == source_manifest["files"]["klean_export.py"], exporter_hash)
check("producer klean_export.py hash matches generator manifest",
      exporter_hash == generator_manifest["exporter_sha256"], exporter_hash)
check("producer klean.py hash matches source manifest",
      klean_hash == source_manifest["files"]["klean.py"], klean_hash)
check("producer klean.py hash matches generator manifest",
      klean_hash == generator_manifest["klean_py_sha256"], klean_hash)
image_id = source_manifest["generator_image_id"]
check("producer image agrees between source and generator manifests",
      image_id == generator_manifest["provenance"]["generator_image_id"], image_id)
recorded_source_path_id = "sha256:" + Path(resolution["generation_producer_sources"]).name
check("producer image agrees with audit-input producer path",
      image_id == recorded_source_path_id, recorded_source_path_id)

hashes = resolution["hashes"]
check("producer source tree hash matches audit input",
      pipeline_contract.sha256_tree(reference / "generation-tools") ==
      hashes["generation_producer_sources_sha256"], hashes["generation_producer_sources_sha256"])
check("Stage 1 selected tree hash matches audit input",
      pipeline_contract.sha256_tree(reference / "k-proof") == hashes["k_workspace_sha256"],
      hashes["k_workspace_sha256"])
stage1_export_hash = klean_export.tree_digest(reference / "k-proof")
check("Stage 1 export hash matches audit input",
      stage1_export_hash == hashes["stage1_export_sha256"], stage1_export_hash)
check("Stage 4 selected tree hash matches audit input",
      pipeline_contract.sha256_tree(reference / "klean-generation") ==
      hashes["klean_generation_sha256"], hashes["klean_generation_sha256"])
generated_hash = klean_export.tree_digest(reference / "klean-generation/generated")
check("generated tree hash matches audit input",
      generated_hash == hashes["generated_tree_sha256"], generated_hash)
check("generated tree hash matches generator manifest",
      generated_hash == generator_manifest["generated_tree_sha256"], generated_hash)
discovery_hash = file_hash(reference / "lemma-discovery.json")
check("discovery file hash matches audit input",
      discovery_hash == hashes["discovery_manifest_sha256"], discovery_hash)
check("launcher mode agrees with audit input",
      os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY",
      os.environ.get("AUDIT_MODE"))

inventory = inventory_verification(reference / "k-proof")
rules = inventory["rules"]
check("inventory contains exactly 15 rules", len(rules) == 15, len(rules))
check("inventory closure is exact",
      inventory["verification_modules"] == ["VERIFICATION-SYNTAX", "VERIFICATION"],
      inventory["verification_modules"])
check("inventory hash independently canonicalizes",
      canonical_json_sha256(rules) == inventory["inventory_sha256"],
      inventory["inventory_sha256"])
check("inventory hash matches discovery",
      inventory["inventory_sha256"] == discovery["inventory_sha256"],
      inventory["inventory_sha256"])

ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("inventory source_rule_ids are unique", len(ids) == len(set(ids)), len(ids))
check("discovery source_rule_ids are unique",
      len(discovery_ids) == len(set(discovery_ids)), len(discovery_ids))
check("discovery is an ordered rule bijection", discovery_ids == ids)
for index, rule in enumerate(rules):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    check(f"rule {index + 1:02d} normalized hash and ID",
          digest == rule["normalized_sha256"] and
          rule["source_rule_id"] == f"rule-{digest}",
          f"lines {rule['start_line']}-{rule['end_line']} {digest}")
    check(f"rule {index + 1:02d} discovery classification is DEFINITION",
          discovery["rules"][index]["classification"] == "DEFINITION")

expected_definitions = []
for source, classification in zip(rules, discovery["rules"], strict=True):
    item = dict(source)
    item["classification"] = classification["classification"]
    item["rationale"] = classification["rationale"]
    expected_definitions.append(item)
check("Stage 4 definitions exactly enrich the reconstructed inventory",
      input_manifest["definitions"] == expected_definitions)
check("Stage 4 inventory hash matches reconstruction",
      input_manifest["inventory_sha256"] == inventory["inventory_sha256"] ==
      generator_manifest["provenance"]["inventory_sha256"])
check("Stage 4 verification hash matches reconstruction",
      input_manifest["verification_sha256"] == inventory["verification_sha256"])
check("Stage 4 frozen input hashes match reconstruction",
      input_manifest["frozen_input_sha256"] == stage1_export_hash ==
      input_manifest["stage1_workspace_sha256"] ==
      generator_manifest["provenance"]["stage1_workspace_sha256"] ==
      export_result["frozen_input_sha256"])
check("Stage 4 discovery hashes match reconstruction",
      input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash ==
      generator_manifest["provenance"]["stage3_discovery_manifest_sha256"] ==
      export_result["stage3_discovery_manifest_sha256"])

check("true DOMAIN_LEMMA source set is empty", input_manifest["source_rules"] == [])
check("no operational or proved-derived rules were exported",
      input_manifest["operational_rules"] == [] and
      input_manifest["proved_derived_lemmas"] == [])
check("obligation-map source set is exactly empty", obligation_map["source_rules"] == [])
check("obligation-map obligation set is exactly empty", obligation_map["obligations"] == [])
check("obligation-map trust-parameter set is exactly empty",
      obligation_map["trust_parameters"] == [])
obligation_hash = file_hash(reference / "klean-generation/generated/obligation-map.json")
check("obligation-map hash matches generator manifest",
      obligation_hash == generator_manifest["obligation_map_sha256"], obligation_hash)
check("zero obligation counts agree",
      generator_manifest["obligation_count"] == export_result["obligation_count"] == 0)
check("no target is recorded",
      generator_manifest["target"] is None and
      resolution["target"] is None and
      klean_export.target_statement(reference / "klean-generation/generated") is None)
check("expected generated target is absent",
      klean_export.expected_target_definition(obligation_map) is None)
check("export status is KLEAN_NO_OBLIGATIONS",
      export_result["status"] == resolution["selections"]["klean_generation"]["status"] ==
      "KLEAN_NO_OBLIGATIONS")
check("classification-only audit has no candidate", not Path("/candidate").exists())

lean_files = sorted((reference / "klean-generation/generated").rglob("*.lean"))
target_pattern = re.compile(r"(?m)^\s*(?:theorem|lemma|def)\s+(?:KLeanTarget|Proof\.final)\b")
check("independent Lean source scan finds no generated target declaration",
      not any(target_pattern.search(path.read_text()) for path in lean_files))
check("generated trust inventory has zero proof holes",
      trust_inventory["designated_sorries"] == trust_inventory["other_sorries"] == 0)

print("ALL_STRUCTURAL_CHECKS_PASS")
