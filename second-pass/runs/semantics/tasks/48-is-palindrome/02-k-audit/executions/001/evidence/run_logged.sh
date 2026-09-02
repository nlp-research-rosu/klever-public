#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOG_NAME COMMAND [ARG ...]" >&2
  exit 2
fi

evidence_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log_name="$1"
shift
log_path="${evidence_dir}/${log_name}"
tmp_output="$(mktemp /tmp/audit-command-output.XXXXXX)"

printf 'COMMAND: ' >"${log_path}"
printf '%q ' "$@" >>"${log_path}"
printf '\n' >>"${log_path}"

"$@" >"${tmp_output}" 2>&1
command_status=$?
cat "${tmp_output}" >>"${log_path}"
printf '\nEXIT_STATUS: %d\n' "${command_status}" >>"${log_path}"
cat "${log_path}"
rm -f "${tmp_output}"
exit "${command_status}"
