#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential for parse_music."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path) -> Callable[[str], list[int]]:
    spec = importlib.util.spec_from_file_location(f"audit_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


def observe(fn: Callable[[str], list[int]], value: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(value)}
    except Exception as exc:  # Preserve behavioral divergence, including exceptions.
        return {"kind": "raise", "type": type(exc).__name__, "message": str(exc)}


def build_cases() -> list[dict[str, str]]:
    cases: list[dict[str, str]] = [
        {
            "source": "documented-example",
            "input": "o o| .| o| o| .| .| .| .| o o",
        },
        {"source": "empty-boundary", "input": ""},
        {"source": "separator-only-one", "input": " "},
        {"source": "separator-only-two", "input": "  "},
        {"source": "branch-whole", "input": "o"},
        {"source": "branch-half", "input": "o|"},
        {"source": "branch-quarter", "input": ".|"},
        {"source": "leading-separator", "input": " o"},
        {"source": "trailing-separator", "input": "o "},
        {"source": "repeated-separator", "input": "o  .|"},
        {"source": "all-branch-transitions", "input": "o o| .| o| o .|"},
    ]
    tokens = ("o", "o|", ".|")
    formatters = (
        ("single-spaces", lambda xs: " ".join(xs)),
        ("leading-space", lambda xs: " " + " ".join(xs)),
        ("trailing-space", lambda xs: " ".join(xs) + " "),
        ("double-first-separator", lambda xs: "  ".join(xs)),
    )
    for length in range(1, 4):
        for seq in itertools.product(tokens, repeat=length):
            for name, formatter in formatters:
                cases.append(
                    {
                        "source": f"generated-{name}-length-{length}",
                        "input": formatter(seq),
                    }
                )
    # Preserve first occurrence and its source if two generators coincide.
    unique: dict[str, dict[str, str]] = {}
    for case in cases:
        unique.setdefault(case["input"], case)
    return list(unique.values())


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"))
    candidate = load_entry(Path("/tmp/audit-work/reconstruction/solution.py"))
    cases = build_cases()
    mismatches: list[dict[str, Any]] = []
    for index, case in enumerate(cases):
        expected = observe(canonical, case["input"])
        actual = observe(candidate, case["input"])
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    **case,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    encoded_inputs = json.dumps(cases, ensure_ascii=False, sort_keys=True).encode()
    print(f"case_count={len(cases)}")
    print(f"inputs_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
    print("inputs=" + json.dumps(cases, ensure_ascii=False))
    print(f"mismatch_count={len(mismatches)}")
    print("mismatches=" + json.dumps(mismatches, ensure_ascii=False))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
