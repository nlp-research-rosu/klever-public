#!/usr/bin/env python3
"""Check that the proof's bound closure body is the trusted translation body."""

from pathlib import Path


ROOT = Path("/tmp/audit-work/127-intersection")
mpy_text = (ROOT / "regenerated-solution.mpy").read_text()
verification_text = (ROOT / "candidate-src/verification.k").read_text()


def compact_k(text: str) -> str:
    # The trusted translator emits empty statement lists as an omitted argument;
    # the proof source spells the same K list unit as `.Stmts`.
    return "".join(text.split()).replace(".Stmts", "")


mpy = compact_k(mpy_text)
prefix = 'Module(FuncDef("intersection",Params("interval1","interval2"),'
if not (mpy.startswith(prefix) and mpy.endswith("))")):
    raise AssertionError("unexpected trusted-translator module/function shape")
translated_body = mpy[len(prefix) : -2]

rule_start = verification_text.index("  rule intersectionBody")
body_start = verification_text.index("=>", rule_start) + 2
body_end = verification_text.index("\n\n  // True exactly", body_start)
proof_body = compact_k(verification_text[body_start:body_end])

print(f"translated_body_chars={len(translated_body)}")
print(f"proof_body_chars={len(proof_body)}")
print(f"constructor_identity={translated_body == proof_body}")
if translated_body != proof_body:
    mismatch = next(
        (
            index
            for index, (left, right) in enumerate(zip(translated_body, proof_body))
            if left != right
        ),
        min(len(translated_body), len(proof_body)),
    )
    print(f"first_mismatch={mismatch}")
    print(f"translated_excerpt={translated_body[max(0, mismatch-80):mismatch+80]}")
    print(f"proof_excerpt={proof_body[max(0, mismatch-80):mismatch+80]}")
    raise SystemExit(1)
