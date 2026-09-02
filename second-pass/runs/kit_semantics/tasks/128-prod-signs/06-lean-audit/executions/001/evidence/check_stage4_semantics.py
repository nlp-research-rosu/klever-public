#!/usr/bin/env python3
"""Independent zero-obligation and fixed-target checks for Stage 4."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, "/reference")
from tools import klean_export  # noqa: E402
from tools.lemma_discovery_contract import validate_trust_boundary  # noqa: E402


def require(condition: bool, message: str) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        raise SystemExit(1)


workspace = Path("/reference/k-proof")
generated = Path("/reference/klean-generation/generated")
discovery_path = Path("/reference/lemma-discovery.json")
validated = validate_trust_boundary(workspace, discovery_path)
obligation_map = json.loads((generated / "obligation-map.json").read_text())
input_manifest = json.loads(Path("/reference/klean-generation/input-manifest.json").read_text())
generator_manifest = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
export_result = json.loads(Path("/reference/klean-generation/export-result.json").read_text())
preflight = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

# Independent semantic judgment established in evidence 05/06: the sole local
# rule is an exact prior proved execution transition, not a domain equation.
independent_domain_rule_ids: list[str] = []
protected_domain_rule_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]
manifest_domain_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

require(independent_domain_rule_ids == protected_domain_rule_ids, "protected DOMAIN_LEMMA set agrees with independent classification")
require(independent_domain_rule_ids == manifest_domain_rule_ids, "Stage 4 input source-rule set is exact")
require(independent_domain_rule_ids == mapped_source_ids, "obligation-map source-rule set is exact")
require(independent_domain_rule_ids == obligation_ids, "source-rule/obligation identities are exactly bijective and ordered")
require(len(obligation_ids) == len(set(obligation_ids)), "no duplicate obligation identities")
require(obligation_map["trust_parameters"] == [], "zero obligations have zero trust parameters")
require(klean_export.expected_target_definition(obligation_map) is None, "zero obligations imply no target definition")
require(klean_export.target_statement(generated) is None, "generated project contains no target declaration")
require(generator_manifest["target"] is None, "generator manifest fixes the target as absent")
require(preflight["target"] is None, "recorded preflight fixes the target as absent")
require(audit["target"] is None, "launcher audit input fixes the target as absent")

for label, count in (
    ("generator", generator_manifest["obligation_count"]),
    ("export", export_result["obligation_count"]),
    ("preflight", preflight["obligation_count"]),
):
    require(count == 0, f"{label} obligation count is zero")

for label, status in (
    ("export", export_result["status"]),
    ("preflight", preflight["status"]),
    ("selection", audit["selections"]["klean_generation"]["status"]),
):
    require(status == "KLEAN_NO_OBLIGATIONS", f"{label} no-obligation status")

all_lean = "\n".join(
    path.read_text() for path in sorted(generated.rglob("*.lean"))
)
require(re.search(r"(?m)^\s*(?:theorem|lemma)\s+", all_lean) is None, "no generated theorem or lemma declaration exists")
require("Proof.final" not in all_lean, "no generated or shadow target named Proof.final")
require(not Path("/candidate").exists(), "classification-only mode has no Stage 5 candidate")
print("VACUOUS_CONJUNCT_COUNT=0 (there are no conjuncts)")
print("FIXED_GENERATED_TARGET=ABSENT")
print("STAGE4_SEMANTIC_AND_BIJECTION_CHECKS_PASS")
