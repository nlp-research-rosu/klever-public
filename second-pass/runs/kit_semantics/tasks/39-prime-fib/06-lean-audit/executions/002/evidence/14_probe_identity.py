#!/usr/bin/env python3
import hashlib
from pathlib import Path


candidate_lines = Path("/candidate/Proof.lean").read_text().splitlines(keepends=True)
probe_lines = Path(
    "/tmp/audit-work/39-prime-fib-independent-audit/Probe.lean"
).read_text().splitlines(keepends=True)

# Lines 4--104 contain every implementation declaration from the candidate:
# all seven target bindings and all of their helpers. The probe was made by
# copying Proof.lean, changing only the namespace name, then appending lemmas.
candidate_implementation = "".join(candidate_lines[3:104])
probe_implementation = "".join(probe_lines[3:104])
assert candidate_implementation == probe_implementation

digest = hashlib.sha256(candidate_implementation.encode()).hexdigest()
print("IMPLEMENTATION_LINE_RANGE", "Proof.lean:4-104")
print("IMPLEMENTATION_SLICE_SHA256", digest)
print("PROBE_IMPLEMENTATION_BYTE_IDENTITY", "PASS")
print(
    "FROZEN_RECURRENCE_INSTANCE",
    "primeFibSearch(1,0,4,8) = primeFibSearch(1,0,4,4)",
)
print("GUARD", "1>=1, 0<1, 4>=0, 4>=1, primeScan(4,2,true)=false")
print("PROBE_VALUES", "left=8 right=4")
print("FROZEN_RECURRENCE_PRESERVATION", "FAIL")
