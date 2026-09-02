#!/usr/bin/env python3
import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


frozen = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

validated = validate_trust_boundary(frozen, discovery_path)
input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads(
    (generation / "export-result.json").read_text()
)
recorded_preflight = json.loads(
    (generation / "preflight.json").read_text()
)
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

independent_domain_ids = [
    rule["source_rule_id"] for rule in validated["rules"]
    if rule["source_rule_id"] in {
        entry["source_rule_id"]
        for entry in validated["domain_lemmas"]
    }
]
mapped_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

raw_target_declarations = []
for path in sorted(generated.rglob("*.lean")):
    for match in re.finditer(
        r"(?m)^\s*def\s+targetStatement\b", path.read_text()
    ):
        raw_target_declarations.append(
            {
                "file": path.relative_to(generated).as_posix(),
                "offset": match.start(),
            }
        )

target = klean_export.target_statement(generated)
expected_target = klean_export.expected_target_definition(obligation_map)

checks = {
    "independent domain set is empty": independent_domain_ids == [],
    "input manifest domain source rules empty": (
        input_manifest["source_rules"] == []
    ),
    "mapped domain source rules empty": (
        obligation_map["source_rules"] == []
    ),
    "source/obligation ID sequences are bijective": (
        independent_domain_ids == mapped_source_ids == obligation_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "obligations empty": obligation_map["obligations"] == [],
    "trust parameters empty": obligation_map["trust_parameters"] == [],
    "no vacuous or weakened conjunct exists": (
        len(obligation_map["obligations"]) == 0
    ),
    "generator obligation count zero": (
        generator_manifest["obligation_count"] == 0
    ),
    "export obligation count zero": export_result["obligation_count"] == 0,
    "preflight obligation count zero": (
        recorded_preflight["obligation_count"] == 0
    ),
    "audit obligation count zero": (
        audit["stage4_preflight"]["obligation_count"] == 0
    ),
    "generator target absent": generator_manifest["target"] is None,
    "preflight target absent": recorded_preflight["target"] is None,
    "audit target absent": (
        audit["target"] is None
        and audit["stage4_preflight"]["target"] is None
    ),
    "trusted target parser finds no target": target is None,
    "expected target definition absent": expected_target is None,
    "independent target scan finds no declaration": (
        raw_target_declarations == []
    ),
    "all statuses are KLEAN_NO_OBLIGATIONS": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and audit["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
        and audit["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "definitions preserved in exact order": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "no Stage 5 candidate": not Path("/candidate").exists(),
    "no Stage 5 launcher result": audit["stage5_result"] is None,
    "no Lean workspace or invocation": (
        audit["lean_workspace"] is None
        and audit["lean_invocation"] is None
    ),
}

print(
    json.dumps(
        {
            "independent_domain_rule_ids": independent_domain_ids,
            "mapped_source_rule_ids": mapped_source_ids,
            "obligation_rule_ids": obligation_ids,
            "target_statement": target,
            "expected_target_definition": expected_target,
            "raw_target_declarations": raw_target_declarations,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
