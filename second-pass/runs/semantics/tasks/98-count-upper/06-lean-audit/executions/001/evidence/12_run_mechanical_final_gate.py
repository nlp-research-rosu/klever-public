#!/usr/bin/env python3
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
Path("/audit-output/evidence/mechanical-final-gate-result.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
