#!/usr/bin/env python3
"""Generate a fresh false result mutation from the audited entry claim."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
EVIDENCE = Path("/audit-output/evidence")


def main() -> int:
    source = (ROOT / "spec.k").read_text()
    entry = source[source.index("module SPEC-ENTRY") :]
    old_result = "=> str(antiFinish(.IntSeq, .IntSeq, CODES))"
    new_result = "=> str(iCons(63, antiFinish(.IntSeq, .IntSeq, CODES)))"
    if entry.count(old_result) != 1:
        raise RuntimeError(f"expected one target result, found {entry.count(old_result)}")
    mutation = 'requires "verification.k"\n\n' + entry
    mutation = mutation.replace("module SPEC-ENTRY", "module AUDIT-FALSE-RESULT", 1)
    mutation = mutation.replace(old_result, new_result, 1)
    scratch_path = ROOT / "spec-fresh-vacuity.k"
    evidence_path = EVIDENCE / "spec-fresh-vacuity.k"
    scratch_path.write_text(mutation)
    evidence_path.write_text(mutation)
    print(f"scratch_mutation={scratch_path}")
    print(f"evidence_mutation={evidence_path}")
    print("mutation=prefix code 63 ('?') to the required returned IntSeq")
    print("false_witness=CODES=.IntSeq; actual empty string; mutated postcondition '?' string")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
