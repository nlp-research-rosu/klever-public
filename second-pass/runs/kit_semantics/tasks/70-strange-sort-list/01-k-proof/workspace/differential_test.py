#!/usr/bin/env python3
from itertools import product
from pathlib import Path
import subprocess

from solution import strange_sort_list


def contract_oracle(values):
    remaining = list(values)
    result = []
    take_minimum = True
    while remaining:
        selected = min(remaining) if take_minimum else max(remaining)
        result.append(selected)
        remaining.remove(selected)
        take_minimum = not take_minimum
    return result


python_cases = [
    list(items)
    for length in range(7)
    for items in product((-2, -1, 0, 1, 2), repeat=length)
]

python_mismatches = 0
for case in python_cases:
    original = list(case)
    if strange_sort_list(case) != contract_oracle(case) or case != original:
        python_mismatches += 1

if python_mismatches:
    raise SystemExit(f"CPython mismatches={python_mismatches}")

k_cases = [
    list(items)
    for length in range(5)
    for items in product((-1, 0, 1), repeat=length)
]
k_cases.extend(
    [
        [1, 2, 3, 4],
        [5, 5, 5, 5],
        [3, -1, 3, 2, 0],
    ]
)

solution_source = Path("solution.py").read_text(encoding="utf-8").rstrip()
assertions = "\n".join(
    f"assert strange_sort_list({case!r}) == {contract_oracle(case)!r}"
    for case in k_cases
)
Path("differential-smoke.py").write_text(
    solution_source + "\n\n" + assertions + "\n",
    encoding="utf-8",
)

with Path("differential-smoke.mpy").open("w", encoding="utf-8") as output:
    translated = subprocess.run(
        ["python3", "py2mpy.py", "differential-smoke.py"],
        stdout=output,
        text=True,
        check=False,
    )
if translated.returncode:
    raise SystemExit(f"translation exit={translated.returncode}")

executed = subprocess.run(
    ["krun", "differential-smoke.mpy", "--definition", "runtime-kompiled"],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    check=False,
)
if (
    executed.returncode
    or "<exc>\n    NoExc\n  </exc>" not in executed.stdout
    or "<exit-code>\n    0\n  </exit-code>" not in executed.stdout
):
    print(executed.stdout)
    raise SystemExit(f"K differential execution exit={executed.returncode}")

print(f"CPython cases={len(python_cases)} mismatches=0 input-mutations=0")
print(f"K/LLVM cases={len(k_cases)} mismatches=0")
