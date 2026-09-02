#!/usr/bin/env python3
"""Mutate the encoded sort_even body while leaving its reference result unchanged."""

from __future__ import annotations

import argparse
from pathlib import Path


OLD_BODY = '''      FuncDef("sort_even", Params("l"),
        Return(
          Call(
            Name("rebuild"),
            Name("l"),
            Call(Name("sort_values"), Call(Name("even_values"), Name("l")))))))
'''

NEW_BODY = '''      FuncDef("sort_even", Params("l"),
        Return(Name("l"))))
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("verification", type=Path)
    parser.add_argument("spec", type=Path)
    parser.add_argument("verification_output", type=Path)
    parser.add_argument("spec_output", type=Path)
    args = parser.parse_args()
    verification = args.verification.read_text(encoding="utf-8")
    if verification.count(OLD_BODY) != 1:
        raise RuntimeError("expected exactly one encoded sort_even body")
    args.verification_output.write_text(
        verification.replace(OLD_BODY, NEW_BODY), encoding="utf-8"
    )
    spec = args.spec.read_text(encoding="utf-8")
    if spec.count('requires "verification.k"') != 1:
        raise RuntimeError("unexpected spec requires")
    args.spec_output.write_text(
        spec.replace(
            'requires "verification.k"', 'requires "verification-body-mutated.k"'
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
