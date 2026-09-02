#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -lt 3 ]; then
  echo "usage: run_logged.sh LOG WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

log=$1
workdir=$2
shift 2

{
  printf 'WORKDIR: %q\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  printf 'START_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$log"

(
  cd "$workdir" || exit 72
  export PATH="$HOME/.nix-profile/bin:$PATH"
  "$@"
) 2>&1 | tee -a "$log"
status=${PIPESTATUS[0]}

{
  printf 'EXIT_STATUS: %s\n' "$status"
  printf 'END_UTC: %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log"

exit "$status"
