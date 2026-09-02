#!/usr/bin/env python3
"""Invoke the trusted Stage 4 check_generation function without mutation."""

import json
from pathlib import Path

from tools.klean_preflight import check_generation


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
