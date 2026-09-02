#!/usr/bin/env python3
"""Run the trusted Stage 6 mechanical gate in classification-only mode."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import check_final


result = check_final(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    None,
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    audit_input=Path("/audit-input.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
