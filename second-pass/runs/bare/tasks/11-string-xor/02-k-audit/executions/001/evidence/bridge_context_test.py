#!/usr/bin/env python3
"""Compare fixed and bridge-extended execution with an observable suffix."""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path


FIXED = Path("/tmp/audit-work/11-string-xor-audit/bridge-context-fixed-kompiled")
EXTENDED = Path(
    "/tmp/audit-work/11-string-xor-audit/bridge-context-extended-kompiled"
)
CASES = [
    ("N-zero", "bridgeInput(0,2,seed(0),seed(2))"),
    ("M-zero", "bridgeInput(2,0,seed(1),seed(0))"),
    ("positive-step-equal-and-different", "bridgeInput(2,2,seed(1),seed(0))"),
]

failures = 0
for name, program in CASES:
    outputs = {}
    for variant, definition in (("fixed", FIXED), ("extended", EXTENDED)):
        command = [
            "krun",
            "--definition",
            str(definition),
            f"-cPGM={program}",
            "-cARGS=Args(str(empty),str(empty))",
            "--output",
            "pretty",
        ]
        print("COMMAND: " + shlex.join(command))
        result = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        outputs[variant] = {
            "exit": result.returncode,
            "normalized": "".join(result.stdout.split()),
            "raw": result.stdout,
        }
    equal = (
        outputs["fixed"]["exit"] == 0
        and outputs["extended"]["exit"] == 0
        and outputs["fixed"]["normalized"] == outputs["extended"]["normalized"]
        and "observed(" in outputs["fixed"]["normalized"]
    )
    print(
        json.dumps(
            {
                "case": name,
                "program": program,
                "fixed_exit": outputs["fixed"]["exit"],
                "extended_exit": outputs["extended"]["exit"],
                "same_observed_configuration": equal,
                "normalized_output": outputs["fixed"]["normalized"]
                if equal
                else None,
            },
            sort_keys=True,
        )
    )
    if not equal:
        failures += 1
        for variant in ("fixed", "extended"):
            print(f"{variant.upper()}_OUTPUT_BEGIN")
            print(outputs[variant]["raw"].rstrip())
            print(f"{variant.upper()}_OUTPUT_END")

print(json.dumps({"cases": len(CASES), "failures": failures}, sort_keys=True))
raise SystemExit(1 if failures else 0)
