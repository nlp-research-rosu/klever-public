#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the entry claim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


WORK = Path("/tmp/audit-work/source")


def extract_call(text: str, name: str, start: int = 0) -> str:
    match = re.search(rf"(?<![A-Za-z0-9_#]){re.escape(name)}\s*\(", text[start:])
    assert match is not None, f"missing call {name}"
    begin = start + match.start()
    open_paren = text.find("(", begin)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[begin : index + 1]
    raise AssertionError(f"unbalanced call {name}")


TOKEN = re.compile(
    r"""\s*(?:
        (?P<string>"(?:[^"\\]|\\.)*")
      | (?P<int>-?[0-9]+)
      | (?P<name>\#?[A-Za-z_][A-Za-z0-9_\-]*)
      | (?P<punct>[(),])
    )""",
    re.VERBOSE,
)


def tokenize(text: str) -> list[tuple[str, str]]:
    result = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        assert match is not None, f"unrecognized constructor text at {text[position:position+40]!r}"
        kind = match.lastgroup
        assert kind is not None
        result.append((kind, match.group(kind)))
        position = match.end()
    return result


def parse_constructor(text: str):
    tokens = tokenize(text)
    position = 0

    def parse_term():
        nonlocal position
        kind, value = tokens[position]
        position += 1
        if kind == "string":
            return ("string", json.loads(value))
        if kind == "int":
            return ("int", int(value))
        assert kind == "name"
        if position < len(tokens) and tokens[position] == ("punct", "("):
            position += 1
            arguments = []
            if tokens[position] != ("punct", ")"):
                while True:
                    arguments.append(parse_term())
                    if tokens[position] == ("punct", ","):
                        position += 1
                        continue
                    break
            assert tokens[position] == ("punct", ")")
            position += 1
            return ("call", value, arguments)
        return ("atom", value)

    term = parse_term()
    assert position == len(tokens), f"unconsumed tokens: {tokens[position:]}"
    return term


solution_text = (WORK / "solution.mpy").read_text()
spec_text = (WORK / "spec.k").read_text()

solution_program = parse_constructor(extract_call(solution_text, "Module"))
claim_program = parse_constructor(extract_call(spec_text, "Module"))
assert claim_program == solution_program

_, module_name, module_args = solution_program
assert module_name == "Module" and len(module_args) == 1
_, function_name, function_args = module_args[0]
assert function_name == "FuncDef" and len(function_args) == 3
declared_name, parameters, function_body = function_args
assert declared_name == ("string", "is_palindrome")
assert parameters == ("call", "Params", [("string", "text")])

binding = parse_constructor(extract_call(spec_text, "#function"))
assert binding == ("call", "#function", [("string", "text"), function_body])

invocation_text = re.sub(r"\b([A-Z][A-Za-z0-9_]*)\s*:\s*[A-Z][A-Za-z0-9_]*\b", r"\1", extract_call(spec_text, "#invoke"))
invocation = parse_constructor(invocation_text)
assert invocation[0:2] == ("call", "#invoke")
assert invocation[2][0] == declared_name
assert invocation[2][1] == ("call", "PyString", [("atom", "S")])

claim_text = spec_text[spec_text.index("claim") :]
assert not re.search(r"(?m)^\s+requires\s+", claim_text)
assert re.search(r"<functions>\s*\.Map\s*=>", spec_text)
assert re.search(r"<env>\s*\.Map\s*</env>", spec_text)

normalized = json.dumps(solution_program, separators=(",", ":"), ensure_ascii=True)
digest = hashlib.sha256(normalized.encode()).hexdigest()
print(f"solution_program_normalized_sha256={digest}")
print("PASS claim <k> Module constructor equals submitted solution.mpy constructor")
print("PASS claimed #function parameter/body equals submitted FuncDef parameter/body")
print("PASS claimed #invoke target equals submitted function name and passes symbolic S")
print("PASS entry claim has no requires restriction and starts from empty functions/env")
