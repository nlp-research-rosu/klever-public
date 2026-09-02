#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
status=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf 'STAGE 5 BRIDGE CONNECTION AND BODY SENSITIVITY\n'
run python3 "$evidence/compare_bridges.py"

printf '\n$ cd %q && kprove stage5-body-mutation.k --definition fresh-verification-kompiled --spec-module STAGE5-BODY-MUTATION\n' "$work"
(cd "$work" && kprove stage5-body-mutation.k \
  --definition fresh-verification-kompiled \
  --spec-module STAGE5-BODY-MUTATION) \
  > "$evidence/stage5-body-mutation-kprove.log" 2>&1
rc=$?
sed -n '1,240p' "$evidence/stage5-body-mutation-kprove.log"
printf '[exit %d; expected nonzero]\n' "$rc"
if [ "$rc" -eq 0 ]; then
  status=1
fi
run rg -n 'WarnStuckClaimState|false|true|cannot be rewritten further' \
  "$evidence/stage5-body-mutation-kprove.log"

exit "$status"
