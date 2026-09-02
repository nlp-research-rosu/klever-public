#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/80-is-happy
definition="$scratch/verification-audit-kompiled"
spec_root="$scratch/positive-specs"
failed=0

run_claim() {
  local file=$1
  local module=$2
  printf 'BEGIN %s module=%s\n' "$file" "$module"
  kprove "$spec_root/$file" \
    --definition "$definition" \
    -I "$scratch" \
    --spec-module "$module"
  local status=$?
  printf 'END %s exit=%s\n' "$file" "$status"
  if [[ $status -ne 0 ]]; then
    failed=1
  fi
}

run_claim spec-00-helper.k AUDIT-SPEC-00-HELPER
run_claim spec-01-entry.k AUDIT-SPEC-01-ENTRY
run_claim spec-02-example-a.k AUDIT-SPEC-02-EXAMPLE-A
run_claim spec-03-example-aa.k AUDIT-SPEC-03-EXAMPLE-AA
run_claim spec-04-example-abcd.k AUDIT-SPEC-04-EXAMPLE-ABCD
run_claim spec-05-example-aabb.k AUDIT-SPEC-05-EXAMPLE-AABB
run_claim spec-06-example-adb.k AUDIT-SPEC-06-EXAMPLE-ADB
run_claim spec-07-example-xyy.k AUDIT-SPEC-07-EXAMPLE-XYY

exit "$failed"
