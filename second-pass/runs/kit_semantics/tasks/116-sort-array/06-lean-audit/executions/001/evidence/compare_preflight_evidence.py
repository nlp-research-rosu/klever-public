#!/usr/bin/env python3
"""Compare the fresh check_generation result with launcher-recorded evidence."""

from __future__ import annotations

import json
from pathlib import Path


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
log = Path("/audit-output/evidence/26_check_generation_rerun.log").read_text()
start = log.index("{")
end = log.rindex("}") + 1
fresh = json.loads(log[start:end])
stored = json.loads(Path("/reference/klean-generation/preflight.json").read_text())

report = {
    "fresh_equals_launcher_record": fresh == audit["stage4_preflight"],
    "fresh_equals_generation_sidecar": fresh == stored,
    "fresh_status": fresh["status"],
    "fresh_obligation_count": fresh["obligation_count"],
    "fresh_target": fresh["target"],
    "fresh_diagnostics": fresh["diagnostics"],
}
report["overall"] = all(
    value for key, value in report.items() if key.startswith("fresh_equals_")
)
print(json.dumps(report, indent=2, sort_keys=True))
