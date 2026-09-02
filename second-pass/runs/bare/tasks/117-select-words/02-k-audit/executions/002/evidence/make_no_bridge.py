#!/usr/bin/env python3
"""Create a proof definition with the whole-expression evaluator removed."""

from __future__ import annotations

import re
import shutil
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")
TARGET = SCRATCH / "no-bridge"
TARGET.mkdir(exist_ok=True)

semantic = (SCRATCH / "semantic.k").read_text()
pattern = re.compile(
    r"\n  rule eval\(\n"
    r".*?"
    r"\n       => pyList\(filterWords\(words\(S\), N\)\)\n",
    flags=re.DOTALL,
)
semantic_without_bridge, count = pattern.subn("\n", semantic)
if count != 1:
    raise SystemExit(f"expected one whole-expression bridge, removed {count}")

(TARGET / "semantic.k").write_text(semantic_without_bridge)
for name in ("verification.k", "spec-claim-1.k", "solution.mpy"):
    shutil.copy2(SCRATCH / name, TARGET / name)

print("target", TARGET)
print("removed-whole-expression-eval-rules", count)
print("remaining-eval-rules", semantic_without_bridge.count("rule eval("))
