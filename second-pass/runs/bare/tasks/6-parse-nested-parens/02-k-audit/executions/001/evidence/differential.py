#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval/6."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable, Iterable


CANONICAL_PATH = Path(
    "/tmp/audit-work/6-parse-nested-parens/trusted/canonical.py"
)
CANDIDATE_PATH = Path(
    "/tmp/audit-work/6-parse-nested-parens/candidate-src/solution.py"
)


def load_entry(path: Path, module_name: str) -> Callable[[str], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


def balanced_groups(pairs: int) -> Iterable[str]:
    def visit(prefix: str, opened: int, closed: int) -> Iterable[str]:
        if opened == pairs and closed == pairs:
            yield prefix
            return
        if opened < pairs:
            yield from visit(prefix + "(", opened + 1, closed)
        if closed < opened:
            yield from visit(prefix + ")", opened, closed + 1)

    yield from visit("", 0, 0)


def test_cases() -> list[str]:
    documented_and_boundaries = [
        "(()()) ((())) () ((())()())",
        "",
        " ",
        "  ",
        "()",
        "(())",
        "() ()",
        "()  ()",
        " ()",
        "() ",
        " (()())  ((())) ",
        "(()(())((())))",
        "() (()) ((())) (((())))",
    ]
    groups = [
        group
        for pairs in range(1, 5)
        for group in balanced_groups(pairs)
    ]
    generated = list(groups)
    generated.extend(f"{left} {right}" for left in groups for right in groups)
    generated.extend(f"{left}  {right}" for left in groups[:8] for right in groups[:8])
    generated.extend(f" {group}" for group in groups)
    generated.extend(f"{group} " for group in groups)
    return list(dict.fromkeys(documented_and_boundaries + generated))


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    candidate = load_entry(CANDIDATE_PATH, "audited_candidate")
    cases = test_cases()
    mismatches = 0
    print(
        json.dumps(
            {
                "canonical": str(CANONICAL_PATH),
                "candidate": str(CANDIDATE_PATH),
                "scope": (
                    "documented example; empty/single/double/leading/trailing "
                    "space boundaries; every balanced group through four pairs; "
                    "all ordered pairs of those groups; representative repeated-"
                    "separator pairs"
                ),
                "case_count": len(cases),
            },
            sort_keys=True,
        )
    )
    for index, value in enumerate(cases):
        expected = canonical(value)
        actual = candidate(value)
        equal = expected == actual
        if not equal:
            mismatches += 1
        print(
            json.dumps(
                {
                    "index": index,
                    "input": value,
                    "canonical": expected,
                    "candidate": actual,
                    "equal": equal,
                },
                sort_keys=True,
            )
        )
    print(json.dumps({"mismatch_count": mismatches}, sort_keys=True))
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
