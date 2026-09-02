#!/usr/bin/env python3
"""Independent CPython differential: trusted canonical versus generated entry point."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[str, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fruit_distribution


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/candidate/solution.py"), "generated_solution")

cases: list[tuple[str, int, str, str]] = [
    ("5 apples and 6 oranges", 19, "prompt-example", "in"),
    ("0 apples and 1 oranges", 3, "prompt-example", "in"),
    ("2 apples and 3 oranges", 100, "prompt-example", "in"),
    ("100 apples and 1 oranges", 120, "prompt-example", "in"),
    ("0 apples and 0 oranges", 0, "zero-and-equality-boundary", "in"),
    ("1 apples and 0 oranges", 1, "zero-orange-boundary", "in"),
    ("0 apples and 1 oranges", 1, "zero-apple-boundary", "in"),
    ("999999999999999999999999 apples and 1 oranges", 10**24, "unbounded-int-boundary", "in"),
    ("  7   apples\tand  8 oranges\n", 20, "whitespace-boundary", "in"),
    ("٠ apples and ١ oranges", 3, "unicode-decimal-digit", "in"),
    ("", 5, "empty-string-probe", "out"),
    ("5 apples and oranges", 10, "missing-number-probe", "out"),
    ("There are 5 apples and 6 oranges", 20, "free-prose-probe", "out"),
    ("-1 apples and 2 oranges", 5, "negative-count-probe", "out"),
    ("5 apples and 6 oranges and 2 pears", 20, "extra-number-probe", "out"),
    ("5 apples and 6 oranges", 3, "inconsistent-total-probe", "out"),
]

for apples in [0, 1, 9, 10, 99, 100, 10**6]:
    for oranges in [0, 1, 9, 10, 99, 100, 10**6]:
        for mangoes in [0, 1, 17]:
            cases.append(
                (
                    f"{apples} apples and {oranges} oranges",
                    apples + oranges + mangoes,
                    "generated-valid-grid",
                    "in",
                )
            )


def outcome(function: Callable[[str, int], int], text: str, total: int) -> tuple[str, Any]:
    try:
        return ("value", function(text, total))
    except Exception as error:  # Deliberately compare exception classes for probes.
        return ("exception", type(error).__name__)


in_domain_mismatches = 0
out_domain_divergences = 0
for index, (text, total, label, domain) in enumerate(cases):
    trusted = outcome(canonical, text, total)
    submitted = outcome(generated, text, total)
    same = trusted == submitted
    if domain == "in" and not same:
        in_domain_mismatches += 1
    if domain == "out" and not same:
        out_domain_divergences += 1
    if label != "generated-valid-grid" or not same:
        print(
            f"case={index} domain={domain} label={label} "
            f"text={text!r} total={total} canonical={trusted!r} "
            f"generated={submitted!r} same={same}"
        )

print(
    f"cases={len(cases)} in_domain_mismatches={in_domain_mismatches} "
    f"out_domain_divergences={out_domain_divergences}"
)
raise SystemExit(1 if in_domain_mismatches else 0)
