#!/usr/bin/env python3
"""Differentially exercise solution.py under CPython and the supplied K runtime."""

from __future__ import annotations

import heapq
import importlib.util
from pathlib import Path
import random
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent


def oracle(arr, k):
    return sorted(heapq.nlargest(k, arr))


def load_solution():
    spec = importlib.util.spec_from_file_location("candidate_solution", ROOT / "solution.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.maximum


def cases():
    fixed = [
        ([-3, -4, 5], 3),
        ([4, -4, 4], 2),
        ([-3, 2, 1, 2, -1, -2, 1], 1),
        ([7], 0),
        ([7], 1),
        ([-1000, 0, 1000, -1000, 1000], 4),
        ([1000] * 8, 5),
        ([-1000] * 8, 8),
    ]
    rng = random.Random(20260725)
    generated = []
    for length in range(1, 13):
        for _ in range(4):
            arr = [rng.randint(-1000, 1000) for _ in range(length)]
            generated.append((arr, rng.randint(0, length)))
    arr = [rng.randint(-1000, 1000) for _ in range(50)]
    generated.extend((arr, k) for k in (0, 1, 25, 49, 50))
    return fixed + generated


def main():
    maximum = load_solution()
    samples = cases()
    expected = [oracle(arr, k) for arr, k in samples]

    mismatches = []
    for (arr, k), want in zip(samples, expected):
        got = maximum(list(arr), k)
        if got != want:
            mismatches.append((arr, k, got, want))
    if mismatches:
        raise AssertionError(f"CPython mismatches: {mismatches[:3]}")

    source = (ROOT / "solution.py").read_text(encoding="utf-8")
    assertions = [
        f"assert maximum({arr!r}, {k}) == {want!r}"
        for (arr, k), want in zip(samples, expected)
    ]

    with tempfile.TemporaryDirectory(prefix="maximum-k-differential-") as tmp:
        tmp_path = Path(tmp)
        test_py = tmp_path / "test.py"
        test_mpy = tmp_path / "test.mpy"
        test_py.write_text(source + "\n\n" + "\n".join(assertions) + "\n", encoding="utf-8")

        with test_mpy.open("w", encoding="utf-8") as output:
            translate = subprocess.run(
                ["python3", str(ROOT / "py2mpy.py"), str(test_py)],
                cwd=ROOT,
                stdout=output,
                text=True,
                check=False,
            )
        if translate.returncode != 0:
            raise SystemExit(translate.returncode)

        run = subprocess.run(
            [
                "krun",
                str(test_mpy),
                "--definition",
                str(ROOT / "runtime-kompiled"),
                "--output",
                "none",
            ],
            cwd=ROOT,
            text=True,
            check=False,
        )
        if run.returncode != 0:
            raise SystemExit(run.returncode)

    print(
        f"DIFFERENTIAL_PASSED: {len(samples)} cases; "
        "CPython mismatches=0; K exit=0"
    )


if __name__ == "__main__":
    main()
