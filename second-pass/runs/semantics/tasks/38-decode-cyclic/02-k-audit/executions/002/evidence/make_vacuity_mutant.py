#!/usr/bin/env python3
"""Create a fresh false-result mutation while retaining the induction helper."""

from pathlib import Path


scratch = Path("/tmp/audit-work/38-decode-cyclic")
spec = (scratch / "spec.k").read_text(encoding="utf-8")
old = "str(decodeCodes(CS))"
new = "str(seqConcat(decodeCodes(CS), iCons(33, .IntSeq)))"
if spec.count(old) != 2:
    # The helper ret postcondition and the entry postcondition both contain it.
    raise RuntimeError(f"expected two postcondition sites, got {spec.count(old)}")

# Mutate only the entry claim (the last occurrence); the helper remains the
# exact candidate induction lemma, avoiding an unrelated recursive-proof failure.
prefix, separator, suffix = spec.rpartition(old)
if not separator:
    raise RuntimeError("entry postcondition site not found")
mutant = prefix + new + suffix
mutant = mutant.replace("module SPEC\n", "module SPEC-VACUITY\n", 1)
(scratch / "spec-vacuity.k").write_text(mutant, encoding="utf-8")

print(f"mutation={old} -> {new} (entry claim only)")
print('satisfying_false_witness=CS=.IntSeq / Python input=""')
print('claimed_mutant_result="!" / actual_result=""')
