#!/usr/bin/env python3
"""Concrete generated-semantics checks against both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


def label(term: dict) -> str:
    return term["label"]["name"]


def find_cell(term: dict, cell_label: str) -> dict:
    if term.get("node") == "KApply" and label(term) == cell_label:
        return term["args"][0]
    for child in term.get("args", []):
        if isinstance(child, dict):
            try:
                return find_cell(child, cell_label)
            except KeyError:
                pass
    raise KeyError(cell_label)


def has_prefix(term: dict, prefix: str) -> bool:
    return term.get("node") == "KApply" and label(term).startswith(prefix)


def decode_text(term: dict) -> str:
    if has_prefix(term, "literal("):
        return json.loads(term["args"][0]["token"])
    if has_prefix(term, "number("):
        return str(int(term["args"][0]["token"]))
    if has_prefix(term, "concat("):
        return decode_text(term["args"][0]) + decode_text(term["args"][1])
    raise AssertionError(f"unexpected Text term: {json.dumps(term, sort_keys=True)}")


def decode_value(term: dict):
    if has_prefix(term, "pyString("):
        return decode_text(term["args"][0])
    if has_prefix(term, "pyInt("):
        return int(term["args"][0]["token"])
    if has_prefix(term, "pyBool("):
        return term["args"][0]["token"] == "true"
    if has_prefix(term, "pyList("):
        return decode_values(term["args"][0])
    raise AssertionError(f"unexpected Value term: {json.dumps(term, sort_keys=True)}")


def decode_values(term: dict) -> list:
    if has_prefix(term, "noValues"):
        return []
    if has_prefix(term, "value("):
        return [decode_value(term["args"][0])] + decode_values(term["args"][1])
    raise AssertionError(f"unexpected Values term: {json.dumps(term, sort_keys=True)}")


def digits_term(value: str) -> str:
    result = "noDigits"
    for character in reversed(value):
        parity = "oddDigit" if int(character) % 2 else "evenDigit"
        result = f"digit({parity},{result})"
    return result


def input_term(values: list[str]) -> str:
    result = "noValues"
    for value in reversed(values):
        result = f"value(pyString(inputDigits({digits_term(value)})),{result})"
    return f"pyList({result})"


if len(sys.argv) != 5:
    raise SystemExit(
        "usage: generated_semantics_concrete_test.py "
        "WORKDIR CANONICAL.py SOLUTION.py DEFINITION"
    )

workdir = Path(sys.argv[1])
canonical = load_function("concrete_trusted_canonical", Path(sys.argv[2]))
submitted = load_function("concrete_submitted_solution", Path(sys.argv[3]))
definition = Path(sys.argv[4])

cases = [
    [],
    [""],
    ["0"],
    ["1"],
    ["0123456789"],
    ["1234567"],
    ["3", "11111111"],
    ["1" * 9],
    ["1" * 10],
    ["1" * 11],
    ["", "2468", "13579"],
    ["9876543210" * 20],
]

for index, case in enumerate(cases, 1):
    value = input_term(case)
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={value}",
        "--definition",
        str(definition),
        "--output",
        "json",
    ]
    print(f"COMMAND[{index}]: {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=workdir,
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"EXIT[{index}]: {result.returncode}")
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    document = json.loads(result.stdout)
    term = document["term"]
    k_cell = find_cell(term, "<k>")
    assert k_cell.get("node") == "KSequence" and not k_cell.get("items")
    actual = decode_value(find_cell(term, "<output>"))
    canonical_result = canonical(case)
    submitted_result = submitted(case)
    print(
        f"CASE[{index}]: input={case!r} "
        f"k={actual!r} canonical={canonical_result!r} submitted={submitted_result!r}"
    )
    assert actual == canonical_result == submitted_result

print(f"cases={len(cases)} mismatches=0")
print("GENERATED_SEMANTICS_CONCRETE=PASS")
