#!/usr/bin/env python3
import json
from pathlib import Path

from tools.klean_final_gate import check_proof_candidate


print(
    "$ PYTHONPATH=/reference python3 "
    "/audit-output/evidence/run_stage5_final_gate.py"
)
result = check_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
)
print(json.dumps(result, indent=2, sort_keys=True))
