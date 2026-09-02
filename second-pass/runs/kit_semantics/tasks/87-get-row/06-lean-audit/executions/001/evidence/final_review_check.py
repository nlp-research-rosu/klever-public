#!/usr/bin/env python3
"""Sanity-check the completed audit report and core evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path


def main() -> int:
    review = Path("/audit-output/REVIEW.md").read_text()
    expected_end = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
    links = re.findall(r"\]\((/audit-output/evidence/[^)]+)\)", review)
    missing_links = [path for path in links if not Path(path).is_file()]
    malformed_command_logs = []
    for path in sorted(Path("/audit-output/evidence").glob("*-command.json")):
        try:
            record = json.loads(path.read_text())
            if not all(key in record for key in ("command", "cwd", "exit_code", "output")):
                malformed_command_logs.append(path.name)
        except Exception:
            malformed_command_logs.append(path.name)
    mechanical = json.loads(
        Path("/audit-output/evidence/mechanical-summary.json").read_text()
    )
    stage4 = json.loads(
        Path("/audit-output/evidence/stage4-judgment-command.json").read_text()
    )
    stage4_output = json.loads(stage4["output"])
    result = {
        "ends_with_exact_pair": review.endswith(expected_end),
        "verdict_line_count": len(re.findall(r"(?m)^VERDICT:", review)),
        "legitimacy_line_count": len(re.findall(r"(?m)^LEGITIMACY:", review)),
        "evidence_link_count": len(links),
        "missing_evidence_links": missing_links,
        "malformed_command_logs": malformed_command_logs,
        "mechanical_summary": mechanical,
        "stage4_checks_pass": stage4_output["all_stage4_checks_pass"],
    }
    ok = (
        result["ends_with_exact_pair"]
        and result["verdict_line_count"] == 1
        and result["legitimacy_line_count"] == 1
        and not missing_links
        and not malformed_command_logs
        and all(
            (
                mechanical["producer_authentication"],
                mechanical["recorded_hashes"],
                mechanical["stage1_source_hashes"],
                mechanical["inventory_bijection"],
                mechanical["preflight_status"] == "KLEAN_NO_OBLIGATIONS",
                mechanical["preflight_obligation_count"] == 0,
                mechanical["preflight_target"] is None,
                result["stage4_checks_pass"],
            )
        )
    )
    result["ok"] = ok
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
