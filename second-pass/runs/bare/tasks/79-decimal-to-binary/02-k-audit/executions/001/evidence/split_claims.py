#!/usr/bin/env python3
"""Split each unchanged claim from spec.k into an independently runnable module."""

from __future__ import annotations

import hashlib
from pathlib import Path


SOURCE = Path("/tmp/audit-work/build-proof/spec.k")
OUTPUT_DIR = SOURCE.parent


def main() -> int:
    lines = SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line == "  claim\n"]
    if len(starts) != 5:
        raise RuntimeError(f"expected 5 claims, found {len(starts)}")
    ends = starts[1:] + [len(lines) - 1]
    for number, (start, end) in enumerate(zip(starts, ends), 1):
        body = "".join(lines[start:end]).rstrip() + "\n"
        module_name = f"AUDIT-SPEC-CLAIM-{number}"
        rendered = (
            'requires "verification.k"\n\n'
            f"module {module_name}\n"
            "  imports VERIFICATION\n\n"
            f"{body}"
            "endmodule\n"
        )
        output = OUTPUT_DIR / f"spec-claim-{number}.k"
        output.write_text(rendered, encoding="utf-8")
        digest = hashlib.sha256(body.encode()).hexdigest()
        print(
            f"{output}: unchanged claim body lines={body.count(chr(10))}; "
            f"sha256={digest}; module={module_name}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
