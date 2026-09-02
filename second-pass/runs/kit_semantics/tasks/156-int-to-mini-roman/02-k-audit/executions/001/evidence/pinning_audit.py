#!/usr/bin/env python3
"""Mechanical real-program and ground-claim pinning checks."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/rebuild")
VERIFICATION = ROOT / "verification.k"
SPEC = ROOT / "spec.k"
MPY = ROOT / "regenerated.mpy"
CANONICAL = Path("/reference/canonical.py")


def compact_k(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


def load_canonical():
    spec = importlib.util.spec_from_file_location("pinning_canonical", CANONICAL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.int_to_mini_roman


def expected_claim(number: int, result: str) -> str:
    return compact_k(
        f"""
  claim [roman-{number:04d}]:
    <k> #loadAll(solutionCall({number})) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "__result" |-> str(strToCodes("{result}"))
        "int_to_mini_roman" |->
          closureVal("number", .ParamNames, intToMiniRomanBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
"""
    )


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def main() -> int:
    mpy = compact_k(MPY.read_text(encoding="utf-8"))
    prefix = 'Module(FuncDef("int_to_mini_roman",Params("number"),'
    if not mpy.startswith(prefix) or not mpy.endswith("))"):
        fail("trusted regenerated constructor term has unexpected shape")
    translated_body = mpy[len(prefix):-2]

    verification = compact_k(VERIFICATION.read_text(encoding="utf-8"))
    if verification.count("syntaxStmts::=") != 1:
        fail("unexpected Stmts macro declaration count")
    if verification.count("syntaxModule::=") != 1:
        fail("unexpected Module macro declaration count")
    if verification.count("rule") != 3:
        fail("verification.k does not contain exactly three rules")
    for prohibited in (
        "[function",
        "[total",
        "[functional",
        "[simplification",
        "[concrete",
        "[priority",
        "claim",
        "opaque",
    ):
        if prohibited in verification.lower():
            fail(f"proof-local prohibited extension marker present: {prohibited}")

    body_marker = "ruleintToMiniRomanBody=>"
    module_marker = "rulesolutionModule=>"
    call_marker = "rulesolutionCall"
    body = verification.split(body_marker, 1)[1].split(module_marker, 1)[0]
    # The translator prints an empty Stmts list as an empty surface slot.
    body = body.replace(",.Stmts)", ",)")
    if body != translated_body:
        fail("macro body is not constructor-identical to trusted regeneration")

    expected_module = (
        'Module(FuncDef("int_to_mini_roman",Params("number"),'
        "intToMiniRomanBody))"
    )
    module_term = verification.split(module_marker, 1)[1].split(
        call_marker, 1
    )[0]
    if module_term != expected_module:
        fail("solutionModule expansion differs from the regenerated binding")

    expected_call = (
        '(N:Int)=>Module(FuncDef("int_to_mini_roman",Params("number"),'
        'intToMiniRomanBody)Assign(Name("__result"),'
        'Call(Name("int_to_mini_roman"),Int(N))))'
    )
    call_term = verification.split(call_marker, 1)[1].split("endmodule", 1)[0]
    if call_term != expected_call:
        fail("solutionCall expansion differs from exact binding/body/call harness")

    spec_text = SPEC.read_text(encoding="utf-8")
    header = compact_k(
        'requires "verification.k"\nmodule SPEC\nimports VERIFICATION\n'
    )
    footer = compact_k("endmodule")
    canonical = load_canonical()
    expected = header + "".join(
        expected_claim(number, canonical(number))
        for number in range(1, 1001)
    ) + footer
    actual = compact_k(spec_text)
    if actual != expected:
        mismatch = next(
            (
                offset
                for offset, pair in enumerate(zip(actual, expected))
                if pair[0] != pair[1]
            ),
            min(len(actual), len(expected)),
        )
        fail(
            "spec.k differs from exact canonical ground claims at compact "
            f"offset {mismatch}: actual={actual[mismatch:mismatch+120]!r} "
            f"expected={expected[mismatch:mismatch+120]!r}"
        )

    compiled_rules = ROOT / "verification-kompiled" / "allRules.txt"
    compiled_text = compiled_rules.read_text(encoding="utf-8")
    leaked = [
        token
        for token in (
            "intToMiniRomanBody",
            "solutionModule",
            "solutionCall",
        )
        if token in compiled_text
    ]
    if leaked:
        fail(f"macro token leaked into runtime allRules.txt: {leaked}")

    print(f"regenerated_program={MPY}")
    print("constructor_body_match=PASS")
    print("function_binding_and_call_harness_match=PASS")
    print("proof_local_inventory=3 syntax macros, 3 macro rules, 0 runtime rules")
    print("compiled_runtime_macro_leak_count=0")
    print("claim_count=1000")
    print("claim_domain=every integer 1..1000 exactly once")
    print("all_claims_ground_and_canonical=PASS")
    print("all entry prestates are the supplied concrete initial configuration")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
