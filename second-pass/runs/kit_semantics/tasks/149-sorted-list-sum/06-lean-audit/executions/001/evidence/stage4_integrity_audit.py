#!/usr/bin/env python3
"""Independently audit Stage 4 sidecars, mapping, and fixed target identity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import klean_export


GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
DISCOVERY = Path("/reference/lemma-discovery.json")
AUDIT_INPUT = Path("/audit-input.json")


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


generator = json.loads((GENERATION / "generator-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)
audit_target = json.loads(AUDIT_INPUT.read_text())["resolution"]["target"]
discovery = json.loads(DISCOVERY.read_text())

source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
parameters = obligation_map["trust_parameters"]
expected_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
observed_ids = [entry["source_rule_id"] for entry in obligations]
source_ids = [entry["source_rule_id"] for entry in source_rules]

expected_conjunct = (
    "∀ (V : SortVal) "
    "(h : («isStrV(_)_MPY-BUILTINS_Bool_Val» V) = true), "
    "((«seqLen(_)_MPY-BUILTINS_Int_Val?» V).isSome = true) ↔ (True)"
)
target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)

binding_checks = []
for parameter in parameters:
    unbound = {
        key: value
        for key, value in parameter.items()
        if key != "binding_sha256"
    }
    recomputed = sha_text(
        json.dumps(
            unbound, sort_keys=True, separators=(",", ":")
        )
    )
    binding_checks.append(
        {
            "name": parameter["name"],
            "recorded": parameter["binding_sha256"],
            "recomputed": recomputed,
            "match": parameter["binding_sha256"] == recomputed,
        }
    )

report = {
    "sidecar_hashes": {
        "obligation_map": {
            "recorded": generator["obligation_map_sha256"],
            "recomputed": sha_bytes(GENERATED / "obligation-map.json"),
        },
        "trust_inventory": {
            "recorded": export_result["trust_inventory_sha256"],
            "recomputed": sha_bytes(GENERATION / "trust-inventory.json"),
        },
        "discovery": {
            "recorded": input_manifest[
                "stage3_discovery_manifest_sha256"
            ],
            "recomputed": sha_bytes(DISCOVERY),
        },
    },
    "bijection": {
        "expected_domain_ids": expected_ids,
        "source_rule_ids": source_ids,
        "obligation_ids": observed_ids,
        "unique_obligation_ids": len(set(observed_ids)) == len(observed_ids),
        "exact_ordered_bijection": (
            expected_ids == source_ids == observed_ids
        ),
        "counts": {
            "manifest": generator["obligation_count"],
            "export_result": export_result["obligation_count"],
            "source_rules": len(source_rules),
            "obligations": len(obligations),
        },
    },
    "obligation": {
        "recorded_conjunct": obligations[0]["lean_conjunct"],
        "independently_expected_conjunct": expected_conjunct,
        "exact_match": obligations[0]["lean_conjunct"] == expected_conjunct,
        "recorded_conjunct_sha256": obligations[0][
            "lean_conjunct_sha256"
        ],
        "recomputed_conjunct_sha256": sha_text(
            obligations[0]["lean_conjunct"]
        ),
        "nonvacuity_countermodel_shape": (
            "A SortVal on which isStrV returns true and seqLen? returns none "
            "falsifies the conjunct; ↔ True does not erase the isSome goal."
        ),
    },
    "parameter_bindings": binding_checks,
    "target": {
        "extracted": target,
        "generator_manifest": generator["target"],
        "audit_input": audit_target,
        "all_target_records_equal": (
            target == generator["target"] == audit_target
        ),
        "expected_definition": expected_definition,
        "expected_definition_sha256": sha_text(expected_definition),
        "lemmas_file_contains_expected_definition": (
            target["definition_sha256"] == sha_text(expected_definition)
        ),
        "statement_sha256_recomputed": sha_text(target["statement"]),
    },
}

for entry in report["sidecar_hashes"].values():
    entry["match"] = entry["recorded"] == entry["recomputed"]

print(json.dumps(report, indent=2, sort_keys=True))
