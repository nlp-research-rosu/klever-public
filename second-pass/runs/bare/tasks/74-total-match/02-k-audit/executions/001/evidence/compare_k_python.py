#!/usr/bin/env python3
"""Compare freshly built generated K semantics against two Python executions."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, name: str) -> Callable[[list[str], list[str]], list[str]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


def k_string(value: str) -> str:
    encoded: list[str] = ['"']
    for character in value:
        codepoint = ord(character)
        if character == '"':
            encoded.append('\\"')
        elif character == "\\":
            encoded.append("\\\\")
        elif 0x20 <= codepoint <= 0x7E:
            encoded.append(character)
        elif codepoint <= 0xFF:
            encoded.append(f"\\x{codepoint:02x}")
        elif codepoint <= 0xFFFF:
            encoded.append(f"\\u{codepoint:04x}")
        else:
            encoded.append(f"\\U{codepoint:08x}")
    encoded.append('"')
    return "".join(encoded)


def k_list(values: list[str]) -> str:
    items = " :: ".join(f"pyStr({k_string(value)})" for value in values)
    body = f"{items} :: .StrVals" if items else ".StrVals"
    return f"pyList({body})"


def find_label(node: dict[str, Any], prefix: str) -> dict[str, Any] | None:
    label = node.get("label", {}).get("name", "")
    if label.startswith(prefix):
        return node
    for child in node.get("args", []):
        found = find_label(child, prefix)
        if found is not None:
            return found
    for child in node.get("items", []):
        found = find_label(child, prefix)
        if found is not None:
            return found
    return None


def decode_string(node: dict[str, Any]) -> str:
    py_string = find_label(node, "pyStr(_)")
    if py_string is None:
        raise ValueError(f"expected pyStr node: {node}")
    token = py_string["args"][0]["token"]
    return ast.literal_eval(token)


def decode_list_node(node: dict[str, Any]) -> list[str]:
    label = node.get("label", {}).get("name", "")
    if label.startswith(".StrVals_"):
        return []
    if not label.startswith("_::__"):
        raise ValueError(f"expected StrVals cons: {node}")
    return [decode_string(node["args"][0])] + decode_list_node(node["args"][1])


def decode_result(stdout: str) -> list[str]:
    document = json.loads(stdout)
    py_list = find_label(document["term"], "pyList(_)")
    if py_list is None:
        raise ValueError(f"no pyList result in: {stdout}")
    return decode_list_node(py_list["args"][0])


parser = argparse.ArgumentParser()
parser.add_argument("definition", type=Path)
parser.add_argument("mpy", type=Path)
parser.add_argument("canonical", type=Path)
parser.add_argument("generated", type=Path)
parser.add_argument("results", type=Path)
args = parser.parse_args()

canonical = load_entry(args.canonical, "trusted_canonical_k_compare")
generated = load_entry(args.generated, "candidate_solution_k_compare")

cases = [
    {"name": "documented-empty-tie", "lst1": [], "lst2": []},
    {"name": "documented-left-longer", "lst1": ["hi", "admin"], "lst2": ["hI", "Hi"]},
    {
        "name": "documented-left-shorter",
        "lst1": ["hi", "admin"],
        "lst2": ["hi", "hi", "admin", "project"],
    },
    {"name": "empty-string-tie", "lst1": [""], "lst2": []},
    {"name": "left-strict", "lst1": ["a"], "lst2": ["bb"]},
    {"name": "right-strict", "lst1": ["bb"], "lst2": ["a"]},
    {"name": "nonempty-tie", "lst1": ["a", "b"], "lst2": ["cc"]},
    {"name": "unicode-astral-vs-ascii", "lst1": ["🙂"], "lst2": ["ab"]},
    {"name": "unicode-accent-vs-ascii", "lst1": ["é"], "lst2": ["a"]},
    {"name": "unicode-combining", "lst1": ["e\u0301"], "lst2": ["ab"]},
    {"name": "embedded-nul", "lst1": ["\u0000"], "lst2": ["a"]},
    {"name": "multi-element-boundary", "lst1": ["", "abc"], "lst2": ["d", "ef"]},
]

records: list[dict[str, Any]] = []
for case in cases:
    left = case["lst1"]
    right = case["lst2"]
    cargs = f"args({k_list(left)},{k_list(right)})"
    command = [
        "krun",
        str(args.mpy),
        "--definition",
        str(args.definition),
        f"-cARGS={cargs}",
        "--output",
        "json",
    ]
    process = subprocess.run(command, text=True, capture_output=True, check=False)
    k_result = decode_result(process.stdout) if process.returncode == 0 else None
    canonical_result = canonical(left, right)
    generated_result = generated(left, right)
    record = {
        **case,
        "python_lengths": [sum(map(len, left)), sum(map(len, right))],
        "canonical_result": canonical_result,
        "generated_result": generated_result,
        "k_args": cargs,
        "krun_command": command,
        "krun_exit": process.returncode,
        "krun_result": k_result,
        "krun_stderr": process.stderr,
        "match": (
            process.returncode == 0
            and canonical_result == generated_result
            and k_result == canonical_result
        ),
    }
    records.append(record)
    print(
        f"{case['name']}: python={canonical_result!r}; "
        f"k={k_result!r}; match={record['match']}"
    )

summary = {
    "definition": str(args.definition),
    "mpy": str(args.mpy),
    "case_count": len(records),
    "mismatch_count": sum(not record["match"] for record in records),
    "records": records,
}
args.results.write_text(
    json.dumps(summary, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(
    f"SUMMARY: cases={summary['case_count']} "
    f"mismatches={summary['mismatch_count']} results={args.results}"
)
raise SystemExit(1 if summary["mismatch_count"] else 0)
