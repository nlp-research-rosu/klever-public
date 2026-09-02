#!/usr/bin/env python3
"""Split an unlabeled multi-claim K spec into one module per exact claim."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} SPEC.k OUTPUT_DIR")
        return 2
    source_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    text = source_path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^  claim\s*$", text)
    if match is None:
        raise ValueError("no claims found")
    prefix = text[: match.start()]
    claim_region = text[match.start() :]
    if not claim_region.rstrip().endswith("endmodule"):
        raise ValueError("expected final endmodule")
    claim_region = re.sub(r"(?m)^endmodule\s*$", "", claim_region).rstrip()
    claims = re.split(r"(?m)(?=^  claim\s*$)", claim_region)
    claims = [claim.rstrip() for claim in claims if claim.strip()]

    out_dir.mkdir(parents=True, exist_ok=True)
    for index, claim in enumerate(claims, 1):
        module_name = f"EAT-SPEC-BRANCH-{index}"
        branch_prefix = re.sub(
            r"(?m)^module EAT-SPEC\s*$", f"module {module_name}", prefix
        )
        output = out_dir / f"spec-branch-{index}.k"
        output.write_text(branch_prefix + claim + "\nendmodule\n", encoding="utf-8")
        print(f"branch={index} module={module_name} output={output}")
    print(f"claim_count={len(claims)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
