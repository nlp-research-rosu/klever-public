#!/usr/bin/env python3
"""Mutate the Program term actually executed by a claim (1 -> 2 append)."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate-src")
TARGET = Path("/tmp/audit-work/body-mutant")


def main() -> None:
    TARGET.mkdir(parents=True, exist_ok=True)
    (TARGET / "semantic.k").write_bytes((SOURCE / "semantic.k").read_bytes())
    verification = (SOURCE / "verification.k").read_text()
    verification = verification.replace(
        "module MINPATH-VERIFICATION\n",
        "module MINPATH-VERIFICATION-BODY-MUTANT\n",
        1,
    )
    old = 'Expr(Call(Attribute(Name("answer"), "append"), Int(1))),'
    new = 'Expr(Call(Attribute(Name("answer"), "append"), Int(2))),'
    assert verification.count(old) == 1
    verification = verification.replace(old, new, 1)
    (TARGET / "verification-body-mutant.k").write_text(verification)

    spec = """requires "verification-body-mutant.k"

module MINPATH-BODY-MUTATION-SPEC
  imports MINPATH-VERIFICATION-BODY-MUTANT

  claim [body-sensitive]:
    <k> solutionProgram ~> start(grid3(1, 2, 3, 4, 5, 6, 7, 8, 9), 3)
      => .K </k>
    <result> none => some(path3(2)) </result>
    <env> .Map => ?_ </env>
    <functions> .Map => ?_ </functions>
endmodule
"""
    (TARGET / "spec-body-mutant.k").write_text(spec)
    print(f"target={TARGET}")
    print(f"mutation={old} -> {new}")
    print("actual_solutionProgram_term_mutated=true")


if __name__ == "__main__":
    main()
