#!/usr/bin/env python3
import importlib.util
import re
import subprocess
import sys

sys.dont_write_bytecode = True


def load_function(path: str):
    spec = importlib.util.spec_from_file_location("trusted_canonical_k_oracle", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def k_list(values):
    if not values:
        return "ListVal(.Ints)"
    return "ListVal(" + ", ".join(str(value) for value in values) + ")"


canonical = load_function("/reference/canonical.py")
definition = "/tmp/audit-work/semantic-llvm-kompiled-audit"
program = "/tmp/audit-work/candidate-src/solution.mpy"
cases = [
    [],
    [1],
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4],
    [-1, -5, 2, -1, -5],
]
cases.extend([
    [(-index if index % 2 else index + 1) for index in range(length)]
    for length in range(5, 14)
])
cases.extend([
    [0, 0, 0, 0, 0, 0, 0, 0, -11],
    [10**20, -(10**20), 7, -9, 4],
])

pattern = re.compile(r"VInt\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K")
mismatches = []
for ordinal, case in enumerate(cases):
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cARGS={k_list(case)}",
    ]
    print("COMMAND:", " ".join(repr(piece) for piece in command))
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"CASE[{ordinal}]={case!r}")
    print(f"EXIT_STATUS={completed.returncode}")
    if completed.stderr:
        print("STDERR:")
        print(completed.stderr.rstrip())
    if completed.returncode != 0:
        print("STDOUT:")
        print(completed.stdout.rstrip())
        mismatches.append((ordinal, "krun failure"))
        continue
    match = pattern.search(completed.stdout)
    if match is None:
        print("STDOUT:")
        print(completed.stdout.rstrip())
        mismatches.append((ordinal, "no terminal VInt"))
        continue
    k_value = int(match.group(1))
    python_value = canonical(case.copy())
    same = k_value == python_value
    print(f"K_RESULT={k_value}")
    print(f"PYTHON_RESULT={python_value}")
    print(f"MATCH={same}")
    if not same:
        mismatches.append((ordinal, k_value, python_value))

print(f"concrete_cases={len(cases)}")
print(f"concrete_mismatches={len(mismatches)}")
if mismatches:
    print(f"MISMATCHES={mismatches!r}")
    raise SystemExit(1)
