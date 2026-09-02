#!/usr/bin/env python3
"""Split each submitted positive claim into an independently runnable spec."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path("/tmp/audit-work/146-specialFilter/candidate/spec.k")
OUT = Path("/tmp/audit-work/146-specialFilter/positive-claims")


def main() -> int:
    lines = SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line.startswith("  claim ")]
    endmodule = next(index for index, line in enumerate(lines) if line.strip() == "endmodule")
    starts.append(endmodule)
    OUT.mkdir(parents=True, exist_ok=True)

    for ordinal, (start, stop) in enumerate(zip(starts, starts[1:]), 1):
        while stop > start and (
            not lines[stop - 1].strip() or lines[stop - 1].lstrip().startswith("//")
        ):
            stop -= 1
        module = f"AUDIT-SPEC-{ordinal:02d}"
        body = "".join(lines[start:stop])
        artifact = (
            'requires "../candidate/verification.k"\n\n'
            f"module {module}\n"
            "  imports VERIFICATION\n\n"
            f"{body}"
            "endmodule\n"
        )
        target = OUT / f"claim-{ordinal:02d}.k"
        target.write_text(artifact, encoding="utf-8")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        source_line = start + 1
        print(
            f"claim={ordinal:02d} module={module} source_line={source_line} "
            f"path={target} sha256={digest}"
        )
    print(f"claim_count={len(starts) - 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
