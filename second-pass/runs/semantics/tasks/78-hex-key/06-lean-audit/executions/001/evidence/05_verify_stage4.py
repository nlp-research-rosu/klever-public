#!/usr/bin/env python3
"""Independent no-obligation, bijection, and fixed-target checks."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from tools import klean_export as trusted_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


generation = Path("/reference/klean-generation")
generated = generation / "generated"
manifest = json.loads(Path("/reference/lemma-discovery.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
inventory = inventory_verification(Path("/reference/k-proof"))
validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

producer_spec = importlib.util.spec_from_file_location(
    "generation_time_klean_export",
    "/reference/generation-tools/klean_export.py",
)
assert producer_spec is not None and producer_spec.loader is not None
producer_export = importlib.util.module_from_spec(producer_spec)
sys.modules[producer_spec.name] = producer_export
producer_spec.loader.exec_module(producer_export)

failures: list[str] = []


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status}: {label}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        failures.append(label)


# This is the independent semantic classification reached from verification.k:
# two named AST macros, two named predicate/indicator equations, and the
# base/step recurrences for two named summaries.  None asserts a free-standing
# mathematical fact.
independent_classification = {
    "rule-a21c4e1376187971c7643f3e565cabcbfd4adf8fb326ad1b1ed66d8ccf2ee5dc": "DEFINITION",
    "rule-997f1164935d81cf0a177321cded75d4547861c8641b38c27297eb3d9a029072": "DEFINITION",
    "rule-05b5f69701a4c26d96e9102f57d9aa376b71ec50124579bbae35e8fbfd93bf81": "DEFINITION",
    "rule-3532524624ac91c8c5bef2d87f5c2bf88f8419752a22a63b80e9c9fca7ff5702": "DEFINITION",
    "rule-1f493419665e264916f30ab5358e05eef39549f5227088474c1ff240d5e27abe": "DEFINITION",
    "rule-690663e02cb1ae6cd79a33453a4d2c75dbd0a76973cc10dc57fcdd89a7cf8993": "DEFINITION",
    "rule-2c5863a720c0bb1e81a39efe6316267a1af396797c22acd873b152227333ade3": "DEFINITION",
    "rule-f95b3740442b75f1ff5a75424586af712960c05b37858b16c5f6802d8b9b2d38": "DEFINITION",
}
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
check(
    "independent classification covers exact ordered inventory",
    list(independent_classification),
    inventory_ids,
)
manifest_classification = {
    entry["source_rule_id"]: entry["classification"]
    for entry in manifest["rules"]
}
check(
    "protected classification equals independent classification",
    manifest_classification,
    independent_classification,
)
check(
    "input-manifest definitions preserve reconstructed order and content",
    input_manifest["definitions"],
    validated["definitions"],
)
check("input-manifest operational rules", input_manifest["operational_rules"], [])
check(
    "input-manifest proved-derived lemmas",
    input_manifest["proved_derived_lemmas"],
    [],
)
check(
    "input-manifest summary functions",
    input_manifest["summary_functions"],
    [
        {
            "name": "isPrimeHexCode",
            "return_sort": "Bool",
            "argument_sorts": ["Int"],
        },
        {
            "name": "primeHexBit",
            "return_sort": "Int",
            "argument_sorts": ["Int"],
        },
        {
            "name": "hexCount",
            "return_sort": "Int",
            "argument_sorts": ["IntSeq"],
        },
        {
            "name": "finalDigit",
            "return_sort": "Val",
            "argument_sorts": ["IntSeq", "Val"],
        },
    ],
)

true_domain_ids = [
    source_rule_id
    for source_rule_id, role in independent_classification.items()
    if role == "DOMAIN_LEMMA"
]
check("independently classified domain set", true_domain_ids, [])
check("input-manifest domain source rules", input_manifest["source_rules"], [])
check("obligation-map source rules", obligation_map["source_rules"], [])
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("export obligation count", export_result["obligation_count"], 0)
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")

producer_target = producer_export.target_statement(generated)
trusted_target = trusted_export.target_statement(generated)
producer_expected_definition = producer_export.expected_target_definition(
    obligation_map
)
trusted_expected_definition = trusted_export.expected_target_definition(
    obligation_map
)
check("generation-time producer target", producer_target, None)
check("trusted checker target", trusted_target, None)
check("generation-time expected target definition", producer_expected_definition, None)
check("trusted expected target definition", trusted_expected_definition, None)
check("generator-manifest fixed target", generator_manifest["target"], None)

raw_target_declarations: list[str] = []
for path in sorted(generated.rglob("*.lean")):
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", path.read_text()):
        raw_target_declarations.append(
            f"{path.relative_to(generated).as_posix()}:{match.start()}"
        )
check("raw generated target declaration set", raw_target_declarations, [])

lemmas_text = (generated / "Klean78HexKey" / "Lemmas.lean").read_text()
check("Lemmas.lean has no proposition body", "targetStatement" in lemmas_text, False)
check("classification-only candidate absence", Path("/candidate").exists(), False)

print("SOURCE_RULE_OBLIGATION_BIJECTION=[] <-> []")
print("No conjunct exists to be irrelevant, weakened, duplicated, or vacuous.")
print(f"TOTAL_FAILURES={len(failures)}")
if failures:
    print("FAILED_LABELS=" + json.dumps(failures))
    raise SystemExit(1)
