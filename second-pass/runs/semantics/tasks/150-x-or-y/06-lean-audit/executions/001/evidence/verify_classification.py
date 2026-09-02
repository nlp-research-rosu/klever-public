#!/usr/bin/env python3
"""Independent semantic checks for the Stage 3 classifications."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


VERIFICATION = Path("/reference/k-proof/verification.k")
SPEC = Path("/reference/k-proof/spec.k")
PROVE = Path("/reference/k-proof/prove.sh")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalized(text: str) -> str:
    return " ".join(text.split())


verification_text = VERIFICATION.read_text()
spec_text = SPEC.read_text()
prove_text = PROVE.read_text()

claim_match = re.search(
    r"(?ms)^  claim(?P<body>.*?)^    \[label\(loop_correct\)\]$",
    spec_text,
)
rule_match = re.search(
    r"(?ms)^  rule(?P<body>.*?)^    \[priority\(40\)\]$",
    verification_text[
        verification_text.index("module X-OR-Y-SUMMARY") :
    ],
)
require(claim_match is not None, "cannot locate loop_correct claim")
require(rule_match is not None, "cannot locate summary rewrite")
claim_core = normalized(claim_match.group("body"))
rule_core = normalized(rule_match.group("body"))
require(claim_core == rule_core, "proved claim and reused rewrite bodies differ")

module_imports: dict[str, list[str]] = {}
for match in re.finditer(
    r"(?ms)^module (?P<name>[A-Z0-9-]+)\n(?P<body>.*?)^endmodule$",
    verification_text + "\n" + spec_text,
):
    module_imports[match.group("name")] = re.findall(
        r"(?m)^  imports ([A-Z0-9-]+)$", match.group("body")
    )

require(
    module_imports["X-OR-Y-LOOP-SPEC"] == ["X-OR-Y-VERIFICATION"],
    "loop proof imports something other than the base verification module",
)
require(
    "X-OR-Y-SUMMARY" not in module_imports["X-OR-Y-LOOP-SPEC"],
    "loop proof imports the summary rule it is meant to prove",
)
require(
    module_imports["X-OR-Y-SUMMARY"] == ["X-OR-Y-VERIFICATION"],
    "summary module does not extend exactly the base module",
)
require(
    module_imports["X-OR-Y-MAIN-SPEC"] == ["X-OR-Y-SUMMARY"],
    "main proof does not import the proved summary later",
)

ordered_markers = [
    "--main-module X-OR-Y-VERIFICATION",
    "--spec-module X-OR-Y-LOOP-SPEC",
    "--claims loop_correct",
    "--main-module X-OR-Y-SUMMARY",
    "--spec-module X-OR-Y-MAIN-SPEC",
    "--claims main_correct",
]
positions = [prove_text.index(marker) for marker in ordered_markers]
require(
    positions == sorted(positions) and len(positions) == len(set(positions)),
    "prove.sh does not prove the base-module claim before later summary use",
)


def source_suffix(n: int, d: int, x: str, y: str) -> str:
    if n < 2:
        return y
    for divisor in range(d, n):
        if n % divisor == 0:
            return y
    return x


def prime_select(n: int, d: int, x: str, y: str) -> str:
    if n < 2:
        return y
    if d >= n:
        return x
    if n % d == 0:
        return y
    return prime_select(n, d + 1, x, y)


def source_scan_last(n: int, d: int, old: int) -> int:
    for divisor in range(d, n):
        old = divisor
        if n % divisor == 0:
            return old
    return old


def scan_last(n: int, d: int, old: int) -> int:
    if d >= n:
        return old
    if n % d == 0:
        return d
    return scan_last(n, d + 1, d)


prime_mismatches: list[dict[str, object]] = []
scan_mismatches: list[dict[str, object]] = []
prime_cases = 0
scan_cases = 0
for n in range(-8, 81):
    for d in range(2, 84):
        prime_cases += 1
        observed = prime_select(n, d, "X", "Y")
        expected = source_suffix(n, d, "X", "Y")
        if observed != expected:
            prime_mismatches.append(
                {"n": n, "d": d, "expected": expected, "observed": observed}
            )
        if n >= 2:
            for old in (-7, 0, 2, 79):
                scan_cases += 1
                observed_last = scan_last(n, d, old)
                expected_last = source_scan_last(n, d, old)
                if observed_last != expected_last:
                    scan_mismatches.append(
                        {
                            "n": n,
                            "d": d,
                            "old": old,
                            "expected": expected_last,
                            "observed": observed_last,
                        }
                    )
require(not prime_mismatches, "primeSelect counterexample found")
require(not scan_mismatches, "scanLast counterexample found")

counterfactuals = [
    {
        "mutation": "primeSelect base N<2 returns X",
        "witness": {"n": 1, "d": 2, "x": "X", "y": "Y"},
        "source": source_suffix(1, 2, "X", "Y"),
        "mutant": "X",
    },
    {
        "mutation": "primeSelect divisor case returns X",
        "witness": {"n": 15, "d": 3, "x": "X", "y": "Y"},
        "source": source_suffix(15, 3, "X", "Y"),
        "mutant": "X",
    },
    {
        "mutation": "primeSelect terminal case returns Y",
        "witness": {"n": 7, "d": 7, "x": "X", "y": "Y"},
        "source": source_suffix(7, 7, "X", "Y"),
        "mutant": "Y",
    },
    {
        "mutation": "scanLast recursive step keeps OLD",
        "witness": {"n": 7, "d": 2, "old": -7},
        "source": source_scan_last(7, 2, -7),
        "mutant": -7,
    },
]
require(
    all(item["source"] != item["mutant"] for item in counterfactuals),
    "counterfactual witness does not discriminate",
)

result = {
    "derived_lemma": {
        "claim_core_equals_rule_core": True,
        "core_sha256": hashlib.sha256(claim_core.encode()).hexdigest(),
        "claim_attribute": "label(loop_correct)",
        "reuse_attribute": "priority(40)",
        "attribute_effect": (
            "label names the proof claim; priority schedules later application "
            "and does not alter the proved reachability relation"
        ),
        "module_imports": module_imports,
        "prove_sh_order": ordered_markers,
        "base_proof_excludes_summary": True,
        "later_main_proof_imports_summary": True,
    },
    "definition_checks": {
        "primeSelect": {
            "tested_cases": prime_cases,
            "mismatches": prime_mismatches,
            "coverage": (
                "D>=2 partitions into N<2; or N>=2 with D>=N; or "
                "D<N and pyMod equal/non-equal to zero"
            ),
            "descent": "the only recursive branch increases D until D>=N",
        },
        "scanLast": {
            "tested_cases": scan_cases,
            "mismatches": scan_mismatches,
            "coverage": (
                "N>=2,D>=2 partitions into D>=N; or D<N and "
                "pyMod equal/non-equal to zero"
            ),
            "descent": "the only recursive branch increases D until D>=N",
        },
        "counterfactuals": counterfactuals,
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
