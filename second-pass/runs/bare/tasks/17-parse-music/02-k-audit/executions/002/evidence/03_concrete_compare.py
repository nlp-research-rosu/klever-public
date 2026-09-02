#!/usr/bin/env python3
"""Execute the fresh LLVM semantics and compare results with both Python programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


canonical = load_function(SCRATCH / "trusted-canonical.py", "trusted_canonical_k")
submitted = load_function(SCRATCH / "solution.py", "submitted_solution_k")

inputs = [
    "o o| .| o| o| .| .| .| .| o o",
    "o",
    "o|",
    ".|",
    "",
    " ",
    "o  o|",
    " o| .| ",
]

for input_string in inputs:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        "audit-semantic-kompiled",
        f"-cINPUT={json.dumps(input_string)}",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        capture_output=True,
        check=False,
    )
    combined = completed.stdout + completed.stderr
    result_match = re.search(r"<result>\s*(.*?)\s*</result>", combined, re.S)
    assert result_match is not None, combined
    result_text = result_match.group(1)
    k_result = [
        int(value)
        for value in re.findall(r"pyInt\s*\(\s*(-?\d+)\s*\)", result_text)
    ]
    submitted_result = submitted(input_string)
    canonical_result = canonical(input_string)
    print(
        f"input={input_string!r} exit={completed.returncode} "
        f"K={k_result!r} submitted_python={submitted_result!r} "
        f"canonical_python={canonical_result!r}"
    )
    assert completed.returncode == 0
    assert k_result == submitted_result

print("K_VS_SUBMITTED_PYTHON=PASS")
