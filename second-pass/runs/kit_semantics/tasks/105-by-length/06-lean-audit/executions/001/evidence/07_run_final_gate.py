#!/usr/bin/env python3
"""Run the trusted Stage 6 mechanical gate over the bound proof candidate."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import check_final


result = check_final(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    Path("/candidate"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    audit_input=Path("/audit-input.json"),
)
output = Path("/audit-output/evidence/07-final-mechanical-gate.json")
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
