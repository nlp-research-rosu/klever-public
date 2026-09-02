#!/usr/bin/env python3
"""Show that the body mutation is wrong on a satisfying intended input."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("mutated")
    args = parser.parse_args()
    canonical = load_entry(Path(args.canonical), "body_mutation_canonical")
    mutated = load_entry(Path(args.mutated), "body_mutation_generated")
    witness = "("
    print(f"input={witness!r}")
    print(f"canonical={canonical(witness)!r}")
    print(f"mutated={mutated(witness)!r}")
    # Success means the test has demonstrated the intended divergence.
    return 0 if canonical(witness) != mutated(witness) else 1


if __name__ == "__main__":
    raise SystemExit(main())
