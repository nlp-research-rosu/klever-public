#!/usr/bin/env python3
"""Ground every submitted entry claim against both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/124-valid-date")


def import_path(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = import_path("candidate_for_claims", ROOT / "candidate" / "solution.py")
canonical = import_path("canonical_for_claims", ROOT / "canonical.py")
text = (ROOT / "candidate" / "spec.k").read_text(encoding="utf-8")

pattern = re.compile(
    r'claim\s+<k>\s+runProgram\(solutionProgram,\s*"valid_date",\s*'
    r'vals\(strVal\(("(?:[^"\\]|\\.)*")\)\)\)\s*'
    r'=>\s*boolVal\((true|false)\)\s*</k>',
    re.MULTILINE,
)

claims = pattern.findall(text)
candidate_mismatches = 0
canonical_mismatches = 0
for encoded, expected_text in claims:
    value = json.loads(encoded)
    expected = expected_text == "true"
    candidate_result = candidate.valid_date(value)
    canonical_result = canonical.valid_date(value)
    candidate_equal = candidate_result == expected
    canonical_equal = canonical_result == expected
    candidate_mismatches += int(not candidate_equal)
    canonical_mismatches += int(not canonical_equal)
    print(
        f"WITNESS input={value!r} claimed={expected!r} "
        f"candidate_python={candidate_result!r} canonical_python={canonical_result!r} "
        f"candidate_equal={candidate_equal} canonical_equal={canonical_equal}"
    )

print(f"GROUND_ENTRY_CLAIMS={len(claims)}")
print(f"CANDIDATE_PYTHON_MISMATCHES={candidate_mismatches}")
print(f"CANONICAL_PYTHON_MISMATCHES={canonical_mismatches}")
raise SystemExit(0 if claims and candidate_mismatches == 0 else 1)
