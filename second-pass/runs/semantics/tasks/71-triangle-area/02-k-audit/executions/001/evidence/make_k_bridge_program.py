#!/usr/bin/env python3
"""Generate ground MPY assertions comparing concrete K execution to canonical Python."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load(path: Path) -> Callable[[int, int, int], Any]:
    spec = importlib.util.spec_from_file_location(f"k_bridge_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: make_k_bridge_program.py SOLUTION_PY CANONICAL_PY OUTPUT_PY MANIFEST",
            file=sys.stderr,
        )
        return 64

    solution_path, canonical_path, output_path, manifest_path = map(Path, sys.argv[1:])
    canonical = load(canonical_path)
    cases = list(itertools.product(range(-1, 4), repeat=3))
    rng = random.Random(710072)
    cases.extend(
        (rng.randint(0, 10**6), rng.randint(0, 10**6), rng.randint(0, 10**6))
        for _ in range(25)
    )

    assertions: list[str] = []
    for a, b, c in cases:
        expected = canonical(a, b, c)
        assertions.append(f"assert triangle_area({a!r}, {b!r}, {c!r}) == {expected!r}")

    source = solution_path.read_text(encoding="utf-8").rstrip()
    generated = source + "\n\n" + "\n".join(assertions) + "\n"
    output_path.write_text(generated, encoding="utf-8")
    manifest = {
        "oracle": str(canonical_path),
        "submitted_function_source": str(solution_path),
        "scope": {
            "exhaustive_integer_cube": "[-1,3]^3",
            "deterministic_random_nonnegative_integer_triples": 25,
        },
        "total_assertions": len(assertions),
        "generated_python_sha256": hashlib.sha256(generated.encode()).hexdigest(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
