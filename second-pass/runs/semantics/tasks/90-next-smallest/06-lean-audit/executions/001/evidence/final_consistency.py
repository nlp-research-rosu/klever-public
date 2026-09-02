#!/usr/bin/env python3
import json
import re
from pathlib import Path


root = Path("/audit-output")
evidence = root / "evidence"
review = (root / "REVIEW.md").read_text()

references = sorted(set(re.findall(r"`evidence/([^`\s]+)`", review)))
missing = [name for name in references if not (evidence / name).is_file()]

success_logs = [
    "01-producer-integrity-correct-algorithm.log",
    "02-inventory-reconstruction.log",
    "06-stage4-preflight-rerun-success.log",
    "07-stage4-integrity.log",
    "09-stage5-lake-clean.log",
    "10-stage5-lake-build.log",
    "11-proof-final-axioms.log",
    "12-axiom-reconciliation.log",
    "13-candidate-static-and-target.log",
    "14b-bridge-adversarial-examples-passing.log",
]
expected_failure_logs = [
    "16-counterfactual-nsscan-constant.log",
    "17-counterfactual-map-identity.log",
    "19-counterfactual-membership-vacuity.log",
]

checks = {
    "review_exists": (root / "REVIEW.md").is_file(),
    "exact_final_pair": review.endswith(
        "\nVERDICT: PASS\nLEGITIMACY: LEGIT\n"
    ),
    "one_verdict_line": len(
        re.findall(r"(?m)^VERDICT: (?:PASS|CONCERNS|FAIL)$", review)
    )
    == 1,
    "one_legitimacy_line": len(
        re.findall(r"(?m)^LEGITIMACY: (?:LEGIT|NOT_LEGIT)$", review)
    )
    == 1,
    "all_referenced_evidence_exists": not missing,
    "success_logs_exit_zero": all(
        'COMMAND_EXIT_CODE="0"' in (evidence / name).read_text(
            errors="replace"
        )
        for name in success_logs
    ),
    "mutations_exit_one": all(
        'COMMAND_EXIT_CODE="1"' in (evidence / name).read_text(
            errors="replace"
        )
        for name in expected_failure_logs
    ),
    "axiom_output_has_no_sorryAx": (
        "sorryAx" not in (evidence / "11-proof-final-axioms.log").read_text()
    ),
}

result = {
    "checks": checks,
    "missing_references": missing,
    "referenced_evidence_count": len(references),
    "review_bytes": len(review.encode()),
    "status": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["status"] == "PASS" else 1)
