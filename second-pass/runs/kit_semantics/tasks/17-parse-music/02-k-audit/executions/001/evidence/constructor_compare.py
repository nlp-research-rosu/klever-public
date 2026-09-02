#!/usr/bin/env python3
"""Mechanically compare the submitted function constructor with the claim body."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-src")
SOLUTION_MPY = WORK / "solution.regenerated.mpy"
VERIFICATION_K = WORK / "verification.k"
SPEC_K = WORK / "spec.k"
DEFINITION = WORK / "verification-audit-kompiled"
CLAIM_FUNCTION_MPY = Path("/audit-output/evidence/claim_function.mpy")
CLAIM_FUNCTION_RAW = Path("/audit-output/evidence/claim_function_raw.txt")


def extract_rule_rhs(source: str, rule_head: str) -> str:
    lines = source.splitlines()
    start = None
    first = ""
    prefix = f"  rule {rule_head} =>"
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            start = index + 1
            first = line[len(prefix) :].strip()
            break
    if start is None:
        raise AssertionError(f"missing rule {rule_head}")
    body = ([first] if first else []) + lines[start:]
    kept = []
    for line in body:
        if line.startswith("  rule "):
            break
        kept.append(line)
    while kept and (not kept[-1].strip() or kept[-1].lstrip().startswith("//")):
        kept.pop()
    rhs = "\n".join(kept).strip()
    if not rhs:
        raise AssertionError(f"empty RHS for {rule_head}")
    return rhs


def parse_module(path: Path) -> dict:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
        str(path),
    ]
    completed = subprocess.run(
        command, cwd=WORK, text=True, capture_output=True, check=False
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"kast failed exit={completed.returncode}\n{completed.stderr}"
        )
    return json.loads(completed.stdout)["term"]


def find_apply(term: dict, label_prefix: str) -> list[dict]:
    result = []
    if term.get("node") == "KApply":
        name = term["label"]["name"]
        if name.startswith(label_prefix):
            result.append(term)
        for argument in term.get("args", []):
            result.extend(find_apply(argument, label_prefix))
    return result


def stable_digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    verification = VERIFICATION_K.read_text()
    spec_source = SPEC_K.read_text()
    call_pattern = (
        r'Call\s*\(\s*Name\s*\(\s*"parse_music"\s*\)\s*,\s*'
        r"str\s*\(\s*CS:IntSeq\s*\)\s*,\s*\.Exprs\s*\)"
    )
    binding_pattern = (
        r'"parse_music"\s*\|->\s*closureVal\s*\(\s*"music_string"\s*,\s*'
        r"\.ParamNames\s*,\s*parseMusicBody\s*,\s*0\s*\)"
    )
    assert len(re.findall(call_pattern, spec_source)) == 1
    assert len(re.findall(binding_pattern, spec_source)) == 1
    rhs = extract_rule_rhs(verification, "parseMusicBody")
    char_rhs = extract_rule_rhs(verification, "parseMusicCharBody")
    alias_occurrences = rhs.count("parseMusicCharBody")
    assert alias_occurrences == 1
    expanded_rhs = rhs.replace("parseMusicCharBody", char_rhs)
    raw_wrapper = (
        'Module(\n  FuncDef("parse_music", Params("music_string"),\n'
        + expanded_rhs
        + "))\n"
    )
    CLAIM_FUNCTION_RAW.write_text(raw_wrapper)
    # The K-rule outer parser spells empty sequence units as .Exprs/.Stmts.
    # The MPY program parser spells the same units by omission.
    expr_units = expanded_rhs.count(".Exprs")
    stmts_units = expanded_rhs.count(".Stmts")
    normalized_rhs = re.sub(r"\s*,\s*\.Exprs(?=\s*\))", "", expanded_rhs)
    normalized_rhs = normalized_rhs.replace(".Exprs", "")
    normalized_rhs = normalized_rhs.replace(".Stmts", "")
    wrapper = (
        'Module(\n  FuncDef("parse_music", Params("music_string"),\n'
        + normalized_rhs
        + "))\n"
    )
    CLAIM_FUNCTION_MPY.write_text(wrapper)

    solution_term = parse_module(SOLUTION_MPY)
    claim_term = parse_module(CLAIM_FUNCTION_MPY)
    solution_functions = find_apply(solution_term, "FuncDef(_,_,_)")
    claim_functions = find_apply(claim_term, "FuncDef(_,_,_)")
    assert len(solution_functions) == 1
    assert len(claim_functions) == 1
    assert solution_functions[0] == claim_functions[0]

    function = solution_functions[0]
    assert function["args"][0]["token"] == '"parse_music"'
    params = find_apply(function["args"][1], "_,__MPY-SYNTAX_ParamNames")
    assert len(params) == 1
    assert params[0]["args"][0]["token"] == '"music_string"'
    print(f"solution={SOLUTION_MPY}")
    print(f"verification={VERIFICATION_K}")
    print(f"spec={SPEC_K}")
    print(f"extracted_wrapper={CLAIM_FUNCTION_MPY}")
    print(f"expanded_parseMusicCharBody_occurrences={alias_occurrences}")
    print(f"outer_parser_unit_normalization=.Exprs:{expr_units},.Stmts:{stmts_units}")
    print(f"funcdef_kast_sha256={stable_digest(function)}")
    print("function_name=parse_music")
    print("parameter_sequence=music_string,.ParamNames")
    print("entry_call_and_closure_binding_pinned=true")
    print("constructor_equal=true")


if __name__ == "__main__":
    main()
