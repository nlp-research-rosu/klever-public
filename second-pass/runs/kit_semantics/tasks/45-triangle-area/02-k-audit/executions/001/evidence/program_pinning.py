#!/usr/bin/env python3
"""Mechanical constructor-level comparison of translated code and entry claims."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/45-triangle-area")


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    translated = normalize((ROOT / "solution.mpy").read_text())
    regenerated = normalize((ROOT / "solution.regenerated.mpy").read_text())
    spec = normalize((ROOT / "spec.k").read_text())
    exact_load_term = f"#loadAll({translated})"
    exact_load_count = spec.count(exact_load_term)
    labels = re.findall(r"claim\[([^]]+)\]:", spec)
    expected_labels = [
        "triangle-area-int-int",
        "triangle-area-int-float",
        "triangle-area-float-int",
        "triangle-area-float-float",
    ]
    print(f"translated_equals_regenerated={translated == regenerated}")
    print(f"normalized_translated={translated}")
    print(f"exact_translated_module_under_load_count={exact_load_count}")
    print(f"claim_labels={labels}")
    print(f"expected_claim_labels_present={labels == expected_labels}")
    success = (
        translated == regenerated
        and exact_load_count == 4
        and labels == expected_labels
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
