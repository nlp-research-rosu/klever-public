#!/usr/bin/env python3
"""Mutate the function body actually loaded/called by the entry claim."""

from pathlib import Path


source = Path("/tmp/audit-work/111-histogram-audit/spec.k")
destination = Path(
    "/tmp/audit-work/111-histogram-audit/audit-body-sensitivity.k"
)
text = source.read_text(encoding="utf-8")
text = text.replace("module SPEC\n", "module AUDIT-BODY-SENSITIVITY\n", 1)
text = text.replace("claim [histogram]:", "claim [histogram-mutated-body]:", 1)

claim_index = text.index("claim [histogram-mutated-body]:")
prefix = text[:claim_index]
main_claim = text[claim_index:]
needle = 'CmpOp("==", Name("max_count"))'
assert main_claim.count(needle) == 2
main_claim = main_claim.replace(
    needle, 'CmpOp("!=", Name("max_count"))'
)

old_result = """      ~> Call(Name("histogram"), str(CS:IntSeq))
      => histogramResult(CS)"""
new_result = """      ~> Call(
        Name("histogram"),
        str(iCons(97, .IntSeq)))
      =>
      histogramResult(iCons(97, .IntSeq))"""
assert old_result in main_claim
main_claim = main_claim.replace(old_result, new_result, 1)
assert "    requires validHistogramInput(CS)" in main_claim
main_claim = main_claim.replace(
    "    requires validHistogramInput(CS)",
    "    requires validHistogramInput(iCons(97, .IntSeq))",
    1,
)

destination.write_text(prefix + main_claim, encoding="utf-8")
print(f"wrote: {destination}")
print("changed both loaded and post-state closure bodies: second-pass == became !=")
print("ground witness 'a': mutated body returns {}; required summary is {'a': 1}")
