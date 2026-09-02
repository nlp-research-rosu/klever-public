#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: audit-run.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

log_file=$1
shift
capture_file=$(mktemp /tmp/audit-command.XXXXXX)

{
  printf 'WORKDIR: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_file"

"$@" >"$capture_file" 2>&1
command_status=$?
line_count=$(wc -l <"$capture_file")

{
  printf 'EXIT_STATUS: %s\n' "$command_status"
  printf 'OUTPUT_LINES: %s\n' "$line_count"
  if (( line_count <= 320 )); then
    cat "$capture_file"
  else
    sed -n '1,240p' "$capture_file"
    printf '\n[... %s lines omitted by reviewer logger ...]\n\n' "$((line_count - 320))"
    tail -n 80 "$capture_file"
  fi
} >> "$log_file"

rm -f "$capture_file"
cat "$log_file"
exit "$command_status"
