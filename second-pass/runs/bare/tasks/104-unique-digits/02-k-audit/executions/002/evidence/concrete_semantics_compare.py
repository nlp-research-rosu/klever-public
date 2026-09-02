#!/usr/bin/env python3
"""Compare freshly compiled K execution with both Python implementations."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable


SOURCE = Path("/tmp/audit-work/104-unique-digits-audit-002/source")
DEFINITION = Path("/tmp/audit-work/104-unique-digits-audit-002/concrete-kompiled")


def load_function(module_name: str, path: Path) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load_function("trusted_canonical_for_k_compare", Path("/reference/canonical.py"))
candidate = load_function("candidate_for_k_compare", SOURCE / "solution.py")


def invoke(function: Callable[[list[int]], list[int]], values: list[int]) -> tuple[str, object]:
    try:
        return ("value", function(values))
    except BaseException as error:
        return ("exception", type(error).__name__)


def int_seq(values: list[int]) -> str:
    result = ".Ints"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def run_k(values: list[int]) -> tuple[str, object, str]:
    args_term = f"pyList({int_seq(values)})"
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARGS={args_term}",
    ]
    completed = subprocess.run(
        command,
        cwd=SOURCE,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        return ("exception", f"krun-exit-{completed.returncode}", completed.stderr[-500:])
    numbers = [int(token) for token in re.findall(r"(?<![A-Za-z0-9_])-?\d+", completed.stdout)]
    return ("value", numbers, completed.stdout)


def summarize(result: tuple[str, object]) -> str:
    kind, payload = result
    if kind != "value":
        return f"{kind}:{payload}"
    assert isinstance(payload, list)
    lengths = [len(str(value)) for value in payload]
    digest = hashlib.sha256(",".join(map(str, payload)).encode()).hexdigest()[:16]
    sample = payload if max(lengths, default=0) <= 50 else []
    return f"value(len={len(payload)},digit_lengths={lengths},sample={sample},sha256[:16]={digest})"


cases = [
    ("empty", []),
    ("prompt-example-1", [15, 33, 1422, 1]),
    ("predicate-branches", [1, 2, 9, 10, 11, 12, 21]),
    ("duplicates", [97531, 7, 111, 97531]),
    ("recursion-boundary-995-digits", [int("1" * 995)]),
]

failures = 0
for name, values in cases:
    trusted = invoke(canonical, values)
    generated = invoke(candidate, values)
    k_kind, k_payload, raw_output = run_k(values)
    k_result = (k_kind, k_payload)
    k_matches_canonical = k_result == trusted
    k_matches_candidate = k_result == generated
    print(
        f"CASE {name}: K={summarize(k_result)} "
        f"canonical={summarize(trusted)} candidate={summarize(generated)}"
    )
    print(
        f"  krun_exit=0 output_bytes={len(raw_output.encode())} "
        f"K_matches_canonical={k_matches_canonical} K_matches_candidate={k_matches_candidate}"
    )
    if not k_matches_canonical:
        failures += 1

print("COMMAND_RECIPE: krun solution.mpy --definition "
      "/tmp/audit-work/104-unique-digits-audit-002/concrete-kompiled "
      "-cARGS=pyList(<case IntSeq encoded by this preserved script>)")
print(f"CASES={len(cases)} K_CANONICAL_MISMATCHES={failures}")
sys.exit(1 if failures else 0)
