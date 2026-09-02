#!/usr/bin/env bash
set -u

if [[ "$#" -lt 2 ]]; then
  echo "usage: $0 LABEL COMMAND [ARG ...]" >&2
  exit 64
fi

label=$1
shift
evidence_dir=/audit-output/evidence
mkdir -p "$evidence_dir"

{
  printf '%q' "$1"
  shift
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  printf '\n'
} >"$evidence_dir/$label.command.txt"

set +e
bash -lc "$(cat "$evidence_dir/$label.command.txt")" \
  >"$evidence_dir/$label.stdout.txt" \
  2>"$evidence_dir/$label.stderr.txt"
status=$?
set -e
printf '%s\n' "$status" >"$evidence_dir/$label.exitcode.txt"
exit "$status"
