#!/usr/bin/env python3
"""Independent, non-executing comparison of the frozen source and K closure."""

from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from pathlib import Path


WORKSPACE = Path("/reference/k-proof")


@dataclass
class Reader:
    text: str
    pos: int = 0

    def whitespace(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def token(self) -> object:
        self.whitespace()
        if self.pos >= len(self.text):
            raise ValueError("unexpected end of K term")
        char = self.text[self.pos]
        if char == '"':
            start = self.pos
            self.pos += 1
            escaped = False
            while self.pos < len(self.text):
                current = self.text[self.pos]
                self.pos += 1
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == '"':
                    return ("string", ast.literal_eval(self.text[start:self.pos]))
            raise ValueError("unterminated string")
        if char == "-" or char.isdigit():
            start = self.pos
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return ("integer", int(self.text[start:self.pos]))
        if char in "(),":
            self.pos += 1
            return char
        start = self.pos
        while self.pos < len(self.text) and (
            self.text[self.pos].isalnum()
            or self.text[self.pos] in "_.'-"
        ):
            self.pos += 1
        if start == self.pos:
            raise ValueError(f"unexpected character {char!r} at {self.pos}")
        return ("identifier", self.text[start:self.pos])

    def expression(self) -> object:
        atom = self.token()
        if atom == "(":
            elements: list[object] = []
            saved = self.pos
            if self.token() == ")":
                return ("tuple", tuple(elements))
            self.pos = saved
            while True:
                elements.append(self.expression())
                separator = self.token()
                if separator == ")":
                    return ("tuple", tuple(elements))
                if separator != ",":
                    raise ValueError(
                        f"expected tuple comma or close, found {separator!r}"
                    )
        if not isinstance(atom, tuple):
            raise ValueError(f"expected atom, found {atom!r}")
        saved = self.pos
        following = self.token()
        if following != "(":
            self.pos = saved
            return atom
        arguments: list[object] = []
        saved = self.pos
        if self.token() == ")":
            return ("call", atom, tuple(arguments))
        self.pos = saved
        while True:
            arguments.append(self.expression())
            separator = self.token()
            if separator == ")":
                break
            if separator != ",":
                raise ValueError(f"expected comma or close, found {separator!r}")
        return ("call", atom, tuple(arguments))


def parse_expression(text: str) -> object:
    reader = Reader(text)
    expression = reader.expression()
    reader.whitespace()
    if reader.pos != len(text):
        raise ValueError(f"unconsumed K term at offset {reader.pos}")
    return expression


def find_balanced_call(text: str, name: str, start: int = 0) -> str:
    marker = name + "("
    call_start = text.index(marker, start)
    index = call_start + len(name)
    depth = 0
    in_string = False
    escaped = False
    while index < len(text):
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
                return text[call_start:index + 1]
        index += 1
    raise ValueError(f"unbalanced {name} call")


def call(term: object, expected: str, arity: int | None = None) -> tuple[object, ...]:
    if not (
        isinstance(term, tuple)
        and len(term) == 3
        and term[0] == "call"
        and term[1] == ("identifier", expected)
    ):
        raise ValueError(f"expected {expected}, found {term!r}")
    arguments = term[2]
    if arity is not None and len(arguments) != arity:
        raise ValueError(f"{expected} arity {len(arguments)}, expected {arity}")
    return arguments


def integer(term: object) -> int:
    if not (isinstance(term, tuple) and term[0] == "integer"):
        raise ValueError(f"expected integer, found {term!r}")
    return int(term[1])


def string(term: object) -> str:
    if not (isinstance(term, tuple) and term[0] == "string"):
        raise ValueError(f"expected string, found {term!r}")
    return str(term[1])


def canonical_k_body(term: object) -> tuple[object, ...]:
    name = term[1][1] if isinstance(term, tuple) and len(term) == 3 else None
    if name == "Return":
        (result,) = call(term, "Return", 1)
        even_term, odd_term = call(result, "TupleExpr", 2)
        (even_value,) = call(even_term, "Int", 1)
        (odd_value,) = call(odd_term, "Int", 1)
        return ("return", integer(even_value), integer(odd_value))
    if name == "If":
        test, yes, no = call(term, "If", 3)
        lhs, operation = call(test, "Compare", 2)
        (variable,) = call(lhs, "Name", 1)
        operator, rhs = call(operation, "CmpOp", 2)
        (threshold,) = call(rhs, "Int", 1)
        if string(variable) != "n" or string(operator) != "<":
            raise ValueError("unexpected decision condition")
        return (
            "if",
            integer(threshold),
            canonical_k_body(yes),
            canonical_k_body(no),
        )
    raise ValueError(f"unexpected body node {term!r}")


def canonical_python_statement(statement: ast.stmt) -> tuple[object, ...]:
    if isinstance(statement, ast.Return):
        value = statement.value
        if not (
            isinstance(value, ast.Tuple)
            and len(value.elts) == 2
            and all(
                isinstance(element, ast.Constant)
                and type(element.value) is int
                for element in value.elts
            )
        ):
            raise ValueError("unexpected Python return")
        return ("return", value.elts[0].value, value.elts[1].value)
    if isinstance(statement, ast.If):
        test = statement.test
        if not (
            isinstance(test, ast.Compare)
            and isinstance(test.left, ast.Name)
            and test.left.id == "n"
            and len(test.ops) == len(test.comparators) == 1
            and isinstance(test.ops[0], ast.Lt)
            and isinstance(test.comparators[0], ast.Constant)
            and type(test.comparators[0].value) is int
            and len(statement.body) == len(statement.orelse) == 1
        ):
            raise ValueError("unexpected Python decision")
        return (
            "if",
            test.comparators[0].value,
            canonical_python_statement(statement.body[0]),
            canonical_python_statement(statement.orelse[0]),
        )
    raise ValueError(f"unexpected Python statement {type(statement).__name__}")


def nodes(term: tuple[object, ...]) -> tuple[int, int]:
    if term[0] == "return":
        return (0, 1)
    left = nodes(term[2])
    right = nodes(term[3])
    return (1 + left[0] + right[0], left[1] + right[1])


def main() -> None:
    verification = (WORKSPACE / "verification.k").read_text()
    solution_mpy = (WORKSPACE / "solution.mpy").read_text()
    solution_py = (WORKSPACE / "solution.py").read_text()

    closure = parse_expression(find_balanced_call(verification, "closureVal"))
    closure_params, closure_body, defining_location = call(closure, "closureVal", 3)
    expected_params = (
        "tuple",
        (("string", "n"), ("identifier", ".ParamNames")),
    )
    if closure_params != expected_params:
        raise ValueError("closure parameter list is not exactly n")
    if integer(defining_location) != 0:
        raise ValueError("closure defining location is not module scope 0")

    module_term = parse_expression(find_balanced_call(solution_mpy, "Module"))
    (function_term,) = call(module_term, "Module", 1)
    function_name, mpy_params, mpy_body = call(function_term, "FuncDef", 3)
    (mpy_parameter,) = call(mpy_params, "Params", 1)
    if string(function_name) != "even_odd_palindrome" or string(mpy_parameter) != "n":
        raise ValueError("unexpected MPY function identity")

    parsed_python = ast.parse(solution_py)
    definitions = [node for node in parsed_python.body if isinstance(node, ast.FunctionDef)]
    if len(definitions) != 1:
        raise ValueError("source must contain one function")
    definition = definitions[0]
    if (
        definition.name != "even_odd_palindrome"
        or [argument.arg for argument in definition.args.args] != ["n"]
        or len(definition.body) != 1
    ):
        raise ValueError("unexpected Python function identity")

    from_rule = canonical_k_body(closure_body)
    from_mpy = canonical_k_body(mpy_body)
    from_python = canonical_python_statement(definition.body[0])
    digest = hashlib.sha256(repr(from_rule).encode()).hexdigest()
    decisions, leaves = nodes(from_rule)
    print(f"function_name={definition.name}")
    print("parameters=[\"n\"]")
    print("defining_location=0")
    print(f"decision_nodes={decisions}")
    print(f"return_leaves={leaves}")
    print(f"canonical_decision_tree_sha256={digest}")
    print(f"verification_equals_solution_mpy={from_rule == from_mpy}")
    print(f"verification_equals_solution_py_ast={from_rule == from_python}")
    print("CLOSURE_IDENTITY=" + (
        "PASS" if from_rule == from_mpy == from_python else "FAIL"
    ))


if __name__ == "__main__":
    main()
