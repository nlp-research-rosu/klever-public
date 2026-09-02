#!/usr/bin/env bash
set -uo pipefail

if [[ "$#" -lt 3 ]]; then
  echo "usage: $0 LOGFILE WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

logfile=$1
workdir=$2
shift 2

mkdir -p "$(dirname "$logfile")"
{
  printf 'WORKDIR: %s\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$logfile"

(
  cd "$workdir" || exit 125
  "$@"
) > >(tee -a "$logfile") 2> >(tee -a "$logfile" >&2)
status=$?
printf 'EXIT_STATUS: %d\n' "$status" | tee -a "$logfile"
exit "$status"
