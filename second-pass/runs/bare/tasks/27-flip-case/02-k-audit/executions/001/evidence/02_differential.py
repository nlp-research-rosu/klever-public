#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for flip_case."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import random
import sys


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


parser = argparse.ArgumentParser()
parser.add_argument("--canonical", type=Path, required=True)
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--inputs-out", type=Path, required=True)
args = parser.parse_args()

canonical = load_function(args.canonical, "audit_canonical")
candidate = load_function(args.candidate, "audit_candidate")

# These cover the documented example, empty input, ASCII classification
# boundaries, uncased characters, multi-code-point expansions, and the
# 1/2/3/4-byte UTF-8 regions used by the K semantics.
explicit_cases = [
    ("documented", "Hello", "hELLO"),
    ("empty", "", ""),
    ("ascii-lower-boundaries", "`az{", "`AZ{"),
    ("ascii-upper-boundaries", "@AZ[", "@az["),
    ("uncased-ascii", "019 !?_", "019 !?_"),
    ("mixed", "aBc XYZ", "AbC xyz"),
    ("expansion-and-greek", "Straße Δelta", "sTRASSE δELTA"),
    ("unicode-expansions", "ßİŉﬃ", "SSi\u0307ʼNFFI"),
    ("two-byte-region", "\u0080µ\u07ff", "\u0080Μ\u07ff"),
    ("three-byte-region", "\u0800Δ\uffff", "\u0800δ\uffff"),
    ("four-byte-region", "\U00010000\U00010400\U0010ffff",
     "\U00010000\U00010428\U0010ffff"),
    ("combining", "A\u0301z", "a\u0301Z"),
    ("embedded-nul", "\x00Aa\x00", "\x00aA\x00"),
    ("lone-surrogates", "\ud800A\udfffz", "\ud800a\udfffZ"),
]

mismatches: list[str] = []
for name, value, expected in explicit_cases:
    oracle = canonical(value)
    actual = candidate(value)
    print(
        f"explicit name={name} input={value!r} "
        f"canonical={oracle!r} candidate={actual!r} expected={expected!r}"
    )
    if oracle != expected or actual != expected:
        mismatches.append(name)

# Exhaust every possible one-code-point Python str, including lone surrogates.
one_char_checked = 0
for codepoint in range(sys.maxunicode + 1):
    value = chr(codepoint)
    oracle = canonical(value)
    actual = candidate(value)
    one_char_checked += 1
    if oracle != actual:
        mismatches.append(f"U+{codepoint:04X}")
        if len(mismatches) >= 20:
            break
print(f"all_single_codepoints_checked={one_char_checked}")

# Reproducible broader strings. The exact generated inputs are preserved.
seed = 270027
sample_count = 5000
max_length = 40
rng = random.Random(seed)
args.inputs_out.parent.mkdir(parents=True, exist_ok=True)
with args.inputs_out.open("w", encoding="utf-8") as output:
    for index in range(sample_count):
        length = rng.randrange(max_length + 1)
        value = "".join(chr(rng.randrange(sys.maxunicode + 1)) for _ in range(length))
        output.write(json.dumps({"index": index, "input": value}, ensure_ascii=True))
        output.write("\n")
        oracle = canonical(value)
        actual = candidate(value)
        if oracle != actual:
            mismatches.append(f"generated-{index}")
            if len(mismatches) >= 20:
                break

print(f"generated_seed={seed}")
print(f"generated_sample_count={sample_count}")
print(f"generated_max_length={max_length}")
print(f"generated_inputs_file={args.inputs_out}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
    raise SystemExit(1)
