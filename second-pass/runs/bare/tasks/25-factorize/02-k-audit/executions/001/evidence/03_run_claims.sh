#!/usr/bin/env bash
set -uo pipefail

source_dir=/tmp/audit-work/25-factorize-audit/source
definition=/tmp/audit-work/25-factorize-audit/verification-fresh-kompiled
evidence_dir=/audit-output/evidence
failures=0

cd "$source_dir" || exit 1

for number in $(seq -w 1 26); do
  spec_file="$source_dir/audit-claim-$number.k"
  module_name="AUDIT-SPEC-$number"
  log_file="$evidence_dir/03_claim_$number.log"
  {
    echo "$ kprove $spec_file --definition $definition --spec-module $module_name"
    kprove "$spec_file" \
      --definition "$definition" \
      --spec-module "$module_name"
    status=$?
    printf '[exit_status=%d]\n' "$status"
    if grep -Fxq '#Top' "$log_file" 2>/dev/null; then
      top=yes
    else
      top=no
    fi
    printf '[printed_exact_top=%s]\n' "$top"
  } >"$log_file" 2>&1
  status=$(sed -n 's/^\[exit_status=\([0-9][0-9]*\)\]$/\1/p' "$log_file" | tail -1)
  top=$(sed -n 's/^\[printed_exact_top=\(yes\|no\)\]$/\1/p' "$log_file" | tail -1)
  printf 'claim=%s exit_status=%s printed_exact_top=%s log=%s\n' \
    "$number" "$status" "$top" "$log_file"
  if [[ "$status" != 0 || "$top" != yes ]]; then
    failures=$((failures + 1))
    tail -30 "$log_file"
  fi
done

printf 'claim_count=26 failure_count=%d\n' "$failures"
if (( failures != 0 )); then
  exit 1
fi
