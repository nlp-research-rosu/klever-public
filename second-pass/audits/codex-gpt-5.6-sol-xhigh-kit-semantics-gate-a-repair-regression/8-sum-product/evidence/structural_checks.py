#!/usr/bin/env python3
"""Independent structural checks for program pinning and bridge containment."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


scratch = Path("/tmp/audit-work/reconstruction")


def compact(text: str) -> str:
    return "".join(text.split())


solution_mpy = (scratch / "solution.mpy").read_text(encoding="utf-8")
spec = (scratch / "spec.k").read_text(encoding="utf-8")
verification = (scratch / "verification.k").read_text(encoding="utf-8")

body = """Assign(Name("total"), Int(0))
Assign(Name("product"), Int(1))
Assign(Name("number"), Int(0))
For(
  Name("number"),
  Name("numbers"),
  AugAssign(Name("total"), "+", Name("number"))
  AugAssign(Name("product"), "*", Name("number"))
)
Return(TupleExpr(Name("total"), Name("product")))"""

closure = f"""closureVal(
  ("numbers", .ParamNames),
  {body},
  0
)"""

print("program_body_occurrences_in_solution_mpy=", compact(solution_mpy).count(compact(body)))
print("exact_closure_occurrences_in_spec=", compact(spec).count(compact(closure)))

loop_claim_match = re.search(
    r"claim \[sum-product-loop\]:(.*?)(?=\nendmodule)",
    spec,
    flags=re.DOTALL,
)
bridge_match = re.search(
    r"module VERIFICATION\s*\n.*?\n\s*rule(.*?)(?=\nendmodule)",
    verification,
    flags=re.DOTALL,
)
if loop_claim_match is None or bridge_match is None:
    raise SystemExit("failed to locate loop claim or bridge")

claim_contract = compact(loop_claim_match.group(1))
bridge_contract = compact(
    re.sub(r"\[priority\(40\)\]\s*$", "", bridge_match.group(1).strip())
)
print("loop_claim_contract_sha256=", hashlib.sha256(claim_contract.encode()).hexdigest())
print("bridge_contract_sha256=", hashlib.sha256(bridge_contract.encode()).hexdigest())
print("bridge_contract_exact_match=", claim_contract == bridge_contract)

ok = (
    compact(solution_mpy).count(compact(body)) == 1
    and compact(spec).count(compact(closure)) == 2
    and claim_contract == bridge_contract
)
raise SystemExit(0 if ok else 1)
