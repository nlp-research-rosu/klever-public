#!/usr/bin/env python3
"""Differentially test the exact solution source in CPython and MPY/LLVM."""

from itertools import product
from pathlib import Path
import subprocess
import tempfile

from solution import sort_array


def expected(values):
    if not values:
        return []
    return sorted(
        values,
        reverse=(values[0] + values[-1]) % 2 == 0,
    )


def main():
    cases = []
    for length in range(5):
        cases.extend(list(values) for values in product(range(4), repeat=length))

    prompt_cases = [
        [],
        [5],
        [2, 4, 3, 0, 1, 5],
        [2, 4, 3, 0, 1, 5, 6],
    ]
    for case in prompt_cases:
        if case not in cases:
            cases.append(case)

    mismatches = 0
    for case in cases:
        before = case.copy()
        actual = sort_array(case)
        oracle = expected(case)
        if actual != oracle or case != before or actual is case:
            mismatches += 1

    solution_source = Path("solution.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="sort-array-diff-") as tmp:
        tmp_path = Path(tmp)
        batch_size = 16
        for batch_no, start in enumerate(range(0, len(cases), batch_size)):
            batch = cases[start : start + batch_size]
            assertions = [
                f"assert sort_array({case!r}) == {expected(case)!r}"
                for case in batch
            ]
            k_test_source = (
                solution_source + "\n" + "\n".join(assertions) + "\n"
            )
            py_path = tmp_path / f"cases-{batch_no}.py"
            mpy_path = tmp_path / f"cases-{batch_no}.mpy"
            py_path.write_text(k_test_source, encoding="utf-8")
            translated = subprocess.run(
                ["python3", "py2mpy.py", str(py_path)],
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            mpy_path.write_text(translated.stdout, encoding="utf-8")
            concrete = subprocess.run(
                [
                    "krun",
                    str(mpy_path),
                    "--definition",
                    "runtime-kompiled",
                ],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if concrete.returncode != 0:
                print(concrete.stdout)
                raise SystemExit(concrete.returncode)

    print(
        "differential: "
        f"{len(cases)} cases, CPython mismatches={mismatches}, "
        "MPY assertion failures=0"
    )
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
