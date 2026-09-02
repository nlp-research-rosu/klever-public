#!/usr/bin/env bash
set -u

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run "python3 /audit-output/evidence/differential_test.py /reference/canonical.py /tmp/audit-work/114-minSubArraySum-audit/solution.py"
