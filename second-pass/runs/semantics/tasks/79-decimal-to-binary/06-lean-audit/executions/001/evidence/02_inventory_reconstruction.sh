#!/usr/bin/env bash
set -euo pipefail

echo '$ sha256sum /reference/k-proof/verification.k /reference/lemma-discovery.json'
sha256sum /reference/k-proof/verification.k /reference/lemma-discovery.json

echo '$ PYTHONPATH=/reference python3 - <<PY  # trusted inventory reconstruction and strict ordered comparison'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

print("RECONSTRUCTED_INVENTORY =")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("MANIFEST_IDENTITIES_IN_ORDER =", [r["source_rule_id"] for r in manifest["rules"]])
print("INVENTORY_IDENTITIES_IN_ORDER =", [r["source_rule_id"] for r in inventory["rules"]])

assert inventory["verification_sha256"] == hashlib.sha256(
    (workspace / "verification.k").read_bytes()
).hexdigest()
assert inventory["inventory_sha256"] == canonical_json_sha256(inventory["rules"])
assert manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert [r["source_rule_id"] for r in manifest["rules"]] == [
    r["source_rule_id"] for r in inventory["rules"]
]
assert len(manifest["rules"]) == len(inventory["rules"])
assert len({r["source_rule_id"] for r in manifest["rules"]}) == len(manifest["rules"])

source_lines = (workspace / "verification.k").read_text().splitlines()
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    span_text = "\n".join(source_lines[rule["start_line"] - 1:rule["end_line"]])
    print("RULE_CHECK =", rule["source_rule_id"])
    print("  module =", rule["module"])
    print("  span =", f'{rule["start_line"]}-{rule["end_line"]}')
    print("  attributes =", rule["attributes"])
    print("  normalized_sha256 =", rule["normalized_sha256"])
    print("  exact_span_matches =", span_text == rule["text"])
    print("  independently_rehashed =", digest)
    assert span_text == rule["text"]
    assert digest == rule["normalized_sha256"]
    assert rule["source_rule_id"] == "rule-" + digest

print("VALIDATED_COUNTS =", json.dumps({
    "definitions": len(validated["definitions"]),
    "operational_rules": len(validated["operational_rules"]),
    "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
    "domain_lemmas": len(validated["domain_lemmas"]),
}, sort_keys=True))
print("INVENTORY_BIJECTION_CHECK = PASS")
PY

echo '$ nl -ba /reference/k-proof/verification.k'
nl -ba /reference/k-proof/verification.k

echo '$ sed -n 1,220p /reference/lemma-discovery.json'
sed -n '1,220p' /reference/lemma-discovery.json
