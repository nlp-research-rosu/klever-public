#!/usr/bin/env bash
set -u
cd /tmp/audit-work/candidate

printf '%s\n' \
  'COMMAND: sed module rename and append ListItem(99) to both result obligations in spec.k > spec-vacuity.k'
sed \
  -e 's/^module SPEC$/module SPEC-VACUITY/' \
  -e 's/listVal(expected(A, B))/listVal(expected(A, B) ListItem(99))/g' \
  spec.k > spec-vacuity.k
printf 'EXIT_STATUS: %d\n' "$?"

cp -a spec-vacuity.k /audit-output/evidence/spec-vacuity.k

printf '%s\n' 'COMMAND: diff -u spec.k spec-vacuity.k'
diff -u spec.k spec-vacuity.k
diff_status=$?
printf 'EXIT_STATUS: %d (expected 1 because the files differ)\n' "$diff_status"
if [[ "$diff_status" -ne 1 ]]; then
  exit 1
fi

dry_command=(
  kprove spec-vacuity.k
  --definition /tmp/audit-work/candidate/verification-kompiled
  --spec-module SPEC-VACUITY
  --dry-run
)
printf 'COMMAND:'
printf ' %q' "${dry_command[@]}"
printf ' > %q\n' /tmp/audit-work/spec-vacuity-dry-run.kore
"${dry_command[@]}" > /tmp/audit-work/spec-vacuity-dry-run.kore
dry_status=$?
printf 'EXIT_STATUS: %d (required zero)\n' "$dry_status"
if [[ "$dry_status" -ne 0 ]]; then
  printf '%s\n' 'VACUITY_BUILD=FAIL'
  exit 1
fi
printf 'DRY_RUN_BYTES: %s\n' "$(wc -c < /tmp/audit-work/spec-vacuity-dry-run.kore)"
sha256sum /tmp/audit-work/spec-vacuity-dry-run.kore

proof_command=(
  kprove spec-vacuity.k
  --definition /tmp/audit-work/candidate/verification-kompiled
  --spec-module SPEC-VACUITY
)
printf 'COMMAND:'
printf ' %q' "${proof_command[@]}"
printf '\n'
"${proof_command[@]}"
proof_status=$?
printf 'EXIT_STATUS: %d (expected nonzero)\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'NON_VACUITY=FAIL_UNEXPECTED_PROOF'
  exit 1
fi
printf '%s\n' 'NON_VACUITY=PASS_EXPECTED_STUCK_PROOF'
