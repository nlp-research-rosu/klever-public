#!/usr/bin/env python3
"""Combine the immutable candidate claims with the omitted entry obligation."""

from __future__ import annotations

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_combined_spec.py CANDIDATE-SPEC OMITTED-SPEC", file=sys.stderr)
        return 2
    candidate = Path(sys.argv[1]).read_text(encoding="utf-8")
    omitted = Path(sys.argv[2]).read_text(encoding="utf-8")

    candidate = candidate.replace("module SPEC\n", "module SPEC-COMBINED\n", 1)
    end_offset = candidate.rfind("endmodule")
    if end_offset < 0:
        raise RuntimeError("candidate spec lacks endmodule")
    candidate_prefix = candidate[:end_offset].rstrip()

    claim_start = omitted.index("  // The result-constraining theorem")
    claim_end = omitted.rfind("endmodule")
    if claim_end < claim_start:
        raise RuntimeError("omitted spec lacks endmodule")
    claim_text = omitted[claim_start:claim_end].rstrip()

    sys.stdout.write(candidate_prefix + "\n\n" + claim_text + "\nendmodule\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
