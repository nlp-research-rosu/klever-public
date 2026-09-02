#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from tools.klean_preflight import check_generation


print(
    "CALL: tools.klean_preflight.check_generation("
    "Path('/reference/k-proof'), "
    "Path('/reference/lemma-discovery.json'), "
    "Path('/reference/klean-generation'), "
    "toolchain_lock=Path('/reference/klean-toolchain.lock.json'))"
)
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print("RETURN:")
print(json.dumps(result, indent=2, sort_keys=True))
