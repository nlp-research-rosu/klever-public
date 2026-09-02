#!/usr/bin/env python3
"""Independently check Stage 4 hashes, bijections, and fixed target identity."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from tools.k_rule_inventory import inventory_verification


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode())


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def load_generation_exporter():
    path = Path("/reference/generation-tools/klean_export.py")
    specification = importlib.util.spec_from_file_location(
        "generation_time_klean_export", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit_input = load_json(Path("/audit-input.json"))["resolution"]
generator_manifest = load_json(generation / "generator-manifest.json")
input_manifest = load_json(generation / "input-manifest.json")
obligation_map = load_json(generated / "obligation-map.json")
discovery = load_json(Path("/reference/lemma-discovery.json"))
inventory = inventory_verification(Path("/reference/k-proof"))
exporter = load_generation_exporter()

classification_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
independent_domain_rules = [
    {
        **rule,
        **classification_by_id[rule["source_rule_id"]],
        "inventory_sha256": inventory["inventory_sha256"],
        "discovery_manifest_sha256": sha256_bytes(
            Path("/reference/lemma-discovery.json").read_bytes()
        ),
    }
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]]["classification"]
    == "DOMAIN_LEMMA"
]

source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
domain_ids = [rule["source_rule_id"] for rule in independent_domain_rules]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [rule["source_rule_id"] for rule in obligations]
target_from_exact_producer = exporter.target_statement(generated)

checks = {
    "one_genuine_domain_rule": len(independent_domain_rules) == 1,
    "input_manifest_source_rule_bijection": (
        input_manifest["source_rules"] == independent_domain_rules
    ),
    "obligation_map_source_rule_bijection": (
        source_rules == independent_domain_rules
    ),
    "source_id_order": source_ids == domain_ids,
    "obligation_id_order": obligation_ids == domain_ids,
    "source_ids_unique": len(set(source_ids)) == len(source_ids),
    "obligation_ids_unique": len(set(obligation_ids))
    == len(obligation_ids),
    "obligation_count": generator_manifest["obligation_count"]
    == len(obligations)
    == 1,
    "obligation_map_sha256": (
        generator_manifest["obligation_map_sha256"]
        == sha256_bytes((generated / "obligation-map.json").read_bytes())
    ),
    "verification_sha256": input_manifest["verification_sha256"]
    == sha256_bytes(Path("/reference/k-proof/verification.k").read_bytes()),
    "inventory_sha256": input_manifest["inventory_sha256"]
    == inventory["inventory_sha256"],
    "target_exact_producer_to_generator": (
        target_from_exact_producer == generator_manifest["target"]
    ),
    "target_generator_to_audit_input": (
        generator_manifest["target"] == audit_input["target"]
    ),
    "target_definition_hash": (
        target_from_exact_producer["definition_sha256"]
        == generator_manifest["target"]["definition_sha256"]
    ),
    "target_statement_hash": (
        sha256_text(generator_manifest["target"]["statement"])
        == generator_manifest["target"]["statement_sha256"]
    ),
    "nonvacuous_guard_present": (
        "isInt" in obligations[0]["lean_conjunct"]
        and "= true" in obligations[0]["lean_conjunct"]
        and "applyCmp" in obligations[0]["lean_conjunct"]
        and "_==Int_" in obligations[0]["lean_conjunct"]
    ),
    "no_true_conjunct": obligations[0]["lean_conjunct"].strip()
    not in {"True", "(True)"},
}

obligation_checks = []
for obligation, source in zip(obligations, independent_domain_rules):
    obligation_checks.append(
        {
            "source_rule_id": obligation["source_rule_id"],
            "source_span_matches": obligation["source_span"]
            == {
                "start_line": source["start_line"],
                "end_line": source["end_line"],
            },
            "normalized_sha256_matches": obligation["normalized_sha256"]
            == source["normalized_sha256"],
            "inventory_sha256_matches": obligation["inventory_sha256"]
            == source["inventory_sha256"],
            "discovery_manifest_sha256_matches": obligation[
                "discovery_manifest_sha256"
            ]
            == source["discovery_manifest_sha256"],
            "lean_conjunct_sha256_matches": obligation[
                "lean_conjunct_sha256"
            ]
            == sha256_text(obligation["lean_conjunct"]),
        }
    )

failed_checks = sorted(name for name, passed in checks.items() if not passed)
failed_obligation_checks = [
    {
        "source_rule_id": row["source_rule_id"],
        "failed": sorted(
            key
            for key, passed in row.items()
            if key != "source_rule_id" and not passed
        ),
    }
    for row in obligation_checks
    if not all(
        passed
        for key, passed in row.items()
        if key != "source_rule_id"
    )
]
result = {
    "checks": checks,
    "failed_checks": failed_checks,
    "failed_obligation_checks": failed_obligation_checks,
    "domain_source_rule_ids": domain_ids,
    "obligation_checks": obligation_checks,
    "lean_conjuncts": [
        {
            "source_rule_id": obligation["source_rule_id"],
            "lean_conjunct": obligation["lean_conjunct"],
        }
        for obligation in obligations
    ],
    "target": target_from_exact_producer,
}
output = Path("/audit-output/evidence/04-stage4-independent-checks.json")
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
if failed_checks or failed_obligation_checks:
    raise SystemExit(1)
