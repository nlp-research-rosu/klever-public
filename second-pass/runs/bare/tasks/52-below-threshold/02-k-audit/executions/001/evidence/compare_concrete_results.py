#!/usr/bin/env python3
"""Compare reviewer krun result cells with both independent Python functions."""

from __future__ import annotations

import importlib.util
import pathlib
import re
import sys


CASES = [
    ("stage3-krun-prompt-true.log", [1, 2, 4, 10], 100),
    ("stage3-krun-prompt-false.log", [1, 20, 4, 10], 5),
    ("stage3-krun-empty.log", [], -100),
    ("stage3-krun-equality.log", [5], 5),
    ("stage3-krun-negative-true.log", [-5, -4, -3], -2),
]


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} EVIDENCE_DIR TRUSTED_CANONICAL.py GENERATED.py",
            file=sys.stderr,
        )
        return 64
    evidence_dir = pathlib.Path(sys.argv[1])
    canonical = load(pathlib.Path(sys.argv[2]), "audit_compare_canonical")
    generated = load(pathlib.Path(sys.argv[3]), "audit_compare_generated")
    mismatches = 0
    for log_name, values, threshold in CASES:
        log_text = (evidence_dir / log_name).read_text(encoding="utf-8")
        matches = re.findall(
            r"<result>\s*result\s*\(\s*(true|false)\s*\)\s*</result>",
            log_text,
            flags=re.DOTALL,
        )
        if len(matches) != 1:
            print(f"{log_name}: expected one final result cell, found {matches!r}")
            mismatches += 1
            continue
        krun_result = matches[0] == "true"
        canonical_result = canonical(list(values), threshold)
        generated_result = generated(list(values), threshold)
        expected = all(value < threshold for value in values)
        good = krun_result == canonical_result == generated_result == expected
        print(
            f"{log_name}: l={values!r}, t={threshold}, krun={krun_result}, "
            f"canonical={canonical_result}, generated={generated_result}, "
            f"mathematical={expected}, ok={good}"
        )
        if not good:
            mismatches += 1
    print(f"mismatches: {mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
