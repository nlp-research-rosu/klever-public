#!/usr/bin/env python3
"""Reproducible identity, oracle, and exhaustive-domain checks."""

import argparse
import ast
import importlib.util
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
VALUES = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
DIGITS = ("m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i")


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def oracle(number):
    result = ""
    for value, digit in zip(VALUES, DIGITS):
        count, number = divmod(number, value)
        result += digit * count
    return result


def compact(text):
    return re.sub(r"\s+", "", text)


def load_function(path):
    spec = importlib.util.spec_from_file_location("checked_solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.int_to_mini_roman


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", default="solution.py")
    args = parser.parse_args()

    solution_path = (ROOT / args.solution).resolve()
    translated = subprocess.check_output(
        [sys.executable, str(ROOT / "py2mpy.py"), str(solution_path)],
        text=True,
    )
    committed_mpy = (ROOT / "solution.mpy").read_text(encoding="utf-8")
    if translated != committed_mpy:
        fail(f"{solution_path.name} does not transliterate to committed solution.mpy")

    solution_term = compact(committed_mpy)
    prefix = 'Module(FuncDef("int_to_mini_roman",Params("number"),'
    if not solution_term.startswith(prefix) or not solution_term.endswith("))"):
        fail("solution.mpy has an unexpected module/function shape")
    solution_body = solution_term[len(prefix):-2]

    verification = compact((ROOT / "verification.k").read_text(encoding="utf-8"))
    body_start = "ruleintToMiniRomanBody=>"
    body_end = "rulesolutionModule=>"
    if body_start not in verification or body_end not in verification:
        fail("verification.k is missing the program-body macros")
    macro_body = verification.split(body_start, 1)[1].split(body_end, 1)[0]
    # py2mpy prints an empty Stmts list as an empty surface slot; the K macro
    # spells the same list explicitly as .Stmts.
    macro_body = macro_body.replace(",.Stmts)", ",)")
    if macro_body != solution_body:
        fail("intToMiniRomanBody is not the exact solution.mpy function body")

    expected_module = (
        'Module(FuncDef("int_to_mini_roman",Params("number"),'
        "intToMiniRomanBody))"
    )
    module_macro = verification.split(body_end, 1)[1].split("rulesolutionCall", 1)[0]
    if module_macro != expected_module:
        fail("solutionModule macro has an unexpected expansion")

    expected_call = (
        "(N:Int)=>Module(FuncDef(\"int_to_mini_roman\",Params(\"number\"),"
        "intToMiniRomanBody)Assign(Name(\"__result\"),"
        "Call(Name(\"int_to_mini_roman\"),Int(N))))"
    )
    call_macro = verification.split("rulesolutionCall", 1)[1].split("endmodule", 1)[0]
    if call_macro != expected_call:
        fail("solutionCall macro has an unexpected expansion")

    solution_ast = ast.parse(solution_path.read_text(encoding="utf-8")).body[0]
    concrete_ast = ast.parse(
        (ROOT / "concrete_tests.py").read_text(encoding="utf-8")
    ).body[0]
    if ast.dump(solution_ast) != ast.dump(concrete_ast):
        fail("concrete_tests.py does not contain the exact solution function")

    claim_re = re.compile(
        r"claim \[roman-(\d{4})\]:"
        r".*?solutionCall\((\d+)\)"
        r".*?\"__result\" \|-> str\(strToCodes\(\"([^\"]*)\"\)\)",
        re.DOTALL,
    )
    claims = claim_re.findall((ROOT / "spec.k").read_text(encoding="utf-8"))
    if len(claims) != 1000:
        fail(f"expected 1000 Roman claims, found {len(claims)}")
    seen = set()
    for label_text, input_text, expected in claims:
        label = int(label_text)
        number = int(input_text)
        if label != number or number in seen:
            fail(f"bad or duplicate claim identity at {label_text}/{input_text}")
        if expected != oracle(number):
            fail(f"claim roman-{label_text} has a noncanonical expected value")
        seen.add(number)
    if seen != set(range(1, 1001)):
        fail("spec.k does not cover exactly the integers 1..1000")

    implementation = load_function(solution_path)
    mismatches = [
        number
        for number in range(1, 1001)
        if implementation(number) != oracle(number)
    ]
    if mismatches:
        fail(f"CPython/oracle mismatches: {mismatches[:10]}")

    examples = {19: "xix", 152: "clii", 426: "cdxxvi"}
    if any(implementation(number) != expected for number, expected in examples.items()):
        fail("one or more prompt examples failed")

    print("PASS: source translation equals solution.mpy")
    print("PASS: verification macros contain the exact translated body and harness")
    print("PASS: spec.k contains canonical claims for exactly 1..1000")
    print("PASS: CPython exhaustive differential has 0 mismatches over 1..1000")
    print("PASS: prompt examples 19, 152, and 426")


if __name__ == "__main__":
    main()
