#!/usr/bin/env python3
"""Split candidate spec.k into one reviewer-generated K module per claim."""

from __future__ import annotations

from pathlib import Path

SOURCE = Path("/tmp/audit-work/25-factorize-audit/source/spec.k")
OUTPUT_DIR = Path("/tmp/audit-work/25-factorize-audit/source")

lines = SOURCE.read_text().splitlines()
starts = [index for index, line in enumerate(lines) if line.startswith("  claim ")]
if len(starts) != 26:
    raise SystemExit(f"expected 26 claims, found {len(starts)}")

for claim_number, start in enumerate(starts, start=1):
    next_start = starts[claim_number] if claim_number < len(starts) else len(lines) - 1
    block = lines[start:next_start]
    while block and not block[-1].strip():
        block.pop()
    module_name = f"AUDIT-SPEC-{claim_number:02d}"
    output = OUTPUT_DIR / f"audit-claim-{claim_number:02d}.k"
    rendered = [
        'requires "verification.k"',
        "",
        f"module {module_name}",
        "  imports VERIFICATION",
        "",
        *block,
        "endmodule",
        "",
    ]
    output.write_text("\n".join(rendered))
    print(
        f"{claim_number:02d} source_line={start + 1} "
        f"module={module_name} file={output.name} head={lines[start].strip()}"
    )

