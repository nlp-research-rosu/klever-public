#!/usr/bin/env bash
set -u

if (( $# < 2 )); then
  printf 'usage: %s LOG COMMAND [ARG ...]\n' "$0" >&2
  exit 2
fi

record_log=$1
shift
exec > >(tee "$record_log") 2>&1

printf '$'
printf ' %q' "$@"
printf '\n'

record_status=0
"$@" || record_status=$?
printf '[exit %d]\n' "$record_status"
exit "$record_status"
