#!/usr/bin/env python3
"""Ground witnesses for the submitted loop claim's result function."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def correct_codes(remaining: str, balance: int) -> bool:
    for character in remaining:
        if character == "(":
            balance += 1
        elif balance == 0:
            return False
        else:
            balance -= 1
    return balance == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("generated")
    args = parser.parse_args()
    canonical = load_entry(Path(args.canonical), "witness_canonical_61")
    generated = load_entry(Path(args.generated), "witness_generated_61")

    claim_substitutions = [
        {"remaining": "", "balance": 0},
        {"remaining": "(", "balance": 0},
        {"remaining": "()", "balance": 0},
        {"remaining": ")", "balance": 0},
        {"remaining": "", "balance": 1},
        {"remaining": ")", "balance": 1},
        {"remaining": "))", "balance": 2},
        {"remaining": ")(", "balance": 1},
    ]
    mismatches = []
    for item in claim_substitutions:
        remaining = item["remaining"]
        balance = item["balance"]
        # A prefix of `balance` opening brackets is a concrete history that
        # reaches the claimed loop state without having gone negative.
        whole_input = "(" * balance + remaining
        result = correct_codes(remaining, balance)
        row = {
            **item,
            "concrete_reaching_input": whole_input,
            "correctCodes": result,
            "canonical": canonical(whole_input),
            "generated": generated(whole_input),
        }
        print(json.dumps(row, sort_keys=True))
        if not (row["correctCodes"] == row["canonical"] == row["generated"]):
            mismatches.append(row)

    print("satisfying_state=B=0,S=.IntSeq,OLD=str(.IntSeq),INPUT=.IntSeq,"
          "GLOBALS=.Map,HEAP=.Map,HLOC=0,CONT=.K")
    print(f"substitutions={len(claim_substitutions)}")
    print(f"mismatches={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
