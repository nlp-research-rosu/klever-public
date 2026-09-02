#!/usr/bin/env bash
set -uo pipefail

source_file=/audit-output/evidence/k_concrete_probes.py
target_file=/tmp/audit-work/reconstruction/k_concrete_probes.mpy

printf 'COMMAND: python3 /tmp/audit-work/reconstruction/py2mpy.py %s > %s\n' \
  "$source_file" "$target_file"
python3 /tmp/audit-work/reconstruction/py2mpy.py "$source_file" >"$target_file"
status=$?
printf 'TRANSLATOR_EXIT_STATUS: %d\n' "$status"
if [[ $status -eq 0 ]]; then
  sha256sum "$source_file" "$target_file"
fi
exit "$status"
