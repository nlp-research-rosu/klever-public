#!/usr/bin/env python3
"""Evaluate every submitted concrete program claim in both Python implementations."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Callable


SPEC = Path("/tmp/audit-work/candidate-src/spec.k")
OUTPUT = Path("/audit-output/evidence/entry_claim_results.json")


def load_entry(path: str, name: str) -> Callable[[str], bool]:
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.valid_date


def call(entry: Callable[[str], bool], value: str) -> Any:
    try:
        return {"kind": "value", "value": entry(value)}
    except Exception as exc:
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}


def main() -> int:
    text = SPEC.read_text(encoding="utf-8")
    pattern = re.compile(
        r'claim\s+<k>\s+runProgram\(solutionProgram,\s*"valid_date",\s*'
        r'vals\(strVal\(("(?:[^"\\]|\\.)*")\)\)\)\s*'
        r'=>\s*boolVal\((true|false)\)\s*</k>',
        re.DOTALL,
    )
    generated = load_entry("/tmp/audit-work/candidate-src/solution.py", "audit_generated")
    canonical = load_entry("/reference/canonical.py", "audit_canonical")
    rows: list[dict[str, Any]] = []
    generated_mismatches = 0
    canonical_mismatches = 0
    for match in pattern.finditer(text):
        value = ast.literal_eval(match.group(1))
        expected = match.group(2) == "true"
        generated_result = call(generated, value)
        canonical_result = call(canonical, value)
        generated_matches = generated_result == {"kind": "value", "value": expected}
        canonical_matches = canonical_result == {"kind": "value", "value": expected}
        generated_mismatches += not generated_matches
        canonical_mismatches += not canonical_matches
        rows.append(
            {
                "source_line": text.count("\n", 0, match.start()) + 1,
                "input": value,
                "claimed": expected,
                "generated": generated_result,
                "canonical": canonical_result,
                "generated_matches_claim": generated_matches,
                "canonical_matches_claim": canonical_matches,
            }
        )
    result = {
        "claim_count": len(rows),
        "generated_mismatch_count": generated_mismatches,
        "canonical_mismatch_count": canonical_mismatches,
        "claims": rows,
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"claim_count={len(rows)} generated_mismatches={generated_mismatches} "
        f"canonical_mismatches={canonical_mismatches}"
    )
    for row in rows:
        if not row["canonical_matches_claim"] or not row["generated_matches_claim"]:
            print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return 1 if generated_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
