#!/usr/bin/env python3
"""Compare CPython and generated K semantics above CPython's digit limit."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("long_input_solution", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def main() -> int:
    root = Path("/tmp/audit-work/reconstruction")
    simplify = load_entry(root / "solution.py")
    numerator = "1" + ("0" * 4_999)
    x = numerator + "/1"
    n = "1/1"
    print(f"python_version={sys.version.split()[0]}")
    print(f"default_max_str_digits={sys.int_info.default_max_str_digits}")
    print(f"numerator_digits={len(numerator)}")
    print(f"input_sha256={hashlib.sha256((x + '|' + n).encode()).hexdigest()}")

    try:
        python_outcome = ("value", simplify(x, n))
    except Exception as error:
        python_outcome = ("exception", type(error).__name__, str(error))
    print(f"python_outcome={python_outcome!r}")

    args = f'strVal("{x}"),strVal("{n}")'
    process = subprocess.run(
        [
            "krun",
            "solution.mpy",
            f"-cARGS={args}",
            "--definition",
            "audit-semantic-kompiled",
        ],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    matches = re.findall(
        r"result\s*\(\s*boolVal\s*\(\s*(true|false)\s*\)\s*\)",
        process.stdout,
    )
    print(f"krun_exit={process.returncode}")
    print(f"krun_boolean_results={matches!r}")
    result_index = process.stdout.rfind("<result>")
    if result_index >= 0:
        result_fragment = process.stdout[result_index : result_index + 180]
        print(f"krun_result_fragment={result_fragment!r}")
    k_start = process.stdout.find("<k>")
    k_end = process.stdout.find("</k>", k_start)
    if k_start >= 0 and k_end >= 0:
        k_fragment = process.stdout[k_start : k_end + 4]
        k_fragment = re.sub(r'"[0-9]{100,}/1"', '"<LONG-DIGITS>/1"', k_fragment)
        print(f"krun_k_fragment={k_fragment[:600]!r}")
    if process.stderr:
        print(f"krun_stderr={process.stderr.strip()!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
