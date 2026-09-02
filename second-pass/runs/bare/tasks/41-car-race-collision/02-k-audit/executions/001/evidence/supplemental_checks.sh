#!/usr/bin/env bash
set -u

evidence_dir=/audit-output/evidence
work_dir=/tmp/audit-work/race41

run_logged() {
  log_name=$1
  shift
  {
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    command_status=$?
    printf '\nEXIT_STATUS: %d\n' "$command_status"
    return "$command_status"
  } > "$evidence_dir/$log_name" 2>&1
}

run_logged tool_versions.log \
  bash -c 'kompile --version && kprove --version && krun --version && python3 --version' ||
  exit 1

run_logged source_hashes.log \
  sha256sum \
  /candidate/solution.py \
  "$work_dir/solution.py" \
  /candidate/solution.mpy \
  "$work_dir/solution.mpy" \
  "$work_dir/solution.regenerated.mpy" \
  /candidate/semantic.k \
  "$work_dir/semantic.k" \
  /candidate/verification.k \
  "$work_dir/verification.k" \
  /candidate/spec.k \
  "$work_dir/spec.k" || exit 2

run_logged reviewed_source_listing.log \
  bash -c 'nl -ba /tmp/audit-work/race41/solution.mpy; nl -ba /tmp/audit-work/race41/semantic.k; nl -ba /tmp/audit-work/race41/verification.k; nl -ba /tmp/audit-work/race41/spec.k' ||
  exit 3

run_logged untrusted_claims.log \
  python3 "$evidence_dir/untrusted_claims_summary.py" || exit 4

printf 'SUPPLEMENTAL_STATUS: 0\n'
