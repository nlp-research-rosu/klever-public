#!/usr/bin/env python3
"""Ground witnesses for every formal entry precondition and postcondition."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


def wrapped(value: Any) -> dict[str, Any]:
    return {"type": type(value).__name__, "value": value}


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: claim_witnesses.py CANONICAL GENERATED OUTPUT_JSON", file=sys.stderr)
        return 64
    canonical = load(Path(sys.argv[1]), "trusted_canonical_for_witness")
    generated = load(Path(sys.argv[2]), "candidate_for_witness")
    output = Path(sys.argv[3])

    cases = [
        ("whitespace", "a b"),
        ("whitespace", "a\tb"),
        ("comma", "a,b"),
        ("comma", ","),
        ("odd-lowercase-count", "abcdef"),
        ("odd-lowercase-count", "\u00ea"),
    ]
    odd_letters = "bdfhjlnprtvxz"
    rows = []
    for claim, text in cases:
        ws_count = sum(text.count(c) for c in (" ", "\t", "\n", "\r"))
        comma_count = text.count(",")
        odd_count = sum(text.count(c) for c in odd_letters)
        if claim == "whitespace":
            precondition = ws_count > 0
            formal_value = text.split()
            formal_configuration = {
                "k": "ref(0)",
                "heap_0": formal_value,
                "heapLoc": 1,
            }
        elif claim == "comma":
            precondition = ws_count <= 0 and comma_count > 0
            formal_value = text.split(",")
            formal_configuration = {
                "k": "ref(0)",
                "heap_0": formal_value,
                "heapLoc": 1,
            }
        else:
            precondition = ws_count <= 0 and comma_count <= 0
            formal_value = odd_count
            formal_configuration = {"k": formal_value, "heap": {}, "heapLoc": 0}

        assert precondition
        row = {
            "claim": claim,
            "input": text,
            "codepoints": [ord(c) for c in text],
            "whitespaceCount": ws_count,
            "commaCount": comma_count,
            "oddAlphabetCount": odd_count,
            "precondition_satisfied": precondition,
            "formal_value": wrapped(formal_value),
            "formal_destination": formal_configuration,
            "generated_python": wrapped(generated(text)),
            "trusted_canonical_python": wrapped(canonical(text)),
        }
        row["formal_equals_generated"] = (
            row["formal_value"] == row["generated_python"]
        )
        row["formal_equals_canonical"] = (
            row["formal_value"] == row["trusted_canonical_python"]
        )
        rows.append(row)
        print(json.dumps(row, ensure_ascii=True, sort_keys=True))

    output.write_text(
        json.dumps({"witnesses": rows}, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
