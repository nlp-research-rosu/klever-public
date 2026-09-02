#!/usr/bin/env python3
"""Generate a K claim connecting solutionProgram to the regenerated .mpy AST."""

from __future__ import annotations

from pathlib import Path
from textwrap import indent


MPY = Path("/tmp/audit-work/rebuild/regenerated-solution.mpy")
SCRATCH_SPEC = Path("/tmp/audit-work/rebuild/audit-program-identity.k")
EVIDENCE_SPEC = Path("/audit-output/evidence/audit-program-identity.k")
SCRATCH_EXTENSION = Path("/tmp/audit-work/rebuild/audit-identity-verification.k")
EVIDENCE_EXTENSION = Path("/audit-output/evidence/audit-identity-verification.k")


def main() -> None:
    term = MPY.read_text(encoding="utf-8").rstrip()
    # The standalone program parser accepts an omitted empty Stmts list after
    # the final comma. Inside a claim, the generic parser needs its explicit
    # unit to disambiguate the same constructor term.
    implicit_empty = "        ))\n    Return(Name(\"result\"))))"
    explicit_empty = "        .Stmts))\n    Return(Name(\"result\"))))"
    if term.count(implicit_empty) != 1:
        raise RuntimeError("expected exactly one implicit empty Stmts tail")
    claim_term = term.replace(implicit_empty, explicit_empty)
    extension = (
        'requires "verification.k"\n\n'
        "module AUDIT-IDENTITY-VERIFICATION\n"
        "  imports MPY-VERIFICATION\n"
        '  syntax KItem ::= "auditHold" "(" Program ")"\n'
        "endmodule\n"
    )
    source = (
        'requires "audit-identity-verification.k"\n\n'
        "module AUDIT-PROGRAM-IDENTITY\n"
        "  imports AUDIT-IDENTITY-VERIFICATION\n\n"
        "  // RHS is generated from regenerated-solution.mpy; its single\n"
        "  // omitted empty Stmts list is written explicitly as .Stmts.\n"
        "  claim [solution-program-expands-to-regenerated-file]:\n"
        "    <mpy>\n"
        "      <k> auditHold(solutionProgram)\n"
        "           => auditHold(\n"
        f"{indent(claim_term, '                ')}\n"
        "              ) </k>\n"
        "      <functions> .Map </functions>\n"
        "      <env> .Map </env>\n"
        "      <result> NoneVal </result>\n"
        "    </mpy>\n"
        "endmodule\n"
    )
    SCRATCH_EXTENSION.write_text(extension, encoding="utf-8")
    EVIDENCE_EXTENSION.write_text(extension, encoding="utf-8")
    SCRATCH_SPEC.write_text(source, encoding="utf-8")
    EVIDENCE_SPEC.write_text(source, encoding="utf-8")
    print(f"source={MPY}")
    print(f"scratch_spec={SCRATCH_SPEC}")
    print(f"evidence_spec={EVIDENCE_SPEC}")
    print(f"scratch_extension={SCRATCH_EXTENSION}")
    print(f"evidence_extension={EVIDENCE_EXTENSION}")
    print(f"term_bytes={len(MPY.read_bytes())}")


if __name__ == "__main__":
    main()
