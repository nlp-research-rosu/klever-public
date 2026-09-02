#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and manifest comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
audit_input = json.loads(AUDIT_INPUT.read_text())
resolution = audit_input["resolution"]
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

checks: list[tuple[str, bool, object]] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append((name, condition, detail))


check(
    "verification source hash matches audit input",
    inventory["verification_sha256"]
    == resolution["stage1_source_hashes"]["verification.k"],
    {
        "reconstructed": inventory["verification_sha256"],
        "recorded": resolution["stage1_source_hashes"]["verification.k"],
    },
)
check(
    "discovery file hash matches audit input",
    sha256_file(DISCOVERY)
    == resolution["hashes"]["discovery_manifest_sha256"],
    {
        "actual": sha256_file(DISCOVERY),
        "recorded": resolution["hashes"]["discovery_manifest_sha256"],
    },
)

recomputed_rule_details = []
for ordinal, rule in enumerate(inventory["rules"]):
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip(" \t\r\n")
    local = {
        "ordinal": ordinal,
        "source_rule_id": rule["source_rule_id"],
        "module": rule["module"],
        "span": [rule["start_line"], rule["end_line"]],
        "attributes": rule["attributes"],
        "normalized_sha256": rule["normalized_sha256"],
        "independent_normalized_sha256": normalized_sha256,
        "span_exact": span_text == rule["text"],
        "id_exact": rule["source_rule_id"] == f"rule-{normalized_sha256}",
    }
    recomputed_rule_details.append(local)
    check(
        f"rule {ordinal} source span and hashes",
        local["span_exact"]
        and local["id_exact"]
        and rule["normalized_sha256"] == normalized_sha256,
        local,
    )

inventory_hash = canonical_json_sha256(inventory["rules"])
check(
    "whole reconstructed inventory hash",
    inventory_hash
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"],
    {
        "independent": inventory_hash,
        "trusted_inventory": inventory["inventory_sha256"],
        "protected_discovery": discovery["inventory_sha256"],
    },
)

reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check(
    "ordered source-rule identity equality",
    reconstructed_ids == discovery_ids,
    {
        "reconstructed": reconstructed_ids,
        "protected_discovery": discovery_ids,
    },
)
check(
    "reconstructed IDs unique",
    len(reconstructed_ids) == len(set(reconstructed_ids)),
    reconstructed_ids,
)
check(
    "protected discovery IDs unique",
    len(discovery_ids) == len(set(discovery_ids)),
    discovery_ids,
)
check(
    "bijection without omissions or extras",
    len(reconstructed_ids) == len(discovery_ids)
    and set(reconstructed_ids) == set(discovery_ids),
    {
        "reconstructed_count": len(reconstructed_ids),
        "discovery_count": len(discovery_ids),
        "omitted_from_discovery": sorted(set(reconstructed_ids) - set(discovery_ids)),
        "extra_in_discovery": sorted(set(discovery_ids) - set(reconstructed_ids)),
    },
)
check(
    "each protected entry has one accounted classification",
    all(
        isinstance(rule.get("classification"), str)
        and bool(rule["classification"])
        and isinstance(rule.get("rationale"), str)
        and bool(rule["rationale"])
        for rule in discovery["rules"]
    ),
    [
        {
            "source_rule_id": rule.get("source_rule_id"),
            "classification": rule.get("classification"),
            "rationale_present": bool(rule.get("rationale")),
        }
        for rule in discovery["rules"]
    ],
)

print(
    json.dumps(
        {
            "reconstructed_inventory": inventory,
            "independent_rule_checks": recomputed_rule_details,
            "checks": [
                {"name": name, "pass": passed, "detail": detail}
                for name, passed, detail in checks
            ],
            "all_checks_pass": all(passed for _name, passed, _detail in checks),
        },
        indent=2,
        ensure_ascii=False,
    )
)
