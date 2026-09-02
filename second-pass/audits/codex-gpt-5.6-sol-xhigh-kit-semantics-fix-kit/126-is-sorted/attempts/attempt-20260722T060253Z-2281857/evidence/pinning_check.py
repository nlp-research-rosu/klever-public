#!/usr/bin/env python3
"""Textual identity checks between translated program and formal entry claim."""

from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/126-is-sorted")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def compact_surface_equivalent(text: str) -> str:
    # The MPY grammar's empty List{Stmt,""} may be elided or printed as .Stmts.
    return compact(text).replace(".Stmts", "")


solution = (ROOT / "solution.mpy").read_text(encoding="utf-8").strip()
spec = (ROOT / "spec.k").read_text(encoding="utf-8")
verification = (ROOT / "verification.k").read_text(encoding="utf-8")

entry_start = spec.index("#loadAll(", spec.index("claim [is-sorted]"))
entry_end = spec.index("~> Call", entry_start)
loaded = spec[entry_start + len("#loadAll(") : entry_end].strip()
if not loaded.endswith(")"):
    raise AssertionError("could not isolate #loadAll argument")
loaded = loaded[:-1].strip()

checks = {
    "entry_load_surface_equivalent_to_solution_mpy":
    compact_surface_equivalent(loaded) == compact_surface_equivalent(solution),
    "entry_calls_named_is_sorted": compact('Call(Name("is_sorted"),(list(intVals(INPUT)),.Exprs))')
    in compact(spec[entry_end :]),
    "entry_rhs_is_result_summary": compact("=> scanSorted(true, -1, 0, INPUT)") in compact(spec),
    "entry_state_repeats_exact_body_fragments": all(
        compact_surface_equivalent(spec).count(compact_surface_equivalent(fragment)) >= 2
        for fragment in (
            'Assign(Name("prev"), UnaryOp("-", Int(1)))',
            'Assign(Name("duplicates"), Int(0))',
            'Assign(Name("result"), Bool(true))',
            'If(Compare(Name("duplicates"), CmpOp(">", Int(1)))',
            'Return(Name("result"))',
        )
    ),
    "verification_contains_exact_loop_body_fragments": all(
        compact(fragment) in compact(verification)
        for fragment in (
            'If(Call(Name("isinstance"),Name("value"),Name("int"))',
            'If(Compare(Name("value"),CmpOp("<",Name("prev")))',
            'If(Compare(Name("value"),CmpOp("==",Name("prev")))',
            'If(Compare(Name("duplicates"),CmpOp(">",Int(1)))',
            'Assign(Name("prev"),Name("value"))',
        )
    ),
}

for name, passed in checks.items():
    print(f"{name}={str(passed).lower()}")

if not all(checks.values()):
    raise SystemExit(1)
