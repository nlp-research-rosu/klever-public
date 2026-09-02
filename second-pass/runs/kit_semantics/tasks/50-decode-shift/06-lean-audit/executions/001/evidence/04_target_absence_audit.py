#!/usr/bin/env python3
"""Independent audit of the empty Stage 4 obligation/target relation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
OUTPUT = Path("/audit-output/evidence/04_target_absence_audit.json")


def load(path: Path):
    return json.loads(path.read_text())


obligation_map = load(GENERATED / "obligation-map.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
audit_resolution = load(Path("/audit-input.json"))["resolution"]
classification = load(
    Path("/audit-output/evidence/02_classification_analysis.json")
)
lemmas_path = GENERATED / "Klean50DecodeShift" / "Lemmas.lean"
root_path = GENERATED / "Klean50DecodeShift.lean"
lemmas_text = lemmas_path.read_text()
root_text = root_path.read_text()

declarations = re.findall(
    r"(?m)^\s*(axiom|opaque|def|theorem|lemma)\s+([^\s:(]+)",
    lemmas_text,
)
forbidden_holes = []
for relative, kind, path in klean_export._tree_entries(GENERATED):
    if kind == "file" and path.suffix == ".lean":
        text = path.read_text()
        for match in re.finditer(r"\b(sorry|admit|unsafe)\b", text):
            forbidden_holes.append(
                {
                    "file": relative,
                    "token": match.group(1),
                    "offset": match.start(),
                }
            )

true_domain_count = classification["checks"]["true_domain_lemma_count"]
target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)

checks = {
    "independently_classified_domain_set_empty": true_domain_count == 0,
    "stage4_source_rule_set_empty": input_manifest.get("source_rules") == [],
    "obligation_map_source_rule_set_empty": obligation_map.get("source_rules") == [],
    "obligation_set_empty": obligation_map.get("obligations") == [],
    "trust_parameter_set_empty": obligation_map.get("trust_parameters") == [],
    "exact_empty_bijection": (
        input_manifest.get("source_rules")
        == obligation_map.get("source_rules")
        == obligation_map.get("obligations")
        == []
    ),
    "expected_target_definition_absent": expected_definition is None,
    "parsed_generated_target_absent": target is None,
    "manifest_target_absent": generator_manifest.get("target") is None,
    "audit_input_target_absent": audit_resolution.get("target") is None,
    "lemma_module_has_no_declarations": declarations == [],
    "generated_project_has_no_proof_holes_or_unsafe": forbidden_holes == [],
    "stage5_candidate_absent": not Path("/candidate").exists(),
    "stage5_result_absent": audit_resolution.get("stage5_result") is None,
}

result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/04_target_absence_audit.py"
    ),
    "checks": checks,
    "source_rules": obligation_map.get("source_rules"),
    "obligations": obligation_map.get("obligations"),
    "trust_parameters": obligation_map.get("trust_parameters"),
    "expected_target_definition": expected_definition,
    "parsed_target": target,
    "lemma_module_declarations": declarations,
    "forbidden_holes": forbidden_holes,
    "Klean50DecodeShift.lean": {
        "sha256": hashlib.sha256(root_text.encode()).hexdigest(),
        "text": root_text,
    },
    "Klean50DecodeShift/Lemmas.lean": {
        "sha256": hashlib.sha256(lemmas_text.encode()).hexdigest(),
        "text": lemmas_text,
    },
}

if not all(checks.values()):
    raise SystemExit(f"target absence check failed: {checks}")

OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
