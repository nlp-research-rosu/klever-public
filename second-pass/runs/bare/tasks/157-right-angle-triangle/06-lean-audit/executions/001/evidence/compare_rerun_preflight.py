#!/usr/bin/env python3
import json
from pathlib import Path

from tools.klean_preflight import check_generation


rerun = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
audit_recorded = json.loads(
    Path("/audit-input.json").read_text()
)["resolution"]["stage4_preflight"]
generation_recorded = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)

print(
    json.dumps(
        {
            "rerun": rerun,
            "checks": {
                "rerun exactly equals audit-input preflight": (
                    rerun == audit_recorded
                ),
                "rerun exactly equals generation preflight": (
                    rerun == generation_recorded
                ),
            },
            "all_checks_pass": (
                rerun == audit_recorded == generation_recorded
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
