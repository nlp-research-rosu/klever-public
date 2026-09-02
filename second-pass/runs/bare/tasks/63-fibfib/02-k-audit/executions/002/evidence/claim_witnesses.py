#!/usr/bin/env python3
"""Concrete satisfying states and substitutions for both reachability claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/63-fibfib")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


def recurrence(n: int) -> int:
    values = [0, 0, 1]
    for index in range(3, n + 3):
        values.append(values[index - 1] + values[index - 2] + values[index - 3])
    return values[n]


def main() -> None:
    canonical = load(ROOT / "reference" / "canonical.py", "witness_canonical")
    generated = load(ROOT / "candidate" / "solution.py", "witness_generated")

    for n in (0, 2, 5, 8):
        claimed = recurrence(n)
        can = canonical(n)
        gen = generated(n)
        print(
            f"ENTRY_WITNESS N={n} precondition={0 <= n} "
            f"claimed_result={claimed} canonical={can} generated={gen}"
        )
        assert claimed == can == gen

    i, n = 0, 5
    initial = {
        "a": recurrence(i),
        "b": recurrence(i + 1),
        "c": recurrence(i + 2),
        "i": i,
        "n": n,
    }
    final = {
        "a": recurrence(n),
        "b": recurrence(n + 1),
        "c": recurrence(n + 2),
        "i": n,
        "n": n,
    }
    print(
        f"LOOP_WITNESS I={i} N={n} precondition={0 <= i <= n} "
        f"initial={initial} final={final} claimed_result={recurrence(n)}"
    )
    assert recurrence(n) == canonical(n) == generated(n)
    print("WITNESS_CHECK_PASS")


if __name__ == "__main__":
    main()
