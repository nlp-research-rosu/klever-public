#!/usr/bin/env python3
"""Run the trusted Stage 1 rule inventory and compare Stage 3 bijectively."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")

inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

print("CANONICAL_INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("STAGE3_MANIFEST")
print(json.dumps(manifest, indent=2, sort_keys=True))

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
print(f"verification_module={inventory['verification_module']}")
print(f"verification_modules={inventory['verification_modules']}")
print(f"verification_sha256={inventory['verification_sha256']}")
print(f"inventory_sha256={inventory['inventory_sha256']}")
print(f"rule_count={len(canonical_ids)}")
print(f"manifest_rule_count={len(manifest_ids)}")
print(f"ordered_identity_match={canonical_ids == manifest_ids}")
print(f"canonical_ids_unique={len(canonical_ids) == len(set(canonical_ids))}")
print(f"manifest_ids_unique={len(manifest_ids) == len(set(manifest_ids))}")
print(f"missing_ids={sorted(set(canonical_ids) - set(manifest_ids))}")
print(f"extra_ids={sorted(set(manifest_ids) - set(canonical_ids))}")
print(f"manifest_inventory_hash_match={manifest['inventory_sha256'] == inventory['inventory_sha256']}")
print(f"validated_definition_count={len(validated['definitions'])}")
print(f"validated_operational_rule_count={len(validated['operational_rules'])}")
print(f"validated_proved_derived_lemma_count={len(validated['proved_derived_lemmas'])}")
print(f"validated_domain_lemma_count={len(validated['domain_lemmas'])}")
