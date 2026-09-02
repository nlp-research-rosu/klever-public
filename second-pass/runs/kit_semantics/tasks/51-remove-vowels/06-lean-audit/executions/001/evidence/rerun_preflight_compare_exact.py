#!/usr/bin/env python3
"""Rerun trusted Stage 4 preflight and compare its full returned document."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_preflight import check_generation


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
    print(f"MATCHES_RECORDED_PREFLIGHT={result == recorded}")
    print(f"MATCHES_LAUNCHER_PREFLIGHT={result == launcher}")
    if result != recorded or result != launcher:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
