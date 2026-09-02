#!/usr/bin/env bash
set -uo pipefail
set -x

overall=0

cmp -s \
  /audit-output/evidence/concrete_driver.py \
  /tmp/audit-work/candidate-src/concrete_driver.py
driver_status=$?
printf 'preserved_concrete_driver_identity_status=%s\n' "$driver_status"
if (( driver_status != 0 )); then
  overall=1
fi

diff -qr --no-dereference \
  /reference/reference-semantics \
  /candidate/reference-semantics
semantics_status=$?
printf 'final_semantics_integrity_status=%s\n' "$semantics_status"
if (( semantics_status != 0 )); then
  overall=1
fi

python3 - <<'PY'
import ast
from pathlib import Path

review = Path("/audit-output/REVIEW.md").read_text()
lines = review.splitlines()
expected = ["VERDICT: PASS", "LEGITIMACY: LEGIT"]
print(f"review_last_two={lines[-2:]!r}")
print(f"review_marker_counts={(review.count('VERDICT:'), review.count('LEGITIMACY:'))}")
if lines[-2:] != expected:
    raise SystemExit(1)
if review.count("VERDICT:") != 1 or review.count("LEGITIMACY:") != 1:
    raise SystemExit(1)

for path in sorted(Path("/audit-output/evidence").glob("*.py")):
    ast.parse(path.read_text(), filename=str(path))
    print(f"python_parse_ok={path}")
PY
review_status=$?
printf 'review_and_python_parse_status=%s\n' "$review_status"
if (( review_status != 0 )); then
  overall=1
fi

for script in /audit-output/evidence/*.sh; do
  bash -n "$script"
  status=$?
  printf 'bash_parse_status=%s path=%s\n' "$status" "$script"
  if (( status != 0 )); then
    overall=1
  fi
done

printf '%s\n' 'EVIDENCE FILE HASHES'
find /audit-output/evidence -maxdepth 1 -type f -print0 |
  LC_ALL=C sort -z |
  xargs -0 sha256sum

printf 'FINAL_CHECKS_OVERALL=%s\n' "$overall"
exit "$overall"
