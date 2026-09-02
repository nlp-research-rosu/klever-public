#!/usr/bin/env python3
"""Ground witnesses for the entry claim and loop claim preconditions."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
VOWELS = "aeiouAEIOU"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def contract(text: str) -> int:
    return sum(char in VOWELS for char in text) + int(
        bool(text) and text[-1] in "yY"
    )


def int_seq(text: str) -> str:
    term = ".IntSeq"
    for code in reversed([ord(char) for char in text]):
        term = f"iCons({code}, {term})"
    return term


def main() -> int:
    canonical = load_entry(ROOT / "canonical.py", "witness_canonical")
    generated = load_entry(ROOT / "solution.py", "witness_generated")

    entry_text = "abcde"
    entry_expected = contract(entry_text)
    entry_can = canonical(entry_text)
    entry_gen = generated(entry_text)
    print("ENTRY_WITNESS")
    print("INPUT=", int_seq(entry_text), sep="")
    print("env=0")
    print('scopes=0|->scope(.Map,parent(-1)) -1|->builtinsScope')
    print("scopeLoc=1 heap=.Map heapLoc=0 stack=.List ret=noRet exc=NoExc exit=0")
    print("claimed_vowelsTail=", entry_expected, sep="")
    print("canonical=", entry_can, sep="")
    print("generated=", entry_gen, sep="")

    loop_original = "abcde"
    loop_remaining = "bcde"
    loop_count = 1
    loop_last = "a"
    loop_expected = loop_count + contract(loop_remaining)
    print("LOOP_WITNESS")
    print("CS=", int_seq(loop_remaining), sep="")
    print("COUNT=1")
    print("LAST=", int_seq(loop_last), sep="")
    print("ORIGINAL=", int_seq(loop_original), sep="")
    print('CHAR=str(iCons(97,.IntSeq)) CALLER=0 CONT=.K CALLSTACK=.List')
    print("scopeLoc=2 heap=.Map heapLoc=0 ret=noRet exc=NoExc exit=0")
    print("claimed_final=", loop_expected, sep="")
    print("canonical_final=", canonical(loop_original), sep="")
    print("generated_final=", generated(loop_original), sep="")

    second = "ACEDY"
    print("SECOND_GROUND_INPUT=", repr(second), sep="")
    print("second_contract=", contract(second), sep="")
    print("second_canonical=", canonical(second), sep="")
    print("second_generated=", generated(second), sep="")

    ok = (
        entry_expected == entry_can == entry_gen
        and loop_expected == canonical(loop_original) == generated(loop_original)
        and contract(second) == canonical(second) == generated(second)
    )
    print("all_ground_equalities=", ok, sep="")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
