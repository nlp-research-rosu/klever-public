#!/usr/bin/env python3
"""Compare translator output with the exact Module term executed by the entry claim."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def label(term: dict) -> str | None:
    return term.get("label", {}).get("name")


def digest(term: dict) -> str:
    payload = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("translated_ast", type=Path)
    parser.add_argument("entry_rule_ast", type=Path)
    args = parser.parse_args()

    translated = json.loads(args.translated_ast.read_text())["term"]
    entry = json.loads(args.entry_rule_ast.read_text())["term"]

    if label(entry) != "<k>" or len(entry["args"]) != 1:
        raise ValueError("entry rule is not a single <k> cell")
    rewrite = entry["args"][0]
    if rewrite.get("node") != "KRewrite":
        raise ValueError("entry rule <k> does not contain a KRewrite")
    lhs = rewrite["lhs"]
    rhs = rewrite["rhs"]
    if not label(lhs).startswith("#loadAll("):
        raise ValueError("entry rule LHS does not start with #loadAll")
    if not label(rhs).startswith("#loadAll("):
        raise ValueError("synthetic rule RHS does not start with #loadAll")
    claim_module = lhs["args"][0]
    duplicate_module = rhs["args"][0]

    print(f"translated root: {label(translated)}")
    print(f"claim root: {label(claim_module)}")
    print(f"translated AST sha256: {digest(translated)}")
    print(f"claim AST sha256: {digest(claim_module)}")
    print(f"synthetic lhs/rhs module identical: {claim_module == duplicate_module}")
    print(f"translated/claim module identical: {translated == claim_module}")
    return 0 if translated == claim_module == duplicate_module else 1


if __name__ == "__main__":
    raise SystemExit(main())
