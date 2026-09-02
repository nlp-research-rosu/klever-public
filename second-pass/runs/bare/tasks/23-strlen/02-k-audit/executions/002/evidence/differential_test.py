#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


TRUSTED = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/23-strlen.30KKVy/work/solution.py")
SEED = 230023


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strlen


def main() -> None:
    canonical = load_entry("trusted_canonical_strlen", TRUSTED)
    generated = load_entry("generated_solution_strlen", GENERATED)
    fixed = [
        "",
        "a",
        "abc",
        " ",
        "\x00",
        "\n",
        "\"'\\",
        "é",
        "e\u0301",
        "😀",
        "a😀é",
        "👩\u200d💻",
        "\ud800",
        "a" * 4096,
    ]
    alphabet = [
        "a",
        "Z",
        "0",
        " ",
        "\x00",
        "\n",
        "é",
        "\u0301",
        "😀",
        "\u200d",
    ]
    rng = random.Random(SEED)
    generated_cases = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 129)))
        for _ in range(500)
    ]
    cases = fixed + generated_cases
    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical(value)
        actual = generated(value)
        if expected != actual:
            mismatches.append((index, repr(value), expected, actual))
    print(f"seed={SEED}")
    print(f"fixed_cases={len(fixed)} generated_cases={len(generated_cases)}")
    print(f"total_cases={len(cases)} mismatches={len(mismatches)}")
    for index, value in enumerate(fixed):
        print(
            f"fixed[{index}]={value!r} "
            f"canonical={canonical(value)} generated={generated(value)}"
        )
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    raise SystemExit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
