#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and submitted solution.py."""

from __future__ import annotations

import importlib.util
import json
import random
import string
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_expected(encoded: str) -> str:
    """Direct per-block inverse rotation; independent of both implementations."""
    return "".join(
        block[-1:] + block[:-1] if len(block) == 3 else block
        for start in range(0, len(encoded), 3)
        for block in [encoded[start : start + 3]]
    )


def main() -> int:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_module("submitted_solution", Path("/candidate/solution.py"))

    fixed = [
        "",
        "a",
        "ab",
        "abc",
        "abcd",
        "abcde",
        "abcdef",
        "abcdefg",
        "abcdefgh",
        "abcdefghi",
        "bca",
        "bcaefd",
        "bcaefdg",
        "elho lorwld",
        "\x00",
        "\x00\x01",
        "\x00\x01\x02",
        "é🙂𝄞",
        "é🙂𝄞x",
        "\ud800\udfffz",
        "\n\t ",
    ]
    # Every branch/group boundary for 0..36, all residue classes modulo 3.
    alphabet = "abC09_ -é🙂"
    fixed.extend("".join(alphabet[i % len(alphabet)] for i in range(n)) for n in range(37))

    rng = random.Random(0x38DEC0DE)
    random_cases = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 301)))
        for _ in range(5000)
    ]
    cases = fixed + random_cases

    mismatches: list[dict[str, object]] = []
    encode_roundtrip_mismatches: list[dict[str, object]] = []
    for index, encoded in enumerate(cases):
        expected = independent_expected(encoded)
        canonical_value = canonical.decode_cyclic(encoded)
        generated_value = generated.decode_cyclic(encoded)
        if not (expected == canonical_value == generated_value):
            mismatches.append(
                {
                    "index": index,
                    "input_repr": repr(encoded),
                    "oracle_repr": repr(expected),
                    "canonical_repr": repr(canonical_value),
                    "generated_repr": repr(generated_value),
                }
            )

        raw = encoded
        canonical_encoded = canonical.encode_cyclic(raw)
        generated_encoded = generated.encode_cyclic(raw)
        canonical_roundtrip = canonical.decode_cyclic(canonical_encoded)
        generated_roundtrip = generated.decode_cyclic(generated_encoded)
        if not (
            canonical_encoded == generated_encoded
            and canonical_roundtrip == raw
            and generated_roundtrip == raw
        ):
            encode_roundtrip_mismatches.append(
                {
                    "index": index,
                    "raw_repr": repr(raw),
                    "canonical_encoded_repr": repr(canonical_encoded),
                    "generated_encoded_repr": repr(generated_encoded),
                    "canonical_roundtrip_repr": repr(canonical_roundtrip),
                    "generated_roundtrip_repr": repr(generated_roundtrip),
                }
            )

    summary = {
        "python": sys.version.split()[0],
        "seed": "0x38DEC0DE",
        "fixed_cases": len(fixed),
        "random_cases": len(random_cases),
        "total_cases": len(cases),
        "length_range": [min(map(len, cases)), max(map(len, cases))],
        "alphabet_repr": repr(alphabet),
        "decode_mismatches": len(mismatches),
        "encode_roundtrip_mismatches": len(encode_roundtrip_mismatches),
        "first_decode_mismatches": mismatches[:10],
        "first_roundtrip_mismatches": encode_roundtrip_mismatches[:10],
    }
    print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
    return 1 if mismatches or encode_roundtrip_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
