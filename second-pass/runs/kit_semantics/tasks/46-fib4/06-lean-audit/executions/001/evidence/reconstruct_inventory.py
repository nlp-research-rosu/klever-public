#!/usr/bin/env python3
"""Reconstruct and bijectively compare the Stage 3 K rule inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_path = workspace / "verification.k"

inventory = k_rule_inventory.inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(workspace, manifest_path)

print("CANONICAL INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("\nPROTECTED CLASSIFICATION")
print(json.dumps(manifest, indent=2, sort_keys=True))

source_lines = verification_path.read_text().splitlines()
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]

checks: list[tuple[str, bool]] = []
checks.append(("schema_version", inventory["schema_version"] == manifest["schema_version"] == 2))
checks.append(("inventory_sha256", inventory["inventory_sha256"] == manifest["inventory_sha256"]))
checks.append(("exact ordered source_rule_id sequence", canonical_ids == manifest_ids))
checks.append(("canonical IDs unique", len(canonical_ids) == len(set(canonical_ids))))
checks.append(("manifest IDs unique", len(manifest_ids) == len(set(manifest_ids))))
checks.append(("no omitted IDs", not (set(canonical_ids) - set(manifest_ids))))
checks.append(("no extra IDs", not (set(manifest_ids) - set(canonical_ids))))

print("\nRULE-BY-RULE RECONSTRUCTION")
for index, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    independent_hash = hashlib.sha256(normalized.encode()).hexdigest()
    source_slice = "\n".join(source_lines[rule["start_line"] - 1 : rule["end_line"]])
    expected_id = "rule-" + independent_hash
    print(f"rule_index={index}")
    print(f"  module={rule['module']}")
    print(f"  source_span={rule['start_line']}-{rule['end_line']}")
    print(f"  attributes={rule['attributes']}")
    print(f"  normalized_source={normalized}")
    print(f"  independently_recomputed_sha256={independent_hash}")
    print(f"  inventory_normalized_sha256={rule['normalized_sha256']}")
    print(f"  source_rule_id={rule['source_rule_id']}")
    print(f"  protected_classification={manifest['rules'][index]['classification']}")
    print(f"  source_slice_exact={source_slice == rule['text']}")
    checks.append((f"rule {index} exact source slice", source_slice == rule["text"]))
    checks.append((f"rule {index} normalized hash", independent_hash == rule["normalized_sha256"]))
    checks.append((f"rule {index} source_rule_id", expected_id == rule["source_rule_id"]))

print("\nCONTRACT-JOINED COUNTS")
for name in ("definitions", "operational_rules", "proved_derived_lemmas", "domain_lemmas"):
    print(f"{name}={len(validated[name])}")

print("\nBIJECTION CHECKS")
for label, ok in checks:
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
print(f"TOTAL_CHECKS={len(checks)}")
print(f"FAILED_CHECKS={sum(not ok for _, ok in checks)}")
if not all(ok for _, ok in checks):
    raise SystemExit(1)
