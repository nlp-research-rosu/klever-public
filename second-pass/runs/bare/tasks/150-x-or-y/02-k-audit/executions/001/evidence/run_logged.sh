#!/usr/bin/env bash
set -uo pipefail

if (( $# < 3 )); then
  echo "usage: $0 LABEL WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
workdir=$2
shift 2
log_dir=$(cd "$(dirname "$0")" && pwd)
raw=$(mktemp /tmp/audit-command.XXXXXX)

{
  printf 'LABEL: %s\n' "$label"
  printf 'WORKDIR: %s\n' "$workdir"
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
} > "$log_dir/$label.log"

(
  cd "$workdir" || exit 125
  "$@"
) >"$raw" 2>&1
status=$?
lines=$(wc -l < "$raw")
bytes=$(wc -c < "$raw")

{
  printf 'EXIT_STATUS: %d\n' "$status"
  printf 'OUTPUT_LINES: %d\n' "$lines"
  printf 'OUTPUT_BYTES: %d\n' "$bytes"
  printf '%s\n' '--- OUTPUT (bounded) ---'
  if (( lines <= 480 )); then
    sed -n '1,480p' "$raw"
  else
    sed -n '1,240p' "$raw"
    printf '%s\n' "--- OMITTED $((lines - 480)) MIDDLE LINES ---"
    tail -n 240 "$raw"
  fi
} >> "$log_dir/$label.log"

rm -f "$raw"
cat "$log_dir/$label.log"
exit "$status"
