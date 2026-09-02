#!/usr/bin/env python3
"""Invoke the trusted Stage 4 check_generation entry point and save its return."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_preflight import check_generation


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
Path("/audit-output/evidence/stage4-preflight-returned.json").write_text(
    rendered,
    encoding="utf-8",
)
print(rendered, end="")
