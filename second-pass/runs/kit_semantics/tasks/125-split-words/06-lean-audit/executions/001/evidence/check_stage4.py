#!/usr/bin/env python3
"""Independent empty-domain, obligation-bijection, and target checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT = Path("/audit-input.json")


def load(path: Path) -> dict[str, object]:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def ids(entries: object) -> list[str]:
    assert isinstance(entries, list)
    result = []
    for entry in entries:
        assert isinstance(entry, dict)
        source_rule_id = entry["source_rule_id"]
        assert isinstance(source_rule_id, str)
        result.append(source_rule_id)
    return result


def main() -> None:
    inventory = inventory_verification(K_PROOF)
    discovery = load(DISCOVERY)
    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    audit = load(AUDIT)
    resolution = audit["resolution"]
    assert isinstance(resolution, dict)

    # These are independent semantic judgments, not values copied from Stage 3.
    independent_classifications = {
        "rule-f119e21baa3b2f3f958217ae41d31a07cd861a77cd3db592e16dcd4824e16c2b": "DEFINITION",
        "rule-fe0451a4b26ebe826c1c4ca94a4c96c37fda6ea9eb2e8665a649f842a712f5cb": "DEFINITION",
    }
    inventory_ids = ids(inventory["rules"])
    discovery_ids = ids(discovery["rules"])
    discovered_classifications = {
        entry["source_rule_id"]: entry["classification"]
        for entry in discovery["rules"]
    }
    expected_domain_ids = [
        source_rule_id
        for source_rule_id in inventory_ids
        if independent_classifications[source_rule_id] == "DOMAIN_LEMMA"
    ]
    expected_definition_ids = [
        source_rule_id
        for source_rule_id in inventory_ids
        if independent_classifications[source_rule_id] == "DEFINITION"
    ]

    map_source_ids = ids(obligation_map["source_rules"])
    obligation_entries = obligation_map["obligations"]
    assert isinstance(obligation_entries, list)
    obligation_ids = ids(obligation_entries)
    input_source_ids = ids(input_manifest["source_rules"])
    input_definition_ids = ids(input_manifest["definitions"])

    all_ok = True
    checks = {
        "inventory_order_equals_discovery_order": inventory_ids == discovery_ids,
        "independent_classification_covers_inventory": set(independent_classifications) == set(inventory_ids),
        "independent_equals_discovery": independent_classifications == discovered_classifications,
        "genuine_domain_set_empty": expected_domain_ids == [],
        "input_definitions_exact": input_definition_ids == expected_definition_ids,
        "input_source_rules_exact": input_source_ids == expected_domain_ids,
        "obligation_map_source_rules_exact": map_source_ids == expected_domain_ids,
        "obligation_ids_exact": obligation_ids == expected_domain_ids,
        "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
        "trust_parameters_empty": obligation_map["trust_parameters"] == [],
        "generator_obligation_count_zero": generator_manifest["obligation_count"] == 0,
        "export_obligation_count_zero": export_result["obligation_count"] == 0,
        "generator_target_null": generator_manifest["target"] is None,
        "trusted_target_parser_null": target_statement(GENERATED) is None,
        "audit_target_null": resolution["target"] is None,
        "audit_stage4_target_null": resolution["stage4_preflight"]["target"] is None,
        "audit_mode_classification_only": resolution["mode"] == "CLASSIFICATION_ONLY",
        "candidate_absent": not Path("/candidate").exists(),
        "lean_workspace_unselected": resolution["lean_workspace"] is None,
        "lean_invocation_unselected": resolution["lean_invocation"] is None,
        "selected_status_no_obligations": resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS",
        "generator_status_no_target": export_result["status"] == "KLEAN_NO_OBLIGATIONS",
        "generated_tree_hash_fixed": tree_digest(GENERATED) == generator_manifest["generated_tree_sha256"],
    }

    theorem_declarations = []
    for source in sorted(GENERATED.rglob("*.lean")):
        text = source.read_text()
        for line_number, line in enumerate(text.splitlines(), start=1):
            code = line.split("--", 1)[0]
            if re.match(r"^\s*(?:private\s+)?(?:theorem|lemma)\b", code):
                theorem_declarations.append(
                    f"{source.relative_to(GENERATED)}:{line_number}:{line.strip()}"
                )
    checks["no_generated_theorem_or_lemma_declaration"] = theorem_declarations == []

    for label, ok in checks.items():
        print(f"{label}={ok}")
        all_ok &= ok
    print(f"inventory_ids={inventory_ids}")
    print(f"independent_classifications={independent_classifications}")
    print(f"expected_domain_ids={expected_domain_ids}")
    print(f"expected_definition_ids={expected_definition_ids}")
    print(f"input_source_ids={input_source_ids}")
    print(f"map_source_ids={map_source_ids}")
    print(f"obligation_ids={obligation_ids}")
    print(f"theorem_declarations={theorem_declarations}")
    print(f"target_statement={target_statement(GENERATED)!r}")
    print(f"OVERALL={'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
