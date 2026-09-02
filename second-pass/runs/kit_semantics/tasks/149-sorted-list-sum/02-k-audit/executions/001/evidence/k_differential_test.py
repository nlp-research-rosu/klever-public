#!/usr/bin/env python3
"""Reviewer-authored Python/LLVM differential test for the supplied semantics."""

from __future__ import annotations

import importlib.util
import itertools
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/149-sorted-list-sum")
SOLUTION = Path("/candidate/solution.py")
TRANSLATOR = Path("/reference/py2mpy.py")
RUNTIME = WORK / "reviewer-runtime-kompiled"


def load_function(path: Path):
    spec = importlib.util.spec_from_file_location("reviewer_k_candidate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def oracle(words: list[str]) -> list[str]:
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def main() -> int:
    pool = ["", "a", "aa", "bb", "cccc"]
    cases = [
        list(items)
        for size in range(4)
        for items in itertools.product(pool, repeat=size)
    ]
    candidate = load_function(SOLUTION)
    python_mismatches = [
        (words, candidate(list(words)), oracle(words))
        for words in cases
        if candidate(list(words)) != oracle(words)
    ]

    smoke_py = WORK / "reviewer_differential_smoke.py"
    smoke_mpy = WORK / "reviewer_differential_smoke.mpy"
    assertions = [
        f"assert sorted_list_sum({words!r}) == {oracle(words)!r}"
        for words in cases
    ]
    smoke_py.write_text(
        SOLUTION.read_text(encoding="utf-8") + "\n\n" + "\n".join(assertions) + "\n",
        encoding="utf-8",
    )
    translated = subprocess.run(
        [sys.executable, str(TRANSLATOR), str(smoke_py)],
        check=False,
        capture_output=True,
        text=True,
    )
    if translated.returncode == 0:
        smoke_mpy.write_text(translated.stdout, encoding="utf-8")
        krun = subprocess.run(
            ["krun", str(smoke_mpy), "--definition", str(RUNTIME)],
            check=False,
            capture_output=True,
            text=True,
        )
    else:
        krun = None

    print(f"pool={pool!r}")
    print("list_lengths=0..3")
    print(f"cases={len(cases)}")
    print(f"python_mismatches={len(python_mismatches)}")
    print(f"translator_exit={translated.returncode}")
    if krun is not None:
        has_empty_k = "<k>\n    .K" in krun.stdout
        has_no_exception = "NoExc" in krun.stdout
        has_zero_exit_cell = "<exit-code>" in krun.stdout and "0" in krun.stdout
        print(f"krun_exit={krun.returncode}")
        print(f"krun_has_final_empty_k={has_empty_k}")
        print(f"krun_has_no_exception={has_no_exception}")
        print(f"krun_has_zero_exit_cell={has_zero_exit_cell}")
    for mismatch in python_mismatches[:10]:
        print(f"FAIL {mismatch!r}")
    if translated.returncode != 0:
        print(translated.stderr[-2000:])
        return 1
    assert krun is not None
    if krun.returncode != 0:
        print(krun.stdout[-2000:])
        print(krun.stderr[-2000:])
        return 1
    return 1 if python_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
