#!/usr/bin/env bash
set -u
cd /tmp/audit-work/candidate

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return "$status"
}

printf '%s\n' \
  'COMMAND: sed -n 9,69p /tmp/audit-work/candidate/spec.k | sed s/\\.Exprs//g;s/\\.Stmts//g > /tmp/audit-work/claim-program.mpy'
sed -n '9,69p' /tmp/audit-work/candidate/spec.k \
  | sed 's/\.Exprs//g; s/\.Stmts//g' \
  > /tmp/audit-work/claim-program.mpy
printf 'EXIT_STATUS: %d\n' "$?"

run kast /tmp/audit-work/candidate/solution.mpy \
  --definition /tmp/audit-work/candidate/semantic-kompiled \
  --sort Program \
  --output json \
  --output-file /tmp/audit-work/solution-program.json || exit $?

run kast /tmp/audit-work/claim-program.mpy \
  --definition /tmp/audit-work/candidate/semantic-kompiled \
  --sort Program \
  --output json \
  --output-file /tmp/audit-work/claim-program.json || exit $?

run cmp -- /tmp/audit-work/solution-program.json /tmp/audit-work/claim-program.json || exit $?
run sha256sum /tmp/audit-work/solution-program.json /tmp/audit-work/claim-program.json
