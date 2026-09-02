#!/usr/bin/env python3
"""Line-based exhaustive inventory of candidate-authored K declarations."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/4-mad-audit/candidate")
FILES = [ROOT / "semantic.k", ROOT / "verification.k", ROOT / "spec.k"]
START = re.compile(r"^\s*(module\b|endmodule\b|imports\b|requires\b|syntax\b|configuration\b|rule\b|claim\b)")


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = (starts[position + 1] - 1) if position + 1 < len(starts) else len(lines) - 1
        # Do not attach separating comments/blanks to the prior declaration.
        while end > start and (not lines[end].strip() or lines[end].lstrip().startswith("//")):
            end -= 1
        yield start + 1, end + 1, lines[start : end + 1]


def main() -> int:
    total_rules = 0
    total_claims = 0
    total_syntax = 0
    for path in FILES:
        print(f"FILE {path}")
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            if any(marker in line for marker in ["[function]", "[total]", "[functional]", "[opaque]", "[priority", "[simplification]"]):
                print(f"ATTRIBUTE line={line_number}: {line.strip()}")
        for start, end, block in blocks(path):
            kind = block[0].strip().split(maxsplit=1)[0]
            if kind == "rule":
                total_rules += 1
            elif kind == "claim":
                total_claims += 1
            elif kind == "syntax":
                total_syntax += 1
            normalized = " ".join(part.strip() for part in block if part.strip() and not part.lstrip().startswith("//"))
            print(f"DECL {kind} lines={start}-{end}: {normalized}")
    print(f"TOTAL syntax_declarations={total_syntax} rules={total_rules} claims={total_claims}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
