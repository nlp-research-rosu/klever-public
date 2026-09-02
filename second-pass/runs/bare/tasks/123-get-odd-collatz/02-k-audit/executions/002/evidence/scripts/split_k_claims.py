#!/usr/bin/env python3
"""Split candidate spec.k into one otherwise-identical spec module per claim."""

from __future__ import annotations

import re
from pathlib import Path


source_path = Path("/tmp/audit-work/candidate-src/spec.k")
destination = Path("/tmp/audit-work/candidate-src/individual-claims")
destination.mkdir(exist_ok=True)
text = source_path.read_text()
lines = text.splitlines(keepends=True)

claim_starts = [index for index, line in enumerate(lines) if re.match(r"^  claim(?:\s|$)", line)]
assert claim_starts, "no claims found"
module_index = next(index for index, line in enumerate(lines) if line.startswith("module SPEC"))
endmodule_index = next(index for index, line in enumerate(lines) if line.strip() == "endmodule")
prefix = lines[:module_index]

for ordinal, start in enumerate(claim_starts, 1):
    stop = claim_starts[ordinal] if ordinal < len(claim_starts) else endmodule_index
    module_name = f"SPEC-CLAIM-{ordinal:02d}"
    artifact = "".join(
        prefix
        + [f"module {module_name}\n", "  imports VERIFICATION\n\n"]
        + lines[start:stop]
        + ["endmodule\n"]
    )
    output = destination / f"spec-claim-{ordinal:02d}.k"
    output.write_text(artifact)
    print(f"{ordinal:02d} module={module_name} source_lines={start + 1}..{stop} path={output}")
print(f"claim_count={len(claim_starts)}")
