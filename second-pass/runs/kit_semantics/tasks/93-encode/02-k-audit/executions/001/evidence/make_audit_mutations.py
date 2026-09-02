#!/usr/bin/env python3
"""Create independent body-sensitivity and false-result K claims in scratch."""

from __future__ import annotations

import sys
from pathlib import Path


if len(sys.argv) != 2:
    raise SystemExit("usage: make_audit_mutations.py SCRATCH_DIRECTORY")

scratch = Path(sys.argv[1])
source_path = scratch / "spec.k"
source = source_path.read_text(encoding="utf-8")

body = source.replace("module SPEC\n", "module SPEC-BODY-AUDIT\n")
assert body != source
assert body.count('Str("Q")') == 2
body = body.replace('Str("Q")', 'Str("R")')
assert body.count('Str("Q")') == 0
assert body.count('Str("R")') == 2
(scratch / "spec-body-audit.k").write_text(body, encoding="utf-8")

false_result = source.replace("module SPEC\n", "module SPEC-FALSE-AUDIT\n")
old_post_tail = """          85,
          87
"""
new_post_tail = """          85,
          88
"""
assert false_result.count(old_post_tail) == 1
false_result = false_result.replace(old_post_tail, new_post_tail)
assert false_result.count(new_post_tail) == 1
(scratch / "spec-false-audit.k").write_text(false_result, encoding="utf-8")

print("body_mutation=Str(\"Q\")->Str(\"R\") in both executed and retained body copies")
print("body_mutation_original_postcondition_preserved=True")
print("false_result_mutation=final replaceC(...,85,87)->replaceC(...,85,88)")
print("false_result_witness=CS=iCons(117,.IntSeq), corresponding to input 'u'")
print("MUTATIONS_CREATED=PASS")
