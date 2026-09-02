#!/usr/bin/env bash
set -uo pipefail
trap 'rc=$?; printf "\nEXIT_CODE=%s\n" "$rc"' EXIT

python3 - <<'PY'
from pathlib import Path

review = Path("/audit-output/REVIEW.md").read_text()
lines = review.rstrip("\n").splitlines()
expected = ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
print("final_pair", lines[-2:])
print("verdict_line_count", review.count("VERDICT:"))
print("legitimacy_line_count", review.count("LEGITIMACY:"))
assert lines[-2:] == expected
assert review.count("VERDICT:") == 1
assert review.count("LEGITIMACY:") == 1
PY

find /audit-output/evidence -maxdepth 1 -type f \
  ! -name '07_final_consistency_results.txt' \
  -print0 | sort -z | xargs -0 sha256sum
sha256sum /audit-output/REVIEW.md
