#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with independent Python."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import re
import subprocess


def load_module(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def k_list(values):
    out = "nil"
    for value in reversed(values):
        out = f"cons({value}, {out})"
    return f"listVal({out})"


candidate = load_module(
    "candidate_solution_stage3",
    Path("/tmp/audit-work/review-57/src/solution.py"),
)
canonical = load_module(
    "trusted_canonical_stage3",
    Path("/tmp/audit-work/review-57/trusted/canonical.py"),
)

program = "/tmp/audit-work/review-57/src/solution.mpy"
definition = "/tmp/audit-work/review-57/build/semantic-llvm-kompiled"
cases = [
    [],
    [7],
    [1, 1],
    [1, 2, 4, 20],
    [4, 1, 0, -10],
    [1, 20, 4, 10],
    [0, 1, 0],
    [-3, -3, 0, 9],
    [9, 0, -3, -3],
    [-(10**30), 0, 10**30],
]

for values in cases:
    argv = ["krun", program, f"-cARG={k_list(values)}", "--definition", definition]
    print("COMMAND:", " ".join(argv))
    proc = subprocess.run(argv, text=True, capture_output=True)
    print("KRUN_EXIT:", proc.returncode)
    print("KRUN_STDOUT:", proc.stdout.strip())
    if proc.stderr:
        print("KRUN_STDERR:", proc.stderr.strip())
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    matches = re.findall(r"boolVal\s*\(\s*(true|false)\s*\)", proc.stdout)
    if len(matches) != 1:
        raise AssertionError(f"could not identify unique K boolean for {values}: {proc.stdout!r}")
    k_result = matches[0] == "true"
    candidate_result = candidate.monotonic(values)
    canonical_result = canonical.monotonic(values)
    print(
        f"COMPARE input={values!r} K={k_result!r} "
        f"candidate_python={candidate_result!r} canonical_python={canonical_result!r}"
    )
    if not (k_result == candidate_result == canonical_result):
        raise AssertionError(f"concrete divergence for {values!r}")

print(f"CASES: {len(cases)}")
print("MISMATCHES: 0")
