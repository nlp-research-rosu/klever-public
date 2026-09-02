from itertools import product
from pathlib import Path
import importlib.util
import subprocess
import sys


def oracle(words):
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def load_solution():
    spec = importlib.util.spec_from_file_location("candidate", "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


pool = ["", "a", "ab", "bb", "cccc"]
cases = [
    list(items)
    for size in range(4)
    for items in product(pool, repeat=size)
]

candidate = load_solution()
python_mismatches = [
    (words, candidate(words), oracle(words))
    for words in cases
    if candidate(words) != oracle(words)
]

solution_source = Path("solution.py").read_text(encoding="utf-8")
assertions = [
    f"assert sorted_list_sum({words!r}) == {oracle(words)!r}"
    for words in cases
]
Path("differential-smoke.py").write_text(
    solution_source + "\n\n" + "\n".join(assertions) + "\n",
    encoding="utf-8",
)

translation = subprocess.run(
    [sys.executable, "py2mpy.py", "differential-smoke.py"],
    check=True,
    capture_output=True,
    text=True,
)
Path("differential-smoke.mpy").write_text(
    translation.stdout,
    encoding="utf-8",
)
krun = subprocess.run(
    [
        "krun",
        "differential-smoke.mpy",
        "--definition",
        "runtime-kompiled",
    ],
    capture_output=True,
    text=True,
)

print(f"cases={len(cases)}")
print(f"python_mismatches={len(python_mismatches)}")
print(f"k_exit={krun.returncode}")
if python_mismatches:
    print(python_mismatches[:5])
if krun.returncode != 0:
    print(krun.stdout[-4000:])
    print(krun.stderr[-4000:])
if python_mismatches or krun.returncode != 0:
    raise SystemExit(1)
