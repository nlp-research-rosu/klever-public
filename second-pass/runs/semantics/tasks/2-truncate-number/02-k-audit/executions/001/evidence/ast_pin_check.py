#!/usr/bin/env python3
"""Check that verification.k's program macro is exactly submitted solution.mpy."""

import re
from pathlib import Path


submitted = Path("/candidate/solution.mpy").read_text(encoding="utf-8").strip()
verification = Path("/candidate/verification.k").read_text(encoding="utf-8")
match = re.search(
    r"rule\s+solutionProgram\s*=>\s*(Module\(.*?\))\s*endmodule",
    verification,
    flags=re.DOTALL,
)
if match is None:
    raise SystemExit("could not extract solutionProgram macro")
macro_ast = match.group(1).strip()


def normalize(source: str) -> str:
    return re.sub(r"\s+", "", source)


print(f"submitted_normalized={normalize(submitted)}")
print(f"macro_normalized={normalize(macro_ast)}")
print(f"AST_MACRO_MATCH={normalize(submitted) == normalize(macro_ast)}")
raise SystemExit(0 if normalize(submitted) == normalize(macro_ast) else 1)
