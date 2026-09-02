#!/usr/bin/env bash
set -u

cd /tmp/audit-work/fresh || exit 90
overall=0

run() {
  echo "$ $*"
  "$@"
  status=$?
  echo "exit_status=$status"
  if (( status != 0 )); then
    overall=1
  fi
}

run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-LABELED \
  --claims acc

# The entry proof uses the separately proved accumulator claim. Mark that
# helper trusted for this single-target replay so only `entry` is an obligation.
run kprove spec-labeled.k \
  --definition verification-kompiled \
  --spec-module HOW-MANY-TIMES-SPEC-LABELED \
  --claims acc,entry \
  --trusted acc

exit "$overall"
