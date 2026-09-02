#!/usr/bin/env bash
set -u

run() {
  local cmd="$1"
  printf '$ %s\n' "$cmd"
  bash -o pipefail -c "$cmd"
  local status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run "sha256sum semantic.k verification.k spec.k solution.mpy"
run "rg -n '^[[:space:]]*(syntax|configuration|rule|claim)([[:space:]]|$)' semantic.k verification.k spec.k"
run "rg -n '\\[(function|functional|total|simplification|concrete|priority)' semantic.k verification.k spec.k"
run "rg -n '\\b(opaque|owise)\\b' semantic.k verification.k spec.k"
run "rg -n '^[[:space:]]*(rule|claim)([[:space:]]|$)' semantic.k verification.k spec.k | wc -l"
run "nl -ba semantic.k"
run "nl -ba verification.k"
run "nl -ba spec.k"
