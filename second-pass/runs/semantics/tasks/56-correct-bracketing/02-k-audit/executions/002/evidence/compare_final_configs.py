#!/usr/bin/env python3
"""Compare fixed-LLVM and bridge-enabled-Haskell concrete final states."""

from __future__ import annotations

import re
from pathlib import Path


def final_configuration(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"<generatedTop>.*?</generatedTop>", text, re.DOTALL)
    if match is None:
        raise ValueError(f"no final configuration in {path}")
    return "".join(match.group(0).split())


fixed = final_configuration(
    Path("/audit-output/evidence/stage3_krun_concrete.log")
)
extended = final_configuration(
    Path("/audit-output/evidence/stage5_extended_concrete.log")
)
print(f"fixed_normalized_length={len(fixed)}")
print(f"extended_normalized_length={len(extended)}")
print(f"final_configurations_equal={fixed == extended}")
if fixed != extended:
    raise SystemExit(1)
