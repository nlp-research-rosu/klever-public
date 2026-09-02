#!/usr/bin/env python3
"""Run the over-broad fused-generator witness in Python and fresh K."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path


def main() -> int:
    source = Path("/tmp/audit-work/126-is-sorted/candidate-src/shadowing_witness.py")
    spec = importlib.util.spec_from_file_location("shadowing_witness", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import witness")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    python_outcome: str
    try:
        python_outcome = f"return:{module.is_sorted([1])!r}"
    except Exception as error:  # The exception class is the observable result.
        python_outcome = f"raise:{type(error).__name__}:{error}"

    command = [
        "krun",
        "/tmp/audit-work/126-is-sorted/candidate-src/shadowing_witness.mpy",
        "--definition",
        "/tmp/audit-work/126-is-sorted/candidate-src/concrete-kompiled",
        "-cARGS=PyList(Cons(1, Nil))",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    print("INPUT=[1]")
    print(f"PYTHON_OUTCOME={python_outcome}")
    print("COMMAND: " + " ".join(command))
    print(f"KRUN_EXIT={completed.returncode}")
    print("K_OUTCOME=" + (completed.stdout + completed.stderr).strip().replace("\n", "\\n"))
    # The witness succeeds when it exposes the discrepancy.
    exposed = (
        python_outcome.startswith("raise:AttributeError:")
        and completed.returncode == 0
        and "BoolVal ( true )" in completed.stdout
    )
    print(f"DISCREPANCY_EXPOSED={exposed}")
    return 0 if exposed else 1


if __name__ == "__main__":
    raise SystemExit(main())
