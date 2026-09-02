#!/usr/bin/env python3
"""Create a fresh false whole-program claim for the satisfiable input "a"."""

from pathlib import Path


source = Path("/tmp/audit-work/111-histogram-audit/spec.k")
destination = Path(
    "/tmp/audit-work/111-histogram-audit/audit-spec-vacuity.k"
)
text = source.read_text(encoding="utf-8")

text = text.replace("module SPEC\n", "module AUDIT-SPEC-VACUITY\n", 1)
text = text.replace(
    "claim [histogram]:",
    "claim [histogram-false-whole-program]:",
    1,
)
old_result = """      ~> Call(Name("histogram"), str(CS:IntSeq))
      => histogramResult(CS)"""
new_result = """      ~> Call(
        Name("histogram"),
        str(iCons(97, .IntSeq)))
      =>
      dictV(
        vCons(str(iCons(97, .IntSeq)), .ValSeq),
        vCons(2, .ValSeq))"""
assert old_result in text
text = text.replace(old_result, new_result, 1)
old_precondition = "    requires validHistogramInput(CS)"
new_precondition = (
    "    requires validHistogramInput(iCons(97, .IntSeq))"
)
assert old_precondition in text
text = text.replace(old_precondition, new_precondition, 1)
destination.write_text(text, encoding="utf-8")
print(f"wrote: {destination}")
print("mutation witness: input 'a' satisfies validHistogramInput")
print("false destination: {'a': 2}; actual submitted/canonical result: {'a': 1}")
