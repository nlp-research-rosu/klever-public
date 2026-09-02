#!/usr/bin/env python3
"""Print concrete satisfying witnesses from both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    generated = load(
        Path("/tmp/audit-work/124-valid-date/solution.py"),
        "generated_witness",
    )
    for value in (
        "",
        "03-11-2000",
        "15-01-2012",
        "02-29-0000",
        "01-31-2000",
    ):
        print(
            f"input={value!r} "
            f"canonical={canonical(value)!r} "
            f"generated={generated(value)!r}"
        )


if __name__ == "__main__":
    main()
