#!/usr/bin/env bash
set -u

overall=0
run() {
  echo "\$ $*"
  "$@"
  status=$?
  echo "EXIT: $status"
  if [ "$status" -ne 0 ]; then overall=1; fi
  return 0
}

cd /tmp/audit-work/fresh || exit 125
run cp /audit-output/evidence/slice-connection.k /tmp/audit-work/fresh/slice-connection.k
run kompile slice-connection.k \
  --backend haskell \
  --main-module SLICE-AUDIT \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-slice-kompiled
run kprove slice-connection.k \
  --definition audit-slice-kompiled \
  --spec-module SLICE-AUDIT-SPEC \
  --output pretty
echo "SLICE_CONNECTION_OVERALL_EXIT: $overall"
exit "$overall"
