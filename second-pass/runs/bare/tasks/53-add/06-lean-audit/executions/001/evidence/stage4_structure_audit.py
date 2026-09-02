#!/usr/bin/env python3
"""Independent structural and zero-obligation audit of Stage 4."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path


REFERENCE = Path("/reference")
GENERATION = REFERENCE / "klean-generation"
GENERATED = GENERATION / "generated"


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_sha256(value: object) -> str:
    return sha256_bytes(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    )


def report(label: str, value: object) -> None:
    print(json.dumps({"check": label, "value": value}, sort_keys=True))


def main() -> int:
    audit_input = read_json(Path("/audit-input.json"))
    resolution = audit_input["resolution"]
    discovery = read_json(REFERENCE / "lemma-discovery.json")
    input_manifest = read_json(GENERATION / "input-manifest.json")
    generator_manifest = read_json(GENERATION / "generator-manifest.json")
    export_result = read_json(GENERATION / "export-result.json")
    obligation_path = GENERATED / "obligation-map.json"
    obligation_map = read_json(obligation_path)

    inventory_rules = discovery["rules"]
    assert inventory_rules == []
    empty_inventory_hash = canonical_json_sha256([])
    assert discovery["inventory_sha256"] == empty_inventory_hash
    report("canonical_empty_inventory_sha256", empty_inventory_hash)

    classified_domain_rules = [
        entry
        for entry in inventory_rules
        if entry["classification"] == "DOMAIN_LEMMA"
    ]
    assert classified_domain_rules == []
    for category in (
        "definitions",
        "operational_rules",
        "proved_derived_lemmas",
        "source_rules",
        "summary_functions",
    ):
        assert input_manifest[category] == []
    report("independently_derived_domain_rule_ids", [])

    source_rules = obligation_map["source_rules"]
    obligations = obligation_map["obligations"]
    trust_parameters = obligation_map["trust_parameters"]
    assert source_rules == classified_domain_rules
    assert obligations == []
    assert trust_parameters == []
    assert len({entry["source_rule_id"] for entry in source_rules}) == len(
        source_rules
    )
    assert [entry["source_rule_id"] for entry in obligations] == [
        entry["source_rule_id"] for entry in source_rules
    ]
    report(
        "source_rule_obligation_bijection",
        {
            "source_rule_ids": [],
            "obligation_ids": [],
            "duplicate_count": 0,
        },
    )

    obligation_map_sha256 = sha256_bytes(obligation_path.read_bytes())
    assert (
        generator_manifest["obligation_map_sha256"]
        == obligation_map_sha256
    )
    assert generator_manifest["obligation_count"] == 0
    assert export_result["obligation_count"] == 0
    report("obligation_map_sha256", obligation_map_sha256)

    target_occurrences: list[str] = []
    forbidden_occurrences: list[str] = []
    for source in sorted(GENERATED.rglob("*.lean")):
        text = source.read_text()
        for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", text):
            target_occurrences.append(
                f"{source.relative_to(GENERATED)}:{text.count(chr(10), 0, match.start()) + 1}"
            )
        for token in ("sorry", "admit", "unsafe"):
            if re.search(rf"\b{token}\b", text):
                forbidden_occurrences.append(
                    f"{source.relative_to(GENERATED)}:{token}"
                )
    assert target_occurrences == []
    assert forbidden_occurrences == []
    assert generator_manifest["target"] is None
    assert resolution["target"] is None
    assert resolution["stage4_preflight"]["target"] is None
    report(
        "fixed_generated_target",
        {
            "target_occurrences": target_occurrences,
            "generator_manifest_target": None,
            "audit_input_target": None,
        },
    )

    assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    assert resolution["selections"]["klean_generation"]["status"] == (
        "KLEAN_NO_OBLIGATIONS"
    )
    assert resolution["stage4_preflight"]["status"] == (
        "KLEAN_NO_OBLIGATIONS"
    )
    assert os.environ.get("AUDIT_MODE") == "CLASSIFICATION_ONLY"
    assert resolution["mode"] == "CLASSIFICATION_ONLY"
    assert resolution["stage5_result"] is None
    assert resolution["lean_workspace"] is None
    assert resolution["lean_invocation"] is None
    assert not Path("/candidate").exists()
    report(
        "classification_only_stage5_absence",
        {
            "candidate_exists": False,
            "lean_workspace": None,
            "lean_invocation": None,
            "stage5_result": None,
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
