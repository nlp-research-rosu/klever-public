#!/usr/bin/env python3
"""Split the candidate's anonymous K claims into independently runnable specs."""

from __future__ import annotations

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")
source = (SCRATCH / "spec.k").read_text().splitlines()
starts = [index for index, line in enumerate(source) if line.strip() == "claim"]
end = next(index for index, line in enumerate(source) if line.strip() == "endmodule")
starts.append(end)

if len(starts) != 8:
    raise SystemExit(f"expected seven claims, found {len(starts) - 1}")

for number, (start, stop) in enumerate(zip(starts, starts[1:]), 1):
    module = f"SPEC-CLAIM-{number}"
    claim = source[start:stop]
    output = [
        'requires "verification.k"',
        "",
        f"module {module}",
        "  imports VERIFICATION",
        "",
        *claim,
        "endmodule",
        "",
    ]
    path = SCRATCH / f"spec-claim-{number}.k"
    path.write_text("\n".join(output))
    print(number, module, path, f"{len(claim)} claim-lines")
