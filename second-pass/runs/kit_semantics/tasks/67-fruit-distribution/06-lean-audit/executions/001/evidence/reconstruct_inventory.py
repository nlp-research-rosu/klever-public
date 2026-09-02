#!/usr/bin/env python3
"""Reconstruct and bijectively compare the frozen proof-local K rule inventory."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract, stage6_resolution_contract


WORKSPACE = Path("/reference/k-proof")
VERIFICATION = WORKSPACE / "verification.k"
DISCOVERY = Path("/reference/lemma-discovery.json")
AUDIT_INPUT = Path("/audit-output/audit-input.json")


def check(label: str, condition: bool) -> None:
    print(f"CHECK {label}: {'PASS' if condition else 'FAIL'}")
    if not condition:
        raise SystemExit(1)


envelope = json.loads(AUDIT_INPUT.read_text())
resolution, _digest = stage6_resolution_contract.verify_audit_input(envelope)
inventory = k_rule_inventory.inventory_verification(WORKSPACE)
manifest = json.loads(DISCOVERY.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, DISCOVERY)
source = VERIFICATION.read_text()
source_sha256 = hashlib.sha256(VERIFICATION.read_bytes()).hexdigest()
manifest_sha256 = hashlib.sha256(DISCOVERY.read_bytes()).hexdigest()
canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
classified_ids = [entry["source_rule_id"] for entry in manifest["rules"]]

print("FROZEN verification.k BEGIN")
print(source, end="" if source.endswith("\n") else "\n")
print("FROZEN verification.k END")
print(f"verification_sha256.direct={source_sha256}")
print(f"discovery_manifest_sha256.direct={manifest_sha256}")
print(f"inventory={json.dumps(inventory, indent=2, sort_keys=True)}")
print(f"discovery={json.dumps(manifest, indent=2, sort_keys=True)}")
print(f"validated.definitions={len(validated['definitions'])}")
print(f"validated.operational_rules={len(validated['operational_rules'])}")
print(f"validated.proved_derived_lemmas={len(validated['proved_derived_lemmas'])}")
print(f"validated.domain_lemmas={len(validated['domain_lemmas'])}")

check("verification source hash self-consistency", inventory["verification_sha256"] == source_sha256)
check(
    "verification source hash matches signed Stage 1 source map",
    source_sha256 == resolution["stage1_source_hashes"]["verification.k"],
)
check(
    "discovery file hash matches signed audit input",
    manifest_sha256 == resolution["hashes"]["discovery_manifest_sha256"],
)
check("selected verification module", inventory["verification_module"] == "VERIFICATION")
check("local verification-module closure", inventory["verification_modules"] == ["VERIFICATION"])
check(
    "independent source scan has no proof-local rule sentence",
    re.search(r"(?m)^\s*rule(?:\s|$)", source) is None,
)
check("canonical inventory has zero entries", inventory["rules"] == [])
check(
    "whole inventory hash recomputation",
    inventory["inventory_sha256"]
    == k_rule_inventory.canonical_json_sha256(inventory["rules"]),
)
check("manifest inventory hash", manifest["inventory_sha256"] == inventory["inventory_sha256"])
check("exact ordered source-rule identity list", classified_ids == canonical_ids)
check("no omitted classifications", len(classified_ids) == len(canonical_ids))
check("no duplicate classifications", len(set(classified_ids)) == len(classified_ids))
check("no extra classifications", set(classified_ids) == set(canonical_ids))
check("validated inventory identity", validated["rules"] == inventory["rules"])
check("genuinely empty independently classified domain set", validated["domain_lemmas"] == [])

print("INDEPENDENT CLASSIFICATION: no entries exist to classify")
print("RESULT: PASS")
