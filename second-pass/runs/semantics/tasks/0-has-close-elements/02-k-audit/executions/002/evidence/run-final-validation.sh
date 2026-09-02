#!/usr/bin/env bash
set -uo pipefail

LOG=/audit-output/evidence/07-review-validation.log
exec > >(tee "$LOG") 2>&1

echo '$ validate REVIEW.md terminal markers'
python3 - <<'PY'
from pathlib import Path

path = Path("/audit-output/REVIEW.md")
lines = path.read_text(encoding="utf-8").splitlines()
expected = ["VERDICT: FAIL", "LEGITIMACY: NOT_LEGIT"]
print(f"review_bytes={path.stat().st_size} review_lines={len(lines)}")
print(f"last_two={lines[-2:]!r}")
print(f"verdict_marker_count={sum(line.startswith('VERDICT:') for line in lines)}")
print(f"legitimacy_marker_count={sum(line.startswith('LEGITIMACY:') for line in lines)}")
raise SystemExit(
    0
    if lines[-2:] == expected
    and sum(line.startswith("VERDICT:") for line in lines) == 1
    and sum(line.startswith("LEGITIMACY:") for line in lines) == 1
    else 1
)
PY
echo "[exit $?]"

echo '$ check reviewer evidence for links or unsupported entries'
find /audit-output/evidence ! -type d ! -type f -printf '%y %p -> %l\n'
echo "[exit $?]"

echo '$ build final SHA-256 manifest of review and evidence (excluding manifest itself)'
(
  cd /audit-output
  {
    sha256sum REVIEW.md
    find evidence -maxdepth 1 -type f \
      ! -name MANIFEST.sha256 \
      ! -name 07-review-validation.log \
      -print0 | sort -z | xargs -0 sha256sum
  }
) > /audit-output/evidence/MANIFEST.sha256
echo "[exit $?]"
wc -l /audit-output/evidence/MANIFEST.sha256
sha256sum /audit-output/evidence/MANIFEST.sha256
echo "[exit $?]"
