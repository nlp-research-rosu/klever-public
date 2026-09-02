#!/usr/bin/env python3
"""Check that the closure body embedded in spec.k is the submitted MPY body."""

from pathlib import Path
import re


solution = Path("/candidate/solution.mpy").read_text()
spec = Path("/candidate/spec.k").read_text()

solution_prefix = 'FuncDef("fib4", Params("n"),'
solution_start = solution.index(solution_prefix) + len(solution_prefix)
if not solution.rstrip().endswith("))"):
    raise SystemExit("unexpected solution.mpy envelope")
solution_body = solution[solution_start : len(solution.rstrip()) - 2]

closure_prefix = '"fib4" |-> closureVal(\n          ("n", .ParamNames),'
closure_start = spec.index(closure_prefix) + len(closure_prefix)
closure_suffix = "\n          .Stmts,\n          0),"
closure_end = spec.index(closure_suffix, closure_start)
closure_body = spec[closure_start:closure_end]

# The translator omits explicit empty/tail `.Stmts` units where the K list
# parser inserts them; the hand-written claim spells those units out.
normalize = lambda text: re.sub(r"(?:\.Stmts)|\s+", "", text)
same = normalize(solution_body) == normalize(closure_body)
print("submitted_solution_body_chars:", len(solution_body))
print("embedded_closure_body_chars:", len(closure_body))
print("surface_syntax_normalized_body_equal:", same)
raise SystemExit(0 if same else 1)
