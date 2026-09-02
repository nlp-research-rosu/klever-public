#!/usr/bin/env python3
"""Probe the generated semantics at the CPython recursion-limit divergence."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/73-smallest-change-fresh")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def outcome(function, values):
    try:
        return ("return", function(list(values)))
    except Exception as error:
        return ("exception", type(error).__name__, str(error))


values = [0] * 2000
k_input = " ".join("ListItem(0)" for _ in values)
command = [
    "krun",
    str(WORK / "solution.mpy"),
    f"-cINPUT={k_input}",
    "--definition",
    str(WORK / "semantic-kompiled-fresh"),
]
print("generated_command=krun solution.mpy -cINPUT=<ListItem(0) repeated 2000>")
print(f"generated_argv_input_length={len(command[2])}")
completed = subprocess.run(command, text=True, capture_output=True, timeout=180)
match = re.search(
    r"<result>\s*(-?[0-9]+)(?:\s*~>\s*\.K)?\s*</result>",
    completed.stdout,
)
k_value = int(match.group(1)) if match else None
canonical = load_function(Path("/reference/canonical.py"), "long_canonical")
candidate = load_function(Path("/candidate/solution.py"), "long_candidate")
canonical_outcome = outcome(canonical, values)
candidate_outcome = outcome(candidate, values)
print(f"input_length={len(values)}")
print(f"krun_exit_status={completed.returncode}")
print(f"krun_stdout_chars={len(completed.stdout)}")
print(f"krun_stderr={completed.stderr!r}")
print(f"k_result={k_value!r}")
print(f"canonical_python={canonical_outcome!r}")
print(f"candidate_python={candidate_outcome!r}")
same = (
    completed.returncode == 0
    and ("return", k_value) == canonical_outcome
    and ("return", k_value) == candidate_outcome
)
print(f"all_three_outcomes_equal={same}")
raise SystemExit(0 if same else 1)
