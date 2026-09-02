#!/usr/bin/env python3
"""Add inert labels to each original positive claim for per-claim replay."""

from pathlib import Path
import sys


labels = [
    "nonnegative",
    "negative",
    "example-15",
    "example-32",
    "example-negative-5",
]
source = Path(sys.argv[1]).read_text()
source = source.replace("module SPEC\n", "module SPEC-LABELED\n", 1)
source = source.replace("endmodule\n", "endmodule\n", 1)
needle = "  claim\n"
if source.count(needle) != len(labels):
    raise SystemExit(f"expected {len(labels)} unlabeled claims, found {source.count(needle)}")
for label in labels:
    source = source.replace(needle, f"  claim [{label}]:\n", 1)
sys.stdout.write(source)
