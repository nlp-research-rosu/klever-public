#!/usr/bin/env python3
"""Independent Stage 3 to Stage 4 bijection and target-identity checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
    validated = validate_trust_boundary(K_PROOF, DISCOVERY)
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())

    domain_rules = validated["domain_lemmas"]
    expected_ids = [rule["source_rule_id"] for rule in domain_rules]
    mapped_source_ids = [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
    obligation_ids = [rule["source_rule_id"] for rule in obligation_map["obligations"]]

    print(f"independently classified domain rule count={len(domain_rules)}")
    print(f"expected domain source-rule IDs={expected_ids}")
    print(f"input-manifest source_rules={input_manifest['source_rules']}")
    print(f"obligation-map source-rule IDs={mapped_source_ids}")
    print(f"obligation source-rule IDs={obligation_ids}")
    print(f"trust_parameters={obligation_map['trust_parameters']}")
    assert domain_rules == []
    assert input_manifest["source_rules"] == []
    assert expected_ids == mapped_source_ids == obligation_ids == []
    assert obligation_map["trust_parameters"] == []
    assert len(obligation_ids) == len(set(obligation_ids))

    empty_categories = (
        "definitions",
        "lowered_structural_definition_rules",
        "operational_rules",
        "proved_derived_lemmas",
        "promoted_structural_definitions",
        "summary_functions",
    )
    for category in empty_categories:
        print(f"input-manifest {category}={input_manifest[category]}")
        assert input_manifest[category] == []

    generated_target = klean_export.target_statement(GENERATED)
    expected_definition = klean_export.expected_target_definition(obligation_map)
    lemmas_text = (GENERATED / "Klean159Eat" / "Lemmas.lean").read_text()
    proposition_declarations = re.findall(
        r"(?m)^\s*(?:theorem|lemma|example)\s+([^\s:(]+)", lemmas_text
    )
    print(f"expected target definition={expected_definition!r}")
    print(f"parsed generated target={generated_target!r}")
    print(f"generator-manifest target={generator_manifest['target']!r}")
    print(f"audit-input target={audit['target']!r}")
    print(f"proposition declarations in Lemmas.lean={proposition_declarations}")
    assert expected_definition is None
    assert generated_target is None
    assert generator_manifest["target"] is None
    assert audit["target"] is None
    assert proposition_declarations == []

    print(f"generator obligation_count={generator_manifest['obligation_count']}")
    print(f"export obligation_count={export_result['obligation_count']}")
    print(f"export status={export_result['status']}")
    assert generator_manifest["obligation_count"] == 0
    assert export_result["obligation_count"] == 0
    assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    assert not Path("/candidate").exists()
    print("vacuous generated conjuncts=[]")
    print("STAGE4_RESULT: PASS")


if __name__ == "__main__":
    main()
