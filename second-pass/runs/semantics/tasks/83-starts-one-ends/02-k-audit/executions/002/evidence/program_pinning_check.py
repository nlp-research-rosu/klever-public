#!/usr/bin/env python3
"""Mechanical source/translation/proof-body identity checks for HumanEval 83."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import symtable
from pathlib import Path


def load_translator(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_py2mpy", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import translator: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact_k(text: str) -> str:
    """Remove layout whitespace but preserve characters inside K strings."""
    out: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    # Explicit empty list identities and the translator's omitted empty
    # sequences are the same constructor term.
    return "".join(out).replace(".Stmts", "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--translator", type=Path, required=True)
    parser.add_argument("--solution-py", type=Path, required=True)
    parser.add_argument("--solution-mpy", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    args = parser.parse_args()

    translator = load_translator(args.translator)
    source = args.solution_py.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(args.solution_py))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert len(tree.body) == 1 and len(functions) == 1
    function = functions[0]
    assert function.name == "starts_one_ends"
    assert [arg.arg for arg in function.args.args] == ["n"]

    translator.SCOPES.clear()
    translator._walk_symtable(
        symtable.symtable(source, str(args.solution_py), "exec")
    )
    regenerated = translator.render(translator.emit_module(tree)) + "\n"
    submitted = args.solution_mpy.read_text(encoding="utf-8")
    mpy_identical = regenerated == submitted

    expected_body = translator.render(translator.emit_stmts(function.body)) + ".Stmts"
    verification = args.verification.read_text(encoding="utf-8")
    body_match = re.search(
        r"rule\s+startsOneEndsBody\s*=>\s*(.*?)\n\s*rule\s+<k>",
        verification,
        re.DOTALL,
    )
    assert body_match is not None
    body_identical = compact_k(expected_body) == compact_k(body_match.group(1))

    wrapper_expected = (
        '<k>#invokeStartsOneEnds(N:Int)'
        '=>Call(Name("starts_one_ends"),Int(N))...</k>'
    )
    wrapper_match = re.search(
        r"rule\s+(<k>\s*#invokeStartsOneEnds.*?</k>)",
        verification,
        re.DOTALL,
    )
    assert wrapper_match is not None
    wrapper_exact = compact_k(wrapper_match.group(1)) == compact_k(wrapper_expected)

    spec = compact_k(args.spec.read_text(encoding="utf-8"))
    binding = (
        '"starts_one_ends"|->'
        'closureVal(("n",.ParamNames),startsOneEndsBody,0)'
    )
    binding_count = spec.count(binding)

    print(f"top_level_ast_nodes={len(tree.body)}")
    print(f"entry_point={function.name}")
    print(f"parameters={[arg.arg for arg in function.args.args]}")
    print(f"submitted_mpy_byte_identical={mpy_identical}")
    print(f"verification_body_constructor_identical={body_identical}")
    print(f"invocation_wrapper_exact={wrapper_exact}")
    print(f"exact_spec_binding_count={binding_count}")
    ok = mpy_identical and body_identical and wrapper_exact and binding_count == 2
    print(f"pinning_check_passed={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
