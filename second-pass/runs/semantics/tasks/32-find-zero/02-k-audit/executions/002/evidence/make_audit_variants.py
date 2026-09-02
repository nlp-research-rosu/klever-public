#!/usr/bin/env python3
"""Create reviewer-owned proof variants in scratch without changing the candidate."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
EVIDENCE = Path("/audit-output/evidence")


def remove_bridge(text: str, name: str) -> str:
    pattern = re.compile(
        rf"\n  rule <k> {re.escape(name)} => \.K \.\.\. </k>\n"
        rf".*?"
        rf"\n    \[priority\(40\)\]\n",
        re.DOTALL,
    )
    rewritten, count = pattern.subn("\n", text)
    if count != 1:
        raise RuntimeError(f"expected one {name} bridge, removed {count}")
    return rewritten


def main() -> int:
    verification = (WORK / "verification.k").read_text()
    no_bridges = remove_bridge(verification, "bracketLoop")
    no_bridges = remove_bridge(no_bridges, "bisectLoop")
    no_bridges = no_bridges.replace(
        "module VERIFICATION", "module AUDIT-NO-BRIDGES-VERIFICATION", 1
    )
    (WORK / "audit-no-bridges-verification.k").write_text(no_bridges)

    spec = (WORK / "spec.k").read_text()
    no_bridges_spec = spec.replace(
        'requires "verification.k"',
        'requires "audit-no-bridges-verification.k"',
        1,
    )
    no_bridges_spec = no_bridges_spec.replace(
        "module SPEC", "module AUDIT-NO-BRIDGES-SPEC", 1
    )
    no_bridges_spec = no_bridges_spec.replace(
        "imports VERIFICATION", "imports AUDIT-NO-BRIDGES-VERIFICATION", 1
    )
    (WORK / "audit-no-bridges-spec.k").write_text(no_bridges_spec)

    for name in ("audit-no-bridges-verification.k", "audit-no-bridges-spec.k"):
        (EVIDENCE / f"stage5-{name}").write_bytes((WORK / name).read_bytes())
    print("removed exactly one bracketLoop and one bisectLoop operational bridge")
    print("preserved all macros, opaque symbols, postcondition rule, and entry claims")
    print("wrote bridge-free verification/spec sources in scratch and evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
