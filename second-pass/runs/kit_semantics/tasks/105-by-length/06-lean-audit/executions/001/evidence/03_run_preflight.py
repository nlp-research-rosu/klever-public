#!/usr/bin/env python3
"""Run the trusted Stage 4 generation preflight and save returned evidence."""

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
output = Path("/audit-output/evidence/03-klean-preflight-result.json")
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
