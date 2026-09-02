#!/usr/bin/env python3
"""Change the program term executed by both claims without changing their RHS."""

from pathlib import Path


source = Path("/tmp/audit-work/reconstruction/spec.k").read_text()
old = """Subscript(
                  Name("values"),
                  BinOp("+", Name("middle"), Int(1))))"""
new = """Subscript(
                  Name("values"),
                  Name("middle")))"""
count = source.count(old)
if count != 2:
    raise SystemExit(f"expected two executed-body sites, found {count}")
mutated = source.replace(old, new)
mutated = mutated.replace("module MEDIAN-SPEC", "module MEDIAN-SPEC-BODY-MUTATION")
mutated = mutated.replace("endmodule", "endmodule", 1)
print(mutated, end="")
