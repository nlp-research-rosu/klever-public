#!/usr/bin/env bash
set -u

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local rc=$?
  printf 'EXIT: %d\n' "$rc"
  return 0
}

run rg -n '^[[:space:]]*(requires|module|endmodule|imports|syntax|rule|configuration|claim)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
run rg -n '\[(function|total|functional|simplification|macro|priority|owise|anywhere|concrete|symbolic|strict|seqstrict)' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
run rg -n '\b(opaque|priority|simplification|total|functional|anywhere|owise)\b' \
  /candidate/semantic.k /candidate/verification.k /candidate/spec.k
