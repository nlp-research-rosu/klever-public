#!/usr/bin/env python3
"""Create a mutation that changes the program term executed by the claim."""

from pathlib import Path


source = Path("/audit-output/evidence/stage6/spec-audit-vacuity.k").read_text()
source = source.replace("SPEC-AUDIT-VACUITY", "SPEC-AUDIT-BODY-MUTATION")
source = source.replace("[false-prime-result]", "[changed-program-body]")
source = source.replace(
    "// Fresh audit mutation: the unchanged program at n=2, x=10, y=20 really\n"
    "  // returns 10, but this claim deliberately demands 20.",
    "// Body-sensitivity mutation: both copies of the executed closure body\n"
    "  // initialize result from y rather than x, but the claim still demands 10.",
)
needle = 'Assign(Name("result"), Name("x"))'
count = source.count(needle)
if count != 2:
    raise SystemExit(f"expected two body occurrences, found {count}")
source = source.replace(needle, 'Assign(Name("result"), Name("y"))')
postcondition = "ensures ?V ==K 20"
if source.count(postcondition) != 1:
    raise SystemExit("unexpected postcondition count")
source = source.replace(postcondition, "ensures ?V ==K 10")
output = Path("/tmp/audit-work/reconstruction/spec-audit-body-mutation.k")
output.write_text(source)
print(f"output={output}")
print(f"program_body_replacements={count}")
print("ground_call=(n=2,x=10,y=20)")
print("expected_original_result=10")
print("mutated_program_result=20")
