#!/usr/bin/env python3
"""Ground witness for the entry claim's unrestricted nested-integer domain."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


def main() -> None:
    canonical = load(Path("/reference/canonical.py"), "stage4_canonical")
    generated = load(
        Path("/tmp/audit-work/src/solution.py"),
        "stage4_generated",
    )
    matrix = [[2, 1, 2], [2], [1, 2, 1, 2]]
    x = 2
    expected = [(0, 2), (0, 0), (1, 0), (2, 3), (2, 1)]
    canonical_result = canonical(matrix, x)
    generated_result = generated(matrix, x)
    assert canonical_result == expected
    assert generated_result == expected
    print(f"RS_python={matrix!r}")
    print("RS_K=vCons(list([2,1,2]),vCons(list([2]),vCons(list([1,2,1,2]),.ValSeq)))")
    print(f"X={x}")
    print("listRows(RS)=true because each head is a list and the tail ends in .ValSeq")
    print(f"canonical={canonical_result!r}")
    print(f"generated={generated_result!r}")
    print(f"expected={expected!r}")
    print("match=true")


if __name__ == "__main__":
    main()
