#!/usr/bin/env python3
"""Ground the formal postcondition on satisfying entry configurations."""

from __future__ import annotations

import importlib.util
import math
import re
import subprocess
from pathlib import Path
from typing import Callable

work = Path("/tmp/audit-work/reconstruction")


def load(path: Path, name: str) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


candidate = load(work / "solution.py", "ground_candidate")
canonical = load(Path("/reference/canonical.py"), "ground_canonical")
cases = [(25, 15), (-25, 15), (25, -15), (0, 0), (-1, 0)]
mismatches: list[tuple[int, int, int, int]] = []

for index, (a, b) in enumerate(cases):
    formal_path = work / f"ground-postcondition-{index}.int"
    formal_path.write_text(f"gcdSpec(normInt({a}), normInt({b}))\n")
    command = [
        "krun",
        formal_path.name,
        "--definition",
        "gcd-eval-haskell-audit",
    ]
    print("COMMAND:", " ".join(command))
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT_STATUS: {completed.returncode}")
    print(completed.stdout.rstrip())
    if completed.returncode != 0:
        raise SystemExit(f"formal postcondition did not execute for {(a, b)}")
    matched = re.search(r"<k>\s*(-?[0-9]+) ~> \.K\s*</k>", completed.stdout)
    if matched is None:
        raise SystemExit(f"formal result did not reduce to an integer for {(a, b)}")
    formal = int(matched.group(1))
    generated = candidate(a, b)
    trusted = canonical(a, b)
    contract = math.gcd(a, b)
    print(
        f"COMPARISON input=({a},{b}) formal={formal} generated={generated} "
        f"canonical={trusted} math.gcd={contract}"
    )
    if formal != generated or formal != contract:
        mismatches.append((a, b, formal, generated))

print(f"satisfying_entry_state_count={len(cases)}")
print(f"formal_vs_generated_or_contract_mismatch_count={len(mismatches)}")
if mismatches:
    raise SystemExit(f"ground postcondition mismatches: {mismatches}")
