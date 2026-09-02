#!/usr/bin/env python3
"""Mechanical token-level comparison of solution.mpy and triangleProgram's RHS."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")


def remove_space(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> None:
    generated = (WORK / "solution.mpy").read_text()
    verification = (WORK / "verification.k").read_text()
    marker = "rule triangleProgram =>"
    if verification.count(marker) != 1:
        raise SystemExit(f"expected exactly one {marker!r}")
    rhs_and_tail = verification.split(marker, 1)[1]
    if rhs_and_tail.count("endmodule") != 1:
        raise SystemExit("unexpected verification module structure")
    rule_rhs = rhs_and_tail.split("endmodule", 1)[0].strip()
    generated_normalized = remove_space(generated)
    rule_normalized = remove_space(rule_rhs)
    print(f"generated constructor term: {generated_normalized}")
    print(f"triangleProgram RHS:       {rule_normalized}")
    print(
        "generated normalized sha256: "
        + hashlib.sha256(generated_normalized.encode()).hexdigest()
    )
    print(
        "rule RHS normalized sha256:   "
        + hashlib.sha256(rule_normalized.encode()).hexdigest()
    )
    print(f"constructor-token identity: {generated_normalized == rule_normalized}")
    if generated_normalized != rule_normalized:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
