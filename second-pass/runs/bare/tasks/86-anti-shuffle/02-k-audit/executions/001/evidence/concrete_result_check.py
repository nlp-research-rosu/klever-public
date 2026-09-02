#!/usr/bin/env python3
"""Compare preserved fresh-krun results with both Python implementations."""

import importlib.util
import ast
import re
import sys
from pathlib import Path


CASES = {
    "empty": "",
    "one-space": " ",
    "hi": "Hi",
    "ba": "ba",
    "aa": "aa",
    "prompt": "Hello World!!!",
    "repeated-spaces": "  ba  dc ",
    "mixed": "zA9! 0b?",
    "unicode-single": "Ω",
    "unicode-bmp": "éa Ωβ",
    "unicode-emoji": "🙂a 🙂!",
}


def load_entry(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def krun_result(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<result>\s*(\"(?:[^\"\\]|\\.)*\")\s*</result>", text)
    if match is None:
        raise RuntimeError(f"no ground String <result> in {path}")
    return ast.literal_eval(match.group(1))


def main():
    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_entry(
        "generated_solution", Path("/tmp/audit-work/reconstruction/solution.py")
    )
    mismatches = 0
    for name, source in CASES.items():
        log = Path(f"/audit-output/evidence/krun-{name}.log")
        k_value = krun_result(log)
        canonical_value = canonical(source)
        generated_value = generated(source)
        ok = k_value == canonical_value == generated_value
        print(
            f"{name}: input={source!r} K={k_value!r} "
            f"canonical={canonical_value!r} generated={generated_value!r} "
            f"match={ok}"
        )
        mismatches += not ok
    print(f"mismatch_count={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
