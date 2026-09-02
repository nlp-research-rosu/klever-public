#!/usr/bin/env bash
set -uo pipefail

audit_log_path=$1
shift
audit_tmp_output=$(mktemp /tmp/kit-audit-command.XXXXXX)

set +e
"$@" >"$audit_tmp_output" 2>&1
audit_status=$?
set -e

{
  printf 'cwd: %s\n' "$PWD"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
  printf 'output-bytes: %s\n' "$(wc -c <"$audit_tmp_output")"
  if [ "$(wc -c <"$audit_tmp_output")" -le 400000 ]; then
    sed -n '1,10000p' "$audit_tmp_output"
  else
    printf '[output bounded: first and last 200000 bytes retained]\n'
    head -c 200000 "$audit_tmp_output"
    printf '\n[... bounded middle omitted ...]\n'
    tail -c 200000 "$audit_tmp_output"
  fi
  printf '\nexit-status: %s\n' "$audit_status"
} >"$audit_log_path"

sed -n '1,120p' "$audit_log_path"
if [ "$(wc -l <"$audit_log_path")" -gt 160 ]; then
  printf '[terminal display bounded; see %s]\n' "$audit_log_path"
  tail -40 "$audit_log_path"
fi

rm -f "$audit_tmp_output"
exit "$audit_status"
