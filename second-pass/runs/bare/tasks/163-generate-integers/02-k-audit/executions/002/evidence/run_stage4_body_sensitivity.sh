#!/usr/bin/env bash
set -u
cd /tmp/audit-work/candidate

printf '%s\n' \
  'COMMAND: sed module rename and line-38 ListExpr(Int(8))->ListExpr(Int(7)) spec.k > spec-body-mutation.k'
sed \
  -e 's/^module SPEC$/module SPEC-BODY-MUTATION/' \
  -e '38s/ListExpr(Int(8))/ListExpr(Int(7))/' \
  spec.k > spec-body-mutation.k
printf 'EXIT_STATUS: %d\n' "$?"

cp -a spec-body-mutation.k /audit-output/evidence/spec-body-mutation.k

printf '%s\n' 'COMMAND: diff -u spec.k spec-body-mutation.k'
diff -u spec.k spec-body-mutation.k
diff_status=$?
printf 'EXIT_STATUS: %d (expected 1 because the files differ)\n' "$diff_status"
if [[ "$diff_status" -ne 1 ]]; then
  exit 1
fi

command=(
  kprove spec-body-mutation.k
  --definition /tmp/audit-work/candidate/verification-kompiled
  --spec-module SPEC-BODY-MUTATION
)
printf 'COMMAND:'
printf ' %q' "${command[@]}"
printf '\n'
"${command[@]}"
proof_status=$?
printf 'EXIT_STATUS: %d (expected nonzero)\n' "$proof_status"
if [[ "$proof_status" -eq 0 ]]; then
  printf '%s\n' 'BODY_SENSITIVITY=FAIL_UNEXPECTED_PROOF'
  exit 1
fi
printf '%s\n' 'BODY_SENSITIVITY=PASS_EXPECTED_STUCK_PROOF'
