#!/usr/bin/env python3
"""Create a body-sensitive mutation that flips the program's equal-bit branch."""

from pathlib import Path


root = Path("/tmp/audit-work/11-string-xor")
source = root / "candidate" / "verification.k"
mutation_root = root / "body-mutation"
mutated = mutation_root / "verification.k"
evidence_copy = Path("/audit-output/evidence/body-mutation-verification.k")

text = source.read_text(encoding="utf-8")
old = (
    'Assign(Name("result"), BinOp("+", Name("result"), Str("0"))),\n'
    '          Assign(Name("result"), BinOp("+", Name("result"), Str("1"))))'
)
new = (
    'Assign(Name("result"), BinOp("+", Name("result"), Str("1"))),\n'
    '          Assign(Name("result"), BinOp("+", Name("result"), Str("1"))))'
)
if text.count(old) != 1:
    raise RuntimeError(f"expected one body occurrence, found {text.count(old)}")
mutated_text = text.replace(old, new)
mutated.write_text(mutated_text, encoding="utf-8")
evidence_copy.write_text(mutated_text, encoding="utf-8")

term = (root / "regenerated-solution.mpy").read_text(encoding="utf-8").rstrip()
indented = "\n".join(f"      {line}" for line in term.splitlines())
pinning = f"""requires "verification.k"

module AUDIT-BODY-PINNING
  imports STRING-XOR-VERIFICATION

  claim
    <k>
      stringXorModule
      =>
{indented}
    </k>
endmodule
"""
(mutation_root / "audit-original-pinning-spec.k").write_text(pinning, encoding="utf-8")
print(f"source={source}")
print(f"mutated={mutated}")
print(f"evidence_copy={evidence_copy}")
print("mutation=equal branch appends '1' instead of '0'")
print("BODY_MUTATION_GENERATED")
