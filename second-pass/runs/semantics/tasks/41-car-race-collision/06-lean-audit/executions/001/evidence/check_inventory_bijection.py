#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification_text = (workspace / "verification.k").read_text()
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)

canonical_rules = inventory["rules"]
manifest_rules = manifest["rules"]
canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]

checks: list[tuple[str, bool, str]] = []


def check(label: str, condition: bool, detail: str) -> None:
    checks.append((label, condition, detail))


check(
    "inventory hash recomputation",
    canonical_json_sha256(canonical_rules) == inventory["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "manifest inventory hash",
    manifest["inventory_sha256"] == inventory["inventory_sha256"],
    f"manifest={manifest['inventory_sha256']} canonical={inventory['inventory_sha256']}",
)
check(
    "identity order",
    manifest_ids == canonical_ids,
    f"manifest={manifest_ids} canonical={canonical_ids}",
)
check(
    "canonical identity uniqueness",
    len(canonical_ids) == len(set(canonical_ids)),
    repr(canonical_ids),
)
check(
    "manifest identity uniqueness",
    len(manifest_ids) == len(set(manifest_ids)),
    repr(manifest_ids),
)
check(
    "no omitted or extra identities",
    set(manifest_ids) == set(canonical_ids),
    f"omitted={sorted(set(canonical_ids)-set(manifest_ids))} "
    f"extra={sorted(set(manifest_ids)-set(canonical_ids))}",
)
check(
    "trusted contract validation",
    len(validated["rules"]) == len(canonical_rules),
    f"validated_count={len(validated['rules'])}",
)

source_lines = verification_text.splitlines()
for index, rule in enumerate(canonical_rules):
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(span_text.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    check(
        f"rule {index} exact source span",
        span_text == rule["text"],
        f"lines={rule['start_line']}-{rule['end_line']}",
    )
    check(
        f"rule {index} normalized source hash",
        normalized_sha256 == rule["normalized_sha256"],
        f"actual={normalized_sha256} recorded={rule['normalized_sha256']}",
    )
    check(
        f"rule {index} source_rule_id",
        rule["source_rule_id"] == "rule-" + normalized_sha256,
        rule["source_rule_id"],
    )

for label, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'}\t{label}\t{detail}")

failures = [label for label, passed, _detail in checks if not passed]
print(f"CANONICAL_RULE_COUNT={len(canonical_rules)}")
print(f"MANIFEST_RULE_COUNT={len(manifest_rules)}")
print(f"TOTAL_CHECKS={len(checks)}")
print(f"TOTAL_FAILURES={len(failures)}")
if failures:
    raise SystemExit(1)
