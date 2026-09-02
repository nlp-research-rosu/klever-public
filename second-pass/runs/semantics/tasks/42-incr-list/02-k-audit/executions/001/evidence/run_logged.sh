#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 64
fi

log_name=$1
shift
evidence_dir=/audit-output/evidence
log_path="$evidence_dir/$log_name"
tmp_path="$evidence_dir/.${log_name}.tmp"

{
  printf 'WORKDIR: %q\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$log_path"

set +e
"$@" >"$tmp_path" 2>&1
command_status=$?
set -e

{
  printf 'EXIT_STATUS: %d\n' "$command_status"
  printf '%s\n' 'OUTPUT_BEGIN'
  sed -n '1,400p' "$tmp_path"
  output_lines=$(wc -l <"$tmp_path")
  if (( output_lines > 400 )); then
    printf '[bounded log: %d total lines; first 400 preserved]\n' "$output_lines"
  fi
  printf '%s\n' 'OUTPUT_END'
} >>"$log_path"

rm -f -- "$tmp_path"
exit "$command_status"
