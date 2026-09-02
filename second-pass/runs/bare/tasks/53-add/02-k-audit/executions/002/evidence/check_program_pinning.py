#!/usr/bin/env python3
"""Mechanically compare the translated program with the program term in SPEC."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import sys


SCRATCH = Path("/tmp/audit-work/53-add-audit-002")


def balanced_argument(text: str, call: str) -> str:
    start = text.index(call) + len(call)
    depth = 1
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
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise AssertionError(f"unbalanced call: {call}")


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def constructor_tokens(text: str) -> list[str]:
    tokens = TOKEN.findall(text)
    residue = TOKEN.sub("", text)
    if not residue.isspace() and residue:
        raise AssertionError(f"unparsed constructor text: {residue!r}")
    return tokens


def inspect_python_body(path: Path) -> tuple[str, list[str], str]:
    tree = ast.parse(path.read_text())
    assert len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef)
    function = tree.body[0]
    assert len(function.body) == 1 and isinstance(function.body[0], ast.Return)
    returned = function.body[0].value
    assert isinstance(returned, ast.BinOp) and isinstance(returned.op, ast.Add)
    assert isinstance(returned.left, ast.Name) and returned.left.id == "x"
    assert isinstance(returned.right, ast.Name) and returned.right.id == "y"
    names = [argument.arg for argument in function.args.args]
    return function.name, names, "x + y"


def main() -> int:
    submitted = (SCRATCH / "solution.mpy").read_bytes()
    regenerated = (SCRATCH / "regenerated.solution.mpy").read_bytes()
    assert submitted == regenerated

    solution_text = submitted.decode()
    spec_text = (SCRATCH / "spec.k").read_text()
    claimed_program = balanced_argument(spec_text, "load(")
    submitted_tokens = constructor_tokens(solution_text)
    claimed_tokens = constructor_tokens(claimed_program)
    assert submitted_tokens == claimed_tokens

    assert spec_text.count("claim") == 1
    assert '~> invoke("add", pyInt(X), pyInt(Y))' in spec_text
    assert "<env> .Map =>" in spec_text
    assert "<result> 0 => X +Int Y </result>" in spec_text

    function_name, parameters, expression = inspect_python_body(SCRATCH / "solution.py")
    print(f"trusted_regeneration_byte_identity={submitted == regenerated}")
    print(f"submitted_constructor_tokens={submitted_tokens}")
    print(f"claimed_constructor_tokens={claimed_tokens}")
    print(f"constructor_level_identity={submitted_tokens == claimed_tokens}")
    print(f"python_function={function_name}")
    print(f"python_parameters={parameters}")
    print(f"python_return_expression={expression}")
    print("entry_claim_count=1")
    print("symbolic_domain=all K Int X and Y (no requires clause)")
    print("PROGRAM_PINNING_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
