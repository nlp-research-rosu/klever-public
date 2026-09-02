#!/usr/bin/env python3
"""Evaluate the concrete satisfiable entry-claim witness with both Python functions."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse


def main() -> int:
    if len(sys.argv) != 3:
        return 64
    canonical = load(sys.argv[1], "canonical_witness")
    candidate = load(sys.argv[2], "candidate_witness")
    values = [1, 2, 3]
    delimiter = 4
    expected = [1, 4, 2, 4, 3]
    record = {
        "claim_substitution": {
            "IS": values,
            "D": delimiter,
            "KONT": ".K",
            "intersperseSpec(IS,D)": expected,
        },
        "canonical": canonical(values.copy(), delimiter),
        "candidate": candidate(values.copy(), delimiter),
    }
    print(json.dumps(record, sort_keys=True))
    return 0 if record["canonical"] == record["candidate"] == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
