#!/usr/bin/env python3
"""Show the concrete equal-extrema behavior of both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def show(label: str, function) -> None:
    values = [2.0, 2.0]
    try:
        print(f"{label}: RETURN {function(values)!r}")
    except BaseException as error:
        print(f"{label}: RAISE {type(error).__name__}: {error}")


def main() -> None:
    show(
        "trusted-canonical",
        load(
            "canonical_boundary",
            Path("/tmp/audit-work/21-rescale-to-unit/trusted-canonical.py"),
        ),
    )
    show(
        "generated-solution",
        load(
            "solution_boundary",
            Path("/tmp/audit-work/21-rescale-to-unit/solution.py"),
        ),
    )


if __name__ == "__main__":
    main()
