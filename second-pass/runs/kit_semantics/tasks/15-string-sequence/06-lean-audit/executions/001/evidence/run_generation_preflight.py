#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.klean_preflight import check_generation

result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
