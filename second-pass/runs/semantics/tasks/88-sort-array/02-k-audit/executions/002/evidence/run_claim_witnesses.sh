#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
log_file="$evidence_dir/claim_witnesses.log"

{
  printf '$ python3 %s/claim_witnesses.py\n' "$evidence_dir"
  python3 "$evidence_dir/claim_witnesses.py"
  status=$?
  printf '[exit %d]\n' "$status"
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
