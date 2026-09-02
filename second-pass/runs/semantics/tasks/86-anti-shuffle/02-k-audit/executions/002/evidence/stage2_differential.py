#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 86."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
CONFIG = Path("/audit-output/evidence/stage2-differential-inputs.json")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    with CONFIG.open("r", encoding="utf-8") as stream:
        config = json.load(stream)

    canonical = load_module("trusted_canonical", ROOT / "canonical.py")
    generated = load_module("generated_solution", ROOT / "solution.py")

    cases: list[tuple[str, str]] = []
    for value in config["documented_examples"]:
        cases.append(("documented", value))
    for value in config["named_boundaries"]:
        cases.append(("boundary", value))

    exhaustive = config["exhaustive"]
    alphabet = exhaustive["alphabet"]
    for length in range(exhaustive["maximum_length"] + 1):
        for chars in itertools.product(alphabet, repeat=length):
            cases.append(("exhaustive", "".join(chars)))

    random_config = config["random"]
    rng = random.Random(random_config["seed"])
    random_alphabet = random_config["alphabet"]
    for _ in range(random_config["count"]):
        length = rng.randint(
            random_config["minimum_length"], random_config["maximum_length"]
        )
        cases.append(
            ("random", "".join(rng.choice(random_alphabet) for _ in range(length)))
        )

    counts: dict[str, int] = {}
    input_hash = hashlib.sha256()
    mismatches: list[tuple[str, str, object, object]] = []
    for category, value in cases:
        counts[category] = counts.get(category, 0) + 1
        encoded = value.encode("utf-8", errors="surrogatepass")
        input_hash.update(len(encoded).to_bytes(8, "big"))
        input_hash.update(encoded)
        try:
            expected: object = ("return", canonical.anti_shuffle(value))
        except Exception as err:
            expected = ("raise", type(err).__name__, str(err))
        try:
            actual: object = ("return", generated.anti_shuffle(value))
        except Exception as err:
            actual = ("raise", type(err).__name__, str(err))
        if expected != actual:
            mismatches.append((category, value, expected, actual))

    for value in config["documented_examples"] + config["named_boundaries"]:
        print(
            "NAMED "
            f"input={value!r} "
            f"canonical={canonical.anti_shuffle(value)!r} "
            f"generated={generated.anti_shuffle(value)!r}"
        )
    print(f"COUNTS={json.dumps(counts, sort_keys=True)}")
    print(f"TOTAL_CASES={len(cases)}")
    print(f"ORDERED_INPUT_SHA256={input_hash.hexdigest()}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
