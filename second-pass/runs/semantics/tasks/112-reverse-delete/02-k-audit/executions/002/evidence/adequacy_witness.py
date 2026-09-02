#!/usr/bin/env python3
"""Ground witnesses for the entry and loop claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def kept_acc(source: list[int], deleted: list[int], accumulator: list[int]):
    return accumulator + [char for char in source if char not in deleted]


def reversed_kept_acc(
    source: list[int], deleted: list[int], accumulator: list[int]
):
    result = list(accumulator)
    for char in source:
        if char not in deleted:
            result = [char] + result
    return result


def main() -> int:
    canonical = load(SCRATCH / "canonical.py", "witness_canonical")
    generated = load(SCRATCH / "solution.py", "witness_generated")

    for source, deleted in [("ab", ""), ("abcde", "ae"), ("abba", "")]:
        s_codes = [ord(char) for char in source]
        c_codes = [ord(char) for char in deleted]
        forward = kept_acc(s_codes, c_codes, [])
        reverse = reversed_kept_acc(s_codes, c_codes, [])
        claimed = ("".join(map(chr, forward)), forward == reverse)
        expected = canonical(source, deleted)
        actual = generated(source, deleted)
        print(
            repr(
                {
                    "s": source,
                    "c": deleted,
                    "S_IntSeq": s_codes,
                    "C_IntSeq": c_codes,
                    "keptAcc": forward,
                    "reversedKeptAcc": reverse,
                    "claimed": claimed,
                    "canonical": expected,
                    "generated": actual,
                }
            )
        )
        if claimed != expected or actual != expected:
            return 1

    print(
        "loop_precondition_witness="
        "L=1, S=ORIG=[97,98], C=[], A=[], RA=[], "
        "V=str([]), P=parent(0), with scope 1 containing the five bindings"
    )
    print(
        "entry_precondition_witness="
        "S=[97,98], C=[], initial env/scopes/heap/stack/ret/exc exactly as SPEC"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
