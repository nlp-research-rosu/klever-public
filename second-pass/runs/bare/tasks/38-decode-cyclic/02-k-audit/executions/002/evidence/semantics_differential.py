#!/usr/bin/env python3
"""Execute the rebuilt generated K semantics and compare it with both Pythons."""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


REBUILD = Path("/tmp/audit-work/rebuild")
DEFINITION = REBUILD / "concrete-kompiled"
PROGRAM = REBUILD / "solution.mpy"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def label(term: dict[str, Any]) -> str | None:
    value = term.get("label")
    return value.get("name") if isinstance(value, dict) else None


def find_cell(term: Any, cell_label: str) -> dict[str, Any]:
    if isinstance(term, dict):
        if term.get("node") == "KApply" and label(term) == cell_label:
            return term
        for value in term.values():
            try:
                return find_cell(value, cell_label)
            except LookupError:
                pass
    elif isinstance(term, list):
        for value in term:
            try:
                return find_cell(value, cell_label)
            except LookupError:
                pass
    raise LookupError(cell_label)


def k_string_result(document: dict[str, Any]) -> tuple[str, str, str]:
    term = document["term"]
    k_cell = find_cell(term, "<k>")
    env_cell = find_cell(term, "<env>")
    result_cell = find_cell(term, "<result>")

    k_content = k_cell["args"][0]
    env_content = env_cell["args"][0]
    result_content = result_cell["args"][0]
    if k_content != {"node": "KSequence", "arity": 0, "items": []}:
        raise ValueError(f"non-final <k>: {k_content}")
    if label(env_content) != ".Map":
        raise ValueError(f"non-empty <env>: {env_content}")
    if not str(label(result_content)).startswith("pyStr("):
        raise ValueError(f"non-string result: {result_content}")
    token = result_content["args"][0]["token"]
    # K's String token renderer uses Python-compatible \xNN escapes in addition
    # to JSON's escape vocabulary, so literal_eval is the appropriate decoder.
    value = ast.literal_eval(token)
    if not isinstance(value, str):
        raise ValueError(f"non-string K token: {token}")
    return value, label(env_content) or "", label(result_content) or ""


def k_quote(value: str) -> str:
    """Render a K String token without UTF-16 surrogate-pair escapes."""
    pieces = ['"']
    short_escapes = {
        '"': r"\"",
        "\\": r"\\",
        "\n": r"\n",
        "\r": r"\r",
        "\t": r"\t",
        "\f": r"\f",
    }
    for character in value:
        if character in short_escapes:
            pieces.append(short_escapes[character])
            continue
        codepoint = ord(character)
        if 0x20 <= codepoint <= 0x7E:
            pieces.append(character)
        elif codepoint < 0x20 or codepoint == 0x7F:
            pieces.append(f"\\x{codepoint:02x}")
        elif codepoint <= 0xFFFF:
            pieces.append(f"\\u{codepoint:04x}")
        else:
            pieces.append(f"\\U{codepoint:08x}")
    pieces.append('"')
    return "".join(pieces)


canonical = load_module("trusted_canonical_for_k", Path("/reference/canonical.py"))
generated = load_module("generated_solution_for_k", Path("/candidate/solution.py"))

cases = [
    "",
    "a",
    "ab",
    "abc",
    "abcd",
    "abcde",
    "abcdef",
    "abcdefg",
    "bca",
    "bcaefdgh",
    "Hello, world!",
    "\"'\\\n\t\x00",
    "éα中🙂𝄞",
    "e\u0301🙂中A",
    "0123456789abcdefghijklmnopqrstuvwxyz",
]

config_safe_only = "--config-safe-only" in sys.argv
if config_safe_only:
    cases = [
        value
        for value in cases
        if all(ord(character) < 128 for character in value)
    ]

failures = 0
print(f"PROGRAM: {PROGRAM}")
print(f"DEFINITION: {DEFINITION}")
print(
    "MODE: "
    + ("ASCII/control configuration bridge" if config_safe_only else "all -cS probes")
)
print(f"CASE_COUNT: {len(cases)}")
for index, value in enumerate(cases):
    injected = k_quote(value)
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        f"-cS={injected}",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        cwd=REBUILD,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    print(f"CASE {index} INPUT={value!r}")
    print(f"  COMMAND={command!r}")
    print(f"  EXIT={completed.returncode}")
    if completed.returncode:
        failures += 1
        print(f"  STDERR={completed.stderr[-1200:]!r}")
        continue

    k_value, final_env, result_label = k_string_result(json.loads(completed.stdout))
    canonical_value = canonical.decode_cyclic(value)
    generated_value = generated.decode_cyclic(value)
    matches = k_value == canonical_value == generated_value
    print(f"  K_RESULT={k_value!r}")
    print(f"  PY_CANONICAL={canonical_value!r}")
    print(f"  PY_GENERATED={generated_value!r}")
    print(f"  FINAL_ENV={final_env}")
    print(f"  RESULT_LABEL={result_label}")
    print(f"  MATCH={matches}")
    failures += not matches

print(f"FAILURE_COUNT: {failures}")
sys.exit(1 if failures else 0)
