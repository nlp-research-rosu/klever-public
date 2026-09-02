#!/usr/bin/env python3
"""Compare the preserved fresh preflight result to all recorded copies."""

from __future__ import annotations

import json
from pathlib import Path


log_text = Path("/audit-output/evidence/check_generation.log").read_text()
json_start = log_text.index("{")
json_end = log_text.index("\n\nScript done", json_start)
fresh = json.loads(log_text[json_start:json_end])
stored = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())
signed = audit_input["resolution"]["stage4_preflight"]

result = {
    "fresh_equals_stored": fresh == stored,
    "fresh_equals_signed": fresh == signed,
    "stored_equals_signed": stored == signed,
    "fresh_status": fresh["status"],
    "fresh_obligation_count": fresh["obligation_count"],
    "fresh_target": fresh["target"],
    "fresh_diagnostics": fresh["diagnostics"],
}
if not all(
    result[key]
    for key in (
        "fresh_equals_stored",
        "fresh_equals_signed",
        "stored_equals_signed",
    )
):
    raise SystemExit(json.dumps(result, indent=2, sort_keys=True))
print(json.dumps(result, indent=2, sort_keys=True))
