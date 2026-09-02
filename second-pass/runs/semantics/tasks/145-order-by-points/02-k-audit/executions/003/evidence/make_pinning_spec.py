#!/usr/bin/env python3
from pathlib import Path

module_term = Path(
    "/tmp/audit-work/source/solution.regenerated.mpy"
).read_text(encoding="utf-8").rstrip()

print('requires "verification.k"')
print()
print("module REVIEWER-PINNING-SPEC")
print("  imports ORDER-BY-POINTS-VERIFICATION")
print()
print("  claim")
print("    <k> solutionModule")
print("         =>")
for line in module_term.splitlines():
    print("         " + line)
print("    </k>")
print("  [label(module_identity)]")
print("endmodule")
