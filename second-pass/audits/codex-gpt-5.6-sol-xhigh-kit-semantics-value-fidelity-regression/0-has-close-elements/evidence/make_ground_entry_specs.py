#!/usr/bin/env python3
"""Create auditable ground entry probes from the candidate's exact target claim."""

from __future__ import annotations

from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")


def specialize(target: str, argument: str) -> str:
    old_rhs = "outerAcc(false, 0, INPUT, INPUT, THRESHOLD)"
    if target.count(old_rhs) != 1:
        raise RuntimeError("unexpected target RHS count")
    target = target.replace(old_rhs, "false")
    old_argument = "list(floatVals(INPUT:FloatSeq)),\n           THRESHOLD:Float"
    if target.count(old_argument) != 1:
        raise RuntimeError("unexpected target argument count")
    target = target.replace(old_argument, f"{argument},\n           0.5")
    return target


def write_spec(filename: str, module: str, imported: str, target: str) -> None:
    rendered = (
        'requires "verification.k"\n\n'
        f"module {module}\n"
        f"  imports {imported}\n\n"
        f"{target}"
        "endmodule\n"
    )
    (WORK / filename).write_text(rendered)


def main() -> int:
    spec = (WORK / "spec.k").read_text()
    start = spec.index("  claim [target]:")
    end = spec.rindex("endmodule")
    target = spec[start:end]

    proof_empty = specialize(target, "list(floatVals(.FloatSeq))")
    actual_empty = specialize(target, "list(.ValSeq)")

    write_spec(
        "ground-proof-empty-base.k",
        "GROUND-PROOF-EMPTY-BASE",
        "VERIFICATION-BASE",
        proof_empty,
    )
    write_spec(
        "ground-proof-empty-extended.k",
        "GROUND-PROOF-EMPTY-EXTENDED",
        "VERIFICATION",
        proof_empty,
    )
    write_spec(
        "ground-actual-empty-base.k",
        "GROUND-ACTUAL-EMPTY-BASE",
        "VERIFICATION-BASE",
        actual_empty,
    )
    for filename in [
        "ground-proof-empty-base.k",
        "ground-proof-empty-extended.k",
        "ground-actual-empty-base.k",
    ]:
        path = WORK / filename
        print(f"WROTE {path} bytes={path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
