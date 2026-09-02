#!/usr/bin/env python3
"""Probe CPython's decimal-conversion limit versus the generated K semantics."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.circular_shift


def call_summary(function, x: int) -> tuple[str, str]:
    try:
        value = function(x, 0)
    except Exception as error:  # This probe records the exact runtime outcome.
        return type(error).__name__, str(error)
    return "RETURN", f"length={len(value)}"


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: stage5_large_int_boundary.py SCRATCH_DIRECTORY DEFINITION"
        )
    root = Path(sys.argv[1])
    definition = Path(sys.argv[2])
    candidate = load(root / "solution.py", "large_candidate")
    canonical = load(root / "trusted-canonical.py", "large_canonical")

    maximum = sys.get_int_max_str_digits()
    # 10**maximum has maximum+1 decimal digits and crosses the default limit.
    x = 10**maximum
    print("sys_get_int_max_str_digits", maximum)
    print("decimal_digit_count_mathematical", maximum + 1)
    print("candidate_python", call_summary(candidate, x))
    print("canonical_python", call_summary(canonical, x))

    # Disable only for serialization of the already-tested integer into the K
    # command line; the two Python program calls above ran with the recorded
    # default limit.
    sys.set_int_max_str_digits(0)
    command = [
        "krun",
        str(root / "solution.mpy"),
        "--definition",
        str(definition),
        "-cENTRY=\"circular_shift\"",
        f"-cARGS=VInt({x}), VInt(0)",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    output = completed.stdout + completed.stderr
    match = re.search(
        r"<result>\s*VString\s*\(\s*\"([0-9-]*)\"\s*\)\s*</result>",
        output,
        re.DOTALL,
    )
    print("k_exit", completed.returncode)
    print("k_returned_string", match is not None)
    print("k_result_length", None if match is None else len(match.group(1)))
    if completed.returncode != 0 or match is None:
        print("bounded_k_output", "\n".join(output.splitlines()[:30]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
