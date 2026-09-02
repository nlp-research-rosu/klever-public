#!/usr/bin/env python3
import json
from pathlib import Path

from tools.klean_preflight import check_generation


evidence = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(evidence, indent=2, sort_keys=True))
