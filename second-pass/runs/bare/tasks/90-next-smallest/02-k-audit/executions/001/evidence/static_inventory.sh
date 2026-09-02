#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

SOURCE=/tmp/audit-work/90-next-smallest/source

run rg -n \
  -e '^[[:space:]]*(requires|module|imports|syntax|configuration|rule|claim)' \
  -e '\[(function|total|functional|concrete|simplification|priority|owise)' \
  "$SOURCE/semantic.k" "$SOURCE/verification.k" "$SOURCE/spec.k"

run rg -c '^[[:space:]]*rule ' \
  "$SOURCE/semantic.k" "$SOURCE/verification.k"
run rg -c '^[[:space:]]*claim([[:space:]]|$)' "$SOURCE/spec.k"
run rg -n 'simplification|priority|owise|functional|opaque' \
  "$SOURCE/semantic.k" "$SOURCE/verification.k" "$SOURCE/spec.k"

run nl -ba "$SOURCE/solution.mpy"
run nl -ba "$SOURCE/semantic.k"
run nl -ba "$SOURCE/verification.k"
run nl -ba "$SOURCE/spec.k"
