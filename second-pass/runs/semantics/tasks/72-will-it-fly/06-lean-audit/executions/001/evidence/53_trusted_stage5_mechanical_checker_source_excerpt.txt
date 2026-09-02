#!/usr/bin/env python3
"""Model-free acceptance check for one Stage 5 Lean proof candidate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import klean_final_gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generation", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    arguments = parser.parse_args(argv)
    gate = subprocess.run(
        ["/usr/local/bin/assert-frozen-toolchain", "agent"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if gate.returncode != 0:
        result = {
            "status": "AUDIT_ERROR",
            "error": "frozen toolchain gate failed",
            "toolchain_output_tail": gate.stdout[-4000:],
        }
    else:
        result = klean_final_gate.evaluate_proof_candidate(
            arguments.generation, arguments.candidate
        )
        result["toolchain_gate"] = "PASS"
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
