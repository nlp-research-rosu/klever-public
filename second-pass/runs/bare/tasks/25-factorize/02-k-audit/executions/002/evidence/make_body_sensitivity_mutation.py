#!/usr/bin/env python3
"""Mutate the divisor passed by the actual SolutionModule program term."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/25-factorize/verification.k")
SCRATCH_MUTATION = Path(
    "/tmp/audit-work/25-factorize/body-sensitivity-verification.k"
)
EVIDENCE_MUTATION = Path(
    "/audit-output/evidence/body-sensitivity-verification.k"
)
SCRATCH_SPEC = Path("/tmp/audit-work/25-factorize/body-sensitivity-spec.k")
EVIDENCE_SPEC = Path("/audit-output/evidence/body-sensitivity-spec.k")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    old = (
        'FuncDef("factorize", Params("n"),\n'
        '        Return(Call(Name("factorize_from"), Name("n"), Int(2)))))'
    )
    new = (
        'FuncDef("factorize", Params("n"),\n'
        '        Return(Call(Name("factorize_from"), Name("n"), Int(3)))))'
    )
    if source.count(old) != 1:
        raise AssertionError(
            f"expected one actual factorize binding/body fragment, found {source.count(old)}"
        )
    mutated = source.replace(old, new)
    SCRATCH_MUTATION.write_text(mutated, encoding="utf-8")
    EVIDENCE_MUTATION.write_text(mutated, encoding="utf-8")

    spec = """requires "body-sensitivity-verification.k"

module BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  claim Run(SolutionMachine(4))
    => Run(Halted(.Map, SolutionFunctions(), .List,
         ListVal(ListItem(IntVal(2)) ListItem(IntVal(2)))))
endmodule
"""
    SCRATCH_SPEC.write_text(spec, encoding="utf-8")
    EVIDENCE_SPEC.write_text(spec, encoding="utf-8")
    print(
        "MUTATION: changed the divisor literal in the executed factorize "
        "function binding from Int(2) to Int(3)"
    )
    print(f"wrote {SCRATCH_MUTATION}")
    print(f"wrote {EVIDENCE_MUTATION}")
    print(f"wrote {SCRATCH_SPEC}")
    print(f"wrote {EVIDENCE_SPEC}")


if __name__ == "__main__":
    main()
