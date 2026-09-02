#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
log_file="$evidence_dir/rule_inventory.log"

{
  printf '$ python3 %s/rule_inventory.py\n' "$evidence_dir"
  python3 "$evidence_dir/rule_inventory.py"
  status=$?
  printf '[exit %d]\n' "$status"
  if [[ "$status" -eq 0 ]]; then
    printf '$ sha256sum %s/rule_inventory.md\n' "$evidence_dir"
    sha256sum "$evidence_dir/rule_inventory.md"
    printf '[exit %d]\n' "$?"
  fi
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
