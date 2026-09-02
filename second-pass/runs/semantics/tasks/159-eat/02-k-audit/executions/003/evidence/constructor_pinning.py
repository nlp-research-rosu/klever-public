#!/usr/bin/env python3
"""Derive the expected closure term from solution.py and extract the submitted one.

The expected term is constructed from the trusted translator's in-memory AST
representation.  Both terms are subsequently parsed by `kast` and compared in
JSON form, so whitespace and explicit-versus-implicit empty K lists do not
affect the result.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import symtable
import sys
from pathlib import Path


def load_translator(path: str):
    spec = importlib.util.spec_from_file_location("trusted_py2mpy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load translator {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_constructor(text: str, start: int) -> str:
    opening = text.find("(", start)
    if opening < 0:
        raise ValueError("constructor opening parenthesis not found")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
            if depth == 0 and index >= opening:
                return text[start : index + 1]
    raise ValueError("unbalanced constructor")


def render_for_rule(translator, node) -> str:
    """Render the trusted translator tree with explicit empty Stmts lists."""
    if isinstance(node, str):
        return node
    if isinstance(node, translator.Seq):
        if not node.items:
            return ".Stmts"
        return " ".join(render_for_rule(translator, item) for item in node.items)
    return (
        node.name
        + "("
        + ", ".join(render_for_rule(translator, arg) for arg in node.args)
        + ")"
    )


def normalize_k_list_surface(text: str) -> str:
    """Erase only whitespace and explicit `.Stmts` list terminators."""
    text = text.replace(".Stmts", "")
    output = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {Path(sys.argv[0]).name} "
            "TRUSTED_PY2MPY SOLUTION.py VERIFICATION.k OUTPUT_DIR"
        )
        return 2

    translator = load_translator(sys.argv[1])
    solution_path = Path(sys.argv[2])
    verification_path = Path(sys.argv[3])
    output_dir = Path(sys.argv[4])

    source = solution_path.read_text(encoding="utf-8")
    translator.SCOPES.clear()
    translator._walk_symtable(symtable.symtable(source, str(solution_path), "exec"))
    module_term = translator.emit_module(ast.parse(source, filename=str(solution_path)))
    statements = module_term.args[0]
    if len(statements.items) != 1:
        raise ValueError("solution module must contain exactly one statement")
    function = statements.items[0]
    if function.name != "FuncDef" or function.args[0] != '"eat"':
        raise ValueError("solution module is not exactly the eat function binding")
    if function.args[1].name != "Params":
        raise ValueError("unexpected parameter constructor")

    params = "(" + ", ".join(function.args[1].args) + ")"
    body = render_for_rule(translator, function.args[2])
    expected = f"closureVal({params},\n    {body},\n    0)\n"

    verification = verification_path.read_text(encoding="utf-8")
    marker = "rule eatClosure"
    rule_start = verification.find(marker)
    if rule_start < 0:
        raise ValueError("eatClosure rule not found")
    arrow = verification.find("=>", rule_start)
    constructor = verification.find("closureVal", arrow)
    if arrow < 0 or constructor < 0:
        raise ValueError("eatClosure RHS not found")
    actual_raw = balanced_constructor(verification, constructor) + "\n"
    # `.Stmts` is the explicit K list terminator accepted in rule syntax.
    # Program parsing uses the equivalent empty juxtaposition.
    actual = actual_raw.replace(".Stmts", "")

    output_dir.mkdir(parents=True, exist_ok=True)
    expected_path = output_dir / "expected-closure.kterm"
    raw_actual_path = output_dir / "actual-closure-raw.kterm"
    actual_path = output_dir / "actual-closure.kterm"
    expected_normalized_path = output_dir / "expected-closure.normalized"
    actual_normalized_path = output_dir / "actual-closure.normalized"
    pinning_spec_path = output_dir / "pinning-spec.k"
    expected_path.write_text(expected, encoding="utf-8")
    raw_actual_path.write_text(actual_raw, encoding="utf-8")
    actual_path.write_text(actual, encoding="utf-8")
    expected_normalized = normalize_k_list_surface(expected)
    actual_normalized = normalize_k_list_surface(actual_raw)
    expected_normalized_path.write_text(expected_normalized + "\n", encoding="utf-8")
    actual_normalized_path.write_text(actual_normalized + "\n", encoding="utf-8")
    if expected_normalized != actual_normalized:
        raise AssertionError("translator-derived and proof-local closure terms differ")
    pinning_spec_path.write_text(
        'requires "verification.k"\n\n'
        "module EAT-PINNING-SPEC\n"
        "  imports EAT-VERIFICATION\n\n"
        "  claim <k> eatClosure\n"
        "          => " + expected.replace("\n", "\n             ").rstrip() + "\n"
        "        </k>\n"
        "endmodule\n",
        encoding="utf-8",
    )
    print(f"expected={expected_path}")
    print(f"actual_raw={raw_actual_path}")
    print(f"actual={actual_path}")
    print(f"expected_normalized={expected_normalized_path}")
    print(f"actual_normalized={actual_normalized_path}")
    print(f"pinning_spec={pinning_spec_path}")
    print("source_function_count=1")
    print("source_binding=eat")
    digest = hashlib.sha256(expected_normalized.encode()).hexdigest()
    print(f"normalized_constructor_sha256={digest}")
    print("normalized_constructor_terms_equal=true")
    print("normalization=explicit .Stmts terminators to empty juxtaposition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
