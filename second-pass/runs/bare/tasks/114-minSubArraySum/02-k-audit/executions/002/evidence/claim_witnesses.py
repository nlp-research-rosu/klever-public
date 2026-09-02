#!/usr/bin/env python3
"""Ground satisfying witnesses for all three universal claims."""

from __future__ import annotations

import importlib.util
import shlex
import subprocess
from pathlib import Path

DEFINITION = Path("/tmp/audit-work/build/verification-kompiled")
TERM_FILE = Path("/tmp/audit-work/source/claim-witness.kterm")
PARSER = (
    "kast --definition /tmp/audit-work/build/verification-kompiled "
    "--module VERIFICATION --sort Int --output kore"
)


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def int_list(values: list[int]) -> str:
    term = "nil"
    for value in reversed(values):
        term = f"cons({value}, {term})"
    return term


def evaluate(function: str, values: list[int]) -> tuple[int, str, list[str]]:
    TERM_FILE.write_text(f"{function}({int_list(values)})\n", encoding="utf-8")
    command = [
        "krun",
        str(TERM_FILE),
        "--definition",
        str(DEFINITION),
        "--term",
        "--parser",
        PARSER,
        "--output",
        "pretty",
    ]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    if completed.returncode:
        raise RuntimeError(completed.stdout)
    return int(completed.stdout.strip()), completed.stdout, command


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "canonical_claim_witness")
    generated = load_entry(Path("/tmp/audit-work/source/solution.py"), "generated_claim_witness")
    checks = [
        ("helper-claim", "minPrefix", [4, -5]),
        ("target-call-claim", "minSubarray", [4, -5]),
        ("end-to-end-claim", "minSubarray", [5, -2, -3, 7, -10, 4]),
    ]
    failures = 0
    for name, summary, values in checks:
        k_value, output, command = evaluate(summary, values)
        if summary == "minPrefix":
            python_value = min(sum(values[:end]) for end in range(1, len(values) + 1))
            canonical_value = None
        else:
            python_value = generated(list(values))
            canonical_value = canonical(list(values))
        agrees = k_value == python_value and (
            canonical_value is None or k_value == canonical_value
        )
        print(f"witness={name}")
        print(f"input={values!r}")
        print(f"satisfying_instantiation=H:{values[0]}, T:{int_list(values[1:])}")
        print(f"command={shlex.join(command)}")
        print(f"k_summary={k_value}")
        print(f"generated_or_brute_prefix={python_value}")
        print(f"canonical={canonical_value!r}")
        print(f"agrees={agrees}")
        print(f"raw_output={output!r}")
        failures += 0 if agrees else 1
    print(f"failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
