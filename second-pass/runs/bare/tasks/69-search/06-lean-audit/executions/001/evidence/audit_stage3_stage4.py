#!/usr/bin/env python3
"""Independent semantic classification and zero-obligation/target audit."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def require(label: str, condition: bool) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {label}")
    print(f"PASS: {label}")


def normalize(text: str) -> str:
    return " ".join(text.split())


validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
require("one canonical inventory rule", len(validated["rules"]) == 1)
require("no definitions in local verification.k closure", not validated["definitions"])
require(
    "no operational rules in local verification.k closure",
    not validated["operational_rules"],
)
require(
    "exactly one protected PROVED_DERIVED_LEMMA classification",
    len(validated["proved_derived_lemmas"]) == 1,
)
require("independently empty DOMAIN_LEMMA set", not validated["domain_lemmas"])

rule = validated["rules"][0]
verification = (WORKSPACE / "verification.k").read_text()
loop_claim = (WORKSPACE / "loop-lemma-spec.k").read_text()
core = (WORKSPACE / "verification-core.k").read_text()
semantic = (WORKSPACE / "semantic.k").read_text()
prove_script = (WORKSPACE / "prove.sh").read_text()

rule_match = re.search(
    r"(?ms)^\s*rule\s+(?P<body><k>.*?</result>)\s*"
    r"\[priority\(40\)\]",
    verification,
)
claim_match = re.search(
    r"(?ms)^\s*claim\s+\[loop-invariant\]:\s*"
    r"(?P<body><k>.*?</result>)",
    loop_claim,
)
require("derived rule and prior claim bodies are found", bool(rule_match and claim_match))
require(
    "derived rule is the exact prior reachability body",
    normalize(rule_match.group("body")) == normalize(claim_match.group("body")),
)
require(
    "prior proof module excludes verification.k and VERIFICATION",
    'requires "verification.k"' not in loop_claim
    and "imports VERIFICATION\n" not in loop_claim
    and 'requires "verification.k"' not in core
    and "module VERIFICATION\n" not in core
    and "module VERIFICATION\n" not in semantic,
)
require(
    "Stage 1 command order proves before compiling the reusable rule",
    prove_script.index("kprove loop-lemma-spec.k")
    < prove_script.index("kompile verification.k"),
)
require(
    "rule is not simplification and therefore has no simplification-class constraint",
    "simplification" not in rule["attributes"],
)

# Independent executable reading of the K recurrence and source loop. The K
# proof supplies the universal result; this finite sweep is an adversarial
# semantic sanity check over negative, zero, and positive integers too.
def promote(full: tuple[int, ...], value: int, answer: int) -> int:
    if full.count(value) >= value and value > answer:
        return value
    return answer


def scan(
    full: tuple[int, ...], remaining: tuple[int, ...], answer: int
) -> int:
    result = answer
    for value in remaining:
        result = promote(full, value, result)
    return result


def source_loop(
    full: tuple[int, ...], remaining: tuple[int, ...], answer: int
) -> int:
    for value in remaining:
        if list(full).count(value) >= value:
            if value > answer:
                answer = value
    return answer


values = (-1, 0, 1, 2, 3)
sequences = [
    sequence
    for length in range(4)
    for sequence in itertools.product(values, repeat=length)
]
test_count = 0
for full in sequences:
    for remaining in sequences:
        for answer in values:
            require_equal = scan(full, remaining, answer) == source_loop(
                full, remaining, answer
            )
            if not require_equal:
                raise SystemExit(
                    "FAIL: recurrence/source mismatch "
                    f"full={full} remaining={remaining} answer={answer}"
                )
            test_count += 1
print(f"PASS: recurrence/source finite sweep ({test_count} states)")
examples = [
    ((4, 1, 2, 2, 3, 1), 2),
    ((1, 2, 2, 3, 3, 3, 4, 4, 4), 3),
    ((5, 5, 4, 4, 4), -1),
]
require(
    "prompt examples agree with scan recurrence",
    all(scan(items, items, -1) == expected for items, expected in examples),
)
require(
    "strict-frequency counterfactual is detected",
    scan((2, 2), (2,), -1) == 2
    and not (list((2, 2)).count(2) > 2),
)
require(
    "constant-minus-one counterfactual is detected",
    scan((1,), (1,), -1) == 1,
)

input_manifest = json.loads(
    (GENERATION / "input-manifest.json").read_bytes()
)
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_bytes()
)
export_result = json.loads((GENERATION / "export-result.json").read_bytes())
preflight = json.loads((GENERATION / "preflight.json").read_bytes())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_bytes())
audit_input = json.loads(Path("/audit-input.json").read_bytes())["resolution"]

require("input manifest DOMAIN source_rules is empty", input_manifest["source_rules"] == [])
require(
    "obligation map source-rule side is empty",
    obligation_map["source_rules"] == [],
)
require(
    "obligation map obligation side is empty",
    obligation_map["obligations"] == [],
)
require(
    "empty source-rule/obligation bijection is exact and duplicate-free",
    [rule["source_rule_id"] for rule in input_manifest["source_rules"]]
    == [item["source_rule_id"] for item in obligation_map["obligations"]]
    == [],
)
require(
    "no trust parameters are attached to nonexistent obligations",
    obligation_map["trust_parameters"] == [],
)
require(
    "obligation-map hash is fixed",
    hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
    == generator_manifest["obligation_map_sha256"],
)
require(
    "all statuses and counts select genuine no-obligations",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
    == 0
    and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and preflight["status"] == "KLEAN_NO_OBLIGATIONS",
)
require(
    "expected generated target definition is absent",
    klean_export.expected_target_definition(obligation_map) is None,
)
require(
    "generated target parser finds no target",
    klean_export.target_statement(GENERATED) is None,
)
require(
    "target is identically null across generator, preflight, and audit input",
    generator_manifest["target"] is None
    and preflight["target"] is None
    and audit_input["target"] is None,
)
lean_sources = "\n".join(
    path.read_text() for path in sorted(GENERATED.rglob("*.lean"))
)
require(
    "no generated target or Proof.final declaration",
    re.search(r"\b(?:def|theorem)\s+Target\b", lean_sources) is None
    and "Proof.final" not in lean_sources,
)
require(
    "no vacuous True conjunct was emitted",
    not obligation_map["obligations"]
    and re.search(r"\bdef\s+Target\s*:\s*Prop\s*:=\s*True\b", lean_sources)
    is None,
)
require("classification-only mode has no candidate", not Path("/candidate").exists())

print(
    json.dumps(
        {
            "classification": "PROVED_DERIVED_LEMMA",
            "source_rule_id": rule["source_rule_id"],
            "domain_lemma_count": 0,
            "obligation_count": 0,
            "target": None,
            "finite_semantic_states_checked": test_count,
        },
        indent=2,
        sort_keys=True,
    )
)
