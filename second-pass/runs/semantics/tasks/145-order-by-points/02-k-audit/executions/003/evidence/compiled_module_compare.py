#!/usr/bin/env python3
"""Compare the trusted-translated constructor tree with the proof's module.

This reads only the independently rebuilt compiled definition. It extracts the
three nullary function equations used to assemble `solutionModule`, expands the
two body symbols in the module RHS, and compares the resulting canonical KAST
text with `kast` output for the trusted regeneration of solution.mpy.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

compiled_path = Path(
    "/tmp/audit-work/source/verification-kompiled/compiled.txt"
)
translated_path = Path(
    "/tmp/audit-work/source/regenerated-module.kast"
)

compiled_lines = compiled_path.read_text(encoding="utf-8").splitlines()

labels = {
    "module": "`solutionModule_ORDER-BY-POINTS-VERIFICATION_Module`(.KList)",
    "digit_body": "`digitSumBody_ORDER-BY-POINTS-VERIFICATION_Stmts`(.KList)",
    "order_body": "`orderByPointsBody_ORDER-BY-POINTS-VERIFICATION_Stmts`(.KList)",
}


def find_rhs(lhs: str) -> str:
    prefix = f"  rule {lhs}=>"
    matches = [line for line in compiled_lines if line.startswith(prefix)]
    if len(matches) != 1:
        raise AssertionError(f"expected one equation for {lhs}, found {len(matches)}")
    line = matches[0]
    rhs, separator, _conditions = line[len(prefix):].partition(
        ' requires #token("true","Bool")'
    )
    if not separator:
        raise AssertionError(f"could not isolate RHS for {lhs}")
    return rhs


module_rhs = find_rhs(labels["module"])
digit_rhs = find_rhs(labels["digit_body"])
order_rhs = find_rhs(labels["order_body"])

expanded = module_rhs.replace(labels["digit_body"], digit_rhs)
expanded = expanded.replace(labels["order_body"], order_rhs)
translated = translated_path.read_text(encoding="utf-8").strip()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


print("compiled_definition:", compiled_path)
print("trusted_translated_kast:", translated_path)
print("solution_module_equation_count:", module_rhs.count("Module"))
print("digit_body_reference_count_before:", module_rhs.count(labels["digit_body"]))
print("order_body_reference_count_before:", module_rhs.count(labels["order_body"]))
print("proof_expanded_sha256:", digest(expanded))
print("translated_sha256:", digest(translated))
print("proof_expanded_length:", len(expanded))
print("translated_length:", len(translated))
print("constructor_identity:", expanded == translated)

if expanded != translated:
    first = next(
        (
            index
            for index, pair in enumerate(zip(expanded, translated))
            if pair[0] != pair[1]
        ),
        min(len(expanded), len(translated)),
    )
    print("first_difference_offset:", first)
    print("proof_context:", repr(expanded[max(0, first - 80):first + 80]))
    print("translated_context:", repr(translated[max(0, first - 80):first + 80]))
    raise SystemExit(1)
