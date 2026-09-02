#!/usr/bin/env bash
set -u

if [[ $# -lt 2 ]]; then
  echo "usage: $0 LOG-NAME COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log_name=$1
shift
audit_log_path="/audit-output/evidence/${audit_log_name}"

{
  printf 'UTC_START: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'CWD: %s\n' "$PWD"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} >"$audit_log_path"

set +e
"$@" 2>&1 | tee -a "$audit_log_path"
audit_pipeline=("${PIPESTATUS[@]}")
audit_status=${audit_pipeline[0]}
set -e

{
  printf 'EXIT_STATUS: %s\n' "$audit_status"
  printf 'UTC_END: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
} >>"$audit_log_path"

exit "$audit_status"
