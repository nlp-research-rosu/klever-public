#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def contract_oracle(n: int) -> list[int]:
    """Direct, independent reading of the prompt's one-based contract."""
    answer: list[int] = []
    for index in range(1, n + 1):
        if index % 2 == 0:
            value = 1
            for factor in range(1, index + 1):
                value *= factor
        else:
            value = sum(range(1, index + 1))
        answer.append(value)
    return answer


def compact(value: list[int]) -> str:
    encoded = json.dumps(value, separators=(",", ":")).encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if len(value) <= 12:
        return f"value={value!r} sha256={digest}"
    return (
        f"len={len(value)} head={value[:4]!r} tail={value[-4:]!r} "
        f"sha256={digest}"
    )


def main() -> int:
    trusted = load_entry(
        Path("/tmp/audit-work/106-f/reference/canonical.py"), "trusted_canonical"
    )
    generated = load_entry(
        Path("/tmp/audit-work/106-f/source/solution.py"), "generated_solution"
    )

    # 0 is the empty-list boundary; 1/2/3 cross the loop and odd/even branches.
    # 0..40 exercises every successive parity boundary, with broader size samples.
    inputs = list(range(0, 41)) + [50, 75, 100]
    print(f"INPUT_DOMAIN: nonnegative Python ints")
    print(f"INPUTS: {inputs}")
    print("DOCUMENTED_EXAMPLE: n=5 expected=[1, 2, 6, 24, 15]")
    mismatches = 0
    for n in inputs:
        canonical_value = trusted(n)
        generated_value = generated(n)
        oracle_value = contract_oracle(n)
        same = canonical_value == generated_value == oracle_value
        if not same:
            mismatches += 1
        print(
            f"n={n} same={same} canonical={compact(canonical_value)} "
            f"generated={compact(generated_value)} oracle={compact(oracle_value)}"
        )
    print(f"MISMATCH_COUNT: {mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
