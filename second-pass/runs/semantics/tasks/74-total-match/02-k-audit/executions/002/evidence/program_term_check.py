#!/usr/bin/env python3
"""Mechanical normalized-constructor comparison for the claimed closure body."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/74-total-match")


def normalize(text: str) -> str:
    # Whitespace is not material in these constructor terms.
    compact = re.sub(r"\s+", "", text)
    # The MPY Stmts list unit can be printed explicitly in K source or omitted
    # between constructor separators by the translator's surface syntax.
    return compact.replace(".Stmts", "")


translated = normalize((ROOT / "regenerated-solution.mpy").read_text())
prefix = 'Module(FuncDef("total_match",Params("lst1","lst2"),'
suffix = "))"
assert translated.startswith(prefix), translated
assert translated.endswith(suffix), translated
body = translated[len(prefix) : -len(suffix)]

expected_call = normalize(
    f"""
    Call(
      closureVal(
        ("lst1", "lst2"),
        {body},
        0),
      list(strVals(A)),
      list(strVals(B)))
    """
)
verification = normalize((ROOT / "verification.k").read_text())
occurrences = verification.count(expected_call)
print(f"TRANSLATED_MODULE_NORMALIZED {translated}")
print(f"EXTRACTED_BODY_NORMALIZED {body}")
print(f"EXPECTED_CALL_NORMALIZED {expected_call}")
print(f"EXPECTED_CALL_OCCURRENCES_IN_VERIFICATION {occurrences}")
print(f"PARAMETER_MAPPING_EXACT {translated.startswith(prefix)}")
raise SystemExit(0 if occurrences == 1 else 1)
