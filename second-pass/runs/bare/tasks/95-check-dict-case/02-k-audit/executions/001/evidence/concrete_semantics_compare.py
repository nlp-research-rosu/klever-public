#!/usr/bin/env python3
"""Run the fresh K semantics and compare with independent Python execution."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SCRATCH = Path("/tmp/audit-work/candidate-src")
DEFINITION = SCRATCH / "concrete-kompiled"


def load_solution():
    spec = importlib.util.spec_from_file_location(
        "concrete_compare_solution", SCRATCH / "solution.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def oracle(mapping: dict[Any, Any]) -> bool:
    if not mapping:
        return False
    if not all(isinstance(key, str) for key in mapping):
        return False
    return all(key.islower() for key in mapping) or all(
        key.isupper() for key in mapping
    )


def k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def k_value(value: Any) -> str:
    if isinstance(value, bool):
        return f"BoolVal({'true' if value else 'false'})"
    if isinstance(value, int):
        return f"IntVal({value})"
    if isinstance(value, str):
        return f"StrVal({k_string(value)})"
    raise TypeError(f"unsupported test key: {value!r}")


def k_dict(mapping: dict[Any, Any]) -> str:
    if not mapping:
        return "DictVal()"
    return "DictVal(" + " ".join(k_value(key) for key in mapping) + ")"


def run_k(mapping: dict[Any, Any]) -> tuple[bool, str]:
    input_term = k_dict(mapping)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={input_term}",
        "--pattern",
        "<result> R:Value </result>",
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print("KRUN_COMMAND:", " ".join(repr(part) for part in command))
    print(completed.stdout.rstrip())
    print("KRUN_EXIT_STATUS:", completed.returncode)
    if completed.returncode != 0:
        raise RuntimeError(f"krun failed for {input_term}")
    match = re.search(r"BoolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
    if not match:
        raise RuntimeError(f"no Boolean result for {input_term}")
    return match.group(1) == "true", input_term


solution = load_solution()
cases = [
    ("empty", {}),
    ("lower", {"a": 0, "b": 0}),
    ("upper", {"STATE": 0, "ZIP": 0}),
    ("mixed", {"a": 0, "A": 0}),
    ("non_string_first", {8: 0, "a": 0}),
    ("non_string_late", {"a": 0, "b": 0, 8: 0}),
    ("title", {"Name": 0, "Age": 0, "City": 0}),
    ("uncased", {"123": 0}),
    ("punctuated_lower", {"abc-123": 0, "z9": 0}),
    ("mixed_one_key", {"aA": 0}),
    ("unicode_lower", {"é": 0, "ß": 0}),
    ("unicode_upper", {"É": 0, "İ": 0}),
    ("unicode_uncased", {"中": 0}),
]

records = []
for label, mapping in cases:
    k_result, input_term = run_k(mapping)
    python_result = solution(mapping)
    oracle_result = oracle(mapping)
    if python_result != oracle_result:
        raise AssertionError(f"solution/oracle disagreement for {label}")
    record = {
        "label": label,
        "keys_repr": repr(list(mapping)),
        "k_input": input_term,
        "k_result": k_result,
        "python_result": python_result,
        "prompt_oracle": oracle_result,
        "match": k_result == python_result,
    }
    records.append(record)
    print("COMPARISON:", json.dumps(record, ensure_ascii=False, sort_keys=True))

mismatches = [record for record in records if not record["match"]]
print(
    "SUMMARY:",
    json.dumps(
        {"cases": len(records), "mismatches": len(mismatches)},
        sort_keys=True,
    ),
)
print("MISMATCHES:")
for record in mismatches:
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
