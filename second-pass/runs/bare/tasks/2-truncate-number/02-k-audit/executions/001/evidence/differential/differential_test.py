#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import math
import pathlib
import random
import struct
import sys


CANONICAL_PATH = pathlib.Path("/reference/canonical.py")
GENERATED_PATH = pathlib.Path("/tmp/audit-work/source/solution.py")
RANDOM_SEED = 0x2A11D17
RANDOM_FINITE_CASES = 4096


def load_entry(path: pathlib.Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


def bits(value: float) -> int:
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def generated_inputs() -> list[tuple[str, float]]:
    cases: list[tuple[str, float]] = [
        ("prompt-example", 3.5),
        ("smallest-subnormal", float.fromhex("0x0.0000000000001p-1022")),
        ("largest-subnormal", float.fromhex("0x0.fffffffffffffp-1022")),
        ("smallest-normal", float.fromhex("0x1.0000000000000p-1022")),
        ("simple-fraction-0.1", 0.1),
        ("simple-fraction-0.5", 0.5),
        ("below-one", math.nextafter(1.0, 0.0)),
        ("one", 1.0),
        ("above-one", math.nextafter(1.0, math.inf)),
        ("below-two", math.nextafter(2.0, 0.0)),
        ("two", 2.0),
        ("above-two", math.nextafter(2.0, math.inf)),
        ("below-2**52", math.nextafter(float(2**52), 0.0)),
        ("2**52", float(2**52)),
        ("above-2**52", math.nextafter(float(2**52), math.inf)),
        ("2**53", float(2**53)),
        ("large-finite", 1.0e300),
        ("max-finite", sys.float_info.max),
    ]

    # Exercise both sides and the exact point of many int-truncation boundaries.
    for integer in list(range(1, 129)) + [255, 256, 257, 1023, 1024, 1025]:
        exact = float(integer)
        cases.extend(
            [
                (f"below-integer-{integer}", math.nextafter(exact, 0.0)),
                (f"integer-{integer}", exact),
                (f"above-integer-{integer}", math.nextafter(exact, math.inf)),
            ]
        )

    rng = random.Random(RANDOM_SEED)
    accepted = 0
    while accepted < RANDOM_FINITE_CASES:
        raw = rng.getrandbits(63)  # positive-sign IEEE-754 binary64
        value = struct.unpack(">d", struct.pack(">Q", raw))[0]
        if value > 0.0 and math.isfinite(value):
            cases.append((f"random-bits-{raw:016x}", value))
            accepted += 1

    # Dedupe by exact binary64 value while retaining the first descriptive label.
    seen: set[int] = set()
    unique: list[tuple[str, float]] = []
    for label, value in cases:
        raw = bits(value)
        if raw not in seen:
            seen.add(raw)
            unique.append((label, value))
    return unique


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "audit_trusted_canonical")
    generated = load_entry(GENERATED_PATH, "audit_generated_solution")
    cases = generated_inputs()
    mismatches = 0

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print("intended_domain=positive finite CPython binary64 floats")
    print("empty_case=not applicable; function input is a scalar float")
    print(f"random_seed={RANDOM_SEED}")
    print(f"requested_random_finite_cases={RANDOM_FINITE_CASES}")
    print(f"unique_total_cases={len(cases)}")

    for index, (label, value) in enumerate(cases):
        canonical_error = generated_error = None
        try:
            expected = canonical(value)
        except Exception as error:  # evidence must expose exception divergence
            expected = None
            canonical_error = f"{type(error).__name__}: {error}"
        try:
            actual = generated(value)
        except Exception as error:
            actual = None
            generated_error = f"{type(error).__name__}: {error}"

        same = (
            canonical_error == generated_error
            and (
                canonical_error is not None
                or (
                    isinstance(expected, float)
                    and isinstance(actual, float)
                    and bits(expected) == bits(actual)
                )
            )
        )
        if not same:
            mismatches += 1

        print(
            f"CASE {index:04d} label={label} input={value!r} "
            f"input_bits={bits(value):016x} expected={expected!r} "
            f"actual={actual!r} canonical_error={canonical_error!r} "
            f"generated_error={generated_error!r} same={same}"
        )

    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
