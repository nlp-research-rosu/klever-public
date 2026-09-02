#!/usr/bin/env python3
"""Compare fresh LLVM K execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


def k_input(text: str) -> str:
    words = ["lbr" if character == "[" else "rbr" for character in text]
    return " ".join(words + [".BString"])


candidate = load_entry(
    Path("/tmp/audit-work/source/solution.py"), "concrete_candidate"
)
canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "concrete_canonical"
)

cases = [
    "",
    "[",
    "]",
    "[[",
    "]]",
    "[]",
    "[[]",
    "[[]]",
    "[]]]]]]][[[[[]",
    "[[][]]",
    "[[]][[",
    "]]][[[]]]][[",
]

mismatches = 0
for text in cases:
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={k_input(text)}",
        "--definition",
        "semantic-kompiled",
    ]
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/source",
        text=True,
        capture_output=True,
        check=False,
    )
    matches = re.findall(
        r"boolVal\s*\(\s*(true|false)\s*\)",
        completed.stdout,
    )
    k_result = None if len(matches) != 1 else matches[0] == "true"
    candidate_result = candidate(text)
    canonical_result = canonical(text)
    agrees = (
        completed.returncode == 0
        and k_result is not None
        and k_result == candidate_result == canonical_result
    )
    print(f"INPUT {text!r}")
    print(f"COMMAND {shlex.join(command)}")
    print(f"EXIT_STATUS {completed.returncode}")
    print(
        "RESULT "
        f"K={k_result!r} candidate={candidate_result!r} "
        f"canonical={canonical_result!r} agrees={agrees}"
    )
    if not agrees:
        mismatches += 1
        print("STDOUT")
        print(completed.stdout)
        print("STDERR")
        print(completed.stderr)

print(f"TOTAL_CASES {len(cases)}")
print(f"MISMATCHES {mismatches}")
raise SystemExit(1 if mismatches else 0)
