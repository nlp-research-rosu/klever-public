#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/body-sensitivity.log
RAW=/audit-output/evidence/body-sensitivity-proof.raw.log
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

cd /tmp/audit-work/body-mutation || exit 1
status=0
printf 'GATE A BODY-SENSITIVITY PROBE\n'
run diff -u ../verification.k verification.k
diff_status=$?
if (( diff_status != 1 )); then
  printf 'ERROR: expected exactly one source difference\n'
  status=1
fi
run python3 -c \
  'x,y=2,3; original=y-1; mutated=y-3; print(f"witness=({x},{y}) original={original} mutated={mutated} distinct={original != mutated}"); assert x>0 and y>0 and x<y and y%2!=0 and original!=mutated' \
  || status=1
run test ! -e body-mut-kompiled || status=1
run kompile semantic.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition body-mut-kompiled || status=1

printf '$ kprove spec-body-mutation.k --definition body-mut-kompiled --spec-module SPEC-BODY-MUTATION 2>&1 | tee %s\n' "$RAW"
kprove spec-body-mutation.k \
  --definition body-mut-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  2>&1 | tee "$RAW"
proof_status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$proof_status"
if (( proof_status == 0 )); then
  printf 'ERROR: materially changed body unexpectedly proved the original result\n'
  status=1
else
  printf 'expected_nonzero_body_mutation_status=%d\n' "$proof_status"
fi
run rg -n 'WarnStuckClaimState' "$RAW" || status=1
run rg -n 'Y \+Int -3|Y \+Int -1|cannot be rewritten further' "$RAW" || status=1
printf 'body_sensitivity_status=%d\n' "$status"
exit "$status"
