#!/usr/bin/env python3
"""Independent contract/canonical differential for HumanEval 162."""

from __future__ import annotations

import hashlib
import importlib.util
import random
import string
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_to_md5


def openssl_md5_utf8(text: str) -> str:
    completed = subprocess.run(
        ["openssl", "dgst", "-md5"],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout.decode("ascii").rsplit("=", 1)[1].strip()


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("submitted_solution", Path("/candidate/solution.py"))

explicit_cases = [
    "",
    "Hello world",
    "a",
    "b",
    "0",
    " ",
    "\n",
    "\t",
    "\0",
    "abc",
    "message digest",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "1234567890" * 8,
    "x" * 55,
    "x" * 56,
    "x" * 63,
    "x" * 64,
    "x" * 65,
    "x" * 255,
    "x" * 256,
    "π",
    "é",
    "e\u0301",
    "漢字",
    "🙂",
    "aπ🙂z",
]

rng = random.Random(162_20260730)
ascii_alphabet = string.ascii_letters + string.digits + string.punctuation + " \n\t"
ascii_cases = [
    "".join(rng.choice(ascii_alphabet) for _ in range(rng.randrange(0, 513)))
    for _ in range(250)
]
unicode_alphabet = ascii_alphabet + "πé漢字🙂"
unicode_cases = [
    "".join(rng.choice(unicode_alphabet) for _ in range(rng.randrange(1, 129)))
    for _ in range(100)
]

cases = explicit_cases + ascii_cases + unicode_cases
generated_contract_failures = []
canonical_ascii_mismatches = []
canonical_unicode_observations = []

for index, text in enumerate(cases):
    contract_expected = None if text == "" else openssl_md5_utf8(text)
    actual = generated(text)
    if actual != contract_expected:
        generated_contract_failures.append((index, repr(text), contract_expected, actual))

    try:
        canonical_result = canonical(text)
    except Exception as error:  # Deliberately records the canonical witness's boundary.
        canonical_unicode_observations.append(
            (index, repr(text), type(error).__name__, str(error))
        )
    else:
        if canonical_result != actual:
            if text.isascii():
                canonical_ascii_mismatches.append(
                    (index, repr(text), canonical_result, actual)
                )
            else:
                canonical_unicode_observations.append(
                    (index, repr(text), canonical_result, actual)
                )

print("COMMAND: python3 /audit-output/evidence/stage2_differential.py")
print(f"TOTAL_CASES={len(cases)}")
print(f"EXPLICIT_CASES={len(explicit_cases)}")
print(f"SEEDED_ASCII_CASES={len(ascii_cases)}")
print(f"SEEDED_UNICODE_CASES={len(unicode_cases)}")
print(f"GENERATED_CONTRACT_FAILURES={len(generated_contract_failures)}")
print(f"CANONICAL_ASCII_MISMATCHES={len(canonical_ascii_mismatches)}")
print(f"CANONICAL_UNICODE_OBSERVATIONS={len(canonical_unicode_observations)}")
print(f"EMPTY_RESULT={generated('')!r}")
print(f"ONE_CHAR_RESULT={generated('a')}")
print(f"PROMPT_EXAMPLE_RESULT={generated('Hello world')}")
print(f"PROMPT_EXAMPLE_EXPECTED=3e25960a79dbc69b674cd4ec67a72c62")
print(f"UNICODE_PI_RESULT={generated('π')}")
print(f"UNICODE_PI_CODEPOINTS={[ord(character) for character in 'π']}")
print(f"UNICODE_PI_UTF8={list('π'.encode('utf-8'))}")
print(f"UNICODE_PI_CANONICAL_OBSERVATION={canonical_unicode_observations[:1]}")
print(
    "CASE_CORPUS_SHA256="
    + hashlib.sha256(
        "\0".join(cases).encode("utf-8")
    ).hexdigest()
)

if generated_contract_failures:
    print("FIRST_GENERATED_FAILURES=" + repr(generated_contract_failures[:5]))
if canonical_ascii_mismatches:
    print("FIRST_CANONICAL_ASCII_MISMATCHES=" + repr(canonical_ascii_mismatches[:5]))

assert generated("") is None
assert generated("Hello world") == "3e25960a79dbc69b674cd4ec67a72c62"
assert not generated_contract_failures
assert not canonical_ascii_mismatches
