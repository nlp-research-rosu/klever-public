#!/usr/bin/env python3
"""Mechanically check that verification.k's named program is solution.mpy."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/72-will-it-fly")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"could not extract {label}")
    return match.group(1).strip()


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    submitted = compact((WORK / "solution.mpy").read_text(encoding="utf-8"))

    result_rhs = extract(
        r"rule\s+willItFlyResult\s*=>\s*(.*?)\n\s*// The translated entry",
        verification,
        "willItFlyResult",
    )
    module_rhs = extract(
        r"rule\s+willItFlyModule\s*=>\s*(.*?)\n\s*syntax Val",
        verification,
        "willItFlyModule",
    )
    closure_rhs = extract(
        r"rule\s+willItFlyClosure\s*=>\s*(.*?)\n\s*endmodule",
        verification,
        "willItFlyClosure",
    )

    expanded_module = compact(module_rhs).replace(
        "willItFlyResult", compact(result_rhs)
    )
    expected_closure = compact(
        f'closureVal(("q","w"),Return({result_rhs}),0)'
    )
    expanded_closure = compact(closure_rhs).replace(
        "willItFlyResult", compact(result_rhs)
    )

    print(f"submitted_mpy_compact_sha256={digest(submitted)}")
    print(f"expanded_module_compact_sha256={digest(expanded_module)}")
    print(f"expanded_closure_compact_sha256={digest(expanded_closure)}")
    print(f"expected_closure_compact_sha256={digest(expected_closure)}")
    print(f"module_equals_submitted={expanded_module == submitted}")
    print(f"closure_equals_loaded_body={expanded_closure == expected_closure}")
    assert expanded_module == submitted
    assert expanded_closure == expected_closure
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
