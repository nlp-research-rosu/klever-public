#!/usr/bin/env python3
"""Mechanical source/claim constructor comparison and concrete witnesses."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "fresh-verification-kompiled"


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
    open_index = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced call beginning at {marker}")


def kast_file(path: Path) -> dict:
    result = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--output",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)["term"]


def kast_rule_term(expression: str) -> dict:
    # Semantic-only constructors such as closureVal are parsed by K's rule
    # parser, not the external-program start sort.  A reflexive rewrite gives
    # us the fully constructor-resolved LHS without changing the term.
    result = subprocess.run(
        [
            "kast",
            "--input",
            "rule",
            "--expression",
            f"{expression} => {expression}",
            "--module",
            "VERIFICATION",
            "--definition",
            str(DEFINITION),
            "--output",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)["term"]["lhs"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def flatten_list(term: dict, constructor_fragment: str) -> list[dict]:
    term_label = label(term)
    if constructor_fragment in term_label and len(term.get("args", [])) == 2:
        head, tail = term["args"]
        return [head, *flatten_list(tail, constructor_fragment)]
    if term_label.startswith(".List{"):
        return []
    raise AssertionError(
        f"unexpected list constructor for {constructor_fragment}: {term_label}"
    )


def seq_text(values: list[int]) -> str:
    result = ".ValSeq"
    for value in reversed(values):
        result = f"vCons({value}, {result})"
    return result


def main() -> None:
    print(
        "COMMAND: python3 "
        "/audit-output/evidence/04_pinning_and_witnesses.py"
    )
    source_term = kast_file(WORK / "solution.regenerated.mpy")
    if not label(source_term).startswith("Module("):
        raise AssertionError(f"unexpected source root: {label(source_term)}")
    statements = flatten_list(
        source_term["args"][0], "_MPY-SYNTAX_Stmts_Stmt_Stmts"
    )
    if len(statements) != 1:
        raise AssertionError(f"expected one module statement: {len(statements)}")
    function = statements[0]
    if not label(function).startswith("FuncDef("):
        raise AssertionError(f"expected FuncDef: {label(function)}")
    source_name, source_params_node, source_body = function["args"]
    if source_name.get("token") != '"generate_integers"':
        raise AssertionError(f"unexpected function name: {source_name}")
    if not label(source_params_node).startswith("Params("):
        raise AssertionError(f"unexpected params node: {label(source_params_node)}")
    source_params = source_params_node["args"][0]

    spec_text = (WORK / "spec.k").read_text(encoding="utf-8")
    closure_text = balanced_call(spec_text, "closureVal")
    closure = kast_rule_term(closure_text)
    if not label(closure).startswith("closureVal("):
        raise AssertionError(f"unexpected closure term: {label(closure)}")
    claim_params, claim_body, claim_scope = closure["args"]

    if source_params != claim_params:
        raise AssertionError("claim parameter constructors differ from source")
    if source_body != claim_body:
        raise AssertionError("claim body constructors differ from source")
    if claim_scope.get("token") != "0":
        raise AssertionError(f"claim closure scope is not 0: {claim_scope}")
    if (
        '"generate_integers" |->' not in spec_text
        or 'Call(Name("generate_integers"), Int(A:Int), Int(B:Int), .Exprs)'
        not in spec_text
    ):
        raise AssertionError("claim binding/call does not name generate_integers")

    print(
        "PASS constructor identity: trusted-regenerated FuncDef parameters/body "
        "equal the SPEC closureVal parameters/body after K parsing; "
        "binding key and invoked name are generate_integers; closure scope=0"
    )

    canonical = load_entry("pinning_canonical", Path("/reference/canonical.py"))
    generated = load_entry("pinning_generated", WORK / "solution.py")
    witnesses = ((2, 8), (10, 14), (6, 6), (1, 10**100))
    for a, b in witnesses:
        if not (a > 0 and b > 0):
            raise AssertionError(f"precondition false for witness {(a, b)}")
        low, high = min(a, b), max(a, b)
        formal_values = [
            digit for digit in (2, 4, 6, 8) if low <= digit <= high
        ]
        canonical_value = canonical(a, b)
        generated_value = generated(a, b)
        if formal_values != canonical_value or canonical_value != generated_value:
            raise AssertionError(
                (a, b, formal_values, canonical_value, generated_value)
            )
        print(
            "WITNESS "
            f"A={a} B={b} PRECONDITION=true "
            "FORMAL_POST=<k>ref(0)</k> "
            f"<heap>0|->list({seq_text(formal_values)})</heap> "
            f"CANONICAL={canonical_value} GENERATED={generated_value}"
        )
    print("RESULT: claim pinning and satisfying witnesses passed")


if __name__ == "__main__":
    main()
