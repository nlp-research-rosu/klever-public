#!/usr/bin/env python3
"""Rerun the trusted checker and compare its result to both signed copies."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_preflight import check_generation


def load(path: Path) -> dict:
    result = json.loads(path.read_text())
    if not isinstance(result, dict):
        raise TypeError(f"{path} is not a JSON object")
    return result


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
recorded = load(Path("/reference/klean-generation/preflight.json"))
signed = load(Path("/audit-input.json"))["resolution"]["stage4_preflight"]
print(
    json.dumps(
        {
            "returned": result,
            "matches_recorded_preflight": result == recorded,
            "matches_signed_audit_preflight": result == signed,
        },
        indent=2,
        sort_keys=True,
    )
)
