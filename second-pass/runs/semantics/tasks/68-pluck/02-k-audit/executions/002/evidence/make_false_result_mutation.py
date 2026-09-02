#!/usr/bin/env python3
"""Generate the fresh result-postcondition mutation for the non-vacuity gate."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate/spec.k")
RUNNABLE = Path("/tmp/audit-work/candidate/spec-false-result.k")
PRESERVED = Path("/audit-output/evidence/spec_false_result.k")


def main() -> None:
    text = SOURCE.read_text()
    if text.count("module PLUCK-SPEC\n") != 1:
        raise SystemExit("unexpected source module count")
    text = text.replace(
        "module PLUCK-SPEC\n", "module PLUCK-SPEC-FALSE-RESULT\n", 1
    )
    if text.count("[pluck-correct]:") != 1:
        raise SystemExit("unexpected entry claim-label count")
    text = text.replace(
        "[pluck-correct]:", "[pluck-correct-false-result]:", 1
    )
    old = '<heap> .Map => 0 |-> list(pluckResult(VS)) </heap>'
    new = '<heap> .Map => 0 |-> list(vCons(0, pluckResult(VS))) </heap>'
    if text.count(old) != 1:
        raise SystemExit(f"expected one result postcondition, found {text.count(old)}")
    text = text.replace(old, new, 1)
    RUNNABLE.write_text(text)
    PRESERVED.write_text(text)
    print(f"source={SOURCE}")
    print(f"runnable={RUNNABLE}")
    print(f"preserved={PRESERVED}")
    print("mutation=prefix integer 0 to required returned list contents")
    print("satisfying_witness=VS:.ValSeq allNonNegative(.ValSeq)=true")
    print("actual_python_result=[]")
    print("mutated_required_result=[0]")
    print("FALSE_RESULT_MUTATION_GENERATION=PASS")


if __name__ == "__main__":
    main()
