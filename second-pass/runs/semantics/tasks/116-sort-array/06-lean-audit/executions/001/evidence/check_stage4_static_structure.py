#!/usr/bin/env python3
"""Independent static Stage 4 checks, excluding the unavailable Lake build."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, klean_preflight, lemma_discovery_contract


FROZEN = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def main() -> int:
    validated = lemma_discovery_contract.validate_trust_boundary(
        FROZEN, DISCOVERY
    )
    discovery_hash = hashlib.sha256(DISCOVERY.read_bytes()).hexdigest()
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )

    expected_source_rules = klean_export._domain_source_rules(
        validated, discovery_hash
    )
    gated_source_rules, gated_obligations = (
        klean_preflight._source_and_obligation_gate(
            FROZEN,
            DISCOVERY,
            GENERATED,
            input_manifest,
            generator_manifest,
        )
    )
    target = klean_export.target_statement(GENERATED)
    expected_target = klean_export.expected_target_definition(obligation_map)

    sources = klean_preflight._lean_sources(GENERATED)
    declarations = klean_preflight._trust_declarations(sources)
    klean_preflight._reject_proposition_trust(
        GENERATED, sources, declarations
    )
    klean_preflight._check_imports(GENERATED, sources)

    forbidden_hits: dict[str, list[str]] = {}
    target_occurrences: list[str] = []
    for source in sources:
        relative = source.relative_to(GENERATED).as_posix()
        text = source.read_text()
        hits = [
            token
            for token in ("sorry", "admit", "unsafe")
            if re.search(rf"\b{token}\b", text)
        ]
        if hits:
            forbidden_hits[relative] = hits
        if re.search(r"(?m)^\s*def\s+targetStatement\b", text):
            target_occurrences.append(relative)

    result = {
        "inventory_rule_count": len(validated["rules"]),
        "definition_count": len(validated["definitions"]),
        "operational_rule_count": len(validated["operational_rules"]),
        "proved_derived_lemma_count": len(
            validated["proved_derived_lemmas"]
        ),
        "domain_lemma_count": len(validated["domain_lemmas"]),
        "expected_source_rules": expected_source_rules,
        "input_manifest_source_rules": input_manifest["source_rules"],
        "obligation_map_source_rules": obligation_map["source_rules"],
        "gated_source_rules": gated_source_rules,
        "gated_obligations": gated_obligations,
        "obligation_map_obligations": obligation_map["obligations"],
        "obligation_map_trust_parameters": obligation_map[
            "trust_parameters"
        ],
        "generator_obligation_count": generator_manifest[
            "obligation_count"
        ],
        "export_obligation_count": export_result["obligation_count"],
        "export_status": export_result["status"],
        "target_from_generated_project": target,
        "expected_target_definition": expected_target,
        "generator_manifest_target": generator_manifest["target"],
        "target_occurrences": target_occurrences,
        "forbidden_lean_tokens": forbidden_hits,
        "trust_declaration_count": len(declarations),
        "static_source_and_obligation_gate": "PASS",
        "static_proposition_trust_gate": "PASS",
        "static_import_gate": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
