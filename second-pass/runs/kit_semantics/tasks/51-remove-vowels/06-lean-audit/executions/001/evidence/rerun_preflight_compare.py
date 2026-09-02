#!/usr/bin/env python3
"""Rerun preflight and compare deterministic fields and normalized diagnostics."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.klean_preflight import check_generation


def deterministic_part(document: dict) -> dict:
    return {key: value for key, value in document.items() if key != "diagnostics"}


def normalized_diagnostics(document: dict) -> list[dict]:
    normalized = []
    for entry in document["diagnostics"]:
        normalized.append({
            "command": entry["command"],
            "exit_code": entry["exit_code"],
            "output_lines": sorted(
                re.sub(r"^✔ \[\d+/\d+\] ", "", line)
                for line in entry["output_tail"].splitlines()
            ),
        })
    return normalized


def main() -> None:
    result = check_generation(
        Path("/reference/k-proof"),
        Path("/reference/lemma-discovery.json"),
        Path("/reference/klean-generation"),
        toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    )
    recorded = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
    launcher = json.loads(Path("/audit-input.json").read_text())["resolution"]["stage4_preflight"]
    print("RETURNED_PREFLIGHT")
    print(json.dumps(result, indent=2, sort_keys=True))
    deterministic_match = (
        deterministic_part(result) == deterministic_part(recorded)
        and deterministic_part(result) == deterministic_part(launcher)
    )
    diagnostic_match = (
        normalized_diagnostics(result) == normalized_diagnostics(recorded)
        and normalized_diagnostics(result) == normalized_diagnostics(launcher)
    )
    print(f"DETERMINISTIC_FIELDS_MATCH={deterministic_match}")
    print(f"NORMALIZED_DIAGNOSTICS_MATCH={diagnostic_match}")
    print("NOTE=raw lake build output order may vary between independent modules")
    if not deterministic_match or not diagnostic_match:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
