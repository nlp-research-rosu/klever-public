#!/usr/bin/env python3
"""Compare fresh LLVM execution of generated K semantics with both Python entries."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


def k_string(value: str) -> str:
    # K accepts the JSON escape repertoire for these test values.
    return json.dumps(value, ensure_ascii=False)


def k_list(values: list[str]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({k_string(value)}, {result})"
    return result


TOKEN = re.compile(
    r'\s*(listVal|cons|nil|\(|\)|,|"(?:\\.|[^"\\])*")', re.DOTALL
)


def parse_k_output(text: str) -> list[str]:
    match = re.search(r"<output>\s*(.*?)\s*</output>", text, re.DOTALL)
    if not match:
        raise ValueError("missing <output> cell")
    source = match.group(1)
    tokens = []
    position = 0
    while position < len(source):
        token = TOKEN.match(source, position)
        if not token:
            raise ValueError(f"cannot tokenize output near {source[position:position+40]!r}")
        tokens.append(token.group(1))
        position = token.end()
    cursor = 0

    def take(expected: str | None = None) -> str:
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError("unexpected end of output")
        value = tokens[cursor]
        cursor += 1
        if expected is not None and value != expected:
            raise ValueError(f"expected {expected!r}, got {value!r}")
        return value

    def parse_list() -> list[str]:
        tag = take()
        if tag == "nil":
            return []
        if tag != "cons":
            raise ValueError(f"expected cons or nil, got {tag!r}")
        take("(")
        item_token = take()
        if not item_token.startswith('"'):
            raise ValueError(f"expected string token, got {item_token!r}")
        item = ast.literal_eval(item_token)
        # K's pretty printer emits non-BMP characters as escaped UTF-8 bytes
        # (for example "\xf0\x9f\x98\x8a"), while emitting some BMP
        # characters directly as one \x escape. Recover UTF-8 only when the
        # complete byte-like token is valid UTF-8; otherwise keep the scalar
        # characters produced by literal_eval.
        if any(ord(character) >= 128 for character in item):
            try:
                item = bytes(ord(character) for character in item).decode("utf-8")
            except (ValueError, UnicodeDecodeError):
                pass
        take(",")
        rest = parse_list()
        take(")")
        return [item] + rest

    take("listVal")
    take("(")
    result = parse_list()
    take(")")
    if cursor != len(tokens):
        raise ValueError(f"trailing tokens: {tokens[cursor:]!r}")
    return result


canonical = load_entry(
    "audit_concrete_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "audit_concrete_generated", Path("/tmp/audit-work/candidate/solution.py")
)

cases = [
    ("empty-input", [], "a"),
    ("documented-example", ["abc", "bcd", "cde", "array"], "a"),
    ("empty-prefix", ["", "a", "aa", "b"], ""),
    ("prefix-longer", ["a"], "aa"),
    ("equal-match", ["abc"], "abc"),
    ("equal-nonmatch", ["abc"], "abd"),
    ("stable-duplicates", ["a", "ab", "ba", "a"], "a"),
    ("unicode-codepoints", ["é", "élan", "e\u0301lan", "xé"], "é"),
    ("emoji", ["😊", "😊x", "x😊"], "😊"),
    ("spaces-and-escapes", ["a b", "a\tb", "a\\b", '"a'], "a"),
]

mismatches = 0
for name, strings, prefix in cases:
    expected_canonical = canonical(list(strings), prefix)
    expected_generated = generated(list(strings), prefix)
    command = [
        "krun",
        "/tmp/audit-work/candidate/solution.mpy",
        "--definition",
        "/tmp/audit-work/concrete-kompiled",
        f"-cINPUT={k_list(strings)}",
        f"-cPREFIX={k_string(prefix)}",
    ]
    print(f"CASE: {name}")
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/candidate",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT: {completed.returncode}")
    print(completed.stdout.rstrip())
    try:
        actual = parse_k_output(completed.stdout)
    except Exception as error:
        actual = f"PARSE_ERROR: {error}"
    print(f"canonical={expected_canonical!r}")
    print(f"generated_python={expected_generated!r}")
    print(f"generated_k={actual!r}")
    case_ok = (
        completed.returncode == 0
        and expected_canonical == expected_generated
        and actual == expected_canonical
    )
    print(f"MATCH: {case_ok}")
    print()
    if not case_ok:
        mismatches += 1

print(f"cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
