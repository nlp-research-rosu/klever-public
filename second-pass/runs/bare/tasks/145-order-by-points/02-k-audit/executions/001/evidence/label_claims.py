#!/usr/bin/env python3
"""Create a mechanically labeled copy of every unmodified positive claim."""

from pathlib import Path

source = Path("/tmp/audit-work/proof145/spec.k")
target = Path("/tmp/audit-work/proof145/spec-audit-labeled.k")
text = source.read_text(encoding="utf-8")
text = text.replace("module SPEC\n", "module SPEC-AUDIT\n", 1)
text = text.replace("endmodule\n", "endmodule\n", 1)
lines = []
count = 0
for line in text.splitlines(keepends=True):
    if line.startswith("  claim "):
        count += 1
        line = line.replace(
            "  claim ", f"  claim [audit-{count:02d}]: ", 1
        )
    lines.append(line)
if count != 13:
    raise SystemExit(f"expected 13 claims, found {count}")
target.write_text("".join(lines), encoding="utf-8")
print(f"wrote={target} claims={count}")
