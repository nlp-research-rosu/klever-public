#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "usage: run_logged.sh LOGFILE COMMAND [ARG ...]" >&2
  exit 64
fi

audit_log=$1
shift

exec > >(tee "$audit_log") 2>&1

printf 'WORKDIR: %s\n' "$PWD"
printf 'COMMAND:'
printf ' %q' "$@"
printf '\n'

set +e
"$@"
audit_status=$?
set -e

printf 'EXIT_STATUS: %d\n' "$audit_status"
exit "$audit_status"
