#!/usr/bin/env python3
"""Create a scratch proof definition with all five candidate bridges removed."""

from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")
verification = (WORK / "verification.k").read_text(encoding="utf-8")
start_marker = "  // cntSub is intentionally a partial K function"
end_marker = "  // This is the exact statement body emitted in solution.mpy."
start = verification.index(start_marker)
end = verification.index(end_marker)
without_bridges = (
    verification[:start]
    + "  // AUDIT MUTATION: all five proof-only #branch bridges removed.\n"
    + verification[end:]
)
without_bridges = without_bridges.replace(
    "module SPLIT-WORDS-VERIFICATION",
    "module SPLIT-WORDS-NO-BRIDGES",
    1,
)
(WORK / "verification-no-bridges.k").write_text(
    without_bridges,
    encoding="utf-8",
)

spec = (WORK / "spec.k").read_text(encoding="utf-8")
spec = spec.replace('requires "verification.k"', 'requires "verification-no-bridges.k"', 1)
spec = spec.replace(
    "module SPEC",
    "module SPEC-NO-BRIDGES",
    1,
)
spec = spec.replace(
    "imports SPLIT-WORDS-VERIFICATION",
    "imports SPLIT-WORDS-NO-BRIDGES",
    1,
)
(WORK / "spec-no-bridges.k").write_text(spec, encoding="utf-8")
print("removed_region_bytes=", end - start, sep="")
print("remaining_branch_rule_occurrences=", without_bridges.count("rule <k> #branch("), sep="")
