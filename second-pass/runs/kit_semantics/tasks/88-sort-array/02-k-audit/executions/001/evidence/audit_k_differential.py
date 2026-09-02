#!/usr/bin/env python3
"""Compare fresh MPY/LLVM execution with the trusted canonical implementation."""

from __future__ import annotations

import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess


ROOT = Path("/tmp/audit-work/reconstruction")


def load_canonical():
    spec = importlib.util.spec_from_file_location(
        "trusted_canonical_k_diff", ROOT / "canonical.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load_canonical()
    cases = [
        list(values)
        for length in range(5)
        for values in product(range(4), repeat=length)
    ]
    for case in (
        [5],
        [2, 4, 3, 0, 1, 5],
        [2, 4, 3, 0, 1, 5, 6],
    ):
        if case not in cases:
            cases.append(case)

    solution_source = (ROOT / "solution.py").read_text(encoding="utf-8")
    batch_size = 16
    batches = 0
    for start in range(0, len(cases), batch_size):
        batch = cases[start : start + batch_size]
        statements: list[str] = []
        for index, case in enumerate(batch):
            expected = canonical.sort_array(list(case))
            statements.extend(
                (
                    f"input_{index} = {case!r}",
                    f"before_{index} = {case!r}",
                    f"result_{index} = sort_array(input_{index})",
                    f"assert result_{index} == {expected!r}",
                    f"assert input_{index} == before_{index}",
                )
            )
        source_path = ROOT / f"k-diff-batch-{batches:02d}.py"
        mpy_path = ROOT / f"k-diff-batch-{batches:02d}.mpy"
        source_path.write_text(
            solution_source + "\n" + "\n".join(statements) + "\n",
            encoding="utf-8",
        )
        translated = subprocess.run(
            ["python3", "py2mpy.py", source_path.name],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        mpy_path.write_text(translated.stdout, encoding="utf-8")
        concrete = subprocess.run(
            [
                "krun",
                mpy_path.name,
                "--definition",
                "fresh-runtime-kompiled",
                "--output",
                "none",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if concrete.returncode != 0:
            print(
                f"BATCH_FAILURE batch={batches} exit={concrete.returncode}\n"
                f"{concrete.stdout}{concrete.stderr}"
            )
            raise SystemExit(concrete.returncode)
        batches += 1

    digest = hashlib.sha256(
        json.dumps(cases, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "K_DIFFERENTIAL_RESULT PASS "
        f"cases={len(cases)} batches={batches} "
        f"case_sha256={digest} mismatches=0"
    )


if __name__ == "__main__":
    main()
