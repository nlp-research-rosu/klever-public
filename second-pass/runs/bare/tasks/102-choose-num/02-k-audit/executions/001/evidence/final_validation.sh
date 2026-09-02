#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/final-validation.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

status=0
run python3 -c '
from pathlib import Path
p = Path("/audit-output/REVIEW.md")
text = p.read_text(encoding="utf-8")
expected = "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
assert text.endswith(expected)
assert text.count("\nVERDICT:") == 1
assert text.count("\nLEGITIMACY:") == 1
for stage in range(1, 8):
    assert f"## {stage}." in text
print(f"review_bytes={len(text.encode())}")
print("seven_stage_headings=true")
print("terminal_markers_exact=true")
' || status=1

for log in \
  /audit-output/evidence/stage1-integrity.log \
  /audit-output/evidence/stage2-fidelity.log \
  /audit-output/evidence/stage3-reconstruction.log \
  /audit-output/evidence/stage4-5-static.log \
  /audit-output/evidence/stage6-nonvacuity.log \
  /audit-output/evidence/body-sensitivity.log; do
  run test -s "$log" || status=1
done

run tail -n 2 /audit-output/REVIEW.md || status=1
printf 'final_validation_status=%d\n' "$status"
exit "$status"
