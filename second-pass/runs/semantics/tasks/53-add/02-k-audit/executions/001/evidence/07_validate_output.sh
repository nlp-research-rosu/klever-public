#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/07_validate_output.log
MANIFEST=/audit-output/evidence/SHA256SUMS
exec >"$LOG" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf '[exit %d]\n' "$rc"
  return "$rc"
}

run test -f /audit-output/REVIEW.md || exit $?
run test "$(tail -n 2 /audit-output/REVIEW.md | sed -n '1p')" = "VERDICT: CONCERNS" || exit $?
run test "$(tail -n 1 /audit-output/REVIEW.md)" = "LEGITIMACY: LEGIT" || exit $?
run test "$(grep -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1 || exit $?
run test "$(grep -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1 || exit $?

for path in \
  /audit-output/evidence/01_integrity.log \
  /audit-output/evidence/02_prepare_and_translate.log \
  /audit-output/evidence/02_differential.log \
  /audit-output/evidence/differential-inputs.json \
  /audit-output/evidence/03_reconstruct.log \
  /audit-output/evidence/04_pinning_and_ground.log \
  /audit-output/evidence/05_rule_inventory.txt \
  /audit-output/evidence/05_attribute_inventory.txt \
  /audit-output/evidence/05_body_sensitivity.log \
  /audit-output/evidence/06_nonvacuity.log; do
  run test -s "$path" || exit $?
done

run grep -Fx '#Top' /audit-output/evidence/03_reconstruct.log || exit $?
run grep -F 'kprove exit: 0' /audit-output/evidence/03_reconstruct.log || exit $?
run grep -F '"mismatch_count": 0' /audit-output/evidence/02_differential.log || exit $?
run grep -F 'mutated body result -1 versus required 5 visible: yes' \
  /audit-output/evidence/05_body_sensitivity.log || exit $?
run grep -F 'actual 5 versus required 6 visible: yes' \
  /audit-output/evidence/06_nonvacuity.log || exit $?

printf '\n$ find /audit-output/evidence -maxdepth 1 -type f ! -name SHA256SUMS ! -name 07_validate_output.log -print0 | sort -z | xargs -0 sha256sum > %s\n' "$MANIFEST"
find /audit-output/evidence -maxdepth 1 -type f \
  ! -name SHA256SUMS \
  ! -name 07_validate_output.log \
  -print0 |
  sort -z |
  xargs -0 sha256sum > "$MANIFEST"
rc=$?
printf '[exit %d]\n' "$rc"
run wc -l /audit-output/REVIEW.md "$MANIFEST"
run tail -n 2 /audit-output/REVIEW.md
