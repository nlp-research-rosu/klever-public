#!/usr/bin/env python3
"""Concrete satisfying substitutions for all three submitted claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(
    "ground_canonical",
    "/tmp/audit-work/50-decode-shift/trusted-src/canonical.py",
)
candidate = load(
    "ground_candidate",
    "/tmp/audit-work/50-decode-shift/candidate-src/solution.py",
)


def codes(value: str) -> list[int]:
    return [ord(character) for character in value]


def lower_codes(values: list[int]) -> bool:
    return all(97 <= value <= 122 for value in values)


def decode_char(code: int) -> int:
    return ((code - 5 - 97) % 26) + 97


def encode_char(code: int) -> int:
    return ((code + 5 - 97) % 26) + 97


encoded = "mjqqt"
cs = codes(encoded)
decoded_codes = [decode_char(code) for code in cs]
summary_string = "".join(chr(code) for code in decoded_codes)
accumulator = "pre:"

witnesses = {
    "decode-loop": {
        "CS": cs,
        "ACC": codes(accumulator),
        "CH": {"K": "str(.IntSeq)", "Python_analogue": ""},
        "ORIGINAL": cs,
        "precondition_lowerCodes_CS": lower_codes(cs),
        "claimed_result_codes": codes(accumulator) + decoded_codes,
        "claimed_result_string": accumulator + summary_string,
        "claimed_final_ch": "t",
    },
    "decode-shift": {
        "CS": cs,
        "precondition_lowerCodes_CS": lower_codes(cs),
        "K_decodeCodes_as_string": summary_string,
        "canonical": canonical.decode_shift(encoded),
        "candidate": candidate.decode_shift(encoded),
    },
    "char-inverse": {
        "C": ord("h"),
        "precondition_97_le_C_le_122": 97 <= ord("h") <= 122,
        "encodeChar_C": encode_char(ord("h")),
        "decodeChar_encodeChar_C": decode_char(encode_char(ord("h"))),
        "canonical_encode_h": canonical.encode_shift("h"),
        "canonical_decode_encoded": canonical.decode_shift(
            canonical.encode_shift("h")
        ),
        "candidate_decode_encoded": candidate.decode_shift(
            canonical.encode_shift("h")
        ),
    },
}
print(json.dumps(witnesses, indent=2, sort_keys=True))

assert witnesses["decode-shift"]["K_decodeCodes_as_string"] == "hello"
assert witnesses["decode-shift"]["canonical"] == "hello"
assert witnesses["decode-shift"]["candidate"] == "hello"
assert witnesses["char-inverse"]["decodeChar_encodeChar_C"] == ord("h")
assert witnesses["char-inverse"]["canonical_decode_encoded"] == "h"
assert witnesses["char-inverse"]["candidate_decode_encoded"] == "h"
