#!/usr/bin/env python3
"""Independent trusted mechanical Stage 5 gate."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import check_proof_candidate


result = check_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
)
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
