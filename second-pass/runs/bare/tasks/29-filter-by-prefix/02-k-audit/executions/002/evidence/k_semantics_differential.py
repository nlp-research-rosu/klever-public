#!/usr/bin/env python3
"""Finite independent K-semantics vs CPython differential bridge."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import re
import shlex
import subprocess
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


def k_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def k_list(values: list[str]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({k_string(value)}, {result})"
    return result


def compact(term: str) -> str:
    return re.sub(r"\s+", "", term)


oracle = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/trusted/canonical.py"),
    "trusted_canonical_29_k_bridge",
)
candidate = load_function(
    Path("/tmp/audit-work/29-filter-by-prefix/candidate-src/solution.py"),
    "candidate_solution_29_k_bridge",
)

pool = [""]
for length in range(1, 5):
    pool.extend("".join(chars) for chars in itertools.product(("a", "b"), repeat=length))

cases: list[tuple[list[str], str, str]] = []
for prefix in ("", "a", "b", "aa", "ab", "ba", "bb", "aaa", "bbb", "aaaaa"):
    cases.append((list(pool), prefix, "systematic-ascii-pool"))

rng = random.Random(290030)
for _ in range(10):
    values = [rng.choice(pool) for _ in range(rng.randrange(0, 41))]
    prefix = rng.choice(pool)
    cases.append((values, prefix, "seeded-ascii-list"))

workdir = Path("/tmp/audit-work/29-filter-by-prefix/candidate-src")
definition = workdir / "concrete-kompiled"
program = workdir / "solution.mpy"
mismatches: list[str] = []

for index, (values, prefix, label) in enumerate(cases):
    expected = oracle(list(values), prefix)
    candidate_value = candidate(list(values), prefix)
    if candidate_value != expected:
        mismatches.append(
            f"python mismatch case={index} expected={expected!r} "
            f"candidate={candidate_value!r}"
        )
        continue
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cINPUT={k_list(values)}",
        f"-cPREFIX={k_string(prefix)}",
    ]
    completed = subprocess.run(
        command,
        cwd=workdir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
    )
    print(f"case={index} label={label} command={shlex.join(command)}")
    print(f"case={index} exit={completed.returncode}")
    if completed.returncode != 0:
        print(completed.stdout[-2000:])
        mismatches.append(f"K execution failure case={index}")
        continue
    output_match = re.search(r"<output>\s*(.*?)\s*</output>", completed.stdout, re.S)
    if output_match is None:
        mismatches.append(f"missing output cell case={index}")
        continue
    actual_term = compact(output_match.group(1))
    expected_term = compact(f"listVal({k_list(expected)})")
    print(
        f"case={index} prefix={prefix!r} input_count={len(values)} "
        f"expected_count={len(expected)} actual_term={actual_term}"
    )
    if actual_term != expected_term:
        mismatches.append(
            f"K mismatch case={index} expected_term={expected_term} "
            f"actual_term={actual_term}"
        )

print(f"cases={len(cases)}")
print(f"systematic_pair_checks={10 * len(pool)}")
print("seed=290030")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(mismatch)
raise SystemExit(1 if mismatches else 0)
