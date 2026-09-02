#!/usr/bin/env python3
"""Mechanical constructor comparison between solution.mpy and SPEC's closure."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/review-34-unique")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_k(text: str) -> str:
    # This comparison uses files with no escaped whitespace in String tokens.
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


solution_path = SCRATCH / "solution.mpy"
regenerated_path = SCRATCH / "regenerated-solution.mpy"
spec_path = SCRATCH / "spec.k"

solution = compact_k(solution_path.read_text(encoding="utf-8"))
spec = compact_k(spec_path.read_text(encoding="utf-8"))

module_prefix = 'Module(FuncDef("unique",Params("l"),'
assert solution.startswith(module_prefix), solution
assert solution.endswith("))"), solution
source_body = solution[len(module_prefix) : -2]

# K's list syntax permits these empty-list shorthands in a parsed .mpy file.
source_body = source_body.replace("ListExpr()", "ListExpr(.Exprs)")
source_body = source_body.replace(",))Return(", ",.Stmts))Return(")
source_body_with_terminator = source_body + ".Stmts"

closure_prefix = '"unique"<-closureVal(("l",.ParamNames),'
start = spec.index(closure_prefix) + len(closure_prefix)
closure_suffix = ",0)],parent(-1))"
end = spec.index(closure_suffix, start)
claimed_body = spec[start:end]

print("submitted_solution_mpy_sha256", sha256(solution_path))
print("trusted_regenerated_mpy_sha256", sha256(regenerated_path))
print("byte_identical", solution_path.read_bytes() == regenerated_path.read_bytes())
print("function_name", "unique")
print("source_params_constructor", 'Params("l")')
print("claim_params_constructor", '("l",.ParamNames)')
print("claim_definition_environment", 0)
print("normalized_source_body", source_body_with_terminator)
print("normalized_claimed_body", claimed_body)
print("constructor_body_equal", source_body_with_terminator == claimed_body)

assert solution_path.read_bytes() == regenerated_path.read_bytes()
assert source_body_with_terminator == claimed_body
assert '<k>Call(Name("unique"),ref(0))=>ref(2)</k>' in spec
assert '<env>0</env>' in spec
print("entry_call_pinned", True)

