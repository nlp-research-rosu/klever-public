#!/usr/bin/env python3
"""Independent differential test for HumanEval/67.

The core sample is the natural fixed-template reading used by all documented
examples. Edge probes deliberately include empty/malformed/whitespace variants
so any difference in effective domain remains visible rather than being hidden.
"""

from __future__ import annotations

import importlib.util
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Case:
    category: str
    text: str
    total: int


def load_function(path: Path) -> Callable[[str, int], int]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


def outcome(function: Callable[[str, int], int], text: str, total: int) -> tuple:
    try:
        return ("value", function(text, total))
    except Exception as error:  # comparison intentionally records exceptional edges
        return ("exception", type(error).__name__, str(error))


canonical = load_function(Path("/reference/canonical.py"))
generated = load_function(Path("/tmp/audit-work/fruit-audit/solution.py"))

cases = [
    Case("documented", "5 apples and 6 oranges", 19),
    Case("documented", "0 apples and 1 oranges", 3),
    Case("documented", "2 apples and 3 oranges", 100),
    Case("documented", "100 apples and 1 oranges", 120),
    Case("boundary", "0 apples and 0 oranges", 0),
    Case("boundary", "1 apples and 0 oranges", 1),
    Case("boundary", "0 apples and 1 oranges", 1),
    Case("boundary", "999999 apples and 888888 oranges", 1888887),
    Case("outside-total-invariant", "2 apples and 3 oranges", 4),
    Case("edge-empty", "", 0),
    Case("edge-whitespace", "  5  apples and  6 oranges  ", 19),
    Case("edge-whitespace", "5\tapples and 6 oranges", 19),
    Case("edge-extra-token", "basket has 5 apples and 6 oranges", 19),
    Case("edge-extra-number", "5 apples and 6 oranges in 1 basket", 19),
    Case("edge-negative-token", "-1 apples and 2 oranges", 5),
    Case("edge-malformed", "five apples and six oranges", 19),
]

random_generator = random.Random(670067)
for _ in range(100):
    apples = random_generator.randrange(0, 10**6)
    oranges = random_generator.randrange(0, 10**6)
    slack = random_generator.randrange(0, 10**6)
    cases.append(
        Case(
            "generated-fixed-template",
            f"{apples} apples and {oranges} oranges",
            apples + oranges + slack,
        )
    )

core_mismatches = 0
edge_mismatches = 0
for index, case in enumerate(cases):
    canonical_result = outcome(canonical, case.text, case.total)
    generated_result = outcome(generated, case.text, case.total)
    matches = canonical_result == generated_result
    if not matches and case.category.startswith("edge-"):
        edge_mismatches += 1
    elif not matches:
        core_mismatches += 1
    print(
        f"{index:03d} category={case.category} input=({case.text!r}, {case.total}) "
        f"canonical={canonical_result!r} generated={generated_result!r} "
        f"match={matches}"
    )

print(
    f"SUMMARY cases={len(cases)} core_mismatches={core_mismatches} "
    f"edge_mismatches={edge_mismatches}"
)
if core_mismatches:
    raise SystemExit(1)
