#!/usr/bin/env bash
set -u

if [ "$#" -ne 2 ]; then
  echo "usage: $0 LABEL COMMAND" >&2
  exit 2
fi

label=$1
command_text=$2
evidence_root=/audit-output/evidence
record_dir="$evidence_root/$label"

mkdir -p "$record_dir"
printf '%s\n' "$command_text" > "$record_dir/command.txt"

set +e
/bin/bash -lc "$command_text" > "$record_dir/output.log" 2>&1
status=$?
set -e

printf '%s\n' "$status" > "$record_dir/exit_status.txt"
sed -n '1,600p' "$record_dir/output.log"
printf 'EXIT STATUS: %s\n' "$status"
exit "$status"
