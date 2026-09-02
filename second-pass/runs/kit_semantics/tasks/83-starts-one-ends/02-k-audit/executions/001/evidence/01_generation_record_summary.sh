#!/usr/bin/env bash
set -uo pipefail

log_path=/audit-output/evidence/01_generation_record_summary.log
exec >"$log_path" 2>&1

printf '$ python3 /audit-output/evidence/01_generation_record_summary.py\n'
python3 /audit-output/evidence/01_generation_record_summary.py
status=$?
printf '[exit %d]\n' "$status"

printf '\n$ python3 /audit-output/evidence/01_pipeline_tree_hashes.py\n'
python3 /audit-output/evidence/01_pipeline_tree_hashes.py
tree_status=$?
printf '[exit %d]\n' "$tree_status"

printf '\n$ sed -n 1,240p /generation-evidence/codex-last.txt\n'
sed -n 1,240p /generation-evidence/codex-last.txt
printf '[exit %d]\n' "$?"

if [ "$status" -ne 0 ] || [ "$tree_status" -ne 0 ]; then
    final_status=1
else
    final_status=0
fi
printf '\nScript exit: %d\n' "$final_status"
exit "$final_status"
