#!/usr/bin/env python3
"""Expose the generated exact-Rat semantics / CPython-float divergence."""

from __future__ import annotations

import importlib.util
import math
import shlex
import subprocess
from pathlib import Path
from typing import Callable


def load(path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def main() -> int:
    values = [-1.0e308, 1.0e308]
    canonical_result = load(Path("/reference/canonical.py"))(values.copy())
    submitted_result = load(Path("/candidate/solution.py"))(values.copy())
    print(f"finite_input={values!r}")
    print(f"canonical_python={canonical_result!r}")
    print(f"submitted_python={submitted_result!r}")
    print(f"python_second_is_nan={math.isnan(submitted_result[1])}")

    magnitude = "1" + "0" * 308
    k_argument = f"vlist(-{magnitude}, {magnitude})"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "semantic-kompiled",
        f"-cARGS={k_argument}",
        "--output",
        "pretty",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    result = subprocess.run(
        command,
        cwd="/tmp/audit-work/21-rescale-to-unit-audit",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout)
    print(f"KRUN_EXIT_STATUS: {result.returncode}")
    k_returns_zero_one = "vlist ( 0 , 1 , .Rats )" in result.stdout
    print(f"k_returns_exact_zero_one={k_returns_zero_one}")
    python_implementations_agree = (
        len(canonical_result) == len(submitted_result) == 2
        and canonical_result[0] == submitted_result[0] == 0.0
        and math.isnan(canonical_result[1])
        and math.isnan(submitted_result[1])
    )
    print(f"python_implementations_agree={python_implementations_agree}")
    divergence_exposed = (
        python_implementations_agree
        and result.returncode == 0
        and k_returns_zero_one
    )
    print(f"semantic_divergence_exposed={divergence_exposed}")
    return 0 if divergence_exposed else 1


if __name__ == "__main__":
    raise SystemExit(main())
