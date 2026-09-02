#!/usr/bin/env python3
"""Compare the parsed solution function with histogramCheck's first statement."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def first_statement(path: Path):
    document = json.loads(path.read_text(encoding="utf-8"))
    module_term = document["term"]
    statements = module_term["args"][0]
    return statements["args"][0]


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--macro", type=Path, required=True)
    args = parser.parse_args()
    solution_function = first_statement(args.solution)
    macro_function = first_statement(args.macro)
    solution_bytes = canonical_bytes(solution_function)
    macro_bytes = canonical_bytes(macro_function)
    same = solution_bytes == macro_bytes
    print(f"solution_funcdef_sha256={hashlib.sha256(solution_bytes).hexdigest()}")
    print(f"macro_funcdef_sha256={hashlib.sha256(macro_bytes).hexdigest()}")
    print(f"funcdef_ast_identical={str(same).lower()}")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
