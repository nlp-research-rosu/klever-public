#!/usr/bin/env python3
"""Ground the submitted Boolean claim against both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


def main() -> int:
    values = [True, 7, None, "x", 9]
    formal_claim_result = [7, 9]
    canonical_result = load(
        Path("/reference/canonical.py"), "ground_canonical"
    )(values)
    submitted_result = load(
        Path("/candidate/solution.py"), "ground_submitted"
    )(values)
    print(f"satisfying_input={values!r}")
    print(f"formal_order_and_scalars_postcondition={formal_claim_result!r}")
    print(f"trusted_canonical_result={canonical_result!r}")
    print(f"submitted_python_result={submitted_result!r}")
    print(f"canonical_matches_formal={canonical_result == formal_claim_result}")
    print(f"submitted_matches_formal={submitted_result == formal_claim_result}")
    print(f"python_implementations_agree={canonical_result == submitted_result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
