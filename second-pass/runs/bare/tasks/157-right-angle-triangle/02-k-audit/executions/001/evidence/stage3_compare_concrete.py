#!/usr/bin/env python3
"""Compare fresh krun logs with CPython executions of both implementations."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import sys
from collections.abc import Callable
from typing import Any


RESULT_PATTERN = re.compile(r"result\s*\(\s*(true|false)\s*\)")


def load_entry(path: pathlib.Path, name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "right_angle_triangle")


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} CASES.json LOG_DIR CANONICAL.py CANDIDATE.py",
            file=sys.stderr,
        )
        return 64

    cases = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    log_dir = pathlib.Path(sys.argv[2])
    canonical = load_entry(pathlib.Path(sys.argv[3]), "stage3_canonical")
    candidate = load_entry(pathlib.Path(sys.argv[4]), "stage3_candidate")

    failures = 0
    for case in cases:
        args = case["args"]
        log_path = log_dir / f"stage3-krun-{case['name']}.log"
        log_text = log_path.read_text(encoding="utf-8")
        matches = RESULT_PATTERN.findall(log_text)
        if len(matches) != 1:
            raise RuntimeError(f"expected one K result in {log_path}, got {matches}")
        k_value = matches[0] == "true"
        candidate_value = candidate(*args)
        canonical_value = canonical(*args)
        row = {
            "name": case["name"],
            "args": args,
            "k": k_value,
            "candidate_python": candidate_value,
            "canonical_python": canonical_value,
            "k_matches_candidate": k_value == candidate_value,
            "candidate_matches_canonical": candidate_value == canonical_value,
        }
        print(json.dumps(row, sort_keys=True))
        if k_value != candidate_value:
            failures += 1
    print(json.dumps({"k_candidate_mismatches": failures}, sort_keys=True))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
