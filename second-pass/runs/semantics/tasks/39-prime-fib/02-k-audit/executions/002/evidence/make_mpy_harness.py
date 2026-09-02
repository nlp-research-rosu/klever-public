#!/usr/bin/env python3
"""Append a top-level prime_fib call to a regenerated MPY Module term."""

from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
parser.add_argument("destination", type=Path)
parser.add_argument("n", type=int)
args = parser.parse_args()

text = args.source.read_text()
if not text.endswith(")\n"):
    raise SystemExit("source does not end with the expected Module close")
body = text[:-2]
args.destination.write_text(
    body
    + f'  Assign(Name("answer"), Call(Name("prime_fib"), Int({args.n})))\n'
    + ")\n"
)
print(f"wrote {args.destination} with n={args.n}")
