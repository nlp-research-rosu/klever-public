#!/usr/bin/env bash
# Run one command and preserve a bounded combined-output log with its exact
# argv and exit status. Usage: run_and_log.sh LOG COMMAND [ARG ...]
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 64
fi

log_path="$1"
shift
tmp_log="$(mktemp /tmp/audit-command-log.XXXXXX)"

{
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"${tmp_log}"

"$@" >>"${tmp_log}" 2>&1
command_status=$?
printf 'EXIT_STATUS: %d\n' "${command_status}" >>"${tmp_log}"

# Keep the beginning and end when command output is large.
line_count="$(wc -l <"${tmp_log}")"
if (( line_count <= 500 )); then
  cp "${tmp_log}" "${log_path}"
else
  {
    sed -n '1,260p' "${tmp_log}"
    printf '... OMITTED %d INTERIOR LINES ...\n' "$((line_count - 500))"
    tail -n 240 "${tmp_log}"
  } >"${log_path}"
fi

unlink "${tmp_log}"
exit "${command_status}"
