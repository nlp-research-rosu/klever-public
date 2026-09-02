#!/usr/bin/env bash
set -u

if [[ "$#" -lt 3 ]]; then
  echo "usage: $0 NAME WORKDIR COMMAND [ARG ...]" >&2
  exit 64
fi

name="$1"
workdir="$2"
shift 2
evidence_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

{
  printf 'cwd: %q\n' "$workdir"
  printf 'command:'
  printf ' %q' "$@"
  printf '\n'
} > "$evidence_dir/$name.command"

(
  cd "$workdir" || exit 125
  "$@"
) > "$evidence_dir/$name.log" 2>&1
status=$?
printf '%s\n' "$status" > "$evidence_dir/$name.status"
exit "$status"
