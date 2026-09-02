#!/usr/bin/env bash
set -u

if [ "$#" -ne 3 ]; then
  echo "usage: run_recorded.sh LABEL WORKDIR COMMAND" >&2
  exit 2
fi

label=$1
run_workdir=$2
command_text=$3
evidence_dir=$(cd "$(dirname "$0")" && pwd)
raw_log=$(mktemp /tmp/audit-work/recorded-command.XXXXXX)

printf '%s\n' "$command_text" > "$evidence_dir/$label.command"
(
  cd "$run_workdir" || exit 125
  bash -o pipefail -c "$command_text"
) > "$raw_log" 2>&1
status=$?
printf '%s\n' "$status" > "$evidence_dir/$label.status"

bytes=$(wc -c < "$raw_log")
if [ "$bytes" -le 200000 ]; then
  cp "$raw_log" "$evidence_dir/$label.log"
else
  {
    head -c 100000 "$raw_log"
    printf '\n... LOG BOUNDED BY REVIEWER; original_bytes=%s ...\n' "$bytes"
    tail -c 100000 "$raw_log"
  } > "$evidence_dir/$label.log"
fi
rm -f "$raw_log"
exit "$status"
