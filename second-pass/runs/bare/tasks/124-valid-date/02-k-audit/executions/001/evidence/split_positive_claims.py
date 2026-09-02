#!/usr/bin/env python3
"""Split each submitted reachability claim into an independently runnable spec."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate-src/spec.k")
OUTPUT = Path("/audit-output/evidence/positive_claims")


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if re.match(r"^  claim\b", line)]
    claims: list[dict[str, object]] = []
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for ordinal, start in enumerate(starts, start=1):
        next_start = starts[ordinal] if ordinal < len(starts) else len(lines)
        end = next_start
        while end > start and (
            lines[end - 1].strip() == ""
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        body = "".join(lines[start:end]).rstrip() + "\n"
        module = f"AUDIT-CLAIM-{ordinal:03d}"
        text = (
            'requires "/tmp/audit-work/candidate-src/verification.k"\n\n'
            f"module {module}\n"
            "  imports VALID-DATE-VERIFICATION\n\n"
            f"{body}"
            "endmodule\n"
        )
        path = OUTPUT / f"claim-{ordinal:03d}.k"
        path.write_text(text, encoding="utf-8")
        claims.append(
            {
                "ordinal": ordinal,
                "source_start_line": start + 1,
                "source_end_line": end,
                "module": module,
                "file": str(path),
                "claim_sha256": hashlib.sha256(body.encode()).hexdigest(),
            }
        )

    (OUTPUT / "manifest.json").write_text(
        json.dumps(
            {"source": str(SOURCE), "claim_count": len(claims), "claims": claims},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"split {len(claims)} claims into {OUTPUT}")


if __name__ == "__main__":
    main()
