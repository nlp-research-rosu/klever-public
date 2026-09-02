#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval/23 strlen."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strlen


parser = argparse.ArgumentParser()
parser.add_argument("canonical")
parser.add_argument("generated")
parser.add_argument("input_manifest")
args = parser.parse_args()

canonical = load_entry(Path(args.canonical), "trusted_canonical")
generated = load_entry(Path(args.generated), "generated_solution")

named_cases = [
    ("example-empty", ""),
    ("example-abc", "abc"),
    ("one-ascii", "a"),
    ("two-ascii", "ab"),
    ("spaces", " \t\n"),
    ("embedded-nul", "a\x00b"),
    ("combining-sequence", "e\u0301"),
    ("precomposed", "\u00e9"),
    ("bmp-boundaries", "\u0000\ud7ff\ue000\uffff"),
    ("astral", "\U0001f642"),
    ("astral-pair", "\U0001f642\U0001f680"),
    ("explicit-surrogates", "\ud800\udfff"),
    ("long-empty-like-boundary", "x" * 4096),
]

# Exhaust all strings through length 5 over a small alphabet that spans ASCII,
# NUL, combining, BMP, and astral characters.
alphabet = ["a", "\x00", "\u0301", "\u03bb", "\U0001f642"]
exhaustive_cases = [
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(alphabet, repeat=length)
]

# Deterministic broader generated coverage, including valid scalar values and
# explicit surrogate code points (which CPython str values can contain).
seed = 230023
rng = random.Random(seed)
codepoint_pool = [
    0,
    1,
    9,
    10,
    32,
    65,
    127,
    128,
    0x300,
    0x7FF,
    0x800,
    0xD7FF,
    0xD800,
    0xDFFF,
    0xE000,
    0xFFFF,
    0x10000,
    0x10FFFF,
]
random_cases = [
    "".join(chr(rng.choice(codepoint_pool)) for _ in range(rng.randrange(0, 129)))
    for _ in range(1000)
]

all_cases = [value for _, value in named_cases] + exhaustive_cases + random_cases
manifest = {
    "seed": seed,
    "named_cases": [{"name": name, "codepoints": [ord(ch) for ch in value]} for name, value in named_cases],
    "exhaustive_alphabet_codepoints": [ord(ch) for ch in alphabet],
    "exhaustive_max_length": 5,
    "exhaustive_cases": [[ord(ch) for ch in value] for value in exhaustive_cases],
    "random_codepoint_pool": codepoint_pool,
    "random_case_count": len(random_cases),
    "random_max_length_exclusive": 129,
    "random_cases": [[ord(ch) for ch in value] for value in random_cases],
}
manifest_path = Path(args.input_manifest)
with manifest_path.open("w", encoding="utf-8") as stream:
    json.dump(manifest, stream, sort_keys=True, separators=(",", ":"))
    stream.write("\n")

mismatches = []
for index, value in enumerate(all_cases):
    expected = canonical(value)
    actual = generated(value)
    if actual != expected:
        mismatches.append(
            {
                "index": index,
                "codepoints": [ord(ch) for ch in value],
                "canonical": expected,
                "generated": actual,
            }
        )

manifest_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
print(f"canonical={Path(args.canonical)}")
print(f"generated={Path(args.generated)}")
print("implementation_branch_boundaries=none (single return expression)")
print(f"named_cases={len(named_cases)}")
print(f"exhaustive_cases={len(exhaustive_cases)} alphabet_size={len(alphabet)} max_length=5")
print(f"random_cases={len(random_cases)} seed={seed} lengths=0..128")
print(f"total_cases={len(all_cases)}")
print(f"input_manifest={manifest_path}")
print(f"input_manifest_sha256={manifest_digest}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=True, sort_keys=True))
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
