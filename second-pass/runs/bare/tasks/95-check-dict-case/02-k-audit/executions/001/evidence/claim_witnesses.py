#!/usr/bin/env python3
"""Ground satisfying states and concrete results for every submitted claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


SCRATCH = Path("/tmp/audit-work/candidate-src")


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def prompt_oracle(mapping: dict[Any, Any]) -> bool:
    if not mapping:
        return False
    if not all(isinstance(key, str) for key in mapping):
        return False
    return all(key.islower() for key in mapping) or all(
        key.isupper() for key in mapping
    )


solution = load_entry(SCRATCH / "solution.py", "witness_solution")
canonical = load_entry(SCRATCH / "canonical.py", "witness_canonical")

claims = [
    {},
    {"a": 0, "b": 0},
    {"a": 0, "A": 0, "B": 0},
    {"a": 0, 8: 0},
    {"Name": 0, "Age": 0, "City": 0},
    {"STATE": 0, "ZIP": 0},
    {"abc-123": 0, "z9": 0},
    {"ABC-123": 0, "Z9": 0},
    {"123": 0},
    {"aA": 0},
    {True: 0},
]

for index, mapping in enumerate(claims, start=1):
    expected = prompt_oracle(mapping)
    record = {
        "claim": index,
        "satisfying_state": {
            "k": "solutionProgram",
            "input_keys_repr": repr(list(mapping)),
            "env": ".Map",
            "result": "NoneVal",
        },
        "expected_BoolVal": expected,
        "solution_py": solution(mapping),
        "canonical_py": canonical(mapping),
    }
    print(json.dumps(record, sort_keys=True))
    assert record["solution_py"] == expected
    assert record["canonical_py"] == expected
