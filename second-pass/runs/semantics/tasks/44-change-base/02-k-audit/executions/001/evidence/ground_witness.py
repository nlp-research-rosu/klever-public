#!/usr/bin/env python3
"""Concrete satisfying states and result substitution for both entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def mathematical_digits(x: int, base: int) -> str:
    if x == 0:
        return ""
    quotient, remainder = divmod(x, base)
    return mathematical_digits(quotient, base) + chr(48 + remainder)


def main() -> int:
    x, base = 8, 3
    direct_state = {
        "X": x,
        "B": base,
        "env": 0,
        "FRAMES": ".Map",
        "scopeLoc_N": 1,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": ".List",
        "ret": "noRet",
        "exc": "NoExc",
        "exit_code": 0,
    }
    load_state = {
        "X": x,
        "B": base,
        "env": 0,
        "scopes": (
            "0 |-> scope(.Map,parent(-1)) "
            "-1 |-> builtinsScope"
        ),
        "scopeLoc": 1,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": ".List",
        "ret": "noRet",
        "exc": "NoExc",
        "exit_code": 0,
    }
    precondition = (
        x >= 0
        and base >= 2
        and base < 10
        and direct_state["scopeLoc_N"] > 0
        and direct_state["FRAMES"] == ".Map"
    )
    canonical = load(Path("/reference/canonical.py"), "ground_canonical")
    generated = load(
        Path("/tmp/audit-work/reconstruction/solution.py"), "ground_generated"
    )
    summary = mathematical_digits(x, base)
    canonical_result = canonical(x, base)
    generated_result = generated(x, base)

    print(f"DIRECT_STATE={direct_state}")
    print(f"LOAD_STATE={load_state}")
    print(f"PRECONDITIONS_SATISFIED={precondition}")
    print(f"FORMAL_SUMMARY_baseDigits_as_text={summary!r}")
    print(f"TRUSTED_CANONICAL={canonical_result!r}")
    print(f"GENERATED_PYTHON={generated_result!r}")
    print(
        "ALL_RESULTS_EQUAL="
        f"{summary == canonical_result == generated_result}"
    )
    return 0 if precondition and summary == canonical_result == generated_result else 1


if __name__ == "__main__":
    raise SystemExit(main())
