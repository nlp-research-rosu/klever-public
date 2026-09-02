#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare to both Pythons."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


ROOT = Path("/tmp/audit-work/110-exchange")
CANDIDATE = ROOT / "candidate"


def load_exchange(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


canonical = load_exchange("kcheck_canonical", ROOT / "trusted/canonical.py")
generated = load_exchange("kcheck_generated", CANDIDATE / "solution.py")


def k_list(values: list[int]) -> str:
    term = "Nil"
    for value in reversed(values):
        term = f"Cons({value}, {term})"
    return term


cases = [
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([1, 2, 3, 4], [1, 5, 3, 4]),
    ([], []),
    ([], [2]),
    ([1], []),
    ([2], []),
    ([1], [2]),
    ([1], [3]),
    ([0], [-1]),
    ([-1], [-2]),
    ([-3, -2], [-4, -5]),
    ([1, 3, 2], [4, 5]),
    ([1, 3, 2], [4, 6]),
    ([1, 3, 2], [4, 6, 8]),
    ([10**30 + 1, -(10**30 + 2)], [10**30 + 4]),
]

for index, (lst1, lst2) in enumerate(cases):
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "concrete-kompiled",
        f"-cLST1={k_list(lst1)}",
        f"-cLST2={k_list(lst2)}",
        "--output",
        "pretty",
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=CANDIDATE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    print(f"EXIT_STATUS: {completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout)
        raise AssertionError(f"krun failed for case {index}")
    match = re.search(r'<result>\s*"(YES|NO)"\s*</result>', completed.stdout)
    if match is None:
        print(completed.stdout)
        raise AssertionError(f"missing terminal result for case {index}")
    assert re.search(r"<k>\s*\.K\s*</k>", completed.stdout)
    k_result = match.group(1)
    python_result = generated(list(lst1), list(lst2))
    canonical_result = canonical(list(lst1), list(lst2))
    assert k_result == python_result == canonical_result
    print(
        f"CASE {index:02d} lst1={lst1!r} lst2={lst2!r} "
        f"K={k_result} generated={python_result} canonical={canonical_result}"
    )

print(f"CONCRETE_SEMANTICS_OK cases={len(cases)} mismatches=0 stuck=0")
