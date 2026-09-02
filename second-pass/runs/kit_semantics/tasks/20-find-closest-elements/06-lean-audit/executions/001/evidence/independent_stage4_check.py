#!/usr/bin/env python3
"""Independent, stdlib-only Stage 3/4 identity and hash cross-check."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")
RECONSTRUCTED = Path("/audit-output/evidence/reconstructed-inventory.json")

DOMAIN_IDS = [
    "rule-db9d3a3e81dee21bb05c9f3240b23092771092e55e7bb6f53dc9fdcfa44b3188",
    "rule-c31085d90cc1a95717c3310bccb50623ab127a57e9e6010eb23e0aa2e4377dc7",
    "rule-1be94e05a1b1440cd44a316053a753efc65fc522fcdf2fd8218e40d546231a89",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def sha_text(text: str) -> str:
    return sha_bytes(text.encode())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


inventory = load(RECONSTRUCTED)
discovery = load(DISCOVERY)
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)
generator_manifest = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
audit = load(AUDIT_INPUT)["resolution"]

inventory_rules = inventory["rules"]
inventory_ids = [rule["source_rule_id"] for rule in inventory_rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
require(len(inventory_ids) == len(set(inventory_ids)) == 36, "inventory IDs not unique")
require(len(discovery_ids) == len(set(discovery_ids)) == 36, "discovery IDs not unique")
require(discovery_ids == inventory_ids, "discovery/inventory order or identity changed")
require(discovery["inventory_sha256"] == inventory["inventory_sha256"], "inventory hash changed")

classified = {rule["source_rule_id"]: rule["classification"] for rule in discovery["rules"]}
manifest_domain_ids = [source["source_rule_id"] for source in obligation_map["source_rules"]]
require([rule_id for rule_id in inventory_ids if classified[rule_id] == "DOMAIN_LEMMA"] == DOMAIN_IDS,
        "independently selected domain IDs do not match discovery")
require(manifest_domain_ids == DOMAIN_IDS, "source-rule order/identity is not exact")
require(len(manifest_domain_ids) == len(set(manifest_domain_ids)) == 3, "duplicate source rules")

inventory_by_id = {rule["source_rule_id"]: rule for rule in inventory_rules}
discovery_hash = sha_file(DISCOVERY)
require(discovery_hash == audit["hashes"]["discovery_manifest_sha256"], "audit discovery hash")
require(discovery_hash == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
        "generator discovery hash")

obligations = obligation_map["obligations"]
obligation_ids = [obligation["source_rule_id"] for obligation in obligations]
require(obligation_ids == DOMAIN_IDS, "obligation identity/order is not exact")
require(len(obligation_ids) == len(set(obligation_ids)) == 3, "duplicate obligations")
require(generator_manifest["obligation_count"] == len(obligations) == 3, "obligation count")

for source, obligation in zip(obligation_map["source_rules"], obligations, strict=True):
    reconstructed = inventory_by_id[source["source_rule_id"]]
    for field in (
        "source_rule_id", "module", "start_line", "end_line", "text",
        "attributes", "normalized_sha256",
    ):
        require(source[field] == reconstructed[field], f"source field changed: {field}")
    require(source["classification"] == "DOMAIN_LEMMA", "source is not a domain lemma")
    require(source["inventory_sha256"] == inventory["inventory_sha256"], "source inventory hash")
    require(source["discovery_manifest_sha256"] == discovery_hash, "source discovery hash")
    require(obligation["source_rule_id"] == source["source_rule_id"], "obligation source ID")
    require(obligation["source_span"] == {
        "start_line": source["start_line"], "end_line": source["end_line"]
    }, "obligation source span")
    require(obligation["normalized_sha256"] == source["normalized_sha256"],
            "obligation normalized hash")
    require(obligation["inventory_sha256"] == inventory["inventory_sha256"],
            "obligation inventory hash")
    require(obligation["discovery_manifest_sha256"] == discovery_hash,
            "obligation discovery hash")
    require(sha_text(obligation["lean_conjunct"]) == obligation["lean_conjunct_sha256"],
            "conjunct text hash")
    require(obligation["lean_conjunct"].strip() not in {"True", "(True)", "true", "(true)"},
            "vacuous literal conjunct")
    require("∀" in obligation["lean_conjunct"] and "=" in obligation["lean_conjunct"],
            "conjunct lost quantified equation")

map_hash = sha_file(obligation_map_path)
require(map_hash == generator_manifest["obligation_map_sha256"], "obligation-map hash")

parameter_names: list[str] = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    binding_json = json.dumps(binding, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    require(sha_text(binding_json) == parameter["binding_sha256"], "parameter binding hash")
    require(parameter["source_rule_ids"], "unbound target parameter")
    require(set(parameter["source_rule_ids"]).issubset(DOMAIN_IDS), "extra parameter source rule")
    parameter_names.append(parameter["name"])
require(len(parameter_names) == len(set(parameter_names)) == 6, "target parameters not unique")
require(set().union(*(set(p["source_rule_ids"]) for p in obligation_map["trust_parameters"]))
        == set(DOMAIN_IDS), "target parameters do not cover domain set")

expected_definition_lines = ["def targetStatement"]
for parameter in obligation_map["trust_parameters"]:
    expected_definition_lines.append(f"    ({parameter['name']} : {parameter['type']})")
expected_definition_lines.extend((
    "    : Prop :=",
    "    " + "\n    ∧ ".join(f"({o['lean_conjunct']})" for o in obligations),
))
expected_definition = "\n".join(expected_definition_lines)
lemmas_text = (GENERATED / "Klean20FindClosestElements/Lemmas.lean").read_text()
require(lemmas_text.count(expected_definition) == 1, "generated target definition changed/duplicated")
require(len(re.findall(r"(?m)^\s*def\s+targetStatement\b", lemmas_text)) == 1,
        "target declaration count")

target = {
    "declaration": "Klean20FindClosestElements.Lemmas.targetStatement",
    "file": "Klean20FindClosestElements/Lemmas.lean",
    "statement": " ".join((
        "Klean20FindClosestElements.Lemmas.targetStatement", *parameter_names
    )),
    "statement_sha256": sha_text(" ".join((
        "Klean20FindClosestElements.Lemmas.targetStatement", *parameter_names
    ))),
    "definition_sha256": sha_text(expected_definition),
    "parameters": [
        {
            "kore_symbol": p["kore_symbol"],
            "name": p["name"],
            "type": p["type"],
            "source_rule_ids": p["source_rule_ids"],
            "binding_sha256": p["binding_sha256"],
        }
        for p in obligation_map["trust_parameters"]
    ],
}
require(target == generator_manifest["target"], "reconstructed target differs from generator manifest")
require(target == audit["target"], "reconstructed target differs from audit input")
require(target == audit["stage4_preflight"]["target"],
        "reconstructed target differs from recorded preflight")

actual_producer_hashes = {
    "klean_export.py": sha_file(PRODUCERS / "klean_export.py"),
    "klean.py": sha_file(PRODUCERS / "klean.py"),
}
require(actual_producer_hashes == source_manifest["files"], "producer source manifest mismatch")
require(actual_producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"],
        "generator exporter hash")
require(actual_producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"],
        "generator klean.py hash")
require(source_manifest["generator_image_id"] == generator_manifest["provenance"]["generator_image_id"],
        "generator image identity")
require(audit["generation_producer_sources"].endswith(
    source_manifest["generator_image_id"].removeprefix("sha256:")
), "audit input producer directory/image identity")

require(input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
        "input manifest inventory hash")
require(generator_manifest["provenance"]["inventory_sha256"] == inventory["inventory_sha256"],
        "generator inventory hash")

result = {
    "status": "PASS",
    "inventory_rule_count": len(inventory_ids),
    "inventory_sha256": inventory["inventory_sha256"],
    "discovery_manifest_sha256": discovery_hash,
    "independent_domain_rule_ids": DOMAIN_IDS,
    "source_rule_ids": manifest_domain_ids,
    "obligation_source_rule_ids": obligation_ids,
    "obligation_map_sha256": map_hash,
    "producer_hashes": actual_producer_hashes,
    "generator_image_id": source_manifest["generator_image_id"],
    "target": target,
    "checks": {
        "inventory_discovery_bijection_and_order": True,
        "domain_source_obligation_bijection_and_order": True,
        "source_spans_text_and_normalized_hashes": True,
        "conjunct_hashes_and_nonliteral_vacuity": True,
        "parameter_binding_hashes_and_rule_coverage": True,
        "single_fixed_target_and_hashes": True,
        "producer_sources_and_image_identity": True,
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
